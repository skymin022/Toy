import os
import zipfile
import tempfile
import shutil
from django.shortcuts import render, redirect
from django.http import HttpResponse

def extract_zip(file):
    temp_dir = tempfile.mkdtemp()
    with zipfile.ZipFile(file, 'r') as zip_ref:
        zip_ref.extractall(temp_dir)
    return temp_dir

def get_file_tree(root):
    tree = []
    for dirpath, _, filenames in os.walk(root):
        for f in filenames:
            rel = os.path.relpath(os.path.join(dirpath, f), root)
            tree.append(rel)
    return tree

def index(request):
    if request.method == 'POST':
        zip_file = request.FILES.get('zip_file')
        folder_files = request.FILES.getlist('folder_files')
        temp_dir = None

        # 업로드 처리
        if zip_file:
            temp_dir = extract_zip(zip_file)
        elif folder_files:
            temp_dir = tempfile.mkdtemp()
            for f in folder_files:
                dest_path = os.path.join(temp_dir, f.name)
                dest_dir = os.path.dirname(dest_path)
                os.makedirs(dest_dir, exist_ok=True)
                with open(dest_path, 'wb') as out:
                    for chunk in f.chunks():
                        out.write(chunk)

        if temp_dir:
            file_tree = get_file_tree(temp_dir)
            request.session['temp_dir'] = temp_dir
            request.session['file_tree'] = file_tree
            return redirect('select_files')
    return render(request, 'upload.html')

def select_files(request):
    file_tree = request.session.get('file_tree', [])
    return render(request, 'select_files.html', {'file_tree': file_tree})

def save_txt(request):
    temp_dir = request.session.get('temp_dir')
    file_tree = request.session.get('file_tree', [])
    selected = request.POST.getlist('selected_files')
    exclude = request.POST.getlist('exclude_files')

    # 오류 파일 제외 처리
    if exclude:
        selected = [f for f in selected if f not in exclude]

    errors = []
    file_contents = []
    readable_files = set()  # 정상적으로 읽힌 파일만 저장

    for f in sorted(selected):
        try:
            with open(os.path.join(temp_dir, f), encoding='utf-8') as file:
                content = file.read()
            file_contents.append((f, content))
            readable_files.add(f)
        except Exception as e:
            errors.append({'file': f, 'error': str(e)})

    # 오류 발생 시 안내 페이지로 이동
    if errors and not exclude:
        return render(request, 'error_files.html', {
            'errors': errors,
            'selected_files': selected,
        })

    # 오류가 없거나, 오류 파일 제외 후 저장
    response = HttpResponse(content_type='text/plain')
    response['Content-Disposition'] = 'attachment; filename="selected_files.txt"'
    response.write("폴더 구조:\n")
    # 폴더 구조에는 정상적으로 읽힌 파일만 기록
    for f in sorted(file_tree):
        if f in readable_files:
            response.write(f + '\n')
    response.write('\n\n')
    for f, content in file_contents:
        response.write(f"--- {f} ---\n")
        response.write(content + '\n\n')

    # 필요시 임시 폴더 정리 (다운로드 후)
    # 파일 반환 직전 추가
    if temp_dir:
        shutil.rmtree(temp_dir, ignore_errors=True)
        request.session.pop('temp_dir', None)
        request.session.pop('file_tree', None)


    return response
