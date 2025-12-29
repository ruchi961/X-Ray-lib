import os
import json
from flask import Flask, request, jsonify
from flask_cors import CORS
from pathlib import Path
##from json_read_write import read_json
##from json_read_write import write_json
from llm_call import get_reasoning
import base64
app = Flask(__name__)
#CORS(app)
CORS(app, resources={r"/*": {"origins": "*", "methods": ["GET", "POST", "OPTIONS"]}})


#BASE_DIR="C:\Users\Admin\Downloads\vishnudeva'\backend\main_data.json"
main_json_file="main_data_file.json"
def read_json(path):
    with open(path, "r") as f:
        return json.load(f)


def write_json(path, data):
    with open(path, "w") as f:
        json.dump(data, f, indent=2)


@app.route("/full_data", methods=["POST"])
def get_full_data():
    data = request.json
    project = data.get("project")
    
    query_id = data.get("query_id")

    if not project  or not query_id:
        return jsonify({"error": "Missing fields"}), 400

    log_file = Path(project) / "log" / f"single_file.json"
    component_data = read_json(log_file)

    # get only the key-value for the query_id
    result = component_data.get(str(query_id))
    if result is None:
        return jsonify({"error": "Query ID not found"}), 404

    return jsonify(result)

@app.route("/projects", methods=["GET"])
def get_projects():
    data = read_json(main_json_file)
    print(data)
    projects = [p["project_name"] for p in data.get("projects", [])]
    return jsonify({"projects": projects})

@app.route("/components", methods=["POST"])
def get_components():
    data = request.json
    project_name = data.get("project")
    if not project_name:
        return jsonify({"error": "Missing project name"}), 400

    all_data = read_json(main_json_file)
    project = next((p for p in all_data.get("projects", []) if p["project_name"] == project_name), None)
    if not project:
        return jsonify({"error": "Project not found"}), 404

    # Return just the list of component names
    component_names = [c['id']+"_"+c["name"] for c in project.get("components", [])]
    return jsonify({"components": component_names})

@app.route("/get_ids1", methods=["POST"])
def get_ids1():
    if request.method == "OPTIONS":
        return '', 200  # respond to preflight

    data = request.json
    project_name = data.get("project")
    if not project_name:
        return jsonify({"error": "Missing project name"}), 400
    
    project_name=Path(project_name)
    all_data = read_json(os.path.join(project_name,"logs","single_file.json"))
    return jsonify({"ids": list(all_data.keys())})

@app.route("/ids", methods=["POST"])
def get_ids():  # Changed function name
    data = request.json
    project_name = data.get("project")
    if not project_name:
        return jsonify({"error": "Missing project name"}), 400

    log_file = Path(project_name) / "logs" / "single_file.json"
    
    if not log_file.exists():
        return jsonify({"ids": []})
    
    all_data = read_json(log_file)
    
    # Return just the list of IDs (keys from the JSON)
    id_names = list(all_data.keys())
    return jsonify({"ids": id_names})

@app.route("/get_component_data", methods=["POST"])
def get_component_data():
    data = request.json
    project = data.get("project")
    component = data.get("component")
    query_id = data.get("query_id")

    if not project or not component or not query_id:
        return jsonify({"error": "Missing fields"}), 400

    log_file = Path(project) / "log" / f"{component}.json"
    component_data = read_json(log_file)

    # get only the key-value for the query_id
    result = component_data.get(str(query_id))
    if result is None:
        return jsonify({"error": "Query ID not found"}), 404

    return jsonify(result)


#@app.route("/workflow", methods=["POST"])
@app.route("/workflow", methods=["POST", "OPTIONS"])
def workflow():
    if request.method == "OPTIONS":
        return '', 200
    
    data = request.json
    project = data.get("project")
    
    print(f"DEBUG: Project received: {project}")
    
    project_path = Path(project)
    image_path = project_path / "graphs" / "workflow_hierarchy.png"
    
    print(f"DEBUG: Looking for image at: {image_path}")
    print(f"DEBUG: Absolute path: {image_path.absolute()}")
    print(f"DEBUG: File exists: {image_path.exists()}")
    
    if not image_path.exists():
        # Try alternative path structure
        alt_image_path = project_path / "graphs" / "workflow.png"
        print(f"DEBUG: Trying alternative path: {alt_image_path}")
        
        if alt_image_path.exists():
            image_path = alt_image_path
        else:
            return jsonify({
                "error": f"Workflow not found. Checked: {image_path} and {alt_image_path}"
            }), 404
    
    # Read image and convert to base64
    try:
        print(image_path)
        with open(image_path, "rb") as image_file:
            encoded_string = base64.b64encode(image_file.read()).decode()
        
        return jsonify({
            "workflow_image": f"data:image/png;base64,{encoded_string}"
        })
    except Exception as e:
        return jsonify({"error": f"Failed to read image: {str(e)}"}), 500



@app.route("/log", methods=["POST"])
def log_data():
    project = component = query_id = None
    try:
        data = request.json

        project = data.get("project")
        query_id = data.get("query_id")
        component = data.get("component")
        payload = data.get("data")   # contains input/output/metadata
        print(project)

        if not project or not query_id or not component or not payload:
            return jsonify({"error": "Missing fields"}), 400

        template_path = Path(project)/ f"{component}.json"
        if not template_path.exists():
            return jsonify({"error": "Template not found"}), 404

        component_template = read_json(template_path)
        if not component_template:
            return jsonify({"error": "Component not defined in template"}), 404

        #for key in component_template.keys():
            #if key not in payload:
                #return jsonify({"error": f"Missing key: {key}"}), 400

        # Ensure log directory exists
        log_dir = Path(project) / "log"
        os.makedirs(log_dir, exist_ok=True)

        # Single component log
        log_file = log_dir / f"{component}.json"
        if log_file.exists():
            log_data_json = read_json(log_file)
        else:
            log_data_json = {}

        log_data_json[str(query_id)] = {
            "component":component,
            "input": payload.get("input", {}),
            "output": payload.get("output", {}),
            "metadata": payload.get("metadata", {})
        }

        # Add reasoning
        reasoning = get_reasoning(log_data_json[str(query_id)])  # pass dict instead of string
        #reasoning="""The search for insulated stainless steel water bottles successfully retrieved the requested 50 candidates from a total pool of 2,847 results.
        #"""
        log_data_json[str(query_id)]["reasoning"] = reasoning

        write_json(log_file, log_data_json)
        
        # Single file for all queries
        log_file_single = log_dir / "single_file.json"
        print("here")
        if log_file_single.exists():
            log_data_json_single = read_json(log_file_single)
        else:
            log_data_json_single = {}
        update=True
        print(log_data_json_single)
        #print(log_data_json_single[str(query_id)])
        print(log_data_json_single.keys())
        if log_data_json_single:
            if str(query_id) in list(log_data_json_single.keys()):
                for i in log_data_json_single[str(query_id)]:
                    if i['component'] == component:
                        update=False
                        break
        if update:
                
            log_data_json_single.setdefault(str(query_id), [])
            log_data_json_single[str(query_id)].append(log_data_json[str(query_id)])

            write_json(log_file_single, log_data_json_single)

        return jsonify({
            "status": "logged",
            "project": project,
            "component": component,
            "query_id": query_id
        })

    except Exception as e:
        print(e)
        return jsonify({
            "status": "not logged, some error occurred",
            "project": project,
            "component": component,
            "query_id": query_id
        }), 500


@app.route("/", methods=["POST"])
def health():
    return jsonify({"status": "ok"})


if __name__ == "__main__":
    app.run( port=5000)
