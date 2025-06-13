from django import forms

class NotionURLForm(forms.Form):
    notion_url = forms.URLField(label="Notion 페이지 URL")

class ConvertFormatForm(forms.Form):
    FORMAT_CHOICES = [
        ('pdf', 'PDF'),
        ('docx', 'Word'),
        ('txt', 'TXT'),
        ('html', 'HTML'),
    ]
    format = forms.ChoiceField(choices=FORMAT_CHOICES, label="변환 포맷")

class TistoryUploadForm(forms.Form):
    access_token = forms.CharField(label="Tistory Access Token")
    blog_name = forms.CharField(label="블로그명")
    post_title = forms.CharField(label="포스트 제목")
    category = forms.CharField(label="카테고리", required=False)
    tags = forms.CharField(label="태그(쉼표로 구분)", required=False)
