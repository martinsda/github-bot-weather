import os

def replace_variables(template_path, output_path, variables):
    with open(template_path, 'r') as file:
        content = file.read()

    for key, value in variables.items():
        content = content.replace(f'{{{{ {key} }}}}', value)

    with open(output_path, 'w') as file:
        file.write(content)

