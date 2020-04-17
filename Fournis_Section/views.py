from django.shortcuts import render,get_object_or_404,HttpResponse

from .models import Fournis_Data,Fournis_Contact
from django.forms import modelformset_factory
# from .forms import ClientForm,Contact_Form
from django.http import JsonResponse
from .forms import FournisForm,Contact_Fournis_Form
from urllib.parse import parse_qs
import json
from django.contrib import messages
from django.template.loader import render_to_string
# Create your views here.


def home(request):
    return render(request,'Fournis_Section/home_client.html',{'client':client})


def client(request):
    client = Fournis_Data.objects.all()
    return render(request,'Fournis_Section/client.html',{'client':client})

def contact_Fournis(request):
    contact = Fournis_Contact.objects.all()
    return render(request,'Fournis_Contact/contact.html',{'contact':contact})



def see(request,slug):
    data = dict()
    print(request.POST)
    ProductFormSet = modelformset_factory(Fournis_Contact, fields=('Nom','post','Tel','email','contact_type','Fournis'), extra=0)
    client = get_object_or_404(Fournis_Data, slug=slug)

    attig = request.POST or None
    formset = ProductFormSet(data=attig, queryset=Fournis_Contact.objects.filter(Fournis=client))

    for form in formset:
        form.fields['Fournis'].queryset = Fournis_Contact.objects.filter(Fournis=client.id)

    if request.method == 'POST':
        print('hello')
        print(formset.is_bound)
        if formset.is_valid():
          formset.save()






    context = {'form': formset}
    template_name = 'Fournis_Section/partial_client_contact.html'
    data['html_form'] = render_to_string(template_name, context, request=request)
    return JsonResponse(data)
    # return render(request,template_name,context)



def save_client_form(request, form,Fournis_Contact_form, template_name):
    data = dict()
    if request.method == 'POST':
        if form.is_valid() and Fournis_Contact_form.is_valid():
            client = form.save()
            contact = Fournis_Contact_form.save(commit=False)
            contact.Fournis = client
            contact.save()
            form.save()
            Fournis_Contact_form.save()

            data['form_is_valid'] = True
            books = Fournis_Data.objects.all()
            data['html_book_list'] = render_to_string('Fournis_Section/partial_client_c.html', {
                'client': books
            })
        else:
            print(form.errors)
            print(Fournis_Contact_form.errors)
            data['form_is_valid'] = False
    context = {'form': form,'contact_form':Fournis_Contact_form}
    data['html_form'] = render_to_string(template_name, context, request=request)
    return JsonResponse(data)

def save_contact_form(request,Fournis_Contact_form, template_name):
    data = dict()
    if request.method == 'POST':
        if  Fournis_Contact_form.is_valid():

            Fournis_Contact_form.save()

            data['form_is_valid'] = True
            books = Fournis_Contact.objects.all()
            data['html_book_list'] = render_to_string('contact/contact_list.html', {
                'contact': books
            })
        else:

            print(Fournis_Contact_form.errors)
            data['form_is_valid'] = False
    context = {'form':Fournis_Contact_form}
    data['html_form'] = render_to_string(template_name, context, request=request)
    return JsonResponse(data)


def save_client_form_update(request, form, template_name):
    data = dict()
    if request.method == 'POST':
        print(request.method=='POST')
        if form.is_valid():

            form.save()

            data['form_is_valid'] = True
            books = Fournis_Data.objects.all()
            data['html_book_list'] = render_to_string('Fournis_Section/partial_client_c.html', {
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
            books = Fournis_Data.objects.all()
            data['html_book_list'] = render_to_string('Fournis_Section/partial_client_c.html', {
                'client': books
            })
        else:
            print(form.errors)

            data['form_is_valid'] = False
    context = {'form': form}
    data['html_form'] = render_to_string(template_name, context, request=request)
    return JsonResponse(data)



def F_create_contact(request):
    if request.method == 'POST':
        contact_form = Contact_Fournis_Form(request.POST)
    else:
        contact_form = Contact_Fournis_Form()
    return save_contact_form(request,contact_form, 'Fournis_Contact/partial_contact/partial_contact.html')



def client_create(request):
    if request.method == 'POST':
        form = FournisForm(request.POST)
        contact_form = Contact_Fournis_Form(request.POST)
    else:
        form = FournisForm()
        contact_form = Contact_Fournis_Form()
    return save_client_form(request, form,contact_form, 'Fournis_Section/partial_client.html')



def contact_update(request,pk):
    contact = get_object_or_404(Fournis_Contact, pk=pk)
    print(contact)
    if request.method == 'POST':
        print(request.POST)
        form = Contact_Fournis_Form(request.POST, instance=contact)

    else:
        form = Contact_Fournis_Form(instance=contact)


    return save_contact_form(request, form,'Fournis_Contact/partial_contact/partial_contact_update.html')



def client_update(request,slug):
    client = get_object_or_404(Fournis_Data, slug=slug)
    if request.method == 'POST':
        print(request.POST)
        form = FournisForm(request.POST, instance=client)

    else:
        form = FournisForm(instance=client)


    return save_client_form_update(request, form,'Fournis_Section/partial_client_update_update.html')



def contact_delete(request, pk):
    contact = get_object_or_404(Fournis_Contact, pk=pk)
    data = dict()
    if request.method == 'POST':
        contact.delete()
        data['form_is_valid'] = True  # This is just to play along with the existing code
        books = Fournis_Contact.objects.all()
        data['html_book_list'] = render_to_string('Fournis_Contact/contact_list.html', {
            'contact': books
        })
    else:
        context = {'obj': contact}
        data['html_form'] = render_to_string('Fournis_Contact/partial_contact/partial_contact_delete.html',
            context,
            request=request,
        )
    return JsonResponse(data)





def client_delete(request, slug):
    book = get_object_or_404(Fournis_Data, slug=slug)
    data = dict()
    if request.method == 'POST':
        book.delete()
        data['form_is_valid'] = True  # This is just to play along with the existing code
        books = Fournis_Data.objects.all()
        data['html_book_list'] = render_to_string('Fournis_Section/partial_client_c.html', {
            'client': books
        })
    else:
        context = {'obj': book}
        data['html_form'] = render_to_string('Fournis_Section/partial_client_delete.html',
            context,
            request=request,
        )
    return JsonResponse(data)









