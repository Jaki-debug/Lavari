from urllib import request
from django.http import HttpResponse, JsonResponse
from django.shortcuts import redirect, render, get_object_or_404
from django.views import View
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.urls import reverse, reverse_lazy
from .models import Product, Sale, Facture, SearchHistory, Dashboard, Category, Transaction
from . forms import CategoryForm, FactureForm, ProductForm, SearchForm, TransactionForm      
from django.db.models import Q
from .models import Product
from django.urls import reverse_lazy
import matplotlib.pyplot as plt
from datetime import datetime
from django.db.models import Count


   

class SaleListView(ListView):
    model = Sale
    template_name = 'sale_list.html'  # Créez ce fichier dans votre dossier de modèles

class FactureListView(ListView):
    model = Facture
    template_name = 'facture_list.html'  # Créez ce fichier dans votre dossier de modèles

class SearchHistoryListView(ListView):
    model = SearchHistory
    template_name = 'search_history_list.html'  # Créez ce fichier dans votre dossier de modèles




def search_product(request):
    if request.method == 'GET':
        form = SearchForm(request.GET)
        if form.is_valid():
            search_query = form.cleaned_data['search_query']
            results = Product.objects.filter(name__icontains=search_query)
            return render(request, 'search_results.html', {'results': results, 'query': search_query})
    else:
        form = SearchForm()

    return render(request, 'search_product.html', {'form': form})


class PagedesVentes(View):
    template_name = 'pagedevente.html'

    def get(self, request, *args, **kwargs):
        # Récupérer la liste des produits
        products = Product.objects.all()

        # Récupérer les informations du tableau de bord
        dashboard_info = Dashboard.objects.first()

        # Récupérer le terme de recherche
        search_term = request.GET.get('search', '')

        # Filtrer les produits en fonction de la recherche
        search_results = Product.objects.filter(name__icontains=search_term)

        context = {
            'products': products,
            'dashboard_info': dashboard_info,
            'search_results': search_results,
        }

        return render(request, self.template_name, context)
       


    

#Supprimer un article / Supprimer une catégorie :

from django.views.generic.edit import DeleteView


class ProductDeleteView(DeleteView):
    model = Product
    template_name = 'product_confirm_delete.html'
    success_url = reverse_lazy('product_list')

class CategoryDeleteView(DeleteView):
    model = Category
    template_name = 'category_confirm_delete.html'
    success_url = reverse_lazy('category_list')


#Rechercher un article / Rechercher le prix d’un

from django.db.models import Q
from django.views.generic import ListView


class ProductSearchView(ListView):
    model = Product
    template_name = 'product_search.html'
    context_object_name = 'products'

    def get_queryset(self):
        query = self.request.GET.get('q')
        if query:
            return Product.objects.filter(Q(name__icontains=query) | Q(price__icontains=query))
        return Product.objects.all()
    

# emetre une facture 

from django.views import View
from django.db.models import Sum


#Vue pour les statistiques relatives aux transactions 
    
from django.db.models import Sum


def transaction_statistics(request):
    total_sales = Sale.objects.aggregate(total_sales=Sum('total_price'))['total_sales'] or 0

    context = {
        'total_sales': total_sales,
    }

    return render(request, 'transaction_statistics.html', context)


#Vue pour les statistiques des niveaux de stock 




def stock_statistics(request):
    total_stock = Product.objects.aggregate(total_stock=Sum('quantity'))['total_stock'] or 0

    context = {
        'total_stock': total_stock,
    }

    return render(request, 'stock_statistics.html', context)


#Vue pour les statistiques des ventes

def sales_statistics(request):
    total_sales = Sale.objects.aggregate(total_sales=Sum('quantity_sold'))['total_sales'] or 0

    context = {
        'total_sales': total_sales,
    }

    return render(request, 'sales_statistics.html', context)

# recuperation des donne de la bd pour etre utilise par le graph 

def pie_chart(request):
    # Récupérer les données depuis la base de données
    total_sales = Sale.objects.aggregate(total_sales=Sum('total_price'))['total_sales'] or 0
    total_stock = Product.objects.aggregate(total_stock=Sum('quantity'))['total_stock'] or 0

    context = {
        'total_sales': total_sales,
        'total_stock': total_stock,
    }

    return render(request, 'pie_chart.html', context)

def pie_chart_view(request):
    # Récupérez l'objet Dashboard (peut y avoir un seul objet dans votre cas)
    dashboard_info = Dashboard.objects.first()

    # Assurez-vous que dashboard_info n'est pas None avant d'accéder aux champs
    if dashboard_info:
        total_sales = dashboard_info.total_sales
        total_stock = dashboard_info.total_stock
    else:
        total_sales = 0
        total_stock = 0

    context = {
        'total_sales': total_sales,
        'total_stock': total_stock,
    }

    return render(request, 'pie_chart.html', context)

# la vu de la liste des produit



def calculvente_stock_produit(request, product_id):
    product_id  = 1
    
    # Récupéreration les données depuis la base de données
    total_sales = Sale.objects.filter(product_id=product_id).aggregate(total_sales=Sum('quantity_sold'))['total_sales'] or 0
    total_stock = Product.objects.filter(id=product_id).aggregate(total_stock=Sum('quantity'))['total_stock'] or 0

    context = {
        'total_sales': total_sales,
        'total_stock': total_stock,
    }

    return render(request, 'calculvente_stock_produit.html', context)


from django.views.generic.edit import CreateView
from . models import Product

class product(CreateView):
    model = Product
    template_name = 'creerProduit.html'
    fields = ['name', 'category', 'quantity', 'price', 'available']
    success_url = reverse_lazy('listeDesProduit')




class ProductDetailView(DetailView):
    model = Product
    template_name = 'detailProduit.html'  


class ProductListView(ListView):
    model = Product
    template_name = 'listProduit.html'
    context_object_name = 'products'  
    
    def get(self, request, *args, **kwargs):
        products = Product.objects.all()
        return render(request, self.template_name, {'products': products})
    
class ProductListDeleteView(DeleteView):
    model = Product
    template_name = 'listeProduitaSupprimer.html'
    context_object_name = 'produitaSupprimer'

    def get(self, request, *args, **kwargs):
        products = Product.objects.all()
        return render(request, self.template_name, {'products': products})
   

class ProductDeleteView(DeleteView):
    model = Product
    template_name = 'supprimerProduit.html'
    context_object_name = 'products'
    success_url = reverse_lazy('listeDesProduit') 
    
    def get_object(self, queryset=None):
        # Cette méthode assure que l'argument 'id' est utilisé pour récupérer l'objet à supprimer
        return super().get_object(queryset=queryset)
    

    
class ProductListToUpdateViews(ListView):
    model = Product
    template_name = 'listerlesProduitaMisAJour.html'
    context_object_name = 'product_to_update'

    def get(self, request, *args, **kwargs):
        products = Product.objects.all()
        return render(request, self.template_name, {'products': products})

class ProductUpdateView(UpdateView):
    model = Product
    template_name = 'miseAjourProduit.html'  # Le nom du  template pour la mise à jour du produit
    form_class = ProductForm
    success_url =  reverse_lazy('listeDesProduit') 

    # Facultatif : définissez une fonction pour obtenir l'objet à mettre à jour (par son ID)
    def get_object(self, queryset=None):
        id = self.kwargs.get('pk')  # Récupère l'ID du produit à mettre à jour depuis l'URL
        return Product.objects.get(pk=id)  # Retour
    
   #creation de la view de creation categorie
    
class CategoryCreateViews(CreateView):
    model = Category
    template_name = 'creerCategory.html'
    form_class = CategoryForm
    success_url = reverse_lazy('listeDesCategory')

class CategoryListeViews(ListView):
    model = Category
    template_name = 'listedesCategory.html'
    context_object_name = 'categories'

class CategoryDeleteListeViews(ListView):
    model = Category
    template_name = 'listedesCategoryaDelete.html'
    context_object_name = 'categories'
    success_url = reverse_lazy('listeDesCategory')

    def get_queryset(self):
        return Category.objects.all()

    def get(self, request, *args, **kwargs):
        categories = self.get_queryset()
        return render(request, self.template_name, {'categories': categories})
    
class CategoryDeleteViews(DeleteView):
    model = Category
    template_name = 'supprimerCategorie.html'
    context_object_name = 'categorieaSupprimer'
    success_url = reverse_lazy('listeDesCategory')
    
    def get_object(self, queryset=None):
        # Cette méthode assure que l'argument 'id' est utilisé pour récupérer l'objet à supprimer
        return super().get_object(queryset=queryset)





class CreateFactureView(View):
    template_name = 'creerFacture.html'
    model = Facture
    context_object_name = 'facturecreer'
    success_url = reverse_lazy('listeFacture')
    def get(self, request):
        facture_form = FactureForm()
        product_form = ProductForm()
        return render(request, self.template_name, {'facture_form': facture_form, 'product_form': product_form})

    def post(self, request):
        facture_form = FactureForm(request.POST)
        product_form = ProductForm(request.POST)

        if facture_form.is_valid() and product_form.is_valid():
            facture = facture_form.save()

            product = product_form.save(commit=False)
            product.facture = facture
            product.total_price = product.quantity_product * product.product.price
            product.save()

            facture.calcul_prix_total()
            facture.calculer_montant_rendu()

            return redirect('facture_detail', pk=facture.pk)
        else:
            return render(request, self.template_name, {'facture_form': facture_form, 'product_form': product_form})

#creer transaction
class CreateTransactionView(View):
    template_name = 'creerTransaction.html'
    form_class = TransactionForm
    context_object_name = 'lestransaction'
    success_url = reverse_lazy('lesdetaildetransaction')
    

    def get(self, request):
        form = self.form_class()
        return render(request, self.template_name, {'form': form})

    def post(self, request):
        form = self.form_class(request.POST)
        if form.is_valid():
            new_transaction = form.save()

            # Mettez l'ID de la nouvelle transaction dans l'URL de la vue détaillée
            self.success_url = reverse('lesdetaildetransaction', args=[new_transaction.id])

            return redirect(self.success_url)
        return render(request, self.template_name, {'form': form})

#detail des transaction
class TransactionDetailView(DetailView):
    model = Transaction
    template_name = 'transactionDetail.html'
    context_object_name = 'transaction'
    pk_url_kwarg = 'id' 


#affichage de la bare de statisc transaction
def daily_transaction_chart(request):
    # Récupérer les données de transaction depuis le modèle
    transactions = Transaction.objects.all()

    # Filtrer par opération et par opérateur si nécessaire
    # transactions = transactions.filter(operation_type='deposit', operator='T_money')

    # Extraire les données nécessaires pour le graphique
    dates = [transaction.timestamp for transaction in transactions]
    amounts = [float(transaction.amount) for transaction in transactions]

    # Convertir les dates en objets datetime
    dates = [date.replace(tzinfo=None) for date in dates]
    
    # Créer le graphique à barres
    plt.bar(dates, amounts, color='blue')
    plt.xlabel('Date')
    plt.ylabel('Montant des transactions (XOF)')
    plt.title('Montant des transactions journalières')
    plt.xticks(rotation=45)
    plt.tight_layout()

    # Convertir le graphique en format compatible avec HttpResponse
    response = HttpResponse(content_type='image/png')
    plt.savefig(response, format='png')
    plt.close()  # Fermez le graphique pour libérer la mémoire

    return response


class GestionnaireView(View):
    template_name = 'gestionnaire.html'

    def get(self, request):
        # Récupérer les produits et autres éléments que vous souhaitez afficher dans le gestionnaire
        products = Product.objects.all()
        categories = Category.objects.all()

        context = {
            'products': products,
            'categories': categories,
            # Ajoutez d'autres données si nécessaire
        }

        return render(request, self.template_name, context)






# blue/views.py

from django.http import HttpResponse
import matplotlib.pyplot as plt
from io import BytesIO

# views.py

from .models import FactureProduct, Product

def visualiser_produits(request):
    produits_vendus = FactureProduct.objects.exclude(montant_rendu__isnull=True)
    produits_non_vendus = Product.objects.exclude(id__in=produits_vendus.values('product'))

    context = {
        'produits_vendus': produits_vendus,
        'produits_non_vendus': produits_non_vendus,
    }

    return render(request, 'statitics_produits.html', context)



# views.py
from django.shortcuts import render
from .models import Facture

# views
class FactureListView(ListView):
    model = Facture
    template_name = 'facture_list.html'
    context_object_name = 'factures'  # Nom de la variable dans le contexte du template

    def get_queryset(self):
        return Facture.objects.all()





