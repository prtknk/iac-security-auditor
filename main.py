from fastapi import FastAPI, HTTPException, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware # NEW IMPORT
import shutil
import os
from scanner import scan_terraform
from database import init_db, save_scan

init_db()

app = FastAPI(title="IaC Security Auditor API")

# NEW: Configure CORS to allow our React frontend to communicate with the API
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], # In production, you would restrict this to your specific frontend URL
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.post("/scan/terraform/")
async def scan_tf_file(file: UploadFile = File(...)):
    if not file.filename.endswith('.tf'):
        raise HTTPException(status_code=400, detail="Only .tf files are supported.")
    
    temp_file_path = f"temp_{file.filename}"
    with open(temp_file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)
    
    try:
        # 1. Scan the file
        vulnerabilities = scan_terraform(temp_file_path)
        
        # 2. Save results to the SQL database
        scan_id = save_scan(file.filename, vulnerabilities)
        
        os.remove(temp_file_path)
        
        return {
            "scan_id": scan_id, # Return the DB ID
            "filename": file.filename,
            "vulnerabilities_found": len(vulnerabilities),
            "details": vulnerabilities
        }
    except Exception as e:
        if os.path.exists(temp_file_path):
            os.remove(temp_file_path)
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/health")
async def health_check():
    return {"status": "healthy"}