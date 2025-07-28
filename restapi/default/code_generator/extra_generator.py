from jinja2 import Environment, FileSystemLoader
import os

def generate_swagger_config(template_dir: str, output_dir: str):
    env = Environment(loader=FileSystemLoader(template_dir))
    template = env.get_template('SwaggerConfig.tpl')

    rendered = template.render()

    os.makedirs(output_dir, exist_ok=True)
    path = os.path.join(output_dir, 'SwaggerConfig.java')
    with open(path, 'w', encoding='utf-8') as f:
        f.write(rendered)


def generate_pagination(template_dir: str, output_dir: str):
    env = Environment(loader=FileSystemLoader(template_dir))
    template = env.get_template('Pagination.tpl')

    rendered = template.render()

    os.makedirs(output_dir, exist_ok=True)
    path = os.path.join(output_dir, 'Pagination.java')
    with open(path, 'w', encoding='utf-8') as f:
        f.write(rendered)

def generate_base_mapper(template_dir: str, output_dir: str):
    env = Environment(loader=FileSystemLoader(template_dir))
    template = env.get_template('BaseMapper.tpl')

    rendered = template.render()

    os.makedirs(output_dir, exist_ok=True)
    path = os.path.join(output_dir, 'BaseMapper.java')
    with open(path, 'w', encoding='utf-8') as f:
        f.write(rendered)

def generate_base_service(template_dir: str, output_dir: str):
    env = Environment(loader=FileSystemLoader(template_dir))
    template = env.get_template('BaseService.tpl')

    rendered = template.render()

    os.makedirs(output_dir, exist_ok=True)
    path = os.path.join(output_dir, 'BaseService.java')
    with open(path, 'w', encoding='utf-8') as f:
        f.write(rendered)

def generate_application_properties(template_dir: str, output_dir: str):
    env = Environment(loader=FileSystemLoader(template_dir))
    template = env.get_template('application.properties.tpl')

    rendered = template.render()

    os.makedirs(output_dir, exist_ok=True)
    path = os.path.join(output_dir, 'application.properties')
    with open(path, 'w', encoding='utf-8') as f:
        f.write(rendered)
