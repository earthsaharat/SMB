from django import forms

class UploadFileForm(forms.Form):
    imageInput = forms.ImageField()