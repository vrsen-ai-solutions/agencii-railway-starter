from main import parse_all_tools
from agency_swarm.tools import ToolFactory
import inquirer
import pyperclip


if __name__ == '__main__':
    tools = parse_all_tools()
    tool_names = [tool.__name__ for tool in tools]

    questions = [
        inquirer.Checkbox(
            'selected_tools',
            message="Select tools to include in the schema:",
            choices=tool_names,
        ),
        inquirer.Text(
            'server_url',
            message="Enter your server URL:",
        ),
    ]

    answers = inquirer.prompt(questions)
    selected_tool_names = answers['selected_tools']
    server_url = answers['server_url']
    if not server_url.startswith("http"):
        server_url = "https://" + server_url
    selected_tools = [tool for tool in tools if tool.__name__ in selected_tool_names]

    schema = ToolFactory.get_openapi_schema(selected_tools, server_url)
    print(schema)

    # Copy schema to clipboard
    pyperclip.copy(schema)
    print("Schema copied to clipboard.")
