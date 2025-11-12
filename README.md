# DRF File Uploader API

A simple Django REST Framework API to upload images and PDFs with validation and metadata storage.

## Features

- Upload images (`.jpg, .jpeg, .png, .webp`) and PDFs
- Validate size (max 10MB), extension, and MIME type
- Store metadata: original name, extension, MIME, size, SHA256, is_image, created_at
- List files with pagination
- Retrieve single file details
- Authentication required for uploads
- Rate limiting for security

## Setup
git clone <repo-url>
cd <repo-folder>
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt
python manage.py migrate
python manage.py runserver



Validation:

Allowed: .jpg, .jpeg, .png, .webp, .pdf
Max size: 10MB
MIME must match extension
Sanitized filenames (max 200 chars)
PDF must start with %PDF-

أمثلة اختبار (curl)
# رفع ملف صحيح
curl -X POST http://127.0.0.1:8000/api/uploads/ \
  -H "Authorization: Bearer <TOKEN>" \
  -F "file=@sample.jpg"

# ملف امتداده ممنوع
curl -X POST http://127.0.0.1:8000/api/uploads/ \
  -H "Authorization: Bearer <TOKEN>" \
  -F "file=@malware.exe"

# قائمة الملفات
curl http://127.0.0.1:8000/api/uploads/?page=1

# تفاصيل
curl http://127.0.0.1:8000/api/uploads/1/


