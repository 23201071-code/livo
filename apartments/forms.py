from django import forms
from .models import Apartment


class ApartmentForm(forms.ModelForm):
    class Meta:
        model = Apartment
        fields = [
            'name', 'area', 'city', 'address', 'rent_amount',
            'total_rooms', 'has_wifi', 'has_parking', 'has_ac'
        ]
        widgets = {
            'address': forms.Textarea(attrs={'rows': 2, 'placeholder': 'Full street address...'}),
            'name': forms.TextInput(attrs={'placeholder': 'e.g. Green Valley Apartment, Unit 4B'}),
            'area': forms.TextInput(attrs={'placeholder': 'e.g. Gulshan or Banani'}),
            'city': forms.TextInput(attrs={'placeholder': 'e.g. Dhaka'}),
            'rent_amount': forms.NumberInput(attrs={'min': '0'}),
            'total_rooms': forms.NumberInput(attrs={'min': '1'}),
        }

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)

        # Dynamic Label for Rent based on Role
        if user:
            self.fields['rent_amount'].label = "Rent"
            self.fields['rent_amount'].help_text = "Enter the total monthly rent for the property."

        # Apply CSS classes
        for field in self.fields.values():
            if not isinstance(field.widget, forms.CheckboxInput):
                field.widget.attrs.update({'class': 'form-control'})
