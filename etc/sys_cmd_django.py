import subprocess
import os
import click

def create_app(app_name):
    try:
        venv_python = os.path.join(os.environ.get('VIRTUAL_ENV', ''), 'bin', 'python')
        if not os.path.isfile(venv_python):
            raise FileNotFoundError(f"Python executable not found in virtual environment at {venv_python}")

        subprocess.run([venv_python, "manage.py", "startapp", app_name], check=True)
        print(f"Created app: {app_name}")
    except subprocess.CalledProcessError as e:
        print(f"An error occurred: {e}")

def makemigrations():
    try:
        subprocess.run(["python", "manage.py", "makemigrations"], check=True)
        print("Migrations created successfully.")
    except subprocess.CalledProcessError as e:
        print(f"An error occurred: {e}")

def migrate():
    try:
        subprocess.run(["python", "manage.py", "migrate"], check=True)
        print("Migrations applied successfully.")
    except subprocess.CalledProcessError as e:
        print(f"An error occurred: {e}")

def createsuperuser():
    try:
        subprocess.run(["python", "manage.py", "createsuperuser"], check=True)
        print("Superuser created successfully.")
    except subprocess.CalledProcessError as e:
        print(f"An error occurred: {e}")

def collectstatic():
    try:
        subprocess.run(["python", "manage.py", "collectstatic", "--noinput"], check=True)
        print("Static files collected successfully.")
    except subprocess.CalledProcessError as e:
        print(f"An error occurred: {e}")

def runserver():
    try:
        subprocess.run(["python", "manage.py", "runserver"], check=True)
        print("Django development server is running.")
    except subprocess.CalledProcessError as e:
        print(f"An error occurred: {e}")
