from jinja2 import Environment, FileSystemLoader
from table_parser.utils import sql_type_to_java_type
import os

def generate_domain_code(table_info: dict, template_dir: str, output_dir: str):
    env = Environment(loader=FileSystemLoader(template_dir))
    template = env.get_template('domain.tpl')

    # 컬럼별 Java 타입과 변수명 준비
    fields = []
    for col in table_info['columns']:
        fields.append({
            'name': col['name'],
            'java_type': sql_type_to_java_type(col['sql_type']),
            'comment': col['comment']
        })

    rendered = template.render(
        class_name=table_info['table_name'].capitalize(),
        fields=fields
    )

    # 파일 저장
    os.makedirs(output_dir, exist_ok=True)
    file_path = os.path.join(output_dir, f"{table_info['table_name'].capitalize()}.java")
    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(rendered)
