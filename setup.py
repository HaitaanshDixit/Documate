from setuptools import setup, find_packages
from typing import List

def get_requirements(file_path:str)->List[str]:
    '''
    This function will return the list of requirements
    '''
    requirements=[]
    with open(file_path) as file_obj:
        requirements=file_obj.readlines()
        [req.replace("\n", "") for req in requirements]

setup(
    name='Documate',
    version='0.0.1',
    author='Haitaansh Dixit',
    author_email='dixithaitaansh@gmail.com',
    packages=find_packages(),
    install_requires=get_requirements('requirements.txt')
)