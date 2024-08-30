# Generated by Django 4.2.7 on 2024-01-05 17:03

from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255, unique=True)),
            ],
        ),
        migrations.CreateModel(
            name='Client',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
            ],
        ),
        migrations.CreateModel(
            name='Dashboard',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('total_stock', models.PositiveIntegerField(default=0)),
                ('total_sales', models.DecimalField(decimal_places=2, default=0, max_digits=10)),
                ('total_products', models.PositiveIntegerField(default=0)),
                ('date_updated', models.DateTimeField(default=django.utils.timezone.now)),
            ],
        ),
        migrations.CreateModel(
            name='Facture',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nom_client', models.CharField(blank=True, max_length=255, null=True)),
                ('prix_total', models.DecimalField(decimal_places=2, default=0, max_digits=10)),
                ('montant_donner', models.DecimalField(decimal_places=2, default=0, max_digits=10)),
                ('montant_rendu', models.DecimalField(decimal_places=2, default=0, max_digits=10)),
                ('date_facture', models.DateTimeField(default=django.utils.timezone.now)),
            ],
        ),
        migrations.CreateModel(
            name='Product',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('quantity', models.PositiveIntegerField(default=0)),
                ('price', models.DecimalField(decimal_places=2, max_digits=10)),
                ('available', models.BooleanField(default=True)),
                ('category', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='blue.category')),
            ],
        ),
        migrations.CreateModel(
            name='SearchHistory',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('product_name', models.CharField(max_length=255)),
                ('search_date', models.DateTimeField(auto_now_add=True)),
            ],
        ),
        migrations.CreateModel(
            name='Transaction',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('operator', models.CharField(choices=[('T_money', 'T_money'), ('Flooz', 'Flooz')], max_length=10)),
                ('operation_type', models.CharField(choices=[('deposit', 'Dépôt'), ('withdrawal', 'Retrait')], max_length=10)),
                ('recipient_phone', models.PositiveIntegerField()),
                ('amount', models.DecimalField(decimal_places=2, max_digits=10)),
                ('timestamp', models.DateTimeField(auto_now_add=True)),
                ('client', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='blue.client')),
            ],
        ),
        migrations.CreateModel(
            name='Sale',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('quantity_sold', models.PositiveIntegerField()),
                ('total_price', models.DecimalField(decimal_places=2, max_digits=10)),
                ('sale_date', models.DateTimeField(default=django.utils.timezone.now)),
                ('client', models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='blue.client')),
                ('facture_link', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='blue.facture')),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='blue.product')),
            ],
        ),
        migrations.CreateModel(
            name='FactureProduct',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('quantity_product', models.PositiveIntegerField()),
                ('total_price', models.DecimalField(decimal_places=2, max_digits=10)),
                ('facture', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='blue.facture')),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='blue.product')),
            ],
        ),
        migrations.AddField(
            model_name='facture',
            name='products',
            field=models.ManyToManyField(through='blue.FactureProduct', to='blue.product'),
        ),
    ]