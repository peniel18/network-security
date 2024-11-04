from setuptools import setup, find_packages
from typing import List



def get_requirements() -> List[str]:
    """
    Gets requirements for the project
    Returns: 
        List of requirements 
    
    """
    requirementList : List[str] = []
    try: 
        with open("requirements.txt", "r") as file: 
            lines = file.readlines()
            for line in lines: 
                requirement = line.strip()
                # ignore -e. and empty lines
                if requirement and not requirement.startswith("-e ."):
                    requirementList.append(requirement)
    except FileNotFoundError: 
        print("Requirements.txt not found")

    return requirementList


print(get_requirements())





