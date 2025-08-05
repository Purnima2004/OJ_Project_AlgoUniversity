from django import forms
from .models import Problem, Contest, Submission, TestCase

class ProblemSubmissionForm(forms.ModelForm):
    """Form for submitting solutions to problems"""
    
    class Meta:
        model = Submission
        fields = ['code', 'language']
        widgets = {
            'code': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 15,
                'placeholder': 'Write your solution here...',
                'style': 'font-family: monospace;'
            }),
            'language': forms.Select(attrs={
                'class': 'form-control'
            })
        }

class ContestForm(forms.ModelForm):
    """Form for creating/editing contests"""
    
    class Meta:
        model = Contest
        fields = ['title', 'description', 'start_date', 'end_date', 'problems']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 4}),
            'start_date': forms.DateTimeInput(attrs={
                'class': 'form-control',
                'type': 'datetime-local'
            }),
            'end_date': forms.DateTimeInput(attrs={
                'class': 'form-control',
                'type': 'datetime-local'
            }),
            'problems': forms.SelectMultiple(attrs={'class': 'form-control'})
        }

class ProblemForm(forms.ModelForm):
    """Form for creating/editing problems"""
    
    class Meta:
        model = Problem
        fields = ['title', 'description', 'difficulty', 'examples', 'constraints', 'time_limit', 'memory_limit']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 8}),
            'difficulty': forms.Select(attrs={'class': 'form-control'}),
            'examples': forms.Textarea(attrs={'class': 'form-control', 'rows': 6}),
            'constraints': forms.Textarea(attrs={'class': 'form-control', 'rows': 4}),
            'time_limit': forms.NumberInput(attrs={'class': 'form-control'}),
            'memory_limit': forms.NumberInput(attrs={'class': 'form-control'})
        }

class TestCaseForm(forms.ModelForm):
    """Form for creating/editing test cases"""
    
    class Meta:
        model = TestCase
        fields = ['input_data', 'expected_output', 'is_sample', 'order']
        widgets = {
            'input_data': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 4,
                'placeholder': 'Enter test case input...'
            }),
            'expected_output': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 4,
                'placeholder': 'Enter expected output...'
            }),
            'is_sample': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'order': forms.NumberInput(attrs={'class': 'form-control'})
        }

class CodeSubmissionForm(forms.ModelForm):
    """Form for the code playground"""
    
    class Meta:
        model = Submission
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