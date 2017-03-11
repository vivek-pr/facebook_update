from models import FacebookStatus

from django import forms
class FacebookStatusForm(forms.ModelForm):
    class Meta:
        model = FacebookStatus
        fields = ['message']
        widgets = {
            'message': forms.Textarea(attrs={'class': 'form-control', 'rows': 8, 'cols': 70, 'required': 'true',
                                               'placeholder': 'Max 2000 characters'}),
        }