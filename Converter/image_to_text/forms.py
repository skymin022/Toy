from django import forms

class ImageUploadForm(forms.Form):
    image = forms.ImageField(label='이미지 파일 업로드')
