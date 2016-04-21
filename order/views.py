#!/usr/bin/env python
# coding: utf-8

from django.http import HttpResponse
from .models import Order, OrderLista, Kund, Artikel

def index(request):

    # Kolla om man fått en sökning.
    if 'q' in request.GET:
        sok_datum = str(request.GET['q'])
    else:
        sok_datum = "2016-04-21"

    html = '<form action="/order/" method="get"><input type="text" name="q" value="' + sok_datum + '"><input type="submit" value="Search"></form>'
    # skriva ut alla resningsdatum som finns.
    html += '<table><tr><td><h1>Resningar / Hämtningar</h1>'
    html += alla_resnings_ordrar("resning")
    html += '</td><td><h1>Rivningar / Återlämningar</h1>'
    html += alla_resnings_ordrar("rivning")
    html += '</td></tr></table>'
    pris = 0

    html += '<hr /><h1>Sokt datum: ' + sok_datum + '</h1><hr />'

    # Hamta alla ordrar och satta variabler.
    alla_ordrar = Order.objects.all().order_by('datum_resning').filter(datum_resning__lte=sok_datum).filter(datum_rivning__gte=sok_datum)

    # Hamta alla artikel ID och antalet for det IDt.
    dict_antal = alla_artiklar()

    # Loopa igenom alla ordrar och hamta orderrad per order.
    html += '<table><tr><td valign="top"><h3>Aktuella ordrar vid sokt datum.</h3>'
    for orderrad in alla_ordrar:
        # Filtrera en orderlista per order.
        hela_orderlistan = OrderLista.objects.filter(order=orderrad)
        datum_rivning = orderrad.datum_rivning

        # Skriva ut vilken order som finns.
        if str(orderrad.datum_rivning) == sok_datum:
            str_rivning = "RIVNING / ÅTERLÄMNING"
            font_color = "#BBFFB7"
        elif str(orderrad.datum_resning) == sok_datum:
            str_rivning = "RESNING / HÄMTNING"
            font_color = "#A5EAFF"
        else:
            str_rivning = ""
            font_color = "white"

        html += '<u style="background-color:' + font_color + ';">' + str(orderrad) + '</u><br >'
        html += '<b style="background-color:' + font_color + ';">' + str_rivning + '</b><br><ul style="background-color:' + font_color + ';">'


        # Hamta ut alla artiklar som tillhor ordern.
        for artikel_order in hela_orderlistan:
            #artikel_order_order = artikel_order.order
            artikel_order_artikel = artikel_order.artikel
            artikel_order_antal = artikel_order.antal

            # Rakna ut pris for artikeln.
            artikel_pris = artikel_order.antal * artikel_order_artikel.pris
            pris += artikel_pris

            # Reducera antalet for artikeln.

            # TODO Testa om det gar att lagga pa om det ar nermontering samma dag.
            if not str(datum_rivning) == sok_datum:
                dict_antal[artikel_order_artikel.id] -= artikel_order_antal


            # Skriva ut artikel
            html += '<li>' + str(artikel_order_antal) + 'st. ' + str(artikel_order_artikel) + ' (' + str(artikel_pris) + 'kr).</li>'

        html += '<b>Totalt belopp: ' + str(pris) + 'kr.</b></ul><br />'
        pris = 0

    # Loopa igenom artikel-listan och hamta ut antalet artiklar kvar.
    html += '</td><td height="100%" valign="top"><h3>Lediga artiklar</h3>'
    for key, value in dict_antal.items():
        get_artikel = Artikel.objects.get(id=key)
        if value < 0:
            value_color = "#FFB5B7"
        else:
            value_color = "#BBFFB7"

        html += '<li style="background-color:' + value_color + '">' + str(get_artikel) + ': ' + str(value) + 'st. kvar.</li>'

    html += '</td></tr></table>'
    return HttpResponse(html)

# Funktion for att hamta alla artiklar och gora till dictionary.
def alla_artiklar():
    dict_art = {}
    artiklar = Artikel.objects.all()
    for art in artiklar:
        dict_art[art.id] = art.antal

    return dict_art

# Funktion for att hamta alla ordrar och gora till lankar.
def alla_resnings_ordrar(resning_rivning):
    html_ordrar = ""
    senaste_datumet = ""
    ord_datum = ""
    counter = 0

    if resning_rivning == "resning":
        resning_eller_rivning = Order.objects.all().order_by('datum_resning')
    else:
        resning_eller_rivning = Order.objects.all().order_by('datum_rivning')

    for ord in resning_eller_rivning:
        if resning_rivning == "resning":
            ord_datum = str(ord.datum_resning)
        else:
            ord_datum = str(ord.datum_rivning)

        if not ord_datum == senaste_datumet:
            html_ordrar += '<a href="/order/?q=' + ord_datum + '">' + ord_datum + '</a>, '
            senaste_datumet = ord_datum
            counter += 1
            if counter == 5:
                html_ordrar += '<br />'
                counter = 0

    return html_ordrar