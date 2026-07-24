from django import forms
from .models import Trip

class TripForm(forms.ModelForm):
    class Meta:
        model = Trip
        fields = ['title', 'destination', 'description', 'best_places', 'tips', 'rating', 'image', 'duration', 'budget']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'destination': forms.Select(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'best_places': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'tips': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'rating': forms.Select(attrs={'class': 'form-control'}),
            'image': forms.FileInput(attrs={'class': 'form-control'}),
            'duration': forms.NumberInput(attrs={'class': 'form-control'}),
            'budget': forms.NumberInput(attrs={'class': 'form-control'}),
        }


class SearchForm(forms.Form):
    search = forms.CharField(required=False, widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'ابحث...'}))
    trip_type = forms.ChoiceField(required=False, choices=[('', '- اختر النوع -'), ('nature', 'طبيعة'), ('city', 'مدن'), ('heritage', 'آثار')], widget=forms.Select(attrs={'class': 'form-control'}))
    max_budget = forms.IntegerField(required=False, widget=forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'الحد الأقصى للميزانية'}))