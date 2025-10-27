
````{"id":"59104","variant":"standard","title":"README.md for Skika Backend – A Voice for Gatundu North"}
# Skika Backend – A Voice for Gatundu North

## 🧩 Overview
The **Skika Backend System** is the backbone of the Skika platform, powering **USSD interactions**, securely managing data, coordinating **feedback between citizens and leaders**, and ensuring **transparency and accountability**.  

It connects the **frontend (USSD & Dashboard)**, **database (PostgreSQL)**, and **APIs (communication layer)** to achieve these goals.  
The backend is designed for **scalability**, **data security**, and **ease of integration**.

---

## 🎯 Objectives
- Receive and store reports from USSD users across Gatundu North.  
- Facilitate two-way communication between youth (citizens) and administrators (e.g., NG-CDF officers, local leaders).  
- Automate feedback loops using SMS notifications.  
- Ensure data integrity, privacy, and traceability for every interaction.  

---

## 🏗 System Architecture (High-Level)
```
User (Phone)
   ↓
USSD Gateway (Africa's Talking)
   ↓
Django REST API
   ↓
PostgreSQL Database
   ↓
Admin Dashboard (React)
   ↓
SMS Notification (Africa's Talking)
```

---

## 🔄 Data Flow
1. **User Dial:** A citizen dials `*456*01#` and selects an option (Report / Suggest / Track).  
2. **USSD Gateway Request:** Africa's Talking forwards user input to the Skika backend via POST requests.  
3. **API Processing:** Django REST API validates and stores the request, generating a reference code (e.g., `SKK-2025-012`).  
4. **Database Entry:** The report is stored in PostgreSQL under `status = "Received"`.  
5. **Dashboard Update:** Admins can view, filter, and act on reports via the web dashboard.  
6. **Feedback Loop:** Status changes trigger SMS updates to users.  

---

## 🧠 Technology Stack

| **Layer** | **Technology** | **Purpose** |
|------------|----------------|--------------|
| Backend Framework | Django REST Framework (Python) | Rapid API development, scalability, built-in authentication |
| Database | PostgreSQL | Reliable relational database supporting complex queries |
| USSD/SMS Integration | Africa's Talking API | Handles incoming and outgoing USSD/SMS requests |
| Hosting/Deployment | Render / Railway | Simple, scalable, and supports continuous deployment |
| Authentication | JWT (JSON Web Tokens) | Secures dashboard and API endpoints |
| Version Control | GitHub | Team collaboration and change tracking |

---

## ⚙️ Setup Instructions

### Prerequisites
- Python 3.8+  
- PostgreSQL  
- Redis (for caching)  
- Africa's Talking API credentials  

### Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/yourusername/skika-backend.git
   cd skika-backend
   ```

2. **Create a virtual environment and activate it**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Configure environment variables in a `.env` file**
   ```text
   SECRET_KEY=your_secret_key
   DEBUG=True
   DB_USER=your_db_user
   DB_PASSWORD=your_db_password
   AFRICASTALKING_USERNAME=your_africastalking_username
   AFRICASTALKING_API_KEY=your_africastalking_api_key
   ```

5. **Set up the database**
   ```bash
   python manage.py makemigrations
   python manage.py migrate
   ```

6. **Create a superuser**
   ```bash
   python manage.py createsuperuser
   ```

7. **Run the development server**
   ```bash
   python manage.py runserver
   ```

---

## 📡 API Documentation

All endpoints require **JWT authentication** for admin access or **token-based authentication** for USSD.  
Obtain a JWT token via `/api/token/` using `rest_framework_simplejwt`.

### 1. User Management
**Register a new user**
```
POST /api/users/register/
```
**Sample Input**
```json
{
  "phone_number": "+254712345678",
  "role": "citizen",
  "ward": "Ward1"
}
```
**Sample Output (201 Created)**
```json
{
  "id": 1,
  "phone_number": "+254712345678",
  "role": "citizen",
  "ward": "Ward1",
  "created_at": "2025-10-27T11:36:00Z"
}
```

---

**List all users (admin only)**
```
GET /api/users/
```
**Sample Output**
```json
[
  {
    "id": 1,
    "phone_number": "+254712345678",
    "role": "citizen",
    "ward": "Ward1",
    "created_at": "2025-10-27T11:36:00Z"
  }
]
```

---

### 2. Report Management
**Create a new report**
```
POST /api/reports/
```
**Sample Input**
```json
{
  "ward": "Ward1",
  "category": "Infrastructure",
  "description": "Road issue"
}
```
**Sample Output**
```json
{
  "id": 1,
  "ref_id": "SKK-2025-abc123",
  "user": 1,
  "ward": "Ward1",
  "category": "Infrastructure",
  "description": "Road issue",
  "status": "Received",
  "created_at": "2025-10-27T11:36:00Z",
  "updated_at": "2025-10-27T11:36:00Z",
  "audit_trail": "Initial creation at Mon Oct 27 11:36:00 2025"
}
```

**Update report status**
```
POST /api/reports/{id}/update_status/
```
**Sample Input**
```json
{
  "status": "Under Review"
}
```
**Sample Output**
```json
{
  "status": "success"
}
```

---

**Handle USSD menu interactions**
```
POST /api/reports/ussd_menu/
```
**Sample Input**
```json
{
  "sessionId": "session123",
  "text": "1 Test Issue"
}
```
**Sample Output**
```json
{
  "USSResponse": "END Report SKK-2025-xyz789 submitted"
}
```

---

### 3. Project Management
**Create a new project**
```
POST /api/projects/
```
**Sample Input**
```json
{
  "name": "Road Project",
  "ward": "Ward1",
  "description": "New road construction"
}
```
**Sample Output**
```json
{
  "id": 1,
  "name": "Road Project",
  "ward": "Ward1",
  "description": "New road construction",
  "created_at": "2025-10-27T11:36:00Z"
}
```

---

### 4. Feedback Management
**Submit feedback for a report**
```
POST /api/feedback/
```
**Sample Input**
```json
{
  "report": 1,
  "satisfaction": "Yes",
  "comments": "Good work"
}
```
**Sample Output**
```json
{
  "id": 1,
  "report": 1,
  "satisfaction": "Yes",
  "comments": "Good work",
  "created_at": "2025-10-27T11:36:00Z"
}
```

---

### 5. Analytics
**Retrieve sentiment analysis of report descriptions**
```
GET /api/reports/sentiment_analysis/
```
**Sample Output**
```json
{
  "1": 0.5,
  "2": -0.2
}
```

---

## 🧪 Testing
Run tests to verify API functionality:
```bash
python manage.py test
```

---

## 🤝 Contributing
1. Fork the repository.  
2. Create a new branch:
   ```bash
   git checkout -b feature-branch
   ```
3. Commit changes:
   ```bash
   git commit -m "Add new feature"
   ```
4. Push to the branch:
   ```bash
   git push origin feature-branch
   ```
5. Submit a pull request.

---

## ⚖️ License
This project is licensed under the **MIT License** — see the LICENSE file for details.

---

## 📬 Contact
For questions or support, contact the project maintainers at **your-email@example.com**.

---

### 📝 Notes
- Replace placeholders (`yourusername`, `your_secret_key`, `your-email@example.com`) with actual values.  
- The `requirements.txt` file should include:
  ```
  django
  djangorestframework
  djangorestframework-simplejwt
  psycopg2-binary
  python-decouple
  africastalking
  django-redis
  textblob
  ```
````

Would you like me to add GitHub badges (e.g., build passing, Python version, license) or a project logo section at the top?
