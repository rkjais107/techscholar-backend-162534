# TechScholar Backend Assignment

## Introduction

This project is a sub-part of an e-commerce Backend application that provides an API to upload static files (images, pdfs, videos, or any binary file). The uploaded files are encrypted and stored securely, with a public path provided for each file. However, the files cannot be read directly from this path without decryption.

## Requirements

- Python-based framework (FastAPI)
- File encryption before storage
- Public but unreadable file path

## How to Run

### Prerequisites

- Docker (optional)
- Python 3.9+

### Setting Up the Project

1. **Clone the repository**:

   ```bash
   git clone https://github.com/yourusername/techscholar-backend-<6-digit-random>.git
   cd techscholar-backend-<6-digit-random>
   ```

2. **Create a virtual environment**:

   ```bash
   python -m venv venv
   ```

3. **Activate the virtual environment**:

   - On **Windows**:
     ```bash
     venv\Scripts\activate
     ```
   - On **macOS and Linux**:
     ```bash
     source venv/bin/activate
     ```

4. **Install dependencies**:

   ```bash
   pip install -r requirements.txt
   ```

5. **Run the application**:
   ```bash
   uvicorn app.main:app --reload --reload-dir ./app --reload-dir ./tests
   ```

### Running with Docker (optional)

1. **Build the Docker image**:

   ```bash
   docker build -t techscholar-backend .
   ```

2. **Run the Docker container**:
   ```bash
   docker run -d -p 8000:8000 techscholar-backend
   ```

## API Endpoints

### Upload File

- **URL**: `/upload/`
- **Method**: `POST`
- **Request**: `multipart/form-data` with file
- **Response**: JSON with message and path

### Read File

- **URL**: `/files/{filename}`
- **Method**: `GET`
- **Response**: JSON with filename and decrypted contents

## Assumptions

- The encryption key is generated and stored securely in the `secret.key` file.
- Uploaded files are stored in the `uploads` directory.
- The application does not require authentication for simplicity.

## Running Tests

To run the tests, use the following command:

```bash
pytest
```
