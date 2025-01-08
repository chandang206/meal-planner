from django import forms
from .models import Recipe, Ingredients
from django.core.validators import MinValueValidator

class RecipeForm(forms.ModelForm):
    # Make sure input number type are all positive
    cook_time = forms.IntegerField(
        validators=[MinValueValidator(1, message="Must be a positive number")],
        widget=forms.NumberInput(attrs={'class': 'form-control', 'min':'1'})
    )

    prep_time = forms.IntegerField(
        validators=[MinValueValidator(1, message="Must be a positive number")],
        widget=forms.NumberInput(attrs={'class':'form-control', 'min':'1'})
    )
    # Set the form
    class Meta:
        model = Recipe
        fields = ['title', 'description', 'image_url','prep_time', 'cook_time']
        widgets = {
            'title': forms.TextInput(attrs={'class':'form-control'}),
            'description': forms.Textarea(attrs={
                'class':'form-control',
                'rows': 3
            }),
            'image_url': forms.URLInput(attrs={
                'class': 'form-class',
                'placeholder': 'https://media.delight.video/0c18e53b610964fac175fe0e757adc30557e79b7/cb0e0397ffd102279027b8d892036a85e98afa8b/POSTER_USER/v1/539da799-5f01-402c-82d6-601eb4732c2e.gif?quality=90'
            })     
        }

    def clean(self):
        # Additional form validations 
        cleaned_data = super().clean()
        return cleaned_data

class IngredientForm(forms.ModelForm):
    # Make sure positive number
    id = forms.IntegerField(required=False, widget=forms.HiddenInput())
    quantity = forms.DecimalField(
        decimal_places=2,
        max_digits=5,
        validators=[MinValueValidator(0.01, message="Must be a positive number")],
        widget=forms.NumberInput(attrs={
            'class':'form-control',
            'step':'0.01',
            'min':'0.01'
        }),
    )
    
    # Set the form
    class Meta:
        model = Ingredients
        fields = ['id', 'name', 'quantity', 'unit']
        widgets = {
            'name': forms.TextInput(attrs={'class':'form-control'}),
            'unit': forms.Select(attrs={'class':'form-control'}),
        }

    def clean_quantity(self):
        # Additional validations
        quantity = self.cleaned_data.get('quantity')
        if quantity <= 0:
            raise forms.ValidationError("Quantity can not be zero or less")
        return quantity

 # form set to handle multiple ingredients
IngredientFormSet = forms.inlineformset_factory(
    Recipe,
    Ingredients,
    form=IngredientForm,
    extra=1,
    can_delete=True,
    min_num=1,
    validate_min=True
)