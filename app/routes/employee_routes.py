from flask import Blueprint
from app.controllers.employee_controller import EmployeeController

employee_bp = Blueprint('employee_bp', __name__)

# API 1 — Create Employee
@employee_bp.route('/employees', methods=['POST'])
def create_employee():
    return EmployeeController.create_employee()

# API 2 — Create Employee with Minimal Required Information
@employee_bp.route('/employees/basic', methods=['POST'])
def create_basic_employee():
    return EmployeeController.create_basic_employee()

# API 3 — Get Employees with Pagination
@employee_bp.route('/employees', methods=['GET'])
def get_employees():
    return EmployeeController.get_employees()

# API 4 — Get Employee by ID
@employee_bp.route('/employees/<employee_id>', methods=['GET'])
def get_employee_by_id(employee_id):
    return EmployeeController.get_employee_by_id(employee_id)

# API 5 — Update Employee
@employee_bp.route('/employees/<employee_id>', methods=['PUT'])
def update_employee(employee_id):
    return EmployeeController.update_employee(employee_id)

# API 6 — Delete Employee
@employee_bp.route('/employees/<employee_id>', methods=['DELETE'])
def delete_employee(employee_id):
    return EmployeeController.delete_employee(employee_id)
