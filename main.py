import os
from flask import Flask, request, jsonify
from helpers import parse_all_tools
from agency_swarm.tools import ToolFactory

app = Flask(__name__)

db_token = "123"

def create_endpoint(route, tool_class):
    @app.route(route, methods=['POST'], endpoint=tool_class.__name__)
    def endpoint():
        print(f"Endpoint {route} called")  # Debug print
        token = request.headers.get("Authorization").split("Bearer ")[1]
        if token != db_token:
            return jsonify({"message": "Unauthorized"}), 401

        try:
            tool = tool_class(**request.get_json())
            return jsonify({"response": tool.run()})
        except Exception as e:
            return jsonify({"Error": str(e)})
        
def parse_all_tools():
    tools_folder = './tools'
    tools = []
    for filename in os.listdir(tools_folder):
        if filename.endswith('.py'):
            tool_path = os.path.join(tools_folder, filename)
            tool_class = ToolFactory.from_file(tool_path)
            tools.append(tool_class)
    return tools

# create endpoints for each file in ./tools
tools = parse_all_tools()
print(f"Tools found: {tools}")  # Debug print

for tool in tools:
    route = f"/{tool.__name__}"
    print(f"Creating endpoint for {route}")  # Debug print
    create_endpoint(route, tool)

@app.route("/", methods=['POST'])
def tools_handler():
    print("tools_handler called")  # Debug print
    print(request.headers)  # Debug print
    try:
        token = request.headers.get("Authorization").split("Bearer ")[1]
    except Exception:
        return jsonify({"message": "Unauthorized"}), 401
        
    if token != db_token:
        return jsonify({"message": "Unauthorized"}), 401

    with app.request_context(request.environ):
        return app.full_dispatch_request()

if __name__ == '__main__':
    app.run(debug=True, port=os.getenv("PORT", default=5000))