import subprocess

def initialize_git():
    try:
        subprocess.run(["git", "init"], check=True)
        print("Initialized Git repository")
    except subprocess.CalledProcessError as e:
        print(f"An error occurred: {e}")
