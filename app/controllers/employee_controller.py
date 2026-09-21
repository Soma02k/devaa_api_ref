from flask import request
from app.services.employee_service import EmployeeService
from app.utils.response import api_response
from app.utils.validation import validate_employee_payload
from app.utils.exception_handler import ValidationError

class EmployeeController:
    """Controller handling HTTP requests, parameters validation, and delegating to services."""

    @staticmethod
    def create_employee():
        """Handle POST /employees - Create complete employee."""
        data = request.get_json(silent=True)
        if not data:
            raise ValidationError("Invalid or empty JSON body")

        required_fields = [
            'name', 'email', 'phone', 'occupation', 
            'designation', 'salary', 'city', 'marital_status', 'status'
        ]
        is_valid, error_msg = validate_employee_payload(data, required_fields=required_fields)
        if not is_valid:
            raise ValidationError(error_msg)

        employee_data = EmployeeService.create_employee(data)
        return api_response(201, True, "Employee created successfully", employee_data)

    @staticmethod
    def create_basic_employee():
        """Handle POST /employees/basic - Create minimal employee."""
        data = request.get_json(silent=True)
        if not data:
            raise ValidationError("Invalid or empty JSON body")

        required_fields = ['name', 'email', 'phone']
        is_valid, error_msg = validate_employee_payload(data, required_fields=required_fields)
        if not is_valid:
            raise ValidationError(error_msg)

        employee_data = EmployeeService.create_basic_employee(data)
        return api_response(201, True, "Employee created successfully", employee_data)

    @staticmethod
    def get_employees():
        """Handle GET /employees - Fetch paginated employees."""
        page_raw = request.args.get('page', 1)
        limit_raw = request.args.get('limit', 10)

        try:
            page = int(page_raw)
            limit = int(limit_raw)
            if page < 1 or limit < 1:
                raise ValueError()
        except (ValueError, TypeError):
            raise ValidationError("Page and limit query parameters must be positive integers")

        paginated_data = EmployeeService.get_employees_paginated(page=page, limit=limit)
        return api_response(200, True, "Employees fetched successfully", paginated_data)

    @staticmethod
    def get_employee_by_id(employee_id):
        """Handle GET /employees/<id> - Fetch single employee details."""
        try:
            emp_id = int(employee_id)
            if emp_id < 1:
                raise ValueError()
        except (ValueError, TypeError):
            raise ValidationError("Employee ID must be a positive integer")

        employee_data = EmployeeService.get_employee_by_id(emp_id)
        return api_response(200, True, "Employee details fetched successfully", employee_data)

    @staticmethod
    def update_employee(employee_id):
        """Handle PUT /employees/<id> - Update existing employee."""
        try:
            emp_id = int(employee_id)
            if emp_id < 1:
                raise ValueError()
        except (ValueError, TypeError):
            raise ValidationError("Employee ID must be a positive integer")

        data = request.get_json(silent=True)
        if data is None:
            raise ValidationError("Invalid or empty JSON body")

        is_valid, error_msg = validate_employee_payload(data, is_update=True)
        if not is_valid:
            raise ValidationError(error_msg)

        updated_employee = EmployeeService.update_employee(emp_id, data)
        return api_response(200, True, "Employee updated successfully", updated_employee)

    @staticmethod
    def delete_employee(employee_id):
        """Handle DELETE /employees/<id> - Delete employee."""
        try:
            emp_id = int(employee_id)
            if emp_id < 1:
                raise ValueError()
        except (ValueError, TypeError):
            raise ValidationError("Employee ID must be a positive integer")

        EmployeeService.delete_employee(emp_id)
        return api_response(200, True, "Employee deleted successfully", None)
