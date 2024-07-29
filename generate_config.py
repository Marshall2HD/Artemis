import os

def generate_config(template_path, output_path):
    with open(template_path, 'r') as template_file:
        template = template_file.read()
    
    # Replace placeholders with environment variable values
    config_content = template
    for key, value in os.environ.items():
        placeholder = f'${{{key}}}'
        if placeholder in config_content:
            config_content = config_content.replace(placeholder, value)
    
    with open(output_path, 'w') as config_file:
        config_file.write(config_content)

if __name__ == '__main__':
    generate_config('/data/config.toml.sample', '/data/config.toml')
