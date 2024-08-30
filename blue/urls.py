from django import views
from django.urls import path
 
from .views import (
   
    CategoryCreateViews,
    CategoryDeleteListeViews,
    CategoryDeleteViews,
    CategoryListeViews,
    CreateFactureView,
    CreateTransactionView,
    GestionnaireView,
    PagedesVentes,
    ProductDetailView,
    ProductListDeleteView,
    ProductListToUpdateViews,
    ProductListView,
    ProductUpdateView,
    SaleListView,
    FactureListView,
    SearchHistoryListView,
    TransactionDetailView,
    daily_transaction_chart,
    product,
    search_product,
    ProductDeleteView,
    CategoryDeleteView,
    ProductSearchView,
    product,
    transaction_statistics,
    stock_statistics,
    calculvente_stock_produit,
   
)


urlpatterns = [
    path('calculvente_stock_produit/<int:product_id>/', calculvente_stock_produit, name='calculvente_stock_produit'),
    path('sales/', SaleListView.as_view(), name='sale_list'),
    path('factures/', FactureListView.as_view(), name='facture_list'),
    path('search-history/', SearchHistoryListView.as_view(), name='search_history_list'),
    path('search-product/', search_product, name='search_product'),
    path('pagedevente/', PagedesVentes.as_view(), name='dashboard'),
    path('product/<int:pk>/delete/', ProductDeleteView.as_view(), name='product_delete'),
    path('product-search/', ProductSearchView.as_view(), name='product_search'),
    path('transaction-statistics/', transaction_statistics, name='transaction_statistics'),
    path('stock-statistics/', stock_statistics, name='stock_statistics'),
    path('creerproduit', product.as_view(), name='produit'),
    path('listerproduit', ProductListView.as_view(), name='listeDesProduit'),
    path('listeproduitasupprimer', ProductListDeleteView.as_view(), name='listeDeProduitaSupprimer'),
    path('supprimerproduit/<int:pk>/', ProductDeleteView.as_view(), name='suspressionDeProduit'),
    path('miseajourproduct/<int:pk>/update/', ProductUpdateView.as_view(), name='miseajourDeVue'),
    path('listemiseajourproduct',  ProductListToUpdateViews.as_view(), name='listedesProduitmiseajour'),
    path('creercategory', CategoryCreateViews.as_view(), name='creationdeCategory'),
    path('listercategory', CategoryListeViews.as_view(), name='listeDesCategory'),
    path('listedecategorydesuspression', CategoryDeleteListeViews.as_view(), name='listedeCategorieasupprimer'),
    path('supprimercategory/<int:pk>/', CategoryDeleteViews.as_view(), name='suspressiondeCategorie'),
    path('creerfacture', CreateFactureView.as_view(), name='creationdefacture'),
    path('creertransaction', CreateTransactionView.as_view(), name='creationdetransaction'),
    path('detailertransaction/<int:id>/', TransactionDetailView.as_view(), name='lesdetaildetransaction'),
    path('daily_transaction_chart/', daily_transaction_chart, name='daily_transaction_chart'),
    path('gestionnaire/', GestionnaireView.as_view(), name='gestionnaire'),
    path('factures/', FactureListView.as_view(), name='facture_list'),
    
   



   
    
   
]
