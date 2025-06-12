from django import forms
from .models import Todo
from rpg.models import Category

class TodoForm(forms.ModelForm):
    category_large = forms.ModelChoiceField(
        queryset=Category.objects.filter(level=1), required=True, label="대분류"
    )
    category_middle = forms.ModelChoiceField(
        queryset=Category.objects.none(), required=False, label="중분류"
    )
    category_small = forms.ModelChoiceField(
        queryset=Category.objects.none(), required=True, label="소분류"
    )

    class Meta:
        model = Todo
        fields = ['title', 'description', 'due', 'category_large', 'category_middle', 'category_small']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if 'data' in kwargs:
            data = kwargs['data']
            # 중분류: 선택된 대분류의 하위만
            if data.get('category_large'):
                self.fields['category_middle'].queryset = Category.objects.filter(parent=data.get('category_large'), level=2)
            # 소분류: 선택된 중분류의 하위만
            if data.get('category_middle'):
                self.fields['category_small'].queryset = Category.objects.filter(parent=data.get('category_middle'), level=3)
        else:
            self.fields['category_middle'].queryset = Category.objects.none()
            self.fields['category_small'].queryset = Category.objects.none()

    def clean(self):
        cleaned_data = super().clean()
        # 소분류가 선택되었으면 Todo의 category에 소분류를 할당
        cleaned_data['category'] = cleaned_data.get('category_small')
        return cleaned_data
