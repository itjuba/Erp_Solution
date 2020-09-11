from django.shortcuts import render,get_object_or_404,HttpResponse
from django.utils import timezone
from .models import Client_Data,Contact
from django.forms import modelformset_factory
from .forms import ClientForm,Contact_Form       
from django.http import JsonResponse
import datetime
from Proformas.models import Facture,Commande
from django.db.models import Count
from Gestion_Achats.models import Payements,Achats,Association,Article
from Transactionb.models import Transactionb
from urllib.parse import parse_qs
import json
from django.contrib import messages
from django.template.loader import render_to_string
# Create your views here.


def ajax_trans(request):
    data = {}
    days = 30
    start_date = timezone.now() - datetime.timedelta(days=days - 1)
   

    datetime_list = []
    labels = []
    salesItems = []
    d = Transactionb.objects.filter(validation='validé').order_by('Date')
    print(d)
    for n in Transactionb.objects.filter(validation='validé').order_by('Date'):
        for x in range(0, days):
            new_time = start_date + datetime.timedelta(days=x)
            datetime_list.append(new_time)
            if (n.Date == new_time.date()):
                labels.append(new_time.strftime("%a"))
                salesItems.append(n.Montant_HT)
    print(labels)
    data['labels'] = labels
    data['data'] = salesItems
    # print(salesItems)
    # print(labels)
    return JsonResponse(data=data)


def ajax_pay(request):
    data = {}
    days = 30
    start_date = timezone.now() - datetime.timedelta(days=days - 1)

    datetime_list = []
    labels = []
    salesItems = []
    for n in Payements.objects.filter(E_S='Dépence').order_by('Date'):
        for x in range(0, days):
            new_time = start_date + datetime.timedelta(days=x)
            datetime_list.append(new_time)
            if (n.Date == new_time.date()):
                labels.append(new_time.strftime("%a"))
                salesItems.append(n.Montant_HT)
    data['labels'] = labels
    data['data'] = salesItems
    return JsonResponse(data=data)


def ajax(request):

            data = {}
            # data['labels'] = ["sebt", "had", "thnin", "tlata", "larba", "khmis", "djemaa"]
            # data['data'] = [123,100,80,2,10,50,180]
            days = 30
            start_date = timezone.now() - datetime.timedelta(days=days - 1)

            datetime_list = []
            labels = []
            salesItems = []


            for n in Payements.objects.filter(E_S='Vente').order_by('Date'):
                for x in range(0,days):
                    new_time = start_date + datetime.timedelta(days=x)
                    datetime_list.append(new_time)
                    # print(new_time.date())
                    # print(n.Date)

                    if (n.Date == new_time.date()):
                        labels.append(new_time.strftime("%a"))
                        salesItems.append(n.Montant_HT)
                # datetime_list.append(n.Date)
                # labels.append(n.Date)
                # salesItems.append(n.Montant_HT)
            data['labels'] = labels
            data['data'] = salesItems
            # if request.is_ajax():
            return JsonResponse(data=data)



def graph(request,*args,**kwargs):
    print(str(datetime.timedelta(minutes=1)))
    print('her')
    data = {}
    # days = 7
    # stat_date = timezone.now() - datetime.timedelta(days=days - 1)
    # datetime_list = []
    # labels = []
    # salesItems = []
    # for x in range(0,days):
    #     new_time = stat_date + datetime.timedelta(days=x)
    #     datetime_list.append(new_time)
    #     labels.append(new_time.strftime("%a"))
    #     print(labels.append(new_time.strftime("%a")))
    #     salesItems.append(100)
    # data['labels'] = labels
    # data['data'] = salesItems
    factur = Facture.objects.all()

    factur_pay = Facture.objects.filter(Etat=True)
    factur_np = Facture.objects.filter(Etat=False)
    mhtg_p = 0
    mhtg_np = 0
    mhtg = 0
    for x in factur_pay:
        mhtg_p = mhtg_p + x.Montant_HT
    for x in factur_np:
        mhtg_np = mhtg_np + x.Montant_HT
    for x in factur:
        mhtg = mhtg + x.Montant_HT

    if Commande.objects.all():
        print('all')
        top_client = Commande.objects.values_list('Client').annotate(truck_count=Count('Client')).order_by(
            '-truck_count')[0]
        if top_client:
         x = top_client[0]
         x = Client_Data.objects.get(id=x)
    else :
            x='No Client Found !'
    pay_vente = Payements.objects.filter(E_S="Vente")
    total_v = 0
    for d in pay_vente:
        total_v = total_v + d.Montant_HT
    if Association.objects.all():
        top_p = Association.objects.values_list('Id_Article').annotate(truck_count=Count('Id_Article')).order_by(
            '-truck_count')[0]
        p = top_p[0]
        if p:
         produit_top = get_object_or_404(Article,id=p)
         prod = produit_top.Designation
    else :
        prod = 'no product for now '

    context = {'facture': factur,
               'mhtg_p': mhtg_p,
               'mhtg_np': mhtg_np,
               'mhtg': mhtg,
               'data':data,
               'top_c': x,
               'rev': total_v,
               'top_p':prod
               }

    # print(top_client[0])


    return render(request,'Client_Section/home_client.html',context)


def home(request,*args,**kwargs):
    return render(request,'Client_Section/home_client.html',{'client':client})


def client(request):
    client = Client_Data.objects.all()
    return render(request,'Client_Section/client.html',{'client':client})

def contact(request):
    contact = Contact.objects.all()
    return render(request,'contact/contact.html',{'contact':contact})



def see(request,slug):
    data = dict()
    ProductFormSet = modelformset_factory(Contact, fields=('Nom','post','Tel','email','contact_type','client'), extra=0)
    client = get_object_or_404(Client_Data, slug=slug)

    attig = request.POST or None
    formset = ProductFormSet(data=attig, queryset=Contact.objects.filter(client=client))

    for form in formset:
        form.fields['client'].queryset = Contact.objects.filter(client=client.id)

    if request.method == 'POST':
        print('hello')
        print(formset.is_bound)
        if formset.is_valid():
          formset.save()






    context = {'form': formset}
    template_name = 'Client_Section/partial_client_contact.html'
    data['html_form'] = render_to_string(template_name, context, request=request)
    return JsonResponse(data)
    # return render(request,template_name,context)



def save_client_form(request, form,Contact_form, template_name):
    data = dict()
    if request.method == 'POST':
        if form.is_valid() and Contact_form.is_valid():
            client = form.save()
            contact = Contact_form.save(commit=False)
            contact.client = client
            contact.save()
            form.save()
            Contact_form.save()

            data['form_is_valid'] = True
            books = Client_Data.objects.all()
            data['html_book_list'] = render_to_string('Client_Section/partial_client_c.html', {
                'client': books
            })
        else:
            print(Contact_form.non_field_errors())
            print(Contact_form.errors.as_text())
            print(Contact_form.errors)
            print(form.errors)
            # print(Contact_form.non_field_errors.as_data())
            data['form_is_valid'] = False


    context = {'form': form,'contact_form':Contact_form}
    # data['errors'] = repr(Contact_form.errors.as_data())
    data['errors'] = Contact_form.errors.as_text()
    data['errors_c'] = form.errors.as_text()
    data['html_form'] = render_to_string(template_name, context, request=request)
    return JsonResponse(data)

def save_contact_form(request,Contact_form, template_name):
    data = dict()
    if request.method == 'POST':
        if  Contact_form.is_valid():

            Contact_form.save()

            data['form_is_valid'] = True
            books = Contact.objects.all()
            data['html_book_list'] = render_to_string('contact/contact_list.html', {
                'contact': books
            })
        else:


            data['form_is_valid'] = False
    context = {'form':Contact_form}
    print(Contact_form.errors.as_text())
    data['errors'] = Contact_form.errors.as_text()
    data['html_form'] = render_to_string(template_name, context, request=request)
    return JsonResponse(data)


def save_client_form_update(request, form, template_name):
    data = dict()
    if request.method == 'POST':
        print(request.method=='POST')
        if form.is_valid():

            form.save()

            data['form_is_valid'] = True
            books = Client_Data.objects.all()
            data['html_book_list'] = render_to_string('Client_Section/partial_client_c.html', {
                'client': books
            })
        else:
            print(form.errors)

            data['form_is_valid'] = False
    context = {'form': form}
    data['html_form'] = render_to_string(template_name, context, request=request)
    return JsonResponse(data)


def save_client_form_update(request, form, template_name):
    data = dict()
    if request.method == 'POST':
        print(request.method=='POST')
        if form.is_valid():

            form.save()

            data['form_is_valid'] = True
            books = Client_Data.objects.all()
            data['html_book_list'] = render_to_string('Client_Section/partial_client_c.html', {
                'client': books
            })
        else:
            print(form.errors)

            data['form_is_valid'] = False
    context = {'form': form}
    data['html_form'] = render_to_string(template_name, context, request=request)
    return JsonResponse(data)



def Contact_create(request):
    if request.method == 'POST':
        contact_form = Contact_Form(request.POST)
    else:
        contact_form = Contact_Form()
    return save_contact_form(request,contact_form, 'contact/partial_contact/partial_contact.html')



def client_create(request):
    if request.method == 'POST':
        form = ClientForm(request.POST)
        contact_form = Contact_Form(request.POST)
    else:
        form = ClientForm()
        contact_form = Contact_Form()
    return save_client_form(request, form,contact_form, 'Client_Section/partial_client.html')



def contact_update(request,pk):
    contact = get_object_or_404(Contact, pk=pk)
    print(contact)
    if request.method == 'POST':
        print(request.POST)
        form = Contact_Form(request.POST, instance=contact)

    else:
        form = Contact_Form(instance=contact)


    return save_contact_form(request, form,'contact/partial_contact/partial_contact_update.html')



def client_update(request,slug):
    client = get_object_or_404(Client_Data, slug=slug)
    if request.method == 'POST':
        print(request.POST)
        form = ClientForm(request.POST, instance=client)

    else:
        form = ClientForm(instance=client)


    return save_client_form_update(request, form,'Client_Section/partial_client_update_update.html')



def contact_delete(request, pk):
    contact = get_object_or_404(Contact, pk=pk)
    data = dict()
    if request.method == 'POST':
        contact.delete()
        data['form_is_valid'] = True  # This is just to play along with the existing code
        books = Contact.objects.all()
        data['html_book_list'] = render_to_string('contact/contact_list.html', {
            'contact': books
        })
    else:
        context = {'obj': contact}
        data['html_form'] = render_to_string('contact/partial_contact/partial_contact_delete.html',
            context,
            request=request,
        )
    return JsonResponse(data)





def client_delete(request, slug):
    book = get_object_or_404(Client_Data, slug=slug)
    data = dict()
    if request.method == 'POST':
        book.delete()
        data['form_is_valid'] = True  # This is just to play along with the existing code
        books = Client_Data.objects.all()
        data['html_book_list'] = render_to_string('Client_Section/partial_client_c.html', {
            'client': books
        })
    else:
        context = {'obj': book}
        data['html_form'] = render_to_string('Client_Section/partial_client_delete.html',
            context,
            request=request,
        )
    return JsonResponse(data)








#
# def create_client(request):
#     data = dict()
#
#     if request.method == 'POST':
#         form = ClientForm(request.POST)
#         if form.is_valid():
#             form.save()
#             data['form_is_valid'] = True
#             books = Client_Data.objects.all()
#             data['html_book_list'] = render_to_string('Client_Section/partial_client_c.html', {
#                 'client': books
#             })
#         else:
#             data['form_is_valid'] = False
#     else:
#         form = ClientForm()
#
#     context = {'form': form}
#     data['html_form'] = render_to_string('Client_Section/partial_client.html',
#                                          context,
#                                          request=request
#                                          )
#     return JsonResponse(data)
#
#



