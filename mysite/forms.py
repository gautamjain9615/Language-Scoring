from dataclasses import fields
from django import forms
import json
from mysite.models import Input
class InputForm(forms.Form):
    # link = forms.CharField()
    json_input = forms.CharField()
    def clean_jsonfield(self):
         jdata = self.cleaned_data['json_input']
         try:
             json_data = json.loads(jdata) #loads string as json
             #validate json_data
         except:
             raise forms.ValidationError("Invalid data in jsonfield")
         #if json data not valid:
            #raise forms.ValidationError("Invalid data in jsonfield")
         return jdata

    class Meta:
        model = Input
        # fields = ('link', 'json_input')
        fields = ('json_input')
