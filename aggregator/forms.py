from django import forms

class NewSourceForm(forms.Form):
    source_name = forms.CharField()

    def send_source(self):
        pass