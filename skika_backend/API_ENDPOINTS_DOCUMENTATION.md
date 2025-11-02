# SKIKA BACKEND API ENDPOINTS DOCUMENTATION

## Base URL: `http://127.0.0.1:8000/api/`

---

## 📚 TABLE OF CONTENTS

1. [Authentication Endpoints](#authentication-endpoints)
2. [User Management Endpoints](#user-management-endpoints)
3. [Ward Management Endpoints](#ward-management-endpoints)
4. [Project Management Endpoints](#project-management-endpoints)
5. [Report Management Endpoints](#report-management-endpoints)
6. [Feedback Management Endpoints](#feedback-management-endpoints)
7. [Audit Log Endpoints](#audit-log-endpoints)
8. [Notification Endpoints](#notification-endpoints)
9. [Translation & Utility Endpoints](#translation--utility-endpoints)
10. [USSD Integration Endpoint](#ussd-integration-endpoint)

---

## 🔐 AUTHENTICATION ENDPOINTS

### 1. Dashboard Login
**Endpoint:** `POST /api/dashboard-login/`
**Description:** Login for dashboard users (admins, leaders)
**Authentication:** None required
**Content-Type:** `application/json`

**Expected Input:**
```json
{
    "phone_number": "+254712345678",
    "password": "your_password"
}
```

**Success Response (200 OK):**
```json
{
    "refresh": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9...",
    "access": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9...",
    "user": {
        "id": "550e8400-e29b-41d4-a716-446655440000",
        "phone_number": "+254712345678",
        "first_name": "John",
        "last_name": "Doe",
        "role": "admin",
        "ward": "550e8400-e29b-41d4-a716-446655440001"
    }
}
```

**Error Response (401 Unauthorized):**
```json
{
    "error": "Invalid credentials"
}
```

### 2. Register Citizen
**Endpoint:** `POST /api/register-citizen/`
**Description:** Register a citizen via USSD or API
**Authentication:** None required
**Content-Type:** `application/json`

**Expected Input:**
```json
{
    "phone_number": "+254712345678",
    "ward": "Gatundu North"
}
```

**Success Response (201 Created):**
```json
{
    "id": "550e8400-e29b-41d4-a716-446655440000",
    "phone_number": "+254712345678",
    "ward": "550e8400-e29b-41d4-a716-446655440001",
    "created_at": "2025-10-31T10:30:00Z"
}
```

**Error Response (400 Bad Request):**
```json
{
    "error": "phone_number and ward required"
}
```

---

## 👥 USER MANAGEMENT ENDPOINTS

### 3. Dashboard Users List/Create
**Endpoint:** `GET/POST /api/dashboard-users/`
**Description:** List all dashboard users or create new dashboard user
**Authentication:** JWT Token (Admin only)
**Headers:** `Authorization: Bearer <access_token>`

**GET Method - List Users:**
**Success Response (200 OK):**
```json
[
    {
        "id": "550e8400-e29b-41d4-a716-446655440000",
        "phone_number": "+254712345678",
        "first_name": "John",
        "last_name": "Doe",
        "email": "john@example.com",
        "role": "admin",
        "ward": "550e8400-e29b-41d4-a716-446655440001",
        "is_active": true,
        "date_joined": "2025-10-31T10:30:00Z"
    }
]
```

**POST Method - Create User:**
**Expected Input:**
```json
{
    "phone_number": "+254712345679",
    "first_name": "Jane",
    "last_name": "Smith",
    "email": "jane@example.com",
    "password": "securepassword123",
    "role": "leader",
    "ward": "550e8400-e29b-41d4-a716-446655440001"
}
```

### 4. Dashboard User Detail
**Endpoints:** 
- `GET /api/dashboard-users/{id}/` - Get user details
- `PUT /api/dashboard-users/{id}/` - Update user
- `PATCH /api/dashboard-users/{id}/` - Partial update
- `DELETE /api/dashboard-users/{id}/` - Delete user

### 5. Citizens List/Create
**Endpoint:** `GET/POST /api/citizens/`
**Description:** List all citizens or create new citizen
**Authentication:** JWT Token (Admin only)

**GET Method - List Citizens:**
**Success Response (200 OK):**
```json
[
    {
        "id": "550e8400-e29b-41d4-a716-446655440000",
        "phone_number": "+254712345678",
        "ward": {
            "id": "550e8400-e29b-41d4-a716-446655440001",
            "name": "Gatundu North"
        },
        "created_at": "2025-10-31T10:30:00Z"
    }
]
```

---

## 🏘️ WARD MANAGEMENT ENDPOINTS

### 6. Wards List
**Endpoint:** `GET /api/wards/`
**Description:** List all wards (read-only)
**Authentication:** None required

**Success Response (200 OK):**
```json
[
    {
        "id": "550e8400-e29b-41d4-a716-446655440000",
        "name": "Gatundu North",
        "constituency": "Gatundu North",
        "county": "Kiambu",
        "population_estimate": 45000,
        "created_at": "2025-10-31T10:30:00Z"
    }
]
```

### 7. Ward Detail
**Endpoint:** `GET /api/wards/{id}/`
**Description:** Get specific ward details
**Authentication:** None required

---

## 🏗️ PROJECT MANAGEMENT ENDPOINTS

### 8. Projects List/Create
**Endpoint:** `GET/POST /api/projects/`
**Description:** List all projects or create new project
**Authentication:** JWT Token (Admin only)

**GET Method - List Projects:**
**Success Response (200 OK):**
```json
[
    {
        "id": "550e8400-e29b-41d4-a716-446655440000",
        "project_code": "PROJ-2025-001",
        "title_en": "New School Construction",
        "title_sw": "Ujenzi wa Shule Mpya",
        "description_en": "Building a new primary school",
        "description_sw": "Kujenga shule mpya ya msingi",
        "ward": "550e8400-e29b-41d4-a716-446655440001",
        "category_en": "education",
        "category_sw": "elimu",
        "status_en": "ongoing",
        "status_sw": "inaendelea",
        "budget_allocated": "5000000.00",
        "budget_used": "2000000.00",
        "start_date": "2025-01-15",
        "end_date": "2025-12-15",
        "created_by": "550e8400-e29b-41d4-a716-446655440002",
        "created_at": "2025-10-31T10:30:00Z",
        "updated_at": "2025-10-31T10:30:00Z"
    }
]
```

**POST Method - Create Project:**
**Expected Input:**
```json
{
    "project_code": "PROJ-2025-002",
    "title_en": "Road Rehabilitation",
    "title_sw": "Ukarabati wa Barabara",
    "description_en": "Rehabilitate main road",
    "description_sw": "Kukarabati barabara kuu",
    "ward": "550e8400-e29b-41d4-a716-446655440001",
    "category_en": "infrastructure",
    "status_en": "planned",
    "budget_allocated": "3000000.00",
    "start_date": "2025-02-01",
    "end_date": "2025-06-30"
}
```

**Note:** `category_sw` and `status_sw` will be auto-filled based on English selections.

### 9. Project Detail
**Endpoints:** 
- `GET /api/projects/{id}/` - Get project details
- `PUT /api/projects/{id}/` - Update project
- `PATCH /api/projects/{id}/` - Partial update
- `DELETE /api/projects/{id}/` - Delete project

---

## 📝 REPORT MANAGEMENT ENDPOINTS

### 10. Reports List/Create
**Endpoint:** `GET/POST /api/reports/`
**Description:** List reports or create new report
**Authentication:** JWT Token required

**GET Method - List Reports:**
**Query Parameters:**
- `category_en` - Filter by English category
- `status_en` - Filter by English status
- `ward` - Filter by ward ID

**Success Response (200 OK):**
```json
[
    {
        "id": "550e8400-e29b-41d4-a716-446655440000",
        "ref_code": "SKK-2025-001",
        "citizen": "550e8400-e29b-41d4-a716-446655440001",
        "ward": "550e8400-e29b-41d4-a716-446655440002",
        "category_en": "infrastructure",
        "category_sw": "miundombinu",
        "description": "Pothole on main road needs fixing",
        "status_en": "received",
        "status_sw": "imepokelewa",
        "project": null,
        "priority_level_en": "medium",
        "priority_level_sw": "kati",
        "admin_notes": "",
        "created_at": "2025-10-31T10:30:00Z",
        "updated_at": "2025-10-31T10:30:00Z"
    }
]
```

**POST Method - Create Report:**
**Expected Input:**
```json
{
    "citizen": "550e8400-e29b-41d4-a716-446655440001",
    "ward": "550e8400-e29b-41d4-a716-446655440002",
    "category_en": "health",
    "description": "Clinic needs medical supplies",
    "priority_level_en": "high"
}
```

**Note:** Swahili fields (`category_sw`, `status_sw`, `priority_level_sw`) will be auto-filled.

### 11. Report Detail
**Endpoints:** 
- `GET /api/reports/{id}/` - Get report details
- `PUT /api/reports/{id}/` - Update report
- `PATCH /api/reports/{id}/` - Partial update
- `DELETE /api/reports/{id}/` - Delete report

### 12. Update Report Status (Special Action)
**Endpoint:** `POST /api/reports/{id}/update_status/`
**Description:** Update report status with bilingual SMS notification
**Authentication:** JWT Token (Admin only)

**Expected Input:**
```json
{
    "status_en": "under_review"
}
```

**Success Response (200 OK):**
```json
{
    "message": "Status updated and bilingual SMS sent",
    "status_en": "under_review",
    "status_sw": "chini_ya_ukaguzi"
}
```

**SMS Sent to Citizen:**
```
Report SKK-2025-001 is now Under Review. / Ripoti SKK-2025-001 sasa ni Chini ya Ukaguzi.
```

---

## 💬 FEEDBACK MANAGEMENT ENDPOINTS

### 13. Feedback List/Create
**Endpoint:** `GET/POST /api/feedback/`
**Description:** List feedback or create new feedback
**Authentication:** JWT Token required

**POST Method - Create Feedback:**
**Expected Input:**
```json
{
    "report": "550e8400-e29b-41d4-a716-446655440000",
    "citizen": "550e8400-e29b-41d4-a716-446655440001",
    "rating": 4,
    "comment": "Good response time"
}
```

**Success Response (201 Created):**
```json
{
    "id": "550e8400-e29b-41d4-a716-446655440000",
    "report": "550e8400-e29b-41d4-a716-446655440001",
    "citizen": "550e8400-e29b-41d4-a716-446655440002",
    "rating": 4,
    "comment": "Good response time",
    "created_at": "2025-10-31T10:30:00Z"
}
```

---

## 📊 AUDIT LOG ENDPOINTS

### 14. Audit Logs List
**Endpoint:** `GET /api/audit-logs/`
**Description:** List all audit logs (read-only)
**Authentication:** JWT Token (Admin only)

**Success Response (200 OK):**
```json
[
    {
        "id": "550e8400-e29b-41d4-a716-446655440000",
        "user": "550e8400-e29b-41d4-a716-446655440001",
        "action_type": "status_change",
        "table_name": "report",
        "record_id": "550e8400-e29b-41d4-a716-446655440002",
        "description": "Status: received→under_review | imepokelewa→chini_ya_ukaguzi",
        "timestamp": "2025-10-31T10:30:00Z"
    }
]
```

---

## 🔔 NOTIFICATION ENDPOINTS

### 15. Notifications List
**Endpoint:** `GET /api/notifications/`
**Description:** List all notifications (read-only)
**Authentication:** JWT Token (Admin only)

**Success Response (200 OK):**
```json
[
    {
        "id": "550e8400-e29b-41d4-a716-446655440000",
        "recipient_phone": "+254712345678",
        "message": "Report SKK-2025-001 is now Under Review. / Ripoti SKK-2025-001 sasa ni Chini ya Ukaguzi.",
        "status": "sent",
        "trigger_event": "status_updated",
        "created_at": "2025-10-31T10:30:00Z",
        "sent_at": "2025-10-31T10:31:00Z"
    }
]
```

---

## 🌍 TRANSLATION & UTILITY ENDPOINTS

### 16. Get All Translations
**Endpoint:** `GET /api/translations/`
**Description:** Get all available translations for choice fields
**Authentication:** None required

**Success Response (200 OK):**
```json
{
    "database_values": {
        "category": {
            "education": "elimu",
            "infrastructure": "miundombinu",
            "health": "afya",
            "water": "maji",
            "environment": "mazingira",
            "security": "usalama",
            "other": "mengine"
        },
        "project_status": {
            "planned": "imepangwa",
            "ongoing": "inaendelea",
            "completed": "imekamilika",
            "stalled": "imekwama"
        },
        "report_status": {
            "received": "imepokelewa",
            "under_review": "chini_ya_ukaguzi",
            "action_taken": "hatua_imechukuliwa",
            "resolved": "imetatuliwa",
            "closed": "imefungwa"
        },
        "priority": {
            "low": "chini",
            "medium": "kati",
            "high": "juu"
        }
    },
    "display_values": {
        "category": {
            "education": "Elimu",
            "infrastructure": "Miundombinu",
            "health": "Afya"
        }
    },
    "supported_languages": ["en", "sw"],
    "field_types": ["category", "project_status", "report_status", "priority"]
}
```

### 17. Translate Specific Field
**Endpoint:** `POST /api/translate/`
**Description:** Translate a specific field value from English to Swahili
**Authentication:** None required

**Expected Input:**
```json
{
    "field_type": "category",
    "english_value": "health"
}
```

**Success Response (200 OK):**
```json
{
    "field_type": "category",
    "english_value": "health",
    "swahili_value": "afya",
    "display_value": "Afya"
}
```

### 18. Dashboard Statistics
**Endpoint:** `GET /api/dashboard-stats/`
**Description:** Get dashboard statistics with bilingual labels
**Authentication:** JWT Token required

**Success Response (200 OK):**
```json
{
    "reports": {
        "total": 125,
        "by_status_en": {
            "received": 45,
            "under_review": 30,
            "action_taken": 25,
            "resolved": 20,
            "closed": 5
        },
        "by_status_sw": {
            "imepokelewa": 45,
            "chini_ya_ukaguzi": 30,
            "hatua_imechukuliwa": 25,
            "imetatuliwa": 20,
            "imefungwa": 5
        },
        "by_category_en": {
            "infrastructure": 50,
            "health": 30,
            "education": 25,
            "security": 15,
            "other": 5
        },
        "by_category_sw": {
            "miundombinu": 50,
            "afya": 30,
            "elimu": 25,
            "usalama": 15,
            "mengine": 5
        }
    },
    "citizens": 1250,
    "projects": 15,
    "wards": 8
}
```

---

## 📱 USSD INTEGRATION ENDPOINT

### 19. USSD Menu Handler
**Endpoint:** `POST /api/ussd/`
**Description:** Handle USSD menu interactions with bilingual support
**Authentication:** None required
**Content-Type:** `application/json`

**Expected Input:**
```json
{
    "sessionId": "ATUid_1234567890",
    "phoneNumber": "+254712345678",
    "text": "1*2*1*Road has potholes"
}
```

**Success Response (200 OK):**
```json
{
    "USSResponse": "END Thank you! Ref: SKK-2025-001\nAsante! Namba: SKK-2025-001"
}
```

**USSD Flow Examples:**

1. **Main Menu:** `text: ""` 
   ```
   CON Welcome to Skika - Karibu Skika
   1. Report Issue - Ripoti Tatizo
   2. Track Report - Fuatilia Ripoti
   3. Give Feedback - Toa Maoni
   ```

2. **Select Ward:** `text: "1"`
   ```
   CON Select Ward - Chagua Kata:
   1. Gatundu North
   2. Gatundu Central
   3. Gatundu East
   ```

3. **Select Category:** `text: "1*2"`
   ```
   CON Categories - Aina za Matatizo:
   1. Infrastructure - Miundombinu
   2. Health - Afya
   3. Education - Elimu
   4. Security - Usalama
   5. Other - Mengine
   ```

4. **Enter Description:** `text: "1*2*1*Road has potholes"`
   ```
   END Thank you! Ref: SKK-2025-001
   Asante! Namba: SKK-2025-001
   ```

---

## 🔑 AUTHENTICATION HEADERS

For protected endpoints, include the JWT token in the Authorization header:

```
Authorization: Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9...
```

## 📝 COMMON ERROR RESPONSES

### 401 Unauthorized
```json
{
    "detail": "Authentication credentials were not provided."
}
```

### 403 Forbidden
```json
{
    "detail": "You do not have permission to perform this action."
}
```

### 404 Not Found
```json
{
    "detail": "Not found."
}
```

### 400 Bad Request
```json
{
    "field_name": ["This field is required."],
    "another_field": ["Invalid choice."]
}
```

---

## 🌟 SPECIAL FEATURES

### Auto-Translation
- When you provide English values (`category_en`, `status_en`, `priority_level_en`), the corresponding Swahili fields are automatically populated
- Works in both API requests and Django admin interface

### Bilingual SMS Notifications
- Status updates automatically send SMS in both English and Swahili
- Format: "English message / Swahili message"

### USSD Multilingual Support
- All USSD menus display options in both English and Swahili
- Responses are provided in both languages

### Audit Trail
- All actions are logged with bilingual descriptions
- Tracks who made changes and when

---

**Generated on:** October 31, 2025  
**API Version:** 1.0  
**Base URL:** http://127.0.0.1:8000/api/