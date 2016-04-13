#!/usr/bin/env python
# coding: utf-8

from django.http import HttpResponse
from .models import Order, OrderLista, Kund, Artikel

def index(request):

    # exempel sokning.
    sok_datum = "2016-04-09"
    html = ''
    pris = 0

    html = '<h1>Sökt datum: ' + sok_datum + '</h1><hr />'

    # Hamta alla ordrar och satta variabler.
    alla_ordrar = Order.objects.all().order_by('datum_resning').filter(datum_resning__lte=sok_datum).filter(datum_rivning__gte=sok_datum)

    # Hamta alla artikel ID och antalet for det IDt.
    dict_antal = alla_artiklar()

    # Loopa igenom alla ordrar och hamta orderrad per order.
    html += '<h3>Aktuella ordrar vid sökt datum.</h3>'
    for orderrad in alla_ordrar:
        # Filtrera en orderlista per order.
        hela_orderlistan = OrderLista.objects.filter(order=orderrad)

        # Skriva ut vilken order som finns.
        html += '<u>' + str(orderrad) + '</u><br ><ul>'


        # Hamta ut alla artiklar som tillhor ordern.
        for artikel_order in hela_orderlistan:
            #artikel_order_order = artikel_order.order
            artikel_order_artikel = artikel_order.artikel
            artikel_order_antal = artikel_order.antal

            # Rakna ut pris for artikeln.
            artikel_pris = artikel_order.antal * artikel_order_artikel.pris
            pris += artikel_pris

            # Reducera antalet for artikeln.
            dict_antal[artikel_order_artikel.id] -= artikel_order_antal

            # Skriva ut artikel
            html += '<li>' + str(artikel_order_antal) + 'st. ' + str(artikel_order_artikel) + ' (' + str(artikel_pris) + 'kr).</li>'

        html += '<b>Totalt belopp: ' + str(pris) + 'kr.</b></ul><br />'
        pris = 0

    # Loopa igenom artikel-listan och hamta ut antalet artiklar kvar.
    html += '<hr /><h3>Lediga artiklar</h3>'
    for key, value in dict_antal.items():
        get_artikel = Artikel.objects.get(id=key)
        if value < 0:
            value_color = "red"
        else:
            value_color = "green"

        html += '<p style="color:' + value_color + '">' + str(get_artikel) + ': ' + str(value) + 'st. kvar.<br />'

    return HttpResponse(html)

# Funktion for att hamta alla artiklar och gora till dictionary.
def alla_artiklar():
    dict_art = {}
    artiklar = Artikel.objects.all()
    for art in artiklar:
        dict_art[art.id] = art.antal

    return dict_art