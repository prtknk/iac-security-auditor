import pytest
from fastapi.testclient import TestClient
import os
import sys

# Add the parent directory to the path so we can import our app modules
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from main import app
from scanner import scan_terraform

client = TestClient(app)

# --- UNIT TESTS FOR THE CORE ENGINE ---

def test_scanner_catches_vulnerability():
    """Test that the engine correctly identifies a public-read S3 bucket."""
    results = scan_terraform("tests/mock_vulnerable.tf")
    
    assert len(results) == 1
    assert results[0]['resource'] == "bad_bucket"
    assert results[0]['issue'] == "S3 bucket has public-read ACL."
    assert results[0]['severity'] == "HIGH"

def test_scanner_passes_safe_code():
    """Test that the engine returns no vulnerabilities for safe code."""
    results = scan_terraform("tests/mock_safe.tf")
    
    assert len(results) == 0

# --- INTEGRATION TESTS FOR THE API ---

def test_health_check():
    """Test that the API is alive and returning 200 OK."""
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "healthy"}

def test_scan_endpoint_with_vulnerable_file():
    """Test the full API flow with a file upload."""
    with open("tests/mock_vulnerable.tf", "rb") as f:
        response = client.post(
            "/scan/terraform/",
            files={"file": ("mock_vulnerable.tf", f, "application/octet-stream")}
        )
    
    assert response.status_code == 200
    data = response.json()
    assert data["filename"] == "mock_vulnerable.tf"
    assert data["vulnerabilities_found"] == 1
    assert "scan_id" in data  # Proves the database save function fired