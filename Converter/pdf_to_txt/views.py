from django.shortcuts import render
from .forms import PDFUploadForm
import PyPDF2

def pdf_to_txt_view(request):
    text = None
    if request.method == 'POST':
        form = PDFUploadForm(request.POST, request.FILES)
        if form.is_valid():
            pdf_file = form.cleaned_data['pdf']
            try:
                reader = PyPDF2.PdfReader(pdf_file)
                text = ""
                for page in reader.pages:
                    text += page.extract_text() or ""
            except Exception as e:
                text = f"PDF 읽기 오류: {e}"
    else:
        form = PDFUploadForm()
    return render(request, 'pdf_to_txt/upload.html', {'form': form, 'text': text})
