from django import forms
from django.core import files
from inanutshell_app.models import files

class frm_docupload(forms.ModelForm):
   
    class Meta:
        model = files
        fields = ('filename', 'docs', )