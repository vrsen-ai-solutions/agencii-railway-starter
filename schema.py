from main import parse_all_tools
from agency_swarm.tools import ToolFactory
import inquirer
import pyperclip


if __name__ == '__main__':
    tools = parse_all_tools()
    tool_folder_names = list(tools.keys())

    if 'root' in tool_folder_names:
        tool_folder_names.remove('root')
        root_tools = [tool.__name__ for tool in tools['root']]
    else:
        root_tools = []

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

    if root_tools:
        questions.insert(1, inquirer.Checkbox(
            'selected_root_tools',
            message="Select individual tools to include in the schema:",
            choices=root_tools,
        ))

    answers = inquirer.prompt(questions)
    selected_tool_folder_names = answers['selected_tools']
    server_url = answers['server_url']
    if not server_url.startswith("http"):
        server_url = "https://" + server_url
    selected_tools = []
    for tool_folder_name in selected_tool_folder_names:
        selected_tools.extend(tools[tool_folder_name])
    if root_tools:
        selected_tools.extend(answers['selected_root_tools'])

    schema = ToolFactory.get_openapi_schema(selected_tools, server_url)
    print(schema)

    # Copy schema to clipboard
    pyperclip.copy(schema)
    print("Schema copied to clipboard.")
