import click
import os
import subprocess
from dotenv import load_dotenv
import re
import shutil

load_dotenv()

def add_to_installed_apps(settings_path, app_name):
    """Add the new app to INSTALLED_APPS in settings.py."""
    try:
        with open(settings_path, 'r') as file:
            content = file.read()

        installed_apps_pattern = re.compile(r'INSTALLED_APPS\s*=\s*\[(.*?)\]', re.DOTALL)
        match = installed_apps_pattern.search(content)

        if match:
            installed_apps_content = match.group(1)
            if f"'{app_name}'" not in installed_apps_content:
                new_installed_apps_content = f"{installed_apps_content.strip()}\n    '{app_name}',\n"
                new_content = content[:match.start(1)] + new_installed_apps_content + content[match.end(1):]

                with open(settings_path, 'w') as file:
                    file.write(new_content)
                print(f"Added {app_name} to INSTALLED_APPS in settings.py")
            else:
                print(f"{app_name} is already in INSTALLED_APPS")
        else:
            print("INSTALLED_APPS not found in settings.py")
    except Exception as e:
        print(f"An error occurred while adding to INSTALLED_APPS: {e}")

def create_directories(app_name):
    """Create necessary directories for the new app."""
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
        add_to_installed_apps(settings_path, f'{app_name}')
        create_directories(app_name)

        # Copy urls.py if it exists
        existing_urls_path = os.path.join(project_root, 'app', 'urls.py')
        new_app_urls_path = os.path.join(project_root, app_name, 'urls.py')

        if os.path.exists(existing_urls_path):
            shutil.copy(existing_urls_path, new_app_urls_path)
            click.echo(f"Copied urls.py from app/ to {app_name}/")
        else:
            click.echo("urls.py not found in app/ directory. Skipping copy.")
    except subprocess.CalledProcessError as e:
        click.echo(f"An error occurred: {e}")

if __name__ == "__main__":
    command()
