import os
import subprocess

def run_server():
    venv_path = os.path.join(os.environ.get('VIRTUAL_ENV', ''), 'bin', 'python')
    manage_py_path = os.path.join(os.getcwd(), 'manage.py')

    if not os.path.isfile(venv_path):
        print(f"Python executable not found in virtual environment at {venv_path}")
        return

    if not os.path.isfile(manage_py_path):
        print(f"manage.py not found in the current directory at {manage_py_path}")
        return

    try:
        subprocess.run([venv_path, manage_py_path, "runserver"], check=True)
        print("Running the Django development server")
    except subprocess.CalledProcessError as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    run_server()
