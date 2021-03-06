#### This Setup file is required to install dependencies exists in requirements.txt

from setuptools import setup,find_packages
from typing import List

#### Declaring Variable for setup functions

PROJECT_NAME = "housing-predictor"
PROJECT_VERSION = "0.0.2"
PROJECT_AUTHOR = "Vaibhav Yaramwar"
PROJECT_DESCRIPTION = "First Machine Learning Project with Pipeline"
PROJECT_PACKAGE = find_packages()
REQUIREMENTS_FILE_NAME = "requirements.txt"

def get_requirements_list() -> List[str]:
    """
        This function is going to return requirements listed in requirements.txt file
        
        return  : This function is going to return list of name of the requirementes mentioned in requirements.txt
    """
    with open(REQUIREMENTS_FILE_NAME) as requirement_file:
        return requirement_file.readlines().remove("-e .")

setup(name=PROJECT_NAME,version=PROJECT_VERSION,author=PROJECT_AUTHOR,description=PROJECT_DESCRIPTION,packages=PROJECT_PACKAGE,
install_requires=get_requirements_list())






