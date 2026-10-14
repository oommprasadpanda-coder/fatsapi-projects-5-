from fastapi import UploadFile , File , APIRouter , HTTPException 
import shutil
import os 


router = APIRouter()


UPLOAD_DIR ="uploads"
if not os.path.exists (UPLOAD_DIR):
    os.makedirs(UPLOAD_DIR)


@router.post("/upload")
def upload_files(file : UploadFile = File(...)):
    filename = file.filename 
    file_path = os.path.join(UPLOAD_DIR , filename)

    if not filename :
        raise HTTPException(
            status_code=400,
            detail="file not selected"
        )

    with open(file_path, "wb") as buffer :
        shutil.copyfileobj(file.file , buffer)


    return {
        "message" : "File Uploaded Sucessfully",
        "fileName" : filename,
        "file_url" : f"http://127.0.0.1:8000/files/{filename}"

    }






