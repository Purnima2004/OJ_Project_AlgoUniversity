from django import forms
from .models import CodeSubmission


class CodeSubmissionForm(forms.ModelForm):
    """Form for the code playground"""

    class Meta:
        model = CodeSubmission
        fields = ['code', 'language']
        widgets = {
            'code': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 15,
                'placeholder': 'Write your code here...',
                'style': 'font-family: monospace;'
            }),
            'language': forms.Select(attrs={
                'class': 'form-control'
            })
        }
