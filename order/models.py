from __future__ import unicode_literals

from django.db import models
from decimal import Decimal

class Kund(models.Model):
    namn = models.CharField(max_length=100)
    adress_gata = models.CharField(max_length=100)
    adress_stad = models.CharField(max_length=50)
    telefonnummer = models.CharField(max_length=15)
    epost = models.EmailField()

    def __str__(self):
        return self.namn

class Artikel(models.Model):
    artikel_namn = models.CharField(max_length=100)
    typ = models.IntegerField(max_length=None)
    antal = models.IntegerField(max_length=None)
    pris = models.DecimalField(max_digits=8, decimal_places=2, default=Decimal('0.00'))

    def __str__(self):
        return self.artikel_namn


class Order(models.Model):
    kund = models.ForeignKey(Kund, on_delete=models.CASCADE)
    datum_resning = models.DateField()
    datum_rivning = models.DateField()
    pristyp = models.CharField(max_length=100, default='Standard')
    offert = models.BooleanField(default=0)

    def __str__(self):
        return str(self.datum_resning) + ' till ' +  str(self.datum_rivning) + ', ' + self.kund.adress_stad + ' -- ' + str(self.kund)

class OrderLista(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    artikel = models.ForeignKey(Artikel, on_delete=models.CASCADE)
    antal = models.IntegerField(max_length=None)


    def __str__(self):
        return str(self.order) + ' : ' + str(self.antal) + 'st. ' + str(self.artikel)