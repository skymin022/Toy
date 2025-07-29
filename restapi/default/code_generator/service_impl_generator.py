from jinja2 import Environment, FileSystemLoader
import os

def generate_service_impl_code(table_info: dict, template_dir: str, output_dir: str):
    env = Environment(loader=FileSystemLoader(template_dir))
    template = env.get_template('service_impl.tpl')

    class_name = table_info['table_name'].capitalize()

    rendered = template.render(
        class_name=class_name,
        package='com.example.service.impl',
        mapper_package='com.example.mapper',
        fields=table_info['columns']   # 추가 필요
    )


    os.makedirs(output_dir, exist_ok=True)
    file_path = os.path.join(output_dir, f"{class_name}ServiceImpl.java")
    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(rendered)
