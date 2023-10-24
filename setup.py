import subprocess
import os

def install_depedencies():
    requirements_file = os.path.join(os.path.dirname(__file__), 'requirements.txt')
    if os.path.exists(requirements_file):
        try:
            subprocess.check_call(['pip', 'install', '-r', requirements_file])
        except subprocess.CalledProcessError:
            print("error during downloading packages")
    else:
        print("requirements.txt not found")

if __name__ == '__main__':
    install_depedencies()