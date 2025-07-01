from django import forms
from core.models import Check_up

class CheckUpForm(forms.ModelForm):

    class Meta:
        model = Check_up
        fields = (
            'file',
            'comment',
            'phone_number',
            'accept_policy',
        )
        widgets = {
            'file': forms.FileInput(attrs={
        
            }),
            'comment' : forms.TextInput(attrs={
                'placeholder': "Nəyi yoxlamağımızı istədiyinizi qeyd edin (məsələn: qrammatika, üslub, tərcümə)"
            }),
            'phone_number' : forms.TextInput(attrs={
                'placeholder': '+994 ...'
            }),
            'accept_policy' : forms.CheckboxInput(attrs={

            }),
        }
    
    def clean_comment(self):
        value = self.cleaned_data['comment']
        if value.startswith('http'):
            raise forms.ValidationError('Comment can not be a url!')
        elif value.startswith(' '):
            raise forms.ValidationError('Comment can not start with space!')
        return value
    
    def clean_phone_number(self):
        value = self.cleaned_data['phone_number']
        if not value.isdigit():
            raise forms.ValidationError('Phone number must only contain digits!')
        return value