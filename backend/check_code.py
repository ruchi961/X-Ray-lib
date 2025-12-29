import re
import json
from create_workflow import get_code_data
from create_workflow import read_json
import os
def extract_keys(data):
    """
    Recursively extracts all keys from nested JSON/dict/list.
    Returns a set of unique keys.
    """
    keys = set()
    
    if isinstance(data, dict):
        for key, value in data.items():
            keys.add(key)
            if isinstance(value, (dict, list)):
                keys.update(extract_keys(value))
                
    elif isinstance(data, list):
        for item in data:
            if isinstance(item, (dict, list)):
                keys.update(extract_keys(item))
                
    return keys
def check_keys_in_context(context: str,paths):
    found = []
    missing = []
    
    REQUIRED_KEYS_LIST=list(extract_keys(read_json(paths)))
    REQUIRED_KEYS=[]
    for i in REQUIRED_KEYS_LIST:
        try:
        
            if int(i):
                continue
        except Exception as e:
            REQUIRED_KEYS.append(i)
            
    print("some",REQUIRED_KEYS,context)
    for key in REQUIRED_KEYS:
        # key can appear as "key", 'key', or key:
        if key in context:
            found.append(key)
        else:
            missing.append(key)

    return found, missing



def check_code_for_logged_keys(code: str,paths):
    
 
    for idx, ctx in enumerate(code, 1):
        found, missing = check_keys_in_context(code,paths)

        print("Found keys:", found)
        print("Missing keys:", missing)

        if not missing:
            print("ALL REQUIRED KEYS ARE PRESENT")
            return True
        else:
            print("KEYS NOT BEING SENT")
            return False


data =read_json("main_data_file.json")
projects = data.get("projects")
project_id=input("Please enter project id: ")
component = {}
print(projects)
for j in projects:
    if j['project_id']==int(project_id):
        component = j

print(component)
for i in component['components']:

        print(i)
        code = str(get_code_data( os.path.join(i['path'],i['filename']), i['function_name']))
        print(code)
        if check_code_for_logged_keys(code,os.path.join(component['project_name'],i['id']+"_"+i['name']+".json")):
            print("Code check for ",i['name'])
        else:
            print("Code not having loggin for ",i['name'])
        print("----------------")
