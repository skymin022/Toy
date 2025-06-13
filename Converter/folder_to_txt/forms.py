from django import forms

# 단일 파일 처리를 위한 forms
class UploadForm(forms.Form):
    file = forms.FileField(required=False)
    folder = forms.FileField(widget=forms.ClearableFileInput(attrs={'multiple': True}), required=False)

# 여러 파일 처리를 위한 forms
class MultipleFileInput(forms.ClearableFileInput):
    allow_multiple_selected = True

class MultipleFileField(forms.FileField):
    def __init__(self, *args, **kwargs):
        kwargs.setdefault("widget", MultipleFileInput())
        super().__init__(*args, **kwargs)

    def clean(self, data, initial=None):
        single_file_clean = super().clean
        if isinstance(data, (list, tuple)):
            result = [single_file_clean(d, initial) for d in data]
        else:
            result = [single_file_clean(data, initial)]
        return result

class UploadFileForm(forms.Form):
    files = MultipleFileField()
