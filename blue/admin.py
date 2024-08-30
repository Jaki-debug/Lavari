
from django.contrib import admin
from .models import Facture, Product, FactureProduct, Category 

admin.site.register(Facture)
admin.site.register(Product)
admin.site.register(FactureProduct)
admin.site.register(Category)