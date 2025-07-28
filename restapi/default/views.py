from django.shortcuts import render
from django.http import JsonResponse, HttpResponse
from django.views.decorators.csrf import csrf_exempt

from .table_parser.parser import parse_create_table
from .code_generator import (
    domain_generator,
    mapper_generator,
    service_generator,
    service_impl_generator,
    xml_generator,
    extra_generator  # 추가 import
)
import tempfile
import zipfile
import os


def index(request):
    # GET 요청 시 HTML 폼 렌더링
    return render(request, 'default/index.html')


@csrf_exempt
def generate_code_view(request):
    if request.method != 'POST':
        return render(request, 'default/index.html', {'error': 'POST 요청만 지원합니다.'})

    sql = request.POST.get('sql')
    if not sql:
        return render(request, 'default/index.html', {'error': 'SQL CREATE TABLE 구문을 입력해주세요.'})

    try:
        table_info = parse_create_table(sql)
    except Exception as e:
        return render(request, 'default/index.html', {'error': f'파싱 오류: {str(e)}'})

    with tempfile.TemporaryDirectory() as tmpdir:
        template_dir = os.path.join(os.path.dirname(__file__), 'templates')
        output_dir = os.path.join(tmpdir, 'output')
        os.makedirs(output_dir, exist_ok=True)

        # 기존 코드 생성기 호출
        domain_generator.generate_domain_code(table_info, template_dir, output_dir)
        mapper_generator.generate_mapper_code(table_info, template_dir, output_dir)
        service_generator.generate_service_code(table_info, template_dir, output_dir)
        service_impl_generator.generate_service_impl_code(table_info, template_dir, output_dir)
        xml_generator.generate_mapper_xml(table_info, template_dir, output_dir)

        # 추가 코드 생성기 호출 (SwaggerConfig, Pagination, BaseMapper, BaseService, application.properties)
        extra_generator.generate_swagger_config(template_dir, output_dir)
        extra_generator.generate_pagination(template_dir, output_dir)
        extra_generator.generate_base_mapper(template_dir, output_dir)
        extra_generator.generate_base_service(template_dir, output_dir)
        extra_generator.generate_application_properties(template_dir, output_dir)

        # 생성된 파일들을 ZIP으로 묶기
        zip_path = os.path.join(tmpdir, f"{table_info['table_name']}_java_codes.zip")
        with zipfile.ZipFile(zip_path, 'w') as zipf:
            for filename in os.listdir(output_dir):
                filepath = os.path.join(output_dir, filename)
                zipf.write(filepath, arcname=filename)

        with open(zip_path, 'rb') as f:
            response = HttpResponse(f.read(), content_type='application/zip')
            response['Content-Disposition'] = f'attachment; filename={table_info["table_name"]}_java_codes.zip'
            return response
