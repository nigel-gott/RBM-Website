from django import forms

class DBNForm(forms.Form):
    name =  forms.CharField(max_length=200)
    description = forms.CharField(max_length=1000, widget=forms.Textarea)
    height = forms.IntegerField(initial=28)
    width = forms.IntegerField(initial=28)
    labels = forms.IntegerField()
    learning_rate = forms.FloatField()
    layer_count = forms.IntegerField(widget = forms.HiddenInput())

    def __init__(self, *args, **kwargs):
        layers = kwargs.pop('layer', 0)

        super(DBNForm, self).__init__(*args, **kwargs)
        self.fields['layer_count'].initial = layers

        for index in range(int(layers)):
            self.fields['layer_{index}'.format(index=index)] = forms.IntegerField()

    def clean_height(self):
        data = self.cleaned_data['height']
        if (not(0 < data <= 30)):
            raise forms.ValidationError("Height must be a positive integer, maximum of 30!")
        return data

    def clean_width(self):
        data = self.cleaned_data['width']
        if (not(0 < data <= 30)):
            raise forms.ValidationError("Width must be a positive integer, maximum of 30!")
        return data

    def clean_labels(self):
        data = self.cleaned_data['labels']
        if (data <= 0):
            raise forms.ValidationError("Labels must be a positive integer!")
        return data

    def clean_learning_rate(self):
        data = self.cleaned_data['learning_rate']
        if (data <= 0):
            raise forms.ValidationError("Learning rate must be a positive float!")
        return data