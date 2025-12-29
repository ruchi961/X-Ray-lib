import json
import os
from graphviz import Digraph
from pathlib import Path
def render_graph(output_directory):

    try:
        # Load JSON
        with open("main.json") as f:
            workflow = json.load(f)

        # Create output folder
        output_dir = Path(os.path.join(str(output_directory),"graphs"))
        output_dir.mkdir(parents=True, exist_ok=True)

        # Create graph
        dot = Digraph("Workflow", comment="Hierarchical Workflow", format="png")
        dot.attr(rankdir="TB")  # top to bottom

        # Create nodes
        for step in workflow["components"]:
            
            dot.node(step["id"], step['name'])

        # Create edges
        for step in workflow["components_layouts"]:
            for nxt in step.get("next", []):
                dot.edge(step["id"], nxt)

        # Render graph inside folder
        output_path = output_dir / "workflow_hierarchy"
        dot.render(str(output_path), view=True)
        print("done")
        return True
    except Exception:
        return False
        
#render_graph("C:\\Users\\Admin\\Downloads\\vishnudeva'\\backend\\Demo")

