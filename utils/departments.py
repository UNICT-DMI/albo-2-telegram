import re
import yaml
from typing import List, TypedDict

class Department(TypedDict):
    patterns: List[str]
    name: str

with open("departments_regex.yaml") as f:
    deps = yaml.load(f, Loader=yaml.SafeLoader)

def search_department (department: Department, text:str) -> bool: 
    return any([re.search(pattern, text, re.IGNORECASE) for pattern in department['patterns']])

def find_all_departments(text: str, departments: List[Department] = deps) -> List[str]:
    department_tags = [department['name'] for department in departments if search_department(department, text)]
    # Avoid double match for Ingegneria Informatica
    if 'DIEEI' in department_tags and 'DMI' in department_tags:
        department_tags.remove('DMI')
    return department_tags
