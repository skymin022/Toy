from datetime import timezone
from django import forms
from .models import Todo

class TodoForm(forms.ModelForm):
    class Meta:
        model = Todo
        fields = ['title', 'description', 'category', 'due']
        widgets = {
            'due': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
        }

    def clean_title(self):
        title = self.cleaned_data.get('title')
        if len(title) < 3:
            raise forms.ValidationError("제목은 3글자 이상이어야 합니다.")
        return title

    def clean_due(self):
        due = self.cleaned_data.get('due')
        if due is not None and due < timezone.now():
            raise forms.ValidationError("마감일은 미래여야 합니다.")
        return due
