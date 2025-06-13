from django import forms

class PDFUploadForm(forms.Form):
    pdf = forms.FileField(label='PDF 파일 업로드')
