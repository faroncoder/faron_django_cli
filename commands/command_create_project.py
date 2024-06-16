# commands/command_create_project.py
import click
import os
import subprocess
from dotenv import load_dotenv
import re

load_dotenv()

def create_secret_key():
    return os.urandom(24).hex()

def create_env_file(project_name, db_password):
    secret_key = create_secret_key()
    env_content = f"""
DJANGO_SECRET_KEY={secret_key}
DB_NAME={project_name}
DB_USER={project_name}
DB_PASSWORD={db_password}
DB_HOST=localhost
DB_PORT=3306
EMAIL_HOST='xxx.xxxx.ca'
EMAIL_PORT='587'
EMAIL_USE_TLS='True'
EMAIL_HOST_USER='xxx@xxxx.ca'
EMAIL_HOST_PASSWORD='xxxxx'
DJANGO_SETTINGS_MODULE='{project_name}.settings'
"""
    env_file = os.path.join(os.getcwd(), '.env')
    with open(env_file, 'w') as f:
        f.write(env_content)
    print(".env file created and updated with project details.")

default_configuration = """
AUTH_USER_MODEL = 'accounts.CustomUser'

# Where to go after a successful login:
LOGIN_REDIRECT_URL = '/accounts/dashboard/'  # Adjust this to the name of your home page URL

# Where to redirect users when login is required and they are not logged in:
LOGIN_URL = '/accounts/login/'

LOGOUT_REDIRECT_URL = '/'  # Assuming you have a URL named 'home'

LOGOUT_URL = '/accounts/logout/'

EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'

AUTHENTICATION_BACKENDS = ['django.contrib.auth.backends.ModelBackend']

AUTH_USER_MODEL = 'accounts.CustomUser'

REST_FRAMEWORK = {
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.IsAuthenticated',
    ],
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'rest_framework.authentication.SessionAuthentication',
        'rest_framework.authentication.TokenAuthentication',
    ],
}

STATIC_ROOT = [ BASE_DIR / 'staticfiles' ]  # For production use

STATICFILES_DIRS = [ BASE_DIR / 'static']  # Your custom static files directory during development

STATIC_URL = '/static/'

SESSION_IDLE_TIMEOUT = 900  # 15 minutes in seconds

ALLOWED_HOSTS = ['127.0.0.1', '192.168.0.0/24', '142.127.77.144', '198.50.119.128/26', '198.50.119.192/26']
"""

default_requirements = """
asgiref==3.8.1
black==24.4.0
bootstrap4==0.1.0
certifi==2024.2.2
charset-normalizer==3.3.2
click==8.1.7
Django==5.0.4
django-admin==2.0.2
django-auth==0.1.9
django-dotenv==1.4.2
django-email==0.1.10
django-excel-response==2.0.5
django-excel-response2==3.0.6
django-rest-framework==0.1.0
django-session-csrf==0.7.1
django-session-security==2.6.7
django-six==1.0.5
django-wsgi==1.0b1
djangorestframework==3.15.1
et-xmlfile==1.1.0
excel-base==1.0.4
Faker==24.9.0
idna==3.7
iniconfig==2.0.0
isoweek==1.3.3
jdcal==1.4.1
logger==1.4
mypy-extensions==1.0.0
mysql-connector-python==8.4.0
mysqlclient==2.2.4
openpyxl==2.4.11
packaging==24.0
path==16.14.0
pathlib==1.0.1
pathspec==0.12.1
platformdirs==4.2.0
pluggy==1.4.0
pytest==8.1.1
python-dateutil==2.9.0.post0
requests==2.31.0
screen==1.0.1
six==1.10.0
sqlparse==0.4.4
TimeConvert==3.0.13
tzlocal==5.2
urllib3==2.2.1
WebOb==1.8.7
xlwt==1.3.0
"""

default_management = """
#!/usr/bin/env python
## Django's command-line utility for administrative tasks.
import os
import sys

def main():
    ## Run administrative tasks. ##
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "app.settings")
    try:
        from django.core.management import execute_from_command_line
    except ImportError as exc:
        raise ImportError(
            "Couldn't import Django. Are you sure it's installed and "
            "available on your PYTHONPATH environment variable? Did you "
            "forget to activate a virtual environment?"
        ) from exc
    execute_from_command_line(sys.argv)

if __name__ == "__main__":
    main()
"""

def update_manage_py():
    try:
        manager_file = os.path.join(os.getcwd(), 'manage.py')
        with open(manager_file, 'w') as f:
            f.write(default_management)
        print("manage.py updated.")
    except Exception as e:
        print(f"An error occurred while updating manage.py: {e}")

def install_requirements():
    try:
        result = subprocess.run(
            ["pip3", "install", "-r", "requirements.txt"],
            check=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True
        )
        print(result.stdout)
    except subprocess.CalledProcessError as e:
        print(f"An error occurred while installing requirements: {e.stderr}")

def create_requirements_file():
    try:
        requirements_file = os.path.join(os.getcwd(), 'requirements.txt')
        with open(requirements_file, 'w') as f:
            f.write(default_requirements)
        print("requirements.txt created.")
        install_requirements()
    except Exception as e:
        print(f"An error occurred while creating requirements.txt: {e}")

def update_settings():
    try:
        settings_file = os.path.join(os.getcwd(), 'app', 'settings.py')
        with open(settings_file, 'w') as f:
            f.write(default_configuration)
        print("settings.py updated.")
    except Exception as e:
        print(f"An error occurred while updating settings.py: {e}")

def create_virtualenv():
    try:
        subprocess.run(["python3", "-m", "venv", ".venv"], check=True)
        print("Virtual environment created.")
    except subprocess.CalledProcessError as e:
        print(f"An error occurred while creating virtual environment: {e}")

def install_dependencies():
    try:
        subprocess.run([os.path.join(".venv", "bin", "python"), "-m", "pip", "install", "click", "django", "mysqlclient", "python-dotenv"], check=True)
        print("Dependencies installed.")
    except subprocess.CalledProcessError as e:
        print(f"An error occurred while installing dependencies: {e}")

@click.command()
def command_create_project():
    project_name = click.prompt("Enter the Django project name").strip()
    db_password = click.prompt("Enter the database password").strip()

    if not project_name:
        print("Error: You must provide a project name.")
        return

    subprocess.run(["django-admin", "startproject", project_name], check=True)

    os.chdir(project_name)
    subprocess.run(["mv", project_name, "app"], check=True)

    create_virtualenv()
    install_dependencies()
    create_requirements_file()
    update_manage_py()
    update_settings()
    create_env_file(project_name, db_password)

    settings_path = os.path.join(os.getcwd(), 'app', 'settings.py')

    subprocess.run(f"sed -i '/ALLOWED_HOSTS/d' {settings_path}", shell=True, check=True)
    subprocess.run(f"sed -i '/STATIC_URL/d' {settings_path}", shell=True, check=True)

    print("Project setup completed.")

if __name__ == "__main__":
    command_create_project()
