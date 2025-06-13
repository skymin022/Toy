from django import forms

class ScreenUploadForm(forms.Form):
    image = forms.ImageField(label='스크린샷 업로드')
