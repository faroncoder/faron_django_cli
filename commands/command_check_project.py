# commands/command_check_project.py
import click
import os
from dotenv import load_dotenv

load_dotenv()

@click.command()
def command():
    """Check for project root directory and prompt user if not set."""
    project_root = os.getenv('PROJECT_ROOT')

    if not project_root:
        project_root = click.prompt("Please enter the project root directory").strip()

        if os.path.isdir(project_root):
            with open('.env', 'a') as env_file:
                env_file.write(f"\nPROJECT_ROOT={project_root}")
            os.environ['PROJECT_ROOT'] = project_root
            click.echo(f"PROJECT_ROOT set to {project_root}")
        else:
            click.echo(f"The provided directory '{project_root}' is not valid.")
    else:
        click.echo(f"PROJECT_ROOT is already set to {project_root}")

if __name__ == "__main__":
    command()
