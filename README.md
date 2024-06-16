# faron_django_cli
Quicksilver Django CLI


Quicksilver Django Command Line Interface
-----------------------------------------
This CLI tool provides a convenient and organized way to manage Django projects. It automates various tasks, such as:

- creating new apps
- updating configurations
- loading commands dynamically
- preset the CLI with pre-configuration to your own preferences

The tool uses click for command-line interfaces and follows a structured approach for managing commands.

Features
Dynamic Command Loading: Automatically loads commands based on file naming conventions.
Verb-Based Command Organization: Categorizes commands by verbs for intuitive usage.
Environment Variable Handling: Ensures necessary environment variables are set.
Project Management: Provides commands for creating Django apps and updating project settings.
Error Handling: Robust error handling to provide informative feedback.

Project Structure
Ensure your project follows this structure for the CLI tool to function correctly:
