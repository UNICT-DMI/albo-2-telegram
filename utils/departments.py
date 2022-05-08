import re
import yaml
from typing import List, TypedDict

class Department(TypedDict):
    patterns: List[str]
    name: str

with open("departments_regex.yaml") as f:
    deps = yaml.load(f, Loader=yaml.SafeLoader)

def search_department (department: Department, text:str) -> bool: 
    return any([re.search(pattern, text) for pattern in department['patterns']])

def find_all_departments(text: str, departments: List[Department] = deps) -> List[str]:
    return [department['name'] for department in departments if search_department(department, text)]
