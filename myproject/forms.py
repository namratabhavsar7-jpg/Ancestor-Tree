from django import forms
from .models import FamilyMember

class FamilyMemberForm(forms.ModelForm):
    class Meta:
        model = FamilyMember
        # '__all__' likhne se model ke saare fields form mein aa jayenge
        fields = '__all__'
        
        # UI ko premium banane ke liye widgets add karein
        widgets = {
            'first_name': forms.TextInput(attrs={'class': 'form-input', 'placeholder': 'Enter First Name'}),
            'last_name': forms.TextInput(attrs={'class': 'form-input', 'placeholder': 'Enter Last Name'}),
            'address': forms.Textarea(attrs={'class': 'form-input', 'rows': 3}),
            'current_address': forms.Textarea(attrs={'class': 'form-input', 'rows': 3}),
            'bank_details': forms.Textarea(attrs={'class': 'form-input', 'rows': 2}),
            
            # Identity Redaction Placeholder
            'aadhar_card_number': forms.TextInput(attrs={'class': 'form-input', 'placeholder': '12 Digit Aadhaar'}),
            'pan_card_number': forms.TextInput(attrs={'class': 'form-input', 'placeholder': 'ABCDE1234F'}),
        }