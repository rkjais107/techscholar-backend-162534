import sys
import os
import pytest
from fastapi.testclient import TestClient

# Ensure the 'app' module is in the sys.path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app.main import app, UPLOAD_FOLDER, SAMPLE_DATA

# Create a TestClient instance
client = TestClient(app)

# Helper function to clean up uploaded files after tests
def cleanup_uploaded_files():
    for filename in os.listdir(UPLOAD_FOLDER):
        file_path = os.path.join(UPLOAD_FOLDER, filename)
        if os.path.isfile(file_path):
            os.remove(file_path)

@pytest.fixture(scope="module", autouse=True)
def setup_and_teardown():
    # Cleanup before tests
    cleanup_uploaded_files()
    yield
    # Cleanup after tests
    cleanup_uploaded_files()

def test_upload_file():
    # Attempt to upload a file
    sample_file_path = os.path.join(SAMPLE_DATA, "samplefile.txt")
    with open(sample_file_path, "rb") as f:
        file_data = {"file": ("samplefile.txt", f, "multipart/form-data")}
        response = client.post("/upload/", files=file_data)
    assert response.status_code == 200
    assert response.json()["message"] == "File 'samplefile.txt' uploaded successfully"

def test_read_file():
    # Attempt to read a file    
    filename = "samplefile.txt"  
    response = client.get(f"/files/{filename}")
    assert response.status_code == 200
    
def test_upload_pdf_file():
    # Attempt to upload a file
    sample_file_path = os.path.join(SAMPLE_DATA, "samplepdf.pdf")
    with open(sample_file_path, "rb") as f:
        file_data = {"file": ("samplepdf.pdf", f, "multipart/form-data")}
        response = client.post("/upload/", files=file_data)
    assert response.status_code == 200
    assert response.json()["message"] == "File 'samplepdf.pdf' uploaded successfully"

def test_read_pdf_file():
    # Attempt to read a file    
    filename = "samplepdf.pdf"  
    response = client.get(f"/files/{filename}")
    assert response.status_code == 200
    
def test_upload_image_file():
    # Attempt to upload a file
    sample_file_path = os.path.join(SAMPLE_DATA, "sampleimage.png")
    with open(sample_file_path, "rb") as f:
        file_data = {"file": ("sampleimage.png", f, "multipart/form-data")}
        response = client.post("/upload/", files=file_data)
    assert response.status_code == 200
    assert response.json()["message"] == "File 'sampleimage.png' uploaded successfully"

def test_read_image_file():
    # Attempt to read a file    
    filename = "sampleimage.png"  
    response = client.get(f"/files/{filename}")
    assert response.status_code == 200
    
def test_upload_video_file():
    # Attempt to upload a file
    sample_file_path = os.path.join(SAMPLE_DATA, "samplevideo.mp4")
    with open(sample_file_path, "rb") as f:
        file_data = {"file": ("samplevideo.mp4", f, "multipart/form-data")}
        response = client.post("/upload/", files=file_data)
    assert response.status_code == 200
    assert response.json()["message"] == "File 'samplevideo.mp4' uploaded successfully"

def test_read_video_file():
    # Attempt to read a file    
    filename = "samplevideo.mp4"  
    response = client.get(f"/files/{filename}")
    assert response.status_code == 200
    
def test_upload_invalid_file_extension():
    # Attempt to upload a file with an invalid extension
    files = {"file": ("invalid_file.xyz", b"Invalid file content")}
    response = client.post("/upload/", files=files)
    assert response.status_code == 422  # Unprocessable Entity

def test_read_nonexistent_file():
    # Attempt to retrieve a file that does not exist
    response = client.get("/files/nonexistent_file.txt")
    assert response.status_code == 404  # Not Found

def test_upload_multiple_files():
    # Attempt to upload multiple files
    file1 = ("file1.txt", b"File 1 content")
    file2 = ("file2.txt", b"File 2 content")
    files = {"file1": file1, "file2": file2}
    response = client.post("/upload/", files=files)
    assert response.status_code == 422  # Unprocessable Entity

def test_upload_large_file():
    # Attempt to upload a large file (simulate large file upload)
    large_file_content = b"X" * (10 * 1024 * 1024)  # 10 MB
    files = {"file": ("large_file.txt", large_file_content)}
    response = client.post("/upload/", files=files)
    assert response.status_code == 200
    assert response.json()["message"] == "File 'large_file.txt' uploaded successfully"

