# IaC Security Auditor 🛡️

An enterprise-grade, full-stack security tool designed to parse **Infrastructure-as-Code (Terraform)** configurations. It identifies critical security misconfigurations—such as public S3 buckets, open SSH ports, and unencrypted databases—before they are deployed to the cloud.



## 🚀 Features
- **Automated Scanning:** Real-time analysis of `.tf` files for security anti-patterns.
- **Decoupled Architecture:** Asynchronous FastAPI backend optimized for high-velocity CI/CD environments.
- **Security Dashboard:** Responsive React command center for visualizing vulnerability severity.
- **Persistent Audit Trail:** SQLite integration to maintain a historical record of infrastructure scans.
- **Containerized & CI/CD Ready:** Fully Dockerized and validated via GitHub Actions.

## 🏗️ System Design
This project demonstrates a modern microservices approach:
1.  **Frontend:** A React SPA that handles file uploads and dynamic state management.
2.  **API Layer:** A Python FastAPI service that enforces CORS policies and manages request routing.
3.  **Engine:** A custom logic layer using `python-hcl2` to transform HCL into a searchable JSON structure.
4.  **Data Layer:** A persistence layer that logs scan results for future auditing.

## 🛠️ Tech Stack
- **Frontend:** React, Vite, Tailwind CSS
- **Backend:** Python 3.11, FastAPI, Pydantic
- **Parser:** python-hcl2
- **Database:** SQLite
- **DevOps:** Docker, GitHub Actions, Pytest

## 🚦 Getting Started

### Prerequisites
- **Docker Desktop** (Ensures the daemon is running)
- **Node.js** (v18+)
- **Python 3.11+**

### Running with Docker (Recommended)
1.  **Build the Image:**
    ```bash
    docker build -t iac-auditor-api .
    ```
2.  **Run the Container (with Volume Mount):**
    ```bash
    docker run -d -p 8000:8000 -v $(pwd)/scans.db:/app/scans.db --name iac-scanner iac-auditor-api
    ```

### Running the Frontend
1.  **Navigate and Install:**
    ```bash
    cd frontend
    npm install
    ```
2.  **Start Development Server:**
    ```bash
    npm run dev
    ```
    Visit: `http://localhost:5173`

## 🧪 Testing
The system maintains high reliability through automated unit and integration tests.
```bash
# Run the test suite
pytest -v
```
## 🔒 Security Rules Enforced

| ID | Resource | Severity | Issue Detected |
| :--- | :--- | :--- | :--- |
| **S3-001** | `aws_s3_bucket` | HIGH | Public-read ACLs exposing bucket data |
| **SG-001** | `aws_security_group` | CRITICAL | Port 22 (SSH) open to `0.0.0.0/0` |
| **RDS-001** | `aws_db_instance` | HIGH | Storage not encrypted at rest |

## 🗺️ Future Roadmap
- [ ] **Multi-Cloud Support:** Expand scanning logic for Azure (Bicep) and GCP (Deployment Manager).
- [ ] **Auto-Remediation:** Integrate with the GitHub API to automatically open PRs that fix detected vulnerabilities.
- [ ] **Enterprise Auth:** Implement JWT-based authentication for secure dashboard access.
