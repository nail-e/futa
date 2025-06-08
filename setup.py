import os 
import sys 
import subprocess
from setuptools import setup, find_packages

def ensure_sudo():
    if os.geteuid() != 0:
        print("Re-running with sudo...")
        os.execvp("sudo", ["sudo"] + sys.argv)

ensure_sudo()

setup(
    name='futa',
    version='0.1.0',
    package_dir={'': 'src'},
    packages=find_packages(where='src'),
    install_requires=[
        'ollama'
    ],
    entry_points={
        'console_scripts': [
            'futa = futa.cli:main'
        ]
    }
)

