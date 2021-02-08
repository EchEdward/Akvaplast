from django import forms

class Search_form(forms.Form):
    error_css_class = 'error'
    search = forms.CharField(max_length=100, label ='Поиск продукции',
        widget=forms.TextInput(attrs={'id': "search_input","class":"text",
         "placeholder":'Поиск продукции',"autocomplete":"off"}))


    
    def clean_message(self):
        search = self.cleaned_data["search_input"]
        num_words = len(search.split())
        if num_words < 2:
            raise forms.ValidationError('Слишком мало слов')
        return search