from django import forms
from .models import Board


# 게시글 등록 폼
class BoardCreateForm(forms.ModelForm):
    title = forms.CharField(required=False)
    content = forms.CharField(required=False)
    username = forms.CharField(required=False)

    class Meta:
        model = Board
        fields = ["title", "content", "username"]

    # 제목 검증
    def clean_title(self):
        title = self.cleaned_data.get("title")
        if not title:
            raise forms.ValidationError("제목을 입력해주세요.")
        if len(title) < 2:
            raise forms.ValidationError("제목은 최소 2자 이상 입력해주세요.")
        if len(title) > 100:
            raise forms.ValidationError("제목은 최대 100자 이하로 입력해주세요.")
        return title

    # 내용 검증
    def clean_content(self):
        content = self.cleaned_data.get("content")
        if not content:
            raise forms.ValidationError("내용을 입력해주세요.")
        return content

    # 작성자 검증
    def clean_username(self):
        username = self.cleaned_data.get("username")
        if not username:
            raise forms.ValidationError("글쓴이를 입력해주세요.")
        if len(username) < 2:
            raise forms.ValidationError("글쓴이는 최소 2자 이상 입력해주세요.")
        if len(username) > 10:
            raise forms.ValidationError("글쓴이는 최대 10자 이하로 입력해주세요.")
        return username


# 게시글 수정 폼 (title + content만 수정)
class BoardUpdateForm(forms.ModelForm):
    title = forms.CharField(required=False)
    content = forms.CharField(required=False)

    class Meta:
        model = Board
        fields = ["title", "content"]

    def clean_title(self):
        title = self.cleaned_data.get("title")
        if not title:
            raise forms.ValidationError("제목을 입력해주세요.")
        return title

    def clean_content(self):
        content = self.cleaned_data.get("content")
        if not content:
            raise forms.ValidationError("내용을 입력해주세요.")
        return content
