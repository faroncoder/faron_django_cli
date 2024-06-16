import os
import click
import subprocess
from dotenv import load_dotenv

load_dotenv()

@click.group()
def cli():
    """Django CLI Tool"""
    pass

def get_project_root():
    project_root = os.getenv('PROJECT_ROOT')
    if not project_root:
        project_root = click.prompt("Enter the project root directory").strip()
        if not os.path.isdir(project_root):
            click.echo(f"The provided directory '{project_root}' is not valid.")
            return None
        with open('.env', 'a') as env_file:
            env_file.write(f"\nPROJECT_ROOT={project_root}")
        os.environ['PROJECT_ROOT'] = project_root
        click.echo(f"PROJECT_ROOT set to {project_root}")
    else:
        click.echo(f"PROJECT_ROOT is already set to {project_root}")
    return project_root

@cli.command()
@click.option('--app-name', prompt='Enter the app name', help='The app name for your Django project.')
def create_app(app_name):
    """Create a new Django app."""
    project_root = get_project_root()
    if project_root:
        try:
            subprocess.run(["python", os.path.join(project_root, "manage.py"), "startapp", app_name], check=True)
            click.echo(f"App '{app_name}' created successfully.")
        except Exception as e:
            click.echo(f"Error creating app '{app_name}': {e}")

@cli.command()
def check_project():
    """Check for project root directory and prompt user if not set."""
    get_project_root()

if __name__ == "__main__":
    cli()
