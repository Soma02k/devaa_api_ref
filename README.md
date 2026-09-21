# Reference Structure API (Phase 1)

A clean, production-ready backend reference project built with **Python**, **Flask**, **SQLAlchemy**, and **MySQL**. This project demonstrates standard REST API principles, layered architecture, standardized JSON responses, input validation, query pagination, centralized exception handling, and automated unit/integration testing.

---

## 1. Project Overview & Purpose

The purpose of `reference_structure_api` is to establish a modular, scalable, and maintainable backend foundation.

### Key Features (Phase 1):

- **Layered Architecture**: Strict separation of concerns across Routes, Controllers, Services, Models, and Utilities.
- **Standardized API Responses**: Every API returns a uniform JSON envelope (`status_code`, `is_success`, `message`, `data`).
- **Reusable Pagination**: Centralized helper for offset/limit calculations, total counts, and total pages metadata.
- **Robust Validation**: Field presence, string checks, email format regex, numeric constraints, and type safety.
- **Centralized Exception Handling**: Custom application exceptions mapped globally to standard error responses.
- **MySQL Integration**: Object-Relational Mapping (ORM) powered by SQLAlchemy with environment variable configuration.
- **Automated Testing**: Comprehensive Pytest suite for all endpoints, error conditions, and edge cases.

---

## 2. Architecture & Request Flow

The application follows a unidirectional architecture:

```text
Client Request
      │
      ▼
Routes (URL & Method Dispatch)
      │
      ▼
Controller (Data extraction, validation checks, response wrapping)
      │
      ▼
Service (Business logic, database transactions)
      │
      ▼
Model (SQLAlchemy ORM Entities)
      │
      ▼
MySQL Database (Agentic_DB)
      │
      ▼
Service -> Controller -> api_response() -> Client Response
```

### Component Responsibilities:

- **Routes (`app/routes/`)**: Pure routing definitions connecting endpoints to controllers.
- **Controllers (`app/controllers/`)**: Parse HTTP body/query params, execute input validation, invoke services, and wrap results with `api_response()`.
- **Services (`app/services/`)**: Contain core business rules, database queries, and data mutations.
- **Models (`app/models/`)**: Define database table structures, constraints, and serialization helpers (`to_dict()`).
- **Utils (`app/utils/`)**: Reusable helper functions (`response.py`, `pagination.py`, `validation.py`, `exception_handler.py`).

---

## 3. Directory Structure

```text
reference_structure_api/
│
├── app/
│   ├── __init__.py               # Flask application factory
│   ├── config.py                 # Configuration loader from .env
│   │
│   ├── routes/
│   │   └── employee_routes.py    # Route mappings for /employees endpoints
│   │
│   ├── controllers/
│   │   └── employee_controller.py # Request handlers & validation callers
│   │
│   ├── services/
│   │   └── employee_service.py   # Business logic & MySQL DB transactions
│   │
│   ├── models/
│   │   └── employee_model.py     # SQLAlchemy model for employee_details
│   │
│   └── utils/
│       ├── response.py           # Standard api_response() envelope
│       ├── pagination.py         # Global query pagination helper
│       ├── validation.py         # Payload & parameter validator
│       └── exception_handler.py  # Global error handling middleware
│
├── tests/
│   └── test_employees.py         # Pytest automated test suite
│
├── requirements.txt              # Project dependencies
├── .env                          # Local environment settings
├── .env.example                  # Environment template
├── run.py                        # Application entry point
├── schema.sql                    # Database table SQL creation script
└── README.md                     # Project documentation
```

---

## 4. Environment Configuration & Database Setup

### Environment Variables (`.env`)

Database credentials are completely decoupled from Python code and loaded from `.env`:

```env
DB_HOST=localhost
DB_PORT=3306
DB_USER=root
DB_PASSWORD=
DB_NAME=Agentic_DB
FLASK_ENV=development
PORT=5000
```

### Database Schema (`schema.sql`)

Run the following script in MySQL Workbench or Command Line to initialize `Agentic_DB`:

```sql
CREATE DATABASE IF NOT EXISTS `Agentic_DB`;
USE `Agentic_DB`;

CREATE TABLE IF NOT EXISTS `employee_details` (
    `id` INT AUTO_INCREMENT PRIMARY KEY,
    `name` VARCHAR(100) NOT NULL,
    `email` VARCHAR(150) NOT NULL UNIQUE,
    `phone` VARCHAR(20) NOT NULL,
    `occupation` VARCHAR(100) DEFAULT NULL,
    `designation` VARCHAR(100) DEFAULT NULL,
    `salary` DECIMAL(12, 2) DEFAULT NULL,
    `city` VARCHAR(100) DEFAULT NULL,
    `marital_status` VARCHAR(30) DEFAULT NULL,
    `status` VARCHAR(20) DEFAULT 'active',
    `created_at` DATETIME DEFAULT CURRENT_TIMESTAMP,
    `updated_at` DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
```

---

## 5. Installation & Execution

### 1. Install Dependencies

```bash
pip install -r requirements.txt
```

### 2. Run Database Migration / Tables Initialization

Ensure MySQL service is running on `localhost:3306`. The application will automatically verify and create missing tables on startup.

### 3. Run Application

```bash
python run.py
```

The server will start at `http://localhost:5000`.

---

## 6. API Reference (Phase 1)

| Method   | Endpoint                     | Description                                         | Success Code  |
| :------- | :--------------------------- | :-------------------------------------------------- | :------------ |
| `POST`   | `/employees`                 | Create full employee record                         | `201 Created` |
| `POST`   | `/employees/basic`           | Create minimal employee record (name, email, phone) | `201 Created` |
| `GET`    | `/employees?page=1&limit=10` | Get paginated employee list                         | `200 OK`      |
| `GET`    | `/employees/<id>`            | Get single employee details by ID                   | `200 OK`      |
| `PUT`    | `/employees/<id>`            | Partial or full employee update                     | `200 OK`      |
| `DELETE` | `/employees/<id>`            | Delete employee record by ID                        | `200 OK`      |

---

## 7. Requests & Response Examples

### Global Response Format

**Success Response Envelope (`200 OK` / `201 Created`)**:

```json
{
  "status_code": 200,
  "is_success": true,
  "message": "Employees fetched successfully",
  "data": { ... }
}
```

**Error Response Envelope (`400 Bad Request` / `404 Not Found` / `500 Error`)**:

```json
{
  "status_code": 400,
  "is_success": false,
  "message": "Email already exists",
  "data": null
}
```

---

### Endpoints Detail

#### 1. POST `/employees`

**Request Body**:

```json
{
  "name": "John Doe",
  "email": "john@example.com",
  "phone": "9876543210",
  "occupation": "Software Developer",
  "designation": "Senior Developer",
  "salary": 75000,
  "city": "Kolkata",
  "marital_status": "single",
  "status": "active"
}
```

**Response (`201 Created`)**:

```json
{
  "status_code": 201,
  "is_success": true,
  "message": "Employee created successfully",
  "data": {
    "id": 1,
    "name": "John Doe",
    "email": "john@example.com",
    "phone": "9876543210",
    "occupation": "Software Developer",
    "designation": "Senior Developer",
    "salary": 75000.0,
    "city": "Kolkata",
    "marital_status": "single",
    "status": "active",
    "created_at": "2026-09-21T12:00:00",
    "updated_at": "2026-09-21T12:00:00"
  }
}
```

#### 2. POST `/employees/basic`

**Request Body**:

```json
{
  "name": "Jane Doe",
  "email": "jane@example.com",
  "phone": "9876543211"
}
```

**Response (`201 Created`)**:

```json
{
  "status_code": 201,
  "is_success": true,
  "message": "Employee created successfully",
  "data": {
    "id": 2,
    "name": "Jane Doe",
    "email": "jane@example.com",
    "phone": "9876543211",
    "occupation": null,
    "designation": null,
    "salary": null,
    "city": null,
    "marital_status": null,
    "status": "active",
    "created_at": "2026-09-21T12:05:00",
    "updated_at": "2026-09-21T12:05:00"
  }
}
```

#### 3. GET `/employees?page=1&limit=10`

**Response (`200 OK`)**:

```json
{
  "status_code": 200,
  "is_success": true,
  "message": "Employees fetched successfully",
  "data": {
    "items": [
      {
        "id": 1,
        "name": "John Doe",
        "email": "john@example.com",
        "phone": "9876543210",
        "occupation": "Software Developer",
        "designation": "Senior Developer",
        "salary": 75000.0,
        "city": "Kolkata",
        "marital_status": "single",
        "status": "active",
        "created_at": "2026-09-21T12:00:00",
        "updated_at": "2026-09-21T12:00:00"
      }
    ],
    "pagination": {
      "page": 1,
      "limit": 10,
      "total": 1,
      "total_pages": 1
    }
  }
}
```

#### 4. GET `/employees/<id>`

**Response (`200 OK`)**:

```json
{
  "status_code": 200,
  "is_success": true,
  "message": "Employee details fetched successfully",
  "data": {
    "id": 1,
    "name": "John Doe",
    "email": "john@example.com",
    "phone": "9876543210",
    "occupation": "Software Developer",
    "designation": "Senior Developer",
    "salary": 75000.0,
    "city": "Kolkata",
    "marital_status": "single",
    "status": "active",
    "created_at": "2026-09-21T12:00:00",
    "updated_at": "2026-09-21T12:00:00"
  }
}
```

#### 5. PUT `/employees/<id>`

**Request Body**:

```json
{
  "name": "John Updated",
  "designation": "Lead Developer",
  "salary": 90000,
  "city": "Bangalore"
}
```

**Response (`200 OK`)**:

```json
{
  "status_code": 200,
  "is_success": true,
  "message": "Employee updated successfully",
  "data": {
    "id": 1,
    "name": "John Updated",
    "email": "john@example.com",
    "phone": "9876543210",
    "occupation": "Software Developer",
    "designation": "Lead Developer",
    "salary": 90000.0,
    "city": "Bangalore",
    "marital_status": "single",
    "status": "active",
    "created_at": "2026-09-21T12:00:00",
    "updated_at": "2026-09-21T12:10:00"
  }
}
```

#### 6. DELETE `/employees/<id>`

**Response (`200 OK`)**:

```json
{
  "status_code": 200,
  "is_success": true,
  "message": "Employee deleted successfully",
  "data": null
}
```

---

## 8. Workflows

### Endpoint Workflow Illustrations

#### GET `/employees` Workflow

```text
GET /employees?page=1&limit=10
      ↓
employee_routes.py
      ↓
employee_controller.py (Extract query params, validate integers)
      ↓
employee_service.py (Call get_employees_paginated)
      ↓
pagination.py (paginate_query: query offset/limit/count)
      ↓
employee_model.py (to_dict serialization)
      ↓
employee_controller.py
      ↓
api_response()
      ↓
Client (200 OK with items & pagination metadata)
```

#### GET `/employees/<id>` Workflow

```text
GET /employees/10
      ↓
employee_routes.py
      ↓
employee_controller.py (Validate employee_id integer)
      ↓
employee_service.py (Query Employee by ID)
      ↓
[If Not Found] -> NotFoundException (404) -> Centralized Exception Handler
[If Found]     -> employee_model.py (to_dict) -> api_response(200) -> Client
```

#### PUT `/employees/<id>` Workflow

```text
PUT /employees/10
      ↓
employee_routes.py
      ↓
employee_controller.py (Validate JSON body & payload format)
      ↓
employee_service.py (Find ID, check unique email if changed, update fields)
      ↓
MySQL Commit
      ↓
employee_controller.py
      ↓
api_response(200)
      ↓
Client
```

#### DELETE `/employees/<id>` Workflow

```text
DELETE /employees/10
      ↓
employee_routes.py
      ↓
employee_controller.py
      ↓
employee_service.py (Find ID, db.session.delete)
      ↓
MySQL Commit
      ↓
api_response(200, True, "Employee deleted successfully", None)
      ↓
Client
```

---

## 9. Global Utilities & Exception Handling

- **Response Utility (`app/utils/response.py`)**: `api_response(status_code, is_success, message, data=None)` guarantees uniform payload delivery.
- **Pagination Utility (`app/utils/pagination.py`)**: `paginate_query(query, page, limit)` handles page limit boundary checks, offset generation, total count queries, and page calculation.
- **Validation Utility (`app/utils/validation.py`)**: `validate_employee_payload(data, required_fields, is_update)` provides clean field validation, empty string checks, email regex matching, and salary numeric checking.
- **Exception Handler (`app/utils/exception_handler.py`)**: Catches `AppException`, `ValidationError`, `NotFoundException`, `DuplicateEmailException`, `SQLAlchemyError`, and `HTTPException`, transforming errors into standard `api_response()` envelopes.

---

## 10. Running Automated Tests

The project includes unit & integration tests built with **Pytest**.

### Run Test Suite

```bash
pytest tests/test_employees.py -v
```

All 23 test cases cover:

- Successful creations (POST full & basic)
- Required field validation & invalid email checks
- Duplicate email prevention
- Invalid salary checks
- Pagination boundary conditions & parameter validation
- Single record retrieval (existing vs non-existing vs invalid ID)
- Partial updates (PUT) & email duplicate conflict checks on update
- Deletions (DELETE) & verification
- Strict standard API response structure validation
