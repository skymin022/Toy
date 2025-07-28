from django.shortcuts import render

# Create your views here.
from django.http import JsonResponse

def hello_world(request):
    return JsonResponse({'message': 'Hello, world!'})


from django.http import JsonResponse, HttpResponse
from django.views.decorators.csrf import csrf_exempt
from table_parser.parser import parse_create_table
from code_generator import (domain_generator, mapper_generator,
                            service_generator, service_impl_generator,
                            xml_generator)
import tempfile
import zipfile
import os

@csrf_exempt
def generate_code_view(request):
    if request.method != 'POST':
        return JsonResponse({'error': 'POST 요청만 지원합니다.'}, status=405)

    sql = request.POST.get('sql')
    if not sql:
        return JsonResponse({'error': 'sql 파라미터가 필요합니다.'}, status=400)

    try:
        table_info = parse_create_table(sql)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=400)

    # 임시 폴더 생성 (파일저장용)
    with tempfile.TemporaryDirectory() as tmpdir:
        template_dir = os.path.join(os.path.dirname(__file__), 'templates')
        
        # code_generator/output 도 임시폴더 내로 지정 가능
        output_dir = os.path.join(tmpdir, 'output')
        os.makedirs(output_dir, exist_ok=True)

        # 각 코드 생성기 호출
        domain_generator.generate_domain_code(table_info, template_dir, output_dir)
        mapper_generator.generate_mapper_code(table_info, template_dir, output_dir)
        service_generator.generate_service_code(table_info, template_dir, output_dir)
        service_impl_generator.generate_service_impl_code(table_info, template_dir, output_dir)
        xml_generator.generate_mapper_xml(table_info, template_dir, output_dir)

        # 생성된 파일들을 ZIP으로 묶기
        zip_path = os.path.join(tmpdir, f"{table_info['table_name']}_java_codes.zip")
        with zipfile.ZipFile(zip_path, 'w') as zipf:
            for filename in os.listdir(output_dir):
                filepath = os.path.join(output_dir, filename)
                zipf.write(filepath, arcname=filename)

        # ZIP 파일 응답
        with open(zip_path, 'rb') as f:
            response = HttpResponse(f.read(), content_type='application/zip')
            response['Content-Disposition'] = f'attachment; filename={table_info["table_name"]}_java_codes.zip'
            return response
