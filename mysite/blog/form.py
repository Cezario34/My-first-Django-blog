from django import forms

class EmailPostFrom(forms.Form):
    name = forms.CharField(max_length=25)
    email = forms.CharField()
    to  = forms.EmailField()
    comments = forms.CharField(required=False, widget=forms.Textarea)


