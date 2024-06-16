README - DjQuicksilver
DjQuicksilver
DjQuicksilver is a CLI tool designed to provide a convenient and organized way to manage your Django projects. It automates various tasks, such as creating new apps, updating configurations, and dynamically loading commands. The tool uses click for command-line interfaces and follows a structured approach for managing commands and configurations.

Features
Dynamic Command Loading: Automatically loads commands based on file naming conventions.
Verb-Based Command Organization: Categorizes commands by verbs for intuitive usage.
Environment Variable Handling: Ensures necessary environment variables are set.
Project Management: Provides commands for creating Django apps and updating project settings.
Error Handling: Robust error handling to provide informative feedback.
Project Structure
Ensure your project follows this structure for DjQuicksilver to function correctly:
```
DjQuicksilver/
│
├── app/
│   ├── settings.py
│   ├── sys_preload_cli.py
│   ├── sys_switch_project.py
│   └── sys_setup_environment.py
├── commands/
│   ├── command_check_project.py
│   ├── command_create_app.py
│   └── command_setup_environment.py
└── main.py
```

Scalability and Organization
There are two parts of the system that contribute to scalability and organization: `/app` for configuration scripts and `/commands` for command scripts. These two different types of files will dynamically work together in the CLI:

- Command Scripts: Files with a filename pattern of `command_[verb]_[operator].py` must be placed in the `/commands` directory.
- Configuration Scripts: Files with a filename pattern of `sys_[verb]_[instance].py` must be placed in the `/etc` directory.
- This separation ensures that all commands are easily manageable and configurations can be customized without cluttering the command scripts and will not interference with your Django projects.


1. This script initializes the CLI tool, locates the project directory, and dynamically loads command files for the menu.
- `sys_preload_cli.py`

2. This script builds a brand-new Django project on the fly and performs all of the maintenance work for you so you can start your project immediately, and configurations will be already taken care of.
- `sys_setup_environment.py`

3. Main Script (main.py)
- The main script is the heart of the whole application, while the sys_preload_cli.py provides the backbone for the application.
- This is the default script for creating new Django apps, updating settings, and loading configurations from app/sys_preload_cli.py.
- handles menu and pagination of commands for your convenience.

For the rest of the scripts in the application, there are two parts of the system as part of scalability:  `/etc` and `/commands`, and these two different types of files will dynamically work together in the CLI:
All files need to have this prefix structure filename as follows:

`command_[verb]_[operator].py`   and   `system_[verb]_[instance].py`

Example

Template of `command_[verb]_[operator].py`:

This is an example of how each command would be integrated into CLI from a file.
Example:  command_hello_app.py:
```
import click

@click.command()
@click.option('--app-name', prompt='Enter the app name', help='The command for Django to process.')
def command(app_name):
    """Create a new Django app."""
    # Your command implementation here
    print(f"Echoing your app's name: {app_name}")
```

Template of `sys_[verb]_[instance].py`

[Coming soon -- CLI will search for all of Django projects and preload them all at once into a menu]


This is an example of configuring the CLI to switch to a different project while you work on CLI without restarting.
example:  sys_switch_project.py
```
import os

def switch_project(project_path):
    if os.path.isdir(project_path):
        with open('.env', 'a') as env_file:
            env_file.write(f"\nPROJECT_ROOT={project_path}")
        os.environ['PROJECT_ROOT'] = project_path
        print(f"Switched to project: {project_path}")
    else:
        print(f"The provided directory '{project_path}' is not valid.")

```


