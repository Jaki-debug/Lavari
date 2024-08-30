from django import forms
from django.forms import inlineformset_factory
from .models import Category, Facture, Product, FactureProduct, Transaction


class SearchForm(forms.Form):
    search_query = forms.CharField(max_length=255, required=False, label='Rechercher un article')



class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ['name', 'category', 'quantity', 'price', 'available']

class CategoryForm(forms.ModelForm):
    class Meta:
         model = Category
         fields = ['name']




class FactureForm(forms.ModelForm):
    class Meta:
        model = Facture
        fields = ['nom_client']  # Ajoutez ou supprimez les champs selon vos besoins

    # Vous pouvez ajouter des validations personnalisées ou des widgets ici si nécessaire

    def clean(self):
        cleaned_data = super().clean()
        # Ajoutez des validations personnalisées ici si nécessaire
        return cleaned_data
    

class FactureProductForm(forms.ModelForm):
    class Meta:
        model = FactureProduct
        fields = ['product','facture', 'quantity_product', 'total_price']

    def __init__(self, *args, **kwargs):
        super(FactureProductForm, self).__init__(*args, **kwargs)
        # Ajoutez des classes CSS personnalisées ou d'autres attributs au besoin

class TransactionForm(forms.ModelForm):
    class Meta:
        model = Transaction
        fields = ['client', 'operator', 'operation_type', 'recipient_phone', 'amount']

    


    def clean_recipient_phone(self):
        recipient_phone = self.cleaned_data.get('recipient_phone')

        # Validation spécifique pour le champ 'recipient_phone'
        if recipient_phone is not None and not str(recipient_phone).isdigit():
            raise forms.ValidationError("Veuillez saisir un numéro de téléphone valide.")

        # Vous pouvez ajouter d'autres validations ici pour le champ 'recipient_phone'

        return recipient_phone





