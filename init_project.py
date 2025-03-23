import os
import shutil

def create_directory_structure():
    # Define the directory structure
    directories = [
        "app/api/v1",
        "app/core",
        "app/db",
        "app/models",
        "app/schemas",
        "app/utils",
        "app/services",
        "app/templates",
        "alembic/versions",
        "tests",
        "uploads",
        "logs"
    ]
    
    # Create directories
    for directory in directories:
        os.makedirs(directory, exist_ok=True)
        # Create __init__.py in each Python package directory
        if directory.startswith("app/"):
            init_file = os.path.join(directory, "__init__.py")
            if not os.path.exists(init_file):
                open(init_file, "a").close()

def create_initial_files():
    # Create empty files for key modules
    files = [
        "app/api/v1/auth.py",
        "app/api/v1/products.py",
        "app/api/v1/categories.py",
        "app/api/v1/orders.py",
        "app/api/v1/users.py",
        "app/core/config.py",
        "app/core/security.py",
        "app/db/base.py",
        "app/models/user.py",
        "app/models/product.py",
        "app/models/category.py",
        "app/models/order.py",
        "app/schemas/user.py",
        "app/schemas/product.py",
        "app/schemas/category.py",
        "app/schemas/order.py",
        "app/utils/email.py",
        "app/utils/validators.py",
        "app/services/auth.py",
        "app/services/product.py",
        "app/services/order.py",
        "tests/conftest.py",
        "tests/test_auth.py",
        "tests/test_products.py",
        "tests/test_orders.py"
    ]
    
    for file in files:
        if not os.path.exists(file):
            open(file, "a").close()

def main():
    print("Creating project structure...")
    create_directory_structure()
    print("Creating initial files...")
    create_initial_files()
    print("Project structure initialized successfully!")

if __name__ == "__main__":
    main() 