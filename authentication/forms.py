from django import forms
from .models import ConfigurationSettings

class ConfigurationSettingForm(forms.ModelForm):
    class Meta:
        model = ConfigurationSettings
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['rows_per_page'].widget.attrs['class'] = 'form-control'
        self.fields['topbar_link'].widget.attrs['class'] = 'form-control'
        self.fields['topbar_link_text'].widget.attrs['class'] = 'form-control'
        self.fields['sidebar_icon'].widget.attrs['class'] = 'form-control-plaintext'
        self.fields['sidebar_text'].widget.attrs['class'] = 'form-control'
        self.fields['favicon'].widget.attrs['class'] = 'form-control-plaintext'
        self.fields['server_user_name'].widget.attrs['class'] = 'form-control'
        self.fields['user_icon'].widget.attrs['class'] = 'form-control-plaintext'
        self.fields['client_user_name'].widget.attrs['class'] = 'form-control'
        self.fields['allow_host'].widget.attrs['class'] = 'form-control'


