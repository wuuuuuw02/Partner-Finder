# posts/forms.py

from django import forms
from .models import Request

class RequestForm(forms.ModelForm):
    class Meta:
        model = Request
        fields = ['request_type', 'title', 'description']
        widgets = {
            'request_type': forms.Select(attrs={'class': 'form-control'}),
            'title': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Например: Ищу напарника для CS2'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 6, 'placeholder': 'Опишите ваши цели, требования, расписание...'}),
        }
        labels = {
            'request_type': 'Тип заявки',
            'title': 'Заголовок / Тема',
            'description': 'Описание', 
        }