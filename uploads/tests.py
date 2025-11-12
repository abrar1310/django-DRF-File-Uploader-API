from django.contrib.auth.models import User
from django.test import TestCase
from rest_framework.test import APIClient
from django.core.files.uploadedfile import SimpleUploadedFile

class UploadTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='test', password='pass')
        self.client = APIClient()
        self.client.login(username='test', password='pass')

    def test_upload_large_file_rejected(self):
        big_file = SimpleUploadedFile("big.jpg", b"0" * (10*1024*1024 + 1), content_type="image/jpeg")
        response = self.client.post("/api/uploads/", {"file": big_file})
        self.assertEqual(response.status_code, 400)

    def test_upload_invalid_extension_rejected(self):
        file = SimpleUploadedFile("malware.exe", b"abc", content_type="application/octet-stream")
        response = self.client.post("/api/uploads/", {"file": file})
        self.assertEqual(response.status_code, 400)

    def test_upload_invalid_mime_rejected(self):
        file = SimpleUploadedFile("sample.jpg", b"%PDF-1.4 content", content_type="application/pdf")
        response = self.client.post("/api/uploads/", {"file": file})
        self.assertEqual(response.status_code, 400)

    def test_upload_valid_image_pdf_success(self):
        image = SimpleUploadedFile("sample.jpg", b"\xff\xd8\xff\xe0" + b"0"*100, content_type="image/jpeg")
        pdf = SimpleUploadedFile("sample.pdf", b"%PDF-1.4 content", content_type="application/pdf")
        response_img = self.client.post("/api/uploads/", {"file": image})
        response_pdf = self.client.post("/api/uploads/", {"file": pdf})
        self.assertEqual(response_img.status_code, 201)
        self.assertEqual(response_pdf.status_code, 201)
        self.assertIn("sha256", response_img.data)
        self.assertIn("sha256", response_pdf.data)

    def test_list_pagination(self):
        for i in range(15):
            file = SimpleUploadedFile(f"file{i}.jpg", b"\xff\xd8\xff\xe0" + b"0"*100, content_type="image/jpeg")
            self.client.post("/api/uploads/", {"file": file})
        response = self.client.get("/api/uploads/?page=1")
        self.assertEqual(len(response.data['results']), 10)
        response2 = self.client.get("/api/uploads/?page=2")
        self.assertEqual(len(response2.data['results']), 5)
