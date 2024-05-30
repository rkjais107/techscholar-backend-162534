import binascii
from fastapi import HTTPException, FastAPI, File, UploadFile 
from fastapi.responses import JSONResponse, FileResponse
from cryptography.fernet import Fernet
import os

app = FastAPI()  # Ensure this line is present

# Load or generate encryption key
key_file = 'secret.key'
if not os.path.exists(key_file):
    key = Fernet.generate_key()
    with open(key_file, 'wb') as key_out:
        key_out.write(key)
else:
    with open(key_file, 'rb') as key_in:
        key = key_in.read()

cipher_suite = Fernet(key)
UPLOAD_FOLDER = 'uploads'
SAMPLE_DATA = 'sample_data'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

# Function to encrypt image
async def encryptImage(file):
    file_name = file.filename.split(".")[0].lower()
    file_ext  = file.filename.split(".")[-1].lower()
    imgContent = await file.read()
    hexImg = binascii.hexlify(imgContent)
    encHexImg = cipher_suite.encrypt(hexImg)
    imgFilename = file_name + "." + file_ext + ".txt"
    file_location = os.path.join(UPLOAD_FOLDER, imgFilename)
    with open(file_location, mode='wb') as hexValueFile:
        hexValueFile.write(encHexImg)
    return file_location

# Function to decrypt image
async def decryptImage(filename):
    file_name_txt = filename + ".txt"
    file_location = os.path.join(UPLOAD_FOLDER, file_name_txt)
    with open(file_location, "rb") as imageHexValue:
        encHexValue  = imageHexValue.read()
    hexValue  = cipher_suite.decrypt(encHexValue)
    binValue = binascii.unhexlify(hexValue)
    new_filename = filename
    new_file_location = os.path.join(UPLOAD_FOLDER, new_filename)
    with open(new_file_location, mode='wb') as orgImg:
        orgImg.write(binValue)
    return new_file_location

@app.post("/upload/")
async def upload_file(file: UploadFile = File(...)):    
    # Get the file extension
    file_name = file.filename.split(".")[0].lower()
    file_extension = file.filename.split(".")[-1].lower()
    
    # Check if the file extension is valid
    valid_extensions = { "txt", "pdf", "jpg", "jpeg", "png", "mp4" }  
    
    # Add more valid extensions as needed
    if file_extension not in valid_extensions:
        raise HTTPException(status_code=422, detail="Invalid file extension. Only .txt, .pdf, .jpg, .png, .gif are allowed.")
    
    # Working with images - jpg, jpeg, png
    image_extensions = { "jpg", "jpeg", "png", "mp4"}
    textfile_extensions = { "txt", "pdf" }
    if file_extension in image_extensions:
        file_location = await encryptImage(file)
        return JSONResponse(content={"message": f"File '{file.filename}' uploaded successfully"})
    elif file_extension in textfile_extensions:
        file_location = os.path.join(UPLOAD_FOLDER, file.filename + ".txt")
        contents = await file.read()
        encrypted_contents = cipher_suite.encrypt(contents)
        with open(file_location, "wb") as f:
            f.write(encrypted_contents)
        return JSONResponse(content={"message": f"File '{file.filename}' uploaded successfully"})
        
@app.get("/files/{filename}")
async def read_file(filename: str):
    orgfilename = filename.split(".")[0].lower()
    orgfileext = filename.split(".")[1].lower()
    encfilename = filename + ".txt"
    file_location = os.path.join(UPLOAD_FOLDER, encfilename)
    if not os.path.exists(file_location):
        return JSONResponse(content={"error": "File not found"}, status_code=404)
    
    # Image Extension
    image_extension_list = {"jpg", "jpeg", "png", "mp4"}
    textfile_extensions = { "txt", "pdf" }
    if orgfileext in image_extension_list:
        new_file_location = await decryptImage(filename)
        return FileResponse(new_file_location)
    elif orgfileext in textfile_extensions:
        with open(file_location, "rb") as f:
            encrypted_contents = f.read()
        decrypted_contents = cipher_suite.decrypt(encrypted_contents)
        new_file_location = os.path.join(UPLOAD_FOLDER, filename)
        with open(new_file_location, mode='wb') as orgtextfile:
            orgtextfile.write(decrypted_contents)
        return FileResponse(new_file_location)