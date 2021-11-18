from .models import Steps, Documents
from django import forms


class Stepsform(forms.ModelForm):
    DISPLAY_Visibity_CHOICES = [
        ('Yes', 'Yes'),
        ('No', 'No')
    ]
    step_visibility = forms.ChoiceField(choices=DISPLAY_Visibity_CHOICES, widget=forms.RadioSelect(),
                                        label='Visibility')
    step_download = forms.ChoiceField(choices=DISPLAY_Visibity_CHOICES, widget=forms.RadioSelect(), label='Download')
    step_document = forms.FileField(widget=forms.ClearableFileInput(
        {'class': 'form-control form-control-lg', 'name': 'step_document'}))

    class Meta:
        model = Steps
        exclude = ('user',)
        fields = '__all__'


class DocumentsForm(forms.ModelForm):
    DISPLAY_Visibity_CHOICES = [
        ('Yes', 'Yes'),
        ('No', 'No')
    ]
    notarize = forms.ChoiceField(choices=DISPLAY_Visibity_CHOICES, widget=forms.RadioSelect(), label='Notarize',
                                 initial={'notarize': 'No'})
    apostille = forms.ChoiceField(choices=DISPLAY_Visibity_CHOICES, widget=forms.RadioSelect(), label='Apostille',
                                  initial={'apostille': 'No'})
    step_document = forms.FileField(widget=forms.ClearableFileInput(
        {'class': 'form-control form-control-lg', 'name': 'step_document'}))

    class Meta:
        model = Documents
        exclude = ('user',)
        fields = '__all__'
