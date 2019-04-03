from django import forms

class SignUpForm(forms.Form):
    username = forms.CharField(max_length=100, required=True)
    email = forms.EmailField(required=True)
    password = forms.CharField(widget=forms.PasswordInput())

    def __init__(self, *args, **kwargs):
        super(SignUpForm, self).__init__(*args, **kwargs)
        self.fields['username'].widget.attrs={
            'class':'form-control'
        }
        self.fields['email'].widget.attrs={
            'class':'form-control'
        }
        self.fields['password'].widget.attrs={
            'class':'form-control'
        }