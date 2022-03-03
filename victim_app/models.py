from django.db import models


class Victim(models.Model):
    ic = models.CharField(max_length=12, unique=True, verbose_name='IC Number', blank=False,
                   help_text='Enter 12 digits ic number')
    name = models.CharField(max_length=255, verbose_name='Name')
    phone = models.CharField(max_length=255, verbose_name='Phone Number')
    is_kir = models.BooleanField(default=True, verbose_name='Ketua Isi Rumah')
    salary = models.DecimalField(max_digits=8, decimal_places=2, verbose_name='Salary')
    address1 = models.CharField(max_length=255, verbose_name='Address1')
    address2 = models.CharField(max_length=255, verbose_name='Address2')
    city = models.CharField(max_length=255, verbose_name='City')
    mukim = models.CharField(max_length=255, verbose_name='Mukim')
    parlimen = models.CharField(max_length=255, verbose_name='Parlimen')
    state = models.CharField(max_length=255, verbose_name='State')
    poskod = models.CharField(max_length=255, verbose_name='Phone')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Created at')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Updated at')
