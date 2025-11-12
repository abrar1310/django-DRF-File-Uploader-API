# Django DRF File Uploader API

Simple REST API to upload files (images + PDFs), validate them, and view file details.

---

## Requirements

- Python 3.10+  
- Install dependencies:

```bash
pip install -r requirements.txt
requirements.txt:

shell
Copy code
Django>=5.0
djangorestframework
python-magic
Pillow
Run Locally
bash
Copy code
git clone <repo_url>
cd fileuploader
python -m venv venv
# Linux/macOS
source venv/bin/activate
# Windows
venv\Scripts\activate
pip install -r requirements.txt
python manage.py migrate
python manage.py createsuperuser
python manage.py runserver
API base URL: http://127.0.0.1:8000/api/uploads/

Example CURL Requests
Upload a file (login required)
bash
Copy code
curl -X POST http://127.0.0.1:8000/api/uploads/ \
  -u username:password \
  -F "file=@sample.jpg"
List files
bash
Copy code
curl http://127.0.0.1:8000/api/uploads/
File details by ID
bash
Copy code
curl http://127.0.0.1:8000/api/uploads/1/
yaml
Copy code

---

This snippet is **short, clear, and fully GitHub-ready**, covering: requirements, setup, running locally, and example API requests.  

If you want, I can make an **even more compact “one-page” version** suitable for GitHub repos with just **3 sections**. Do you want me to do that?











ChatGPT can make mistak
