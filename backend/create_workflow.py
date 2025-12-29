import json
import os
from pathlib import Path
from jsonschema import validate, ValidationError
from llm_call import get_config_json
from create_graph import render_graph

#SCHEMA
schema_componets = {
    "type": "object",
    "properties": {
        "input": {},
        "output": {},
        "metadata": {},
        "reasoning": {}
    },
    "required": ["input", "output", "metadata", "reasoning"],
    "additionalProperties": True
}
schema_single_query = {
    "type": "object",
    "properties": {
        "queryid": {},
        "queries": {
            "type": "array",
            "minItems": 1,    # at least 1 component
           
            "items": {
                "type": "object",
                "properties": {
                    "component_id":{},
                    "input": {},
                    "output": {},
                    "metadata": {},
                    "reasoning": {}
                },
                "required": ["component_id","input", "output", "metadata", "reasoning"],
                "additionalProperties": True
            }
        }
    },
    "required": ["queryid", "queries"],
    "additionalProperties": True
}


def validate_json_file(json_file,schema):


    try:
        with open(json_file, "r") as f:
            data = json.load(f)
        validate(instance=data, schema=schema)
        print(f"{json_file.name} is valid")
        return True
    except ValidationError as e:
        print(f"{json_file.name} doesnt exists or is invalid: {e.message}")
        return False
    
def read_json(input_file):

    try:
        with open(input_file, "r") as f:
            data = json.load(f)
        return data
    except Exception as e:
        print(f"SOme error occured while reading the {input_file} file {e}")
        return False

def write_json(output_file, data):
    try:
        output_path = Path(output_file)
        output_path.parent.mkdir(parents=True, exist_ok=True)
        print(type(data))
        with open(output_path, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2, ensure_ascii=False)

        print(f"JSON written successfully: {output_path}")
        return True


    except Exception as e:
        print(f"Unexpected error while writing JSON: {e}")

    return False


def extract_python_function(file_path, function_name):
    with open(file_path, "r", encoding="utf-8") as f:
        lines = f.readlines()

    func_lines = []
    inside_func = False
    base_indent = None

    for line in lines:
        #print(line)
        if line.lstrip().startswith(f"def {function_name}("):
            #print("hi",line)
            inside_func = True
            base_indent = len(line) - len(line.lstrip())
            func_lines.append(line)
            #print(func_lines)
            continue

        if inside_func:
            current_indent = len(line) - len(line.lstrip())
            if line.strip() and current_indent <= base_indent:
                break
            func_lines.append(line)

    #print(func_lines)
    return "".join(func_lines)
def extract_js_function(file_path, function_name):
    with open(file_path, "r", encoding="utf-8") as f:
        text = f.read()

    start = text.find(function_name)
    if start == -1:
        return None

    brace_count = 0
    in_func = False
    result = []

    for char in text[start:]:
        result.append(char)
        if char == "{":
            brace_count += 1
            in_func = True
        elif char == "}":
            brace_count -= 1
            if in_func and brace_count == 0:
                break

    return "".join(result)



def get_code_data(file_path, function_name,language="python"):
    if language=="python":
        data = extract_python_function(file_path, function_name)
    else:
        data = extract_js_function(file_path, function_name)
    return data
code_path="C:\\Users\\Admin\\Downloads\\vishnudeva'\\backend\\democ_code"
def main():
    # Flag to check if we should validate
    data = read_json("main.json")
    if data:
        folder = Path(data['project_name'])
        if not folder.exists():
            print("Folder is not created ,please run check_main.py first")
            return
    rendered = render_graph(data['project_name'])
    if rendered:
        print("workflow image created")
    list_temp = []
    for i in range(len(data['components'])):
                   list_temp.append({
                  "component_id": "",
                  "input": {},
                  "output": {},
        "metadata": {
      }})
    single_data={
          "queryid": "",
          "queries": list_temp
    }
    # create single query
    write_json(os.path.join(folder,"single_queries.json"),single_data)
    # call llm 
    if data['create_config_llm'].lower()=="yes" or data['create_config_llm'].lower()=="y":
            for comp in data['components']:
                code_data = get_code_data(os.path.join(code_path,comp['filename']),comp['function_name'])
                print(code_data)
                
                response_data = get_config_json(code_data)
                write_json(os.path.join(data['project_name'],comp['id']+"_"+comp['name']+".json"),response_data)
                
            new_list_temp=[]
            for comp in data['components']:
                new_list_temp.append(read_json(os.path.join(data['project_name'],comp['id']+"_"+comp['name']+".json")))
            single_data={
                  "queryid": "",
                  "queries": new_list_temp
            }  
            write_json(os.path.join(data['project_name'],"single_queries.json"),single_data)
            
    for json_file in folder.glob("*.json"):
            if "single" in str(json_file):
                validate_json_file(json_file,schema_single_query)
            else:
                validate_json_file(json_file,schema_componets)
       
                

        

if __name__ == "__main__":
    main()
