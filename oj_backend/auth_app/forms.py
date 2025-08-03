from django import forms
from .models import CodeSubmission

class CodeSubmissionForm(forms.ModelForm):
    class Meta:
        model = CodeSubmission
        fields = ['language', 'code', 'input_data']
        widgets = {
            'language': forms.Select(attrs={
                'class': 'form-control',
                'id': 'language-select'
            }),
            'code': forms.Textarea(attrs={
                'class': 'form-control code-editor',
                'id': 'code-editor',
                'rows': 20,
                'placeholder': '# Write your code here...\n# For Python: print("Hello World")\n# For C++: #include <iostream>\n# For Java: public class Main {'
            }),
            'input_data': forms.Textarea(attrs={
                'class': 'form-control',
                'id': 'input-data',
                'rows': 5,
                'placeholder': 'Enter your input here (optional)...'
            })
        }
        labels = {
            'language': 'Programming Language',
            'code': 'Your Code',
            'input_data': 'Input Data'
        } 