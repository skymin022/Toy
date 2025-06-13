import pytesseract
from PIL import Image
from django.shortcuts import render
from .forms import ScreenUploadForm

def screen_to_txt_view(request):
    text = None
    if request.method == 'POST':
        form = ScreenUploadForm(request.POST, request.FILES)
        if form.is_valid():
            image = form.cleaned_data['image']
            img = Image.open(image)
            text = pytesseract.image_to_string(img, lang='kor+eng')
    else:
        form = ScreenUploadForm()
    return render(request, 'screen_to_txt/upload.html', {'form': form, 'text': text})
