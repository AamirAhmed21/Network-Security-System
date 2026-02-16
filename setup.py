'''
The setup.py file is used to specify the configuration for packaging and distributing a Python project. It typically includes information such as the project name, version, author, description, and dependencies. This file is essential for creating a distributable package that can be uploaded to PyPI or installed using pip.
'''

from setuptools import setup, find_packages

from typing import List

def get_requirements() -> List[str]:
    '''
    Docstring for get_requirements
    
    :return: Description
    :rtype: List[str]
    '''
    requirement:List[str] = []
    try:
        with open('requirement.txt', 'r') as f:
            ## Read the requirements from the requirement.txt file and split them into a list
            requirement = [line.strip()for line in f if line.strip() and line.strip() != '-e .'
]
    except FileNotFoundError:
        print("requirements.txt file not found. No dependencies will be installed.")
    return requirement

setup(
    name='Network Security System',
    version='0.1',
    description='A network security system built with Python',
    author='Aamir',
    author_email='aamirahmed2132@gmail.com',
    packages=find_packages(),
    install_requires=get_requirements(),
)