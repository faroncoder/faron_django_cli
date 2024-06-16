import click
import os
import subprocess
from dotenv import load_dotenv

load_dotenv()

def add_app_to_installed_apps(settings_path, app_name):
    try:
        with open(settings_path, "r") as file:
            lines = file.readlines()

        with open(settings_path, "w") as file:
            found_installed_apps = False
            for line in lines:
                file.write(line)
                if "INSTALLED_APPS = [" in line:
                    found_installed_apps = True
                if found_installed_apps and "]" in line:
                    file.write(f"    '{app_name}',\n")
                    found_installed_apps = False
        print(f"Added {app_name} to INSTALLED_APPS in settings.py")
    except Exception as e:
        print(f"An error occurred: {e}")

def create_directories(app_name):
    try:
        os.makedirs(f"{app_name}/templates", exist_ok=True)
        os.makedirs(f"{app_name}/static", exist_ok=True)
        print(f"Created directories: {app_name}/templates and {app_name}/static")
    except Exception as e:
        print(f"An error occurred: {e}")

@click.command()
@click.option('--app-name', prompt='Enter the app name', help='The name of the Django app to create.')
def command(app_name):
    project_root = os.getenv('PROJECT_ROOT')

    if not project_root:
        project_root = click.prompt("Please enter the project root directory").strip()
        if not os.path.isdir(project_root):
            click.echo(f"The provided directory '{project_root}' is not valid.")
            return

        with open('.env', 'a') as env_file:
            env_file.write(f"\nPROJECT_ROOT={project_root}")
        os.environ['PROJECT_ROOT'] = project_root
        click.echo(f"PROJECT_ROOT set to {project_root}")
    else:
        click.echo(f"PROJECT_ROOT is already set to {project_root}")

    venv_python = os.path.join(os.environ.get('VIRTUAL_ENV', ''), 'bin', 'python')
    if not os.path.isfile(venv_python):
        raise FileNotFoundError(f"Python executable not found in virtual environment at {venv_python}")

    try:
        subprocess.run([venv_python, "manage.py", "startapp", app_name], check=True)
        click.echo(f"Created app: {app_name}")

        settings_path = os.path.join(project_root, 'settings.py')
        add_app_to_installed_apps(settings_path, app_name)
        create_directories(app_name)
    except subprocess.CalledProcessError as e:
        click.echo(f"An error occurred: {e}")

if __name__ == "__main__":
    command()

