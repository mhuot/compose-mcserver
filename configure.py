#!/usr/bin/env python3
"""
Configuration generator for compose-mcserver

Copyright 2025 HACS Group

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

    http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.
"""

import yaml
import os
import shutil
from pathlib import Path
from jinja2 import Environment, FileSystemLoader


class ConfigGenerator:
    def __init__(self, config_file="config.yaml"):
        self.config_file = config_file
        self.config = self.load_config()
        self.templates_dir = Path("templates")
        self.jinja_env = Environment(loader=FileSystemLoader(self.templates_dir))

    def load_config(self):
        """Load configuration from YAML file"""
        if not os.path.exists(self.config_file):
            print(f"Configuration file {self.config_file} not found.")
            print("Please copy config.yaml.example to config.yaml and customize it.")
            exit(1)
        
        with open(self.config_file, 'r') as f:
            return yaml.safe_load(f)

    def generate_docker_compose(self):
        """Generate docker-compose.yml from template"""
        template = self.jinja_env.get_template('docker-compose.yml.j2')
        content = template.render(**self.config)
        
        with open('docker-compose.yml', 'w') as f:
            f.write(content)
        
        print("Generated docker-compose.yml")

    def generate_terraform_files(self):
        """Generate Terraform configuration files"""
        if not self.config.get('terraform', {}).get('enabled', False):
            print("Terraform generation disabled in config")
            return

        os.makedirs('terraform', exist_ok=True)
        
        # Generate provider.tf
        template = self.jinja_env.get_template('terraform/provider.tf.j2')
        content = template.render(**self.config)
        
        with open('terraform/provider.tf', 'w') as f:
            f.write(content)
        
        # Generate variables.tf
        template = self.jinja_env.get_template('terraform/variables.tf.j2')
        content = template.render(**self.config)
        
        with open('terraform/variables.tf', 'w') as f:
            f.write(content)
        
        print("Generated Terraform files")

    def generate_ansible_files(self):
        """Generate Ansible configuration files"""
        if not self.config.get('ansible', {}).get('enabled', False):
            print("Ansible generation disabled in config")
            return

        os.makedirs('ansible', exist_ok=True)
        
        # Generate inventory
        template = self.jinja_env.get_template('ansible/inventory.j2')
        content = template.render(**self.config)
        
        with open('ansible/inventory', 'w') as f:
            f.write(content)
        
        # Generate mcserver.yml
        template = self.jinja_env.get_template('ansible/mcserver.yml.j2')
        content = template.render(**self.config)
        
        with open('ansible/mcserver.yml', 'w') as f:
            f.write(content)
        
        print("Generated Ansible files")

    def generate_all(self):
        """Generate all configuration files"""
        self.generate_docker_compose()
        self.generate_terraform_files()
        self.generate_ansible_files()
        print("Configuration generation complete!")

    def backup_existing_files(self):
        """Backup existing configuration files"""
        files_to_backup = [
            'docker-compose.yml',
            'terraform/provider.tf',
            'terraform/variables.tf',
            'ansible/inventory',
            'ansible/mcserver.yml'
        ]
        
        for file_path in files_to_backup:
            if os.path.exists(file_path):
                backup_path = f"{file_path}.backup"
                shutil.copy2(file_path, backup_path)
                print(f"Backed up {file_path} to {backup_path}")


def main():
    import argparse
    
    parser = argparse.ArgumentParser(description='Generate configuration files for compose-mcserver')
    parser.add_argument('--config', default='config.yaml', help='Configuration file path')
    parser.add_argument('--backup', action='store_true', help='Backup existing files before generating')
    
    args = parser.parse_args()
    
    generator = ConfigGenerator(args.config)
    
    if args.backup:
        generator.backup_existing_files()
    
    generator.generate_all()


if __name__ == "__main__":
    main()