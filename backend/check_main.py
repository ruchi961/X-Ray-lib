import os
import json
from pathlib import Path
from jsonschema import validate, ValidationError
JSON_FILE="main_data_file.json"

template = {
  "type": "object",
  "properties": {
    "project_id": {
      "type": "integer"
    },
    "project_name": {
      "type": "string"
    },
    "components": {
      "type": "array",
      "minItems": 1,
      "items": {
        "type": "object",
        "properties": {
          "id": {
            "type": "string"
          },
          "name": {
            "type": "string"
          },
          "filename": {
            "type": "string"
          },
          "path": {
            "type": "string"
          },
          "function_name": {
            "type": "string"
          }
        },
        "required": [
          "id",
          "name",
          "filename",
          "path",
          "function_name"
        ],
        "additionalProperties": False
      }
    },
    "components_layouts": {
      "type": "array",
      "minItems": 1,
      "items": {
        "type": "object",
        "properties": {
          "id": {
            "type": "string"
          },
          "next": {
            "type": "array",
            "items": {
              "type": "string"
            }
          }
        },
        "required": [
          "id",
          "next"
        ],
        "additionalProperties": False
      }
    },
    "create_config_llm": {
      "type": "string",
      "enum": ["yes", "no"]
    },
    "create_code_llm": {
      "type": "string",
      "enum": ["yes", "no"]
    }
  },
  "required": [
    "project_id",
    "project_name",
    "components",
    "components_layouts",
    "create_config_llm",
    "create_code_llm"
  ],
  "additionalProperties": False
}

# Validate fields against a template JSON
def validate_json_fields(input_data, template):
    try:
        validate(instance=input_data, schema=template)
       
        return True
    except ValidationError as e:
        print(f"INVALID : {e.message}")
        return False
    



# base template for each component file
def component_template(comp_id):
    return {
        "component_id": comp_id,
        "input": {},
        "output": {},
        "metadata": {},
        "reasoning": ""
    }

def generate_component_files(output_folder,components):
    
    for comp in components:
        comp_id = comp["id"]
        comp_name = comp["name"]

        file_name = f"{comp_id}_{comp_name}.json"
        file_path = os.path.join(output_folder, file_name)

        data = component_template(comp_id)

        with open(file_path, "w") as f:
            json.dump(data, f, indent=2)

        print(f"Created: {file_path}")

def save_json_file(json_data,data):
        json_data["projects"].append(data)
        with open(JSON_FILE, "w") as f:
                json.dump(json_data, f, indent=4)
def main():
    # Input JSON file
    input_file = "main.json"
    with open(input_file, "r") as f:
        data = json.load(f)

    # Template JSON to validate against
   
    if not validate_json_fields(data, template):
        print("Input JSON does not match template fields.")
        return
    # Load existing data
    if os.path.exists(JSON_FILE):
        with open(JSON_FILE, "r") as f:
            json_data = json.load(f)
    else:
        json_data = {"projects": []}

    # Append new project
    if len(json_data['projects'])==0:
        save_json_file(json_data,data)
                
    for projects in json_data['projects']:
        if projects['project_id'] != data['project_id']:
            save_json_file(json_data,data)
            break
                # Create output folder
    output_folder = Path(data['project_name'])
    output_folder.mkdir(exist_ok=True)
    generate_component_files(output_folder,data["components"])

   
    print(f"JSON files saved in '{output_folder}'")

if __name__ == "__main__":
    main()
