import os
import subprocess

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

def main():
    # Generate config.toml from the sample
    generate_config('/data/config.toml.sample', '/data/config.toml')
    
    # Check if config.toml was created
    if os.path.isfile('/data/config.toml'):
        print("DEBUG: config.toml created successfully.")
        # Start the application if config.toml exists
        subprocess.run(['python', '/app/bot.py'])
    else:
        print("DEBUG: Failed to create config.toml. Application will not start.")

if __name__ == '__main__':
    main()
