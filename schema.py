from main import parse_all_tools
from agency_swarm.tools import ToolFactory
import inquirer
import pyperclip


if __name__ == '__main__':
    tools = parse_all_tools()
    tool_folder_names = list(tools.keys())

    if 'root' in tool_folder_names:
        tool_folder_names.remove('root')
        # Store both the tool class and name for root tools
        root_tool_mapping = {tool.__name__: tool for tool in tools['root']}
        root_tool_names = list(root_tool_mapping.keys())
    else:
        root_tool_names = []

    questions = [
        inquirer.Checkbox(
            'selected_tools',
            message="Select the tool folders to include in the schema:",
            choices=tool_folder_names,
        ),
        inquirer.Text(
            'server_url',
            message="Enter your server URL:",
        ),
    ]

    if root_tool_names:
        questions.insert(1, inquirer.Checkbox(
            'selected_root_tools',
            message="Select individual tools to include in the schema:",
            choices=root_tool_names,
        ))

    answers = inquirer.prompt(questions)
    selected_tool_folder_names = answers['selected_tools']
    server_url = answers['server_url']
    if not server_url.startswith("http"):
        server_url = "https://" + server_url

    selected_tools = []
    # Add tools from selected folders
    for tool_folder_name in selected_tool_folder_names:
        selected_tools.extend(tools[tool_folder_name])
    
    # Add selected root tools using the mapping
    if root_tool_names and 'selected_root_tools' in answers:
        selected_root_tools = [root_tool_mapping[name] for name in answers['selected_root_tools']]
        selected_tools.extend(selected_root_tools)

    schema = ToolFactory.get_openapi_schema(selected_tools, server_url)
    print(schema)

    # Copy schema to clipboard
    pyperclip.copy(schema)
    print("Schema copied to clipboard.")