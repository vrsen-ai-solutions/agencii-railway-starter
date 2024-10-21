import os
import subprocess

def run_tests_in_directory(directory):
    """
    Recursively find and run all Python files in the specified directory.
    """
    for root, _, files in os.walk(directory):
        for file in files:
            if file.endswith('.py'):
                file_path = os.path.join(root, file)
                print(f"Running {file_path}")
                subprocess.run(['python', file_path], check=True)

if __name__ == "__main__":
    tools_directory = 'tools'
    run_tests_in_directory(tools_directory)
