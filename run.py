import os
from app import create_app, db

app = create_app()

if __name__ == '__main__':
    with app.app_context():
        # Automatically create database tables if they do not exist
        try:
            db.create_all()
            print("Database initialization check completed.")
        except Exception as e:
            print(f"Database initialization warning: {e}")

    port = int(os.getenv("PORT", 5000))
    debug_mode = os.getenv("FLASK_ENV", "development") == "development"
    print(f"Starting reference_structure_api server on port {port}...")
    app.run(host='0.0.0.0', port=port, debug=debug_mode)
