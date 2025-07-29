from jinja2 import Environment, FileSystemLoader
from ..table_parser.utils import sql_type_to_java_type
import os
import re

def generate_domain_code(table_info: dict, template_dir: str, output_dir: str):
    env = Environment(loader=FileSystemLoader(template_dir))
    template = env.get_template('domain.tpl')

    fields = []
    for col in table_info['columns']:
        raw_sql_type = col['sql_type']

        # 1) sql_type에서 알파벳+숫자, 괄호로 이루어진 실제 타입 부분만 추출
        # 예: 'VARCHAR(64)NOT' -> 'VARCHAR(64)', 'BIGINTNOT' -> 'BIGINT'
        m = re.match(r'([A-Z]+(\(\d+\))?)', raw_sql_type.upper())
        if m:
            clean_sql_type = m.group(1)
        else:
            clean_sql_type = raw_sql_type.upper()  # fallback

        # 2) java 타입 변환
        java_type = sql_type_to_java_type(clean_sql_type)

        fields.append({
            'name': col['name'],
            'java_type': java_type,
            'comment': col['comment']
        })

    rendered = template.render(
        class_name=table_info['table_name'].capitalize(),
        fields=fields
    )

    os.makedirs(output_dir, exist_ok=True)
    file_path = os.path.join(output_dir, f"{table_info['table_name'].capitalize()}.java")
    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(rendered)
