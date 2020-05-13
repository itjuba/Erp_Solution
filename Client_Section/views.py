from django.shortcuts import render,get_object_or_404,HttpResponse

from .models import Client_Data,Contact
from django.forms import modelformset_factory
from .forms import ClientForm,Contact_Form       
from django.http import JsonResponse
from urllib.parse import parse_qs
import json
from django.contrib import messages
from django.template.loader import render_to_string
# Create your views here.

def graph(request,*args,**kwargs):
    data = {
        'sales' : 100,
        'customers':10
    }
    return JsonResponse(data)

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
    print(request.POST)
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
            print(form.errors)
            print(Contact_form.errors)
            data['form_is_valid'] = False
    context = {'form': form,'contact_form':Contact_form}
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

            # print(Contact_form.errors)
            data['form_is_valid'] = False
    context = {'form':Contact_form}
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



