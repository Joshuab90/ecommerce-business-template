from __future__ import unicode_literals
from django.contrib.auth.models import User
from django.db import models

class Cart(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    create_date = models.DateTimeField(verbose_name='create date', auto_now=True)
    checked_out = models.BooleanField(default=False, verbose_name='checked out')

    def __unicode__(self):
        return unicode(self.create_date)

class Product(models.Model):
    title = models.CharField(null=True, blank=True, max_length=100)
    description = models.CharField(null=True, blank=True, max_length=100)
    unit_price = models.DecimalField(max_digits=18, decimal_places=2, verbose_name='unit price')
    total_items = models.IntegerField()

    def __unicode__(self):
        return u'%s - %s' % (self.title, self.unit_price)

class Item(models.Model):
    cart = models.ForeignKey(Cart, verbose_name='cart', related_name='cart', on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(verbose_name='quantity')
    product = models.ForeignKey(Product, verbose_name='product', related_name='product', on_delete=models.CASCADE)

    def __unicode__(self):
        return u'%d units' % (self.quantity)