from contextlib import nullcontext
from datetime import timezone
from django.db import models
from datetime import datetime as dt
dt.now()
from django.utils import timezone
from django.db.models import Sum







class Sale(models.Model):
    product = models.ForeignKey('Product', on_delete=models.CASCADE)
    facture_link = models.ForeignKey('Facture', on_delete=models.CASCADE, null=True, blank=True)
    quantity_sold = models.PositiveIntegerField()
    total_price = models.DecimalField(max_digits=10, decimal_places=2)
    sale_date = models.DateTimeField(default=timezone.now)
    client = models.ForeignKey('Client', on_delete=models.CASCADE, default=1)

    def save(self, *args, **kwargs):
        # Surcharge de la méthode save pour mettre à jour automatiquement le total_price lors de l'enregistrement
        self.total_price = self.product.price * self.quantity_sold
        super().save(*args, **kwargs)

    def __str__(self):
        return f"Sale #{self.id} - {self.product.name} - Facture #{self.facture_link_id}"
#relation one to many entre category et Product
class Category(models.Model):
    name = models.CharField(max_length=255, unique=True)

    def __str__(self):
        return self.name

class Product(models.Model):
    name = models.CharField(max_length=255)
    category = models.ForeignKey(Category, on_delete=models.RESTRICT)
    quantity = models.PositiveIntegerField(default=0)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    available = models.BooleanField(default=True)

    def __str__(self):
        return self.name


    def __str__(self):
        return self.name
    
class Facture(models.Model):
    
    nom_client = models.CharField(max_length=255, blank=True, null=True)
    products = models.ManyToManyField('Product', through='FactureProduct')
    prix_total = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    montant_donner = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    montant_rendu = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    date_facture = models.DateTimeField(default=timezone.now)
    
    
    
    def __str__(self):
        return f"Facture #{self.pk}"
    
    def calcul_prix_total(self):
        # Méthode pour calculer automatiquement le prix total des produits dans la facture.
        prix_total = sum(facture_product.prix_total for facture_product in self.factureproduct_set.all())
        self.prix_total = prix_total
        self.save()

    def calculer_montant_rendu(self):
        # Méthode pour calculer automatiquement le montant rendu en soustrayant le montant total des produits du montant donné.
        self.montant_rendu = self.montant_donner - self.total_produit_price
        self.save()

    def get_heure_minute_seconde(self):
        # Méthode pour obtenir l'heure, la minute et la seconde de la date_facture.
        heure_minute_seconde = self.date_facture.strftime('%H:%M:%S')
        return heure_minute_seconde
    

    #class associative de la relation many to many entre produit et facture

class FactureProduct(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    facture = models.ForeignKey(Facture, on_delete=models.CASCADE)
    quantity_product = models.PositiveIntegerField()
    total_price = models.DecimalField(max_digits=10, decimal_places=2, default=0)

     

    def save(self, *args, **kwargs):
        
        #Surcharge de la méthode save pour mettre à jour automatiquement le total_price lors de l'enregistrement.
       
        self.calculer_prix_total_produit = self.product.price * self.quantity_product
       # Appel à la méthode pour mettre à jour total_price
        super().save(*args, **kwargs)

class SearchHistory(models.Model):
    product_name = models.CharField(max_length=255)
    search_date = models.DateTimeField(auto_now_add=True)

#relation one to many entre client et transaction

class Client(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name

class Transaction(models.Model):
    OPERATOR_CHOICES = [
        ('T_money', 'T_money'),
        ('Flooz', 'Flooz'),
    ]

    OPERATION_CHOICES = [
        ('deposit', 'Dépôt'),
        ('withdrawal', 'Retrait'),
    ]

    client = models.ForeignKey(Client, on_delete=models.CASCADE)
    operator = models.CharField(max_length=10, choices=OPERATOR_CHOICES)
    operation_type = models.CharField(max_length=10, choices=OPERATION_CHOICES)
    recipient_phone = models.PositiveIntegerField()  # Utilisez PositiveIntegerField pour des nombres positifs
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.operation_type.capitalize()} - {self.amount} XOF - {self.timestamp}"




class Dashboard(models.Model):
    total_stock = models.PositiveIntegerField(default=0)
    total_sales = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    total_products = models.PositiveIntegerField(default=0)
    date_updated = models.DateTimeField(default=timezone.now)

    @classmethod
    def calculate_total_stock(cls):
        # Calculer le stock total en additionnant les quantités de tous les produits
        cls.total_stock = Product.objects.aggregate(Sum('quantity'))['quantity__sum'] or 0
        cls.save()

    @classmethod
    def calculate_total_sales(cls):
        # Calculer les ventes totales en additionnant le prix total de toutes les ventes
        cls.total_sales = Sale.objects.aggregate(Sum('total_price'))['total_price__sum'] or 0
        cls.save()

    @classmethod
    def calculate_total_products(cls):
        # Calculer le nombre total de produits
        cls.total_products = Product.objects.count()
        cls.save()

    def save(self, *args, **kwargs):
        # Mettre à jour la date de mise à jour chaque fois que le modèle est sauvegardé
        self.date_updated = timezone.now()
        super().save(*args, **kwargs)

    def __str__(self):
        return f"Dashboard - Last Updated: {self.date_updated}"





