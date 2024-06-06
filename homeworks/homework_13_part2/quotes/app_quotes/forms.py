from django.forms import ModelForm, CharField, TextInput, Textarea
from .models import Author, Quote

class AuthorForm(ModelForm):
    fullname = CharField(widget=TextInput(attrs={'class': 'form-control', 'id': 'fullname'}))
    born_date = CharField(max_length=32, min_length=3, widget=TextInput(attrs={'class': 'form-control', 'id': 'born_date'}))
    born_location = CharField(max_length=128, min_length=3, widget=TextInput(attrs={'class': 'form-control', 'id': 'born_location'}))
    description = CharField(min_length=3, widget=Textarea(attrs={'class': 'form-control', 'id': 'description', 'rows': '4'}))
    
    
    class Meta:
        model = Author
        fields = ['fullname', 'born_date', 'born_location', 'description']

class QuoteForm(ModelForm):
    quote = CharField(min_length=3, required=True, widget=Textarea(attrs={'class': 'form-control', 'id': 'quote', 'rows': '4'}))
    author = CharField(min_length=3, required=True, widget=TextInput(attrs={'class': 'form-control', 'id': 'fullname'}))
    tags = CharField(min_length=3, required=True, widget=TextInput(attrs={'class': 'form-control', 'id': 'tags', "aria-describedby":'tagslHelp'}))
    

    class Meta:
        model = Quote
        fields = ['quote']
        exclude = ['author', 'tags']