from django import forms

class PubBlogForm(forms.Form):
    title = forms.CharField(max_length=200, min_length=2, label="Title")
    content = forms.CharField(min_length=2, widget=forms.Textarea, label="Content")
    category = forms.IntegerField(label="Category")
    img = forms.ImageField(required=False, label="Image")  # 添加图片上传字段
