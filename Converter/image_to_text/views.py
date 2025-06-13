import pytesseract
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'  # 설치 경로에 맞게 수정

from PIL import Image
from django.shortcuts import render
from .forms import ImageUploadForm

def image_to_text_view(request):
    text = None
    if request.method == 'POST':
        form = ImageUploadForm(request.POST, request.FILES)
        if form.is_valid():
            image = form.cleaned_data['image']
            img = Image.open(image)
            # 한글+영어 지원: lang='kor+eng', 필요시 tesseract에 언어팩 설치
            text = pytesseract.image_to_string(img, lang='kor+eng')
    else:
        form = ImageUploadForm()
    return render(request, 'image_to_text/upload.html', {'form': form, 'text': text})
