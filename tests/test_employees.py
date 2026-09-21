import pytest
from app import create_app, db
from app.config import Config
from app.models.employee_model import Employee

class TestConfig(Config):
    TESTING = True
    SQLALCHEMY_DATABASE_URI = "sqlite:///:memory:"
    SQLALCHEMY_TRACK_MODIFICATIONS = False

@pytest.fixture
def client():
    """Flask test client fixture with isolated in-memory database."""
    app = create_app(TestConfig)
    with app.test_client() as client:
        with app.app_context():
            db.create_all()
            yield client
            db.session.remove()
            db.drop_all()

def assert_standard_response(data, expected_status_code, expected_success):
    """Helper to verify standard api_response structure."""
    assert "status_code" in data
    assert "is_success" in data
    assert "message" in data
    assert "data" in data
    assert data["status_code"] == expected_status_code
    assert data["is_success"] == expected_success
    assert isinstance(data["message"], str)

# ==========================================
# API 1: POST /employees
# ==========================================
def test_create_employee_success(client):
    payload = {
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
    response = client.post('/employees', json=payload)
    data = response.get_json()
    assert response.status_code == 201
    assert_standard_response(data, 201, True)
    assert data["data"]["name"] == "John Doe"
    assert data["data"]["email"] == "john@example.com"
    assert data["data"]["id"] is not None

def test_create_employee_missing_required_field(client):
    payload = {
        "name": "John Doe",
        "email": "john_missing@example.com",
        # missing phone
        "occupation": "Developer",
        "designation": "Dev",
        "salary": 50000,
        "city": "Kolkata",
        "marital_status": "single",
        "status": "active"
    }
    response = client.post('/employees', json=payload)
    data = response.get_json()
    assert response.status_code == 400
    assert_standard_response(data, 400, False)

def test_create_employee_invalid_email(client):
    payload = {
        "name": "John Doe",
        "email": "invalid-email-format",
        "phone": "9876543210",
        "occupation": "Developer",
        "designation": "Dev",
        "salary": 50000,
        "city": "Kolkata",
        "marital_status": "single",
        "status": "active"
    }
    response = client.post('/employees', json=payload)
    data = response.get_json()
    assert response.status_code == 400
    assert_standard_response(data, 400, False)
    assert "Invalid email format" in data["message"]

def test_create_employee_duplicate_email(client):
    payload = {
        "name": "John Doe",
        "email": "john_dup@example.com",
        "phone": "9876543210",
        "occupation": "Developer",
        "designation": "Dev",
        "salary": 50000,
        "city": "Kolkata",
        "marital_status": "single",
        "status": "active"
    }
    client.post('/employees', json=payload)
    response = client.post('/employees', json=payload)
    data = response.get_json()
    assert response.status_code == 400
    assert_standard_response(data, 400, False)
    assert "Email already exists" in data["message"]

def test_create_employee_invalid_salary(client):
    payload = {
        "name": "John Doe",
        "email": "john_sal@example.com",
        "phone": "9876543210",
        "occupation": "Developer",
        "designation": "Dev",
        "salary": "not-a-number",
        "city": "Kolkata",
        "marital_status": "single",
        "status": "active"
    }
    response = client.post('/employees', json=payload)
    data = response.get_json()
    assert response.status_code == 400
    assert_standard_response(data, 400, False)

# ==========================================
# API 2: POST /employees/basic
# ==========================================
def test_create_basic_employee_success(client):
    payload = {
        "name": "Jane Doe",
        "email": "jane@example.com",
        "phone": "9876543211"
    }
    response = client.post('/employees/basic', json=payload)
    data = response.get_json()
    assert response.status_code == 201
    assert_standard_response(data, 201, True)
    assert data["data"]["name"] == "Jane Doe"
    assert data["data"]["occupation"] is None

def test_create_basic_employee_missing_name(client):
    payload = {
        "email": "jane_noname@example.com",
        "phone": "9876543211"
    }
    response = client.post('/employees/basic', json=payload)
    data = response.get_json()
    assert response.status_code == 400
    assert_standard_response(data, 400, False)

def test_create_basic_employee_missing_email(client):
    payload = {
        "name": "Jane Doe",
        "phone": "9876543211"
    }
    response = client.post('/employees/basic', json=payload)
    data = response.get_json()
    assert response.status_code == 400
    assert_standard_response(data, 400, False)

def test_create_basic_employee_duplicate_email(client):
    payload = {
        "name": "Jane Doe",
        "email": "jane_dup@example.com",
        "phone": "9876543211"
    }
    client.post('/employees/basic', json=payload)
    response = client.post('/employees/basic', json=payload)
    data = response.get_json()
    assert response.status_code == 400
    assert_standard_response(data, 400, False)
    assert "Email already exists" in data["message"]

# ==========================================
# API 3: GET /employees (Pagination)
# ==========================================
def test_get_employees_pagination_success(client):
    # Seed 15 employees
    for i in range(1, 16):
        client.post('/employees/basic', json={
            "name": f"Employee {i}",
            "email": f"emp{i}@example.com",
            "phone": f"90000000{i:02d}"
        })

    response = client.get('/employees?page=1&limit=10')
    data = response.get_json()
    assert response.status_code == 200
    assert_standard_response(data, 200, True)
    assert len(data["data"]["items"]) == 10
    assert data["data"]["pagination"]["page"] == 1
    assert data["data"]["pagination"]["limit"] == 10
    assert data["data"]["pagination"]["total"] == 15
    assert data["data"]["pagination"]["total_pages"] == 2

def test_get_employees_different_page_values(client):
    for i in range(1, 16):
        client.post('/employees/basic', json={
            "name": f"Employee {i}",
            "email": f"emp_pg{i}@example.com",
            "phone": f"90000000{i:02d}"
        })

    response = client.get('/employees?page=2&limit=10')
    data = response.get_json()
    assert response.status_code == 200
    assert len(data["data"]["items"]) == 5
    assert data["data"]["pagination"]["page"] == 2

def test_get_employees_different_limit_values(client):
    for i in range(1, 16):
        client.post('/employees/basic', json={
            "name": f"Employee {i}",
            "email": f"emp_lim{i}@example.com",
            "phone": f"90000000{i:02d}"
        })

    response = client.get('/employees?page=1&limit=5')
    data = response.get_json()
    assert response.status_code == 200
    assert len(data["data"]["items"]) == 5
    assert data["data"]["pagination"]["total_pages"] == 3

def test_get_employees_invalid_page(client):
    response = client.get('/employees?page=0&limit=10')
    data = response.get_json()
    assert response.status_code == 400
    assert_standard_response(data, 400, False)

def test_get_employees_invalid_limit(client):
    response = client.get('/employees?page=1&limit=abc')
    data = response.get_json()
    assert response.status_code == 400
    assert_standard_response(data, 400, False)

# ==========================================
# API 4: GET /employees/<id>
# ==========================================
def test_get_employee_by_id_existing(client):
    res_create = client.post('/employees/basic', json={
        "name": "Alice",
        "email": "alice@example.com",
        "phone": "9999999999"
    })
    emp_id = res_create.get_json()["data"]["id"]

    response = client.get(f'/employees/{emp_id}')
    data = response.get_json()
    assert response.status_code == 200
    assert_standard_response(data, 200, True)
    assert data["data"]["name"] == "Alice"

def test_get_employee_by_id_non_existing(client):
    response = client.get('/employees/9999')
    data = response.get_json()
    assert response.status_code == 404
    assert_standard_response(data, 404, False)

def test_get_employee_by_id_invalid_id(client):
    response = client.get('/employees/invalid_id')
    data = response.get_json()
    assert response.status_code == 400
    assert_standard_response(data, 400, False)

# ==========================================
# API 5: PUT /employees/<id>
# ==========================================
def test_update_employee_success(client):
    res_create = client.post('/employees/basic', json={
        "name": "John Original",
        "email": "john_orig@example.com",
        "phone": "1234567890"
    })
    emp_id = res_create.get_json()["data"]["id"]

    update_payload = {
        "name": "John Updated",
        "designation": "Lead Developer",
        "salary": 90000,
        "city": "Bangalore"
    }
    response = client.put(f'/employees/{emp_id}', json=update_payload)
    data = response.get_json()
    assert response.status_code == 200
    assert_standard_response(data, 200, True)
    assert data["data"]["name"] == "John Updated"
    assert data["data"]["designation"] == "Lead Developer"
    assert data["data"]["salary"] == 90000
    assert data["data"]["email"] == "john_orig@example.com"  # Unspecified field kept

def test_update_employee_non_existing(client):
    response = client.put('/employees/9999', json={"name": "Nobody"})
    data = response.get_json()
    assert response.status_code == 404
    assert_standard_response(data, 404, False)

def test_update_employee_invalid_email(client):
    res_create = client.post('/employees/basic', json={
        "name": "Bob",
        "email": "bob@example.com",
        "phone": "1234567890"
    })
    emp_id = res_create.get_json()["data"]["id"]

    response = client.put(f'/employees/{emp_id}', json={"email": "bad-email"})
    data = response.get_json()
    assert response.status_code == 400
    assert_standard_response(data, 400, False)

def test_update_employee_invalid_salary(client):
    res_create = client.post('/employees/basic', json={
        "name": "Charlie",
        "email": "charlie@example.com",
        "phone": "1234567890"
    })
    emp_id = res_create.get_json()["data"]["id"]

    response = client.put(f'/employees/{emp_id}', json={"salary": "invalid_num"})
    data = response.get_json()
    assert response.status_code == 400
    assert_standard_response(data, 400, False)

# ==========================================
# API 6: DELETE /employees/<id>
# ==========================================
def test_delete_employee_success(client):
    res_create = client.post('/employees/basic', json={
        "name": "ToDelete",
        "email": "todelete@example.com",
        "phone": "1234567890"
    })
    emp_id = res_create.get_json()["data"]["id"]

    response = client.delete(f'/employees/{emp_id}')
    data = response.get_json()
    assert response.status_code == 200
    assert_standard_response(data, 200, True)

    # Verify deleted
    res_get = client.get(f'/employees/{emp_id}')
    assert res_get.status_code == 404

def test_delete_employee_non_existing(client):
    response = client.delete('/employees/9999')
    data = response.get_json()
    assert response.status_code == 404
    assert_standard_response(data, 404, False)

def test_delete_employee_invalid_id(client):
    response = client.delete('/employees/invalid')
    data = response.get_json()
    assert response.status_code == 400
    assert_standard_response(data, 400, False)
