import hashlib
import magic
import re
from PIL import Image
from rest_framework import serializers
from .models import Upload

ALLOWED_EXTENSIONS = ['.jpg', '.jpeg', '.png', '.webp', '.pdf']
MAX_SIZE = 10 * 1024 * 1024  # 10MB

def sanitize_filename(filename):
    filename = filename.split('/')[-1].split('\\')[-1]  # Remove paths
    filename = re.sub(r'[^A-Za-z0-9._-]', '', filename)
    return filename[:200]

class UploadSerializer(serializers.ModelSerializer):
    file = serializers.FileField(write_only=True)

    class Meta:
        model = Upload
        fields = '__all__'
        read_only_fields = ['original_name', 'extension', 'mime_type', 'size_bytes', 'sha256', 'is_image', 'created_at']

    def validate_file(self, file):
        # Check size
        if file.size > MAX_SIZE:
            raise serializers.ValidationError("File too large (max 10MB).")
        
        # Sanitize name and extract extension
        original_name = sanitize_filename(file.name)
        extension = '.' + original_name.split('.')[-1].lower()
        if extension not in ALLOWED_EXTENSIONS:
            raise serializers.ValidationError(f"Extension {extension} not allowed.")

        # Read bytes to check MIME
        file.seek(0)
        mime = magic.from_buffer(file.read(2048), mime=True)
        file.seek(0)

        if extension == '.pdf' and not mime.startswith('application/pdf'):
            raise serializers.ValidationError("PDF MIME mismatch.")
        if extension in ['.jpg','.jpeg','.png','.webp'] and not mime.startswith('image/'):
            raise serializers.ValidationError("Image MIME mismatch.")
        
        # Check PDF header
        if extension == '.pdf':
            file.seek(0)
            header = file.read(5)
            if header != b'%PDF-':
                raise serializers.ValidationError("Invalid PDF file.")
            file.seek(0)

        return file

    def create(self, validated_data):
        file = validated_data.pop('file')
        original_name = sanitize_filename(file.name)
        extension = '.' + original_name.split('.')[-1].lower()
        size_bytes = file.size
        mime_type = magic.from_buffer(file.read(2048), mime=True)
        file.seek(0)
        sha256_hash = hashlib.sha256(file.read()).hexdigest()
        file.seek(0)
        is_image = extension in ['.jpg','.jpeg','.png','.webp']

        upload = Upload.objects.create(
            file=file,
            original_name=original_name,
            extension=extension,
            mime_type=mime_type,
            size_bytes=size_bytes,
            sha256=sha256_hash,
            is_image=is_image
        )
        return upload
