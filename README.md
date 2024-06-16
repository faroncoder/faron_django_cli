README - DjQuicksilver
DjQuicksilver
DjQuicksilver is a CLI tool that provides a convenient and organized way to manage your Django projects. It automates various tasks, such as:
- creating new apps
- updating configurations
- preloads commands dynamically
- integrate-on-the-fly all new scripts dropped into the `commands` directory

The tool uses click for command-line interfaces and follows a structured approach for managing commands out of best practice in software development with conciouss on security and maitnaaince.

Features
Dynamic Command Loading: Automatically loads commands based on file naming conventions.
Verb-Based Command Organization: Categorizes commands by verbs for intuitive usage.
Environment Variable Handling: Ensures necessary environment variables are set.
Project Management: Provides commands for creating Django apps and updating project settings.
Error Handling: Robust error handling to provide informative feedback.
Project Structure
Ensure your project follows this structure for DjQuicksilver to function correctly:

markdown

Ensure your project follows this structure for the CLI tool to function correctly:

DjQuicksilver
│
├── app/
│   └── settings.py
├── commands/
│   ├── command_check_project.py
│   ├── command_create_app.py
├── etc/
│   ├── sys_preload_cli.py
│   ├── sys_switch_project.py
│   └── sys_setup_environment.py
└── main.py


## Setup

### 1. Preload Configuration (`etc/sys_preload_cli.py`)

This script initializes the CLI tool, locates the project directory, and dynamically loads command files.

```python
# etc/sys_preload_cli.py
import os
import sys

def default_location():
    try:
        for root, dirs, files in os.walk("."):
            if "manage.py" in files:
                project_home = os.path.abspath(root)
                project_name = os.path.basename(project_home)
                print(f"Home Directory Identified: {project_home}")
                print(f"Project Name Identified: {project_name}")
                return project_home
        raise FileNotFoundError("manage.py not found in the directory tree.")
    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1)

project_home = default_location()
command_root = os.path.join(project_home, 'commands')

if not os.path.isdir(command_root):
    print(f"Error: Commands directory not found at {command_root}")
    sys.exit(1)

command_files = [f[:-3] for f in os.listdir(command_root) if f.startswith('command_') and f.endswith('.py')]

# Export these as global variables to be used in main.py
globals().update({
    'PROJECT_HOME': project_home,
    'COMMAND_ROOT': command_root,
    'COMMAND_FILES': command_files
})
