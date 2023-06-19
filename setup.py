
# Imports 
from setuptools import find_packages, setup 
from typing import List 

# Constants 
HYPHEN_E_DOT = '-e .'

# get requirements function 
def get_requirements(file_path:str) -> List[str] :
    '''
    This function will return a list of requirements
    '''
    requirements = []
    with open(file_path) as file_obj : 
        requirements = file_obj.readlines()
        requirements = [ req.replace("\n", "") for req in requirements]

        if HYPHEN_E_DOT in requirements : requirements.remove(HYPHEN_E_DOT) 
    return requirements 

# setup arguments 
setup(
    name="ml_project" ,
    version='0.0.1' ,
    author="Anvesh Dange",
    author_email="dangeanv@gmail.com" ,
    packages=find_packages(),
    install_requires= get_requirements('requirements.txt')
)
