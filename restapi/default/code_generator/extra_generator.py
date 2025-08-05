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

# 컨트롤러 추가 
def find_id_field(columns):
    """
    컬럼 리스트에서 PK 컬럼 또는 id, no 컬럼을 찾아 반환
    없으면 첫 번째 컬럼 반환
    """
    columns_lower = [{**col, 'name_lower': col['name'].lower()} for col in columns]
    # 1. primary 키컬럼 찾기
    for col in columns_lower:
        options = col.get('options', '')
        if options and 'primary' in options.lower():
            return col
    # 2. 컬럼명이 'id' 인 경우
    for col in columns_lower:
        if col['name_lower'] == 'id':
            return col
    # 3. 컬럼명이 'no' 인 경우
    for col in columns_lower:
        if col['name_lower'] == 'no':
            return col
    # 4. 없으면 첫 컬럼
    return columns_lower[0] if columns_lower else None

def generate_controller_code(table_info: dict, template_dir: str, output_dir: str):
    env = Environment(loader=FileSystemLoader(template_dir))
    template_home = env.get_template('home_controller.tpl')
    template_controller = env.get_template('controller.tpl')

    class_name = table_info['table_name'].capitalize()
    fields = table_info['columns']
    table_name = table_info['table_name']

    id_field = find_id_field(fields)

    # HomeController는 항상 생성 (overwrite 방지 고려 가능)
    rendered_home = template_home.render()
    home_path = os.path.join(output_dir, 'HomeController.java')
    with open(home_path, 'w', encoding='utf-8') as f:
        f.write(rendered_home)
    
    # 도메인별 Controller 생성
    rendered_controller = template_controller.render(
        class_name=class_name,
        table_name=table_name,
        fields=fields,
        id_field=id_field  # id_field 파이썬에서 미리 전달
    )
    controller_path = os.path.join(output_dir, f"{class_name}Controller.java")
    with open(controller_path, 'w', encoding='utf-8') as f:
        f.write(rendered_controller)
        
        
from jinja2 import Environment, FileSystemLoader
import os

def generate_home_controller(template_dir: str, output_dir: str):
    env = Environment(loader=FileSystemLoader(template_dir))
    template = env.get_template('home_controller.tpl')

    rendered = template.render()

    os.makedirs(output_dir, exist_ok=True)
    path = os.path.join(output_dir, 'HomeController.java')
    with open(path, 'w', encoding='utf-8') as f:
        f.write(rendered)

def find_id_field(columns):
    """
    컬럼 리스트에서 PK 컬럼 또는 id, no 컬럼을 찾아 반환
    없으면 첫 번째 컬럼 반환
    """
    columns_lower = [{**col, 'name_lower': col['name'].lower()} for col in columns]
    for col in columns_lower:
        options = col.get('options', '')
        if options and 'primary' in options.lower():
            return col
    for col in columns_lower:
        if col['name_lower'] == 'id':
            return col
    for col in columns_lower:
        if col['name_lower'] == 'no':
            return col
    return columns_lower[0] if columns_lower else None

def generate_controller(table_info: dict, template_dir: str, output_dir: str):
    env = Environment(loader=FileSystemLoader(template_dir))
    template = env.get_template('controller.tpl')

    class_name = table_info['table_name'].capitalize()
    fields = table_info['columns']
    table_name = table_info['table_name']

    id_field = find_id_field(fields)

    rendered = template.render(
        class_name=class_name,
        table_name=table_name,
        fields=fields,
        id_field=id_field
    )

    os.makedirs(output_dir, exist_ok=True)
    path = os.path.join(output_dir, f"{class_name}Controller.java")
    with open(path, 'w', encoding='utf-8') as f:
        f.write(rendered)