from django import forms
from .models import ProductReview
class ProductReviewForm(forms.ModelForm):
    class Meta:
        model = ProductReview
        fields = ['review', 'rating']
        widgets = {
            'review': forms.Textarea(attrs={'rows': 4, 'cols': 40}),
            'rating': forms.NumberInput(attrs={'min': 1, 'max': 5, 'step': 1}),
        }