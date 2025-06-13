import os
import tempfile
import requests
from django.shortcuts import render, redirect
from .forms import NotionURLForm, ConvertFormatForm, TistoryUploadForm

# 아래 라이브러리들은 실제로 설치 필요
# from notion_client import Client as NotionClient
# from docx import Document
# from fpdf import FPDF

# 변환 내역 저장용(간단 예시, 실제로는 DB 모델 활용 권장)
CONVERT_HISTORY = []

def notion_upload(request):
    error = None
    html_preview = None
    converted_file = None

    if request.method == 'POST':
        url_form = NotionURLForm(request.POST)
        format_form = ConvertFormatForm(request.POST)
        if url_form.is_valid() and format_form.is_valid():
            notion_url = url_form.cleaned_data['notion_url']
            file_format = format_form.cleaned_data['format']

            try:
                # 1. Notion API로 페이지 데이터 가져오기 (여기선 예시로 간단히)
                notion_content = fetch_notion_content(notion_url)

                # 2. 고급 요소 지원: 이미지, 표, 코드블록 등 포함 변환
                html_content = convert_notion_to_html(notion_content, support_images=True, support_tables=True, support_code=True)

                # 3. 미리보기(HTML)
                html_preview = html_content

                # 4. 선택 포맷으로 변환
                if file_format == 'txt':
                    converted_file = convert_to_txt(notion_content)
                elif file_format == 'pdf':
                    converted_file = convert_to_pdf(notion_content)
                elif file_format == 'docx':
                    converted_file = convert_to_docx(notion_content)
                elif file_format == 'html':
                    converted_file = html_content

                # 5. 변환 내역 저장
                CONVERT_HISTORY.append({
                    'url': notion_url,
                    'format': file_format,
                    'preview': html_content[:500],  # 일부만 저장
                })

            except Exception as e:
                error = f"변환 실패: {str(e)}"
    else:
        url_form = NotionURLForm()
        format_form = ConvertFormatForm()

    return render(request, 'notion_converter/upload.html', {
        'url_form': url_form,
        'format_form': format_form,
        'html_preview': html_preview,
        'converted_file': converted_file,
        'error': error,
        'history': CONVERT_HISTORY,
    })

def tistory_upload(request):
    error = None
    success = None
    if request.method == 'POST':
        form = TistoryUploadForm(request.POST)
        if form.is_valid():
            try:
                # 실제로는 변환된 HTML을 세션이나 DB에서 불러와야 함
                html_content = request.POST.get('html_content')
                payload = {
                    'access_token': form.cleaned_data['access_token'],
                    'output': 'json',
                    'blogName': form.cleaned_data['blog_name'],
                    'title': form.cleaned_data['post_title'],
                    'content': html_content,
                    'visibility': 3,
                    'category': form.cleaned_data['category'],
                    'tag': form.cleaned_data['tags'],
                }
                res = requests.post('https://www.tistory.com/apis/post/write', data=payload)
                result = res.json()
                if result.get('tistory'):
                    success = result['tistory']['url']
                else:
                    error = f"Tistory 업로드 실패: {result}"
            except Exception as e:
                error = f"Tistory 업로드 중 오류: {str(e)}"
    else:
        form = TistoryUploadForm()
    return render(request, 'notion_converter/tistory_upload.html', {
        'form': form,
        'error': error,
        'success': success,
    })

# --- 아래는 실제 구현 필요 (여기선 구조 예시) ---

def fetch_notion_content(notion_url):
    # Notion API로 내용 추출 (여기선 예시)
    # notion = NotionClient(auth='your-integration-token')
    # page_id = extract_page_id(notion_url)
    # return notion.blocks.children.list(page_id)
    return {
        "title": "예시 제목",
        "blocks": [
            {"type": "text", "content": "본문 내용입니다."},
            {"type": "image", "src": "https://example.com/image.png"},
            {"type": "table", "data": [["A1", "B1"], ["A2", "B2"]]},
            {"type": "code", "language": "python", "content": "print('Hello')"},
        ]
    }

def convert_notion_to_html(notion_content, support_images=False, support_tables=False, support_code=False):
    # Notion 데이터 → HTML 변환 (고급 요소 지원)
    html = f"<h1>{notion_content['title']}</h1>"
    for block in notion_content['blocks']:
        if block['type'] == 'text':
            html += f"<p>{block['content']}</p>"
        elif block['type'] == 'image' and support_images:
            html += f"<img src='{block['src']}' alt='이미지'><br>"
        elif block['type'] == 'table' and support_tables:
            html += "<table border='1'>" + "".join(
                "<tr>" + "".join(f"<td>{cell}</td>" for cell in row) + "</tr>" for row in block['data']
            ) + "</table>"
        elif block['type'] == 'code' and support_code:
            html += f"<pre><code class='{block['language']}'>{block['content']}</code></pre>"
    return html

def convert_to_txt(notion_content):
    txt = notion_content['title'] + "\n"
    for block in notion_content['blocks']:
        if block['type'] == 'text':
            txt += block['content'] + "\n"
        elif block['type'] == 'code':
            txt += f"[코드]\n{block['content']}\n"
    return txt

def convert_to_pdf(notion_content):
    # 실제로는 PDF 생성 라이브러리 사용
    return b"%PDF-1.4\n%EOF\n"

def convert_to_docx(notion_content):
    # 실제로는 python-docx 등으로 생성한 파일의 바이트 데이터 반환
    return b"PK\x03\x04"  # DOCX 파일 헤더(ASCII)
