from django import forms

# The search form
# Provides the options for searching and sorting DBNs
class SearchForm(forms.Form):
    criteria = forms.CharField(initial='Enter search criteria...', max_length=200)
    trained = forms.BooleanField(required=False)
    SORTS = (
        ("namedesc", ("Name (A-Z)")),
        ("nameasc", ("Name (Z-A)")),
        ("timedesc", ("Date Added (Recent)")),
        ("timeasc", ("Data Added (Oldest)")),
    )
    order_by = forms.ChoiceField(choices=SORTS)

# The form to create the DBN
# Provides all of the labels allowed to be used
class DBNForm(forms.Form):
    name =  forms.CharField(max_length=200)
    description = forms.CharField(max_length=1000, widget=forms.Textarea)
    height = forms.IntegerField(initial=28)
    width = forms.IntegerField(initial=28)
    labels = forms.IntegerField()
    learning_rate = forms.FloatField(initial=0.1)
    private = forms.BooleanField(required=False, help_text='Check if you want a private DBN')
    layer_count = forms.IntegerField(widget = forms.HiddenInput())

    # Creates the form initially
    # Dynamically adds layers when needed
    def __init__(self, *args, **kwargs):
        layers = kwargs.pop('layer', 0)

        super(DBNForm, self).__init__(*args, **kwargs)
        self.fields['layer_count'].initial = layers

        for index in range(int(layers)):
            self.fields['layer_{index}'.format(index=index)] = forms.IntegerField()

    # Cleans the height field of the DBN
    def clean_height(self):
        data = self.cleaned_data['height']
        if (not(0 < data <= 30)):
            raise forms.ValidationError("Height must be a positive integer, maximum of 30!")
        return data

    # Cleans the width field of the DBN
    def clean_width(self):
        data = self.cleaned_data['width']
        if (not(0 < data <= 30)):
            raise forms.ValidationError("Width must be a positive integer, maximum of 30!")
        return data

    # Cleans the labels field of the DBN
    def clean_labels(self):
        data = self.cleaned_data['labels']
        if (data <= 0):
            raise forms.ValidationError("Labels must be a positive integer!")
        return data

    # Cleans the learning rate field of the DBN
    def clean_learning_rate(self):
        data = self.cleaned_data['learning_rate']
        if (data <= 0):
            raise forms.ValidationError("Learning rate must be a positive float!")
        return data