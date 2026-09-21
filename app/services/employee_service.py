from app import db
from app.models.employee_model import Employee
from app.utils.pagination import paginate_query
from app.utils.exception_handler import (
    NotFoundException,
    DuplicateEmailException,
    ValidationError
)

class EmployeeService:
    """Service layer executing business logic and database operations for Employees."""

    @staticmethod
    def check_email_exists(email: str, exclude_id: int = None) -> bool:
        """Check if an email already exists in the database."""
        query = Employee.query.filter(Employee.email == email.strip())
        if exclude_id is not None:
            query = query.filter(Employee.id != exclude_id)
        return query.first() is not None

    @staticmethod
    def create_employee(data: dict) -> dict:
        """Create a complete employee record."""
        email = data.get('email', '').strip()
        if EmployeeService.check_email_exists(email):
            raise DuplicateEmailException("Email already exists")

        employee = Employee(
            name=data.get('name', '').strip(),
            email=email,
            phone=data.get('phone', '').strip(),
            occupation=data.get('occupation'),
            designation=data.get('designation'),
            salary=data.get('salary'),
            city=data.get('city'),
            marital_status=data.get('marital_status'),
            status=data.get('status', 'active')
        )

        db.session.add(employee)
        db.session.commit()
        return employee.to_dict()

    @staticmethod
    def create_basic_employee(data: dict) -> dict:
        """Create an employee with basic information (name, email, phone)."""
        email = data.get('email', '').strip()
        if EmployeeService.check_email_exists(email):
            raise DuplicateEmailException("Email already exists")

        employee = Employee(
            name=data.get('name', '').strip(),
            email=email,
            phone=data.get('phone', '').strip()
        )

        db.session.add(employee)
        db.session.commit()
        return employee.to_dict()

    @staticmethod
    def get_employees_paginated(page: int = 1, limit: int = 10) -> dict:
        """Retrieve paginated list of employees."""
        query = Employee.query.order_by(Employee.id.asc())
        return paginate_query(query, page=page, limit=limit)

    @staticmethod
    def get_employee_by_id(employee_id: int) -> dict:
        """Retrieve a single employee by ID."""
        employee = db.session.get(Employee, employee_id)
        if not employee:
            raise NotFoundException("Employee not found")
        return employee.to_dict()

    @staticmethod
    def update_employee(employee_id: int, data: dict) -> dict:
        """Update existing employee details (partial update)."""
        employee = db.session.get(Employee, employee_id)
        if not employee:
            raise NotFoundException("Employee not found")

        if 'email' in data and data['email'] is not None:
            email = data['email'].strip()
            if EmployeeService.check_email_exists(email, exclude_id=employee_id):
                raise DuplicateEmailException("Email already exists")
            employee.email = email

        if 'name' in data and data['name'] is not None:
            employee.name = data['name'].strip()
        if 'phone' in data and data['phone'] is not None:
            employee.phone = data['phone'].strip()
        if 'occupation' in data:
            employee.occupation = data['occupation']
        if 'designation' in data:
            employee.designation = data['designation']
        if 'salary' in data:
            employee.salary = data['salary']
        if 'city' in data:
            employee.city = data['city']
        if 'marital_status' in data:
            employee.marital_status = data['marital_status']
        if 'status' in data:
            employee.status = data['status']

        db.session.commit()
        return employee.to_dict()

    @staticmethod
    def delete_employee(employee_id: int) -> bool:
        """Delete an employee record by ID."""
        employee = db.session.get(Employee, employee_id)
        if not employee:
            raise NotFoundException("Employee not found")

        db.session.delete(employee)
        db.session.commit()
        return True
