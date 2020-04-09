from django.shortcuts import render,get_object_or_404,HttpResponse

from .models import Client_Data,Contact
from django.forms import modelformset_factory
from .forms import ClientForm,Contact_Form       
from django.http import JsonResponse
from django.contrib import messages
from django.template.loader import render_to_string
# Create your views here.


def home(request):
    return render(request,'Client_Section/home_client.html',{'client':client})


def client(request):
    client = Client_Data.objects.all()
    return render(request,'Client_Section/client.html',{'client':client})


# def see(request,slug):
#     data = dict()
#     client = get_object_or_404(Client_Data, slug=slug)
#     ProductFormSet = modelformset_factory(Contact, fields = ('Nom','post','Tel','email','contact_type','client'), extra=0)
#     if request.method=='POST':
#
#         form = ClientForm(request.POST,instance=client)
#     else:
#         form = ClientForm(instance=client)
#         datas = request.POST or None
#         formset = ProductFormSet(data=datas, queryset=Contact.objects.filter(client=client.id))
#
#
#     context = {'form': formset}
#     template_name = 'Client_Section/formset.html'
#     data['html_form'] = render_to_string(template_name, context, request=request)
#     return JsonResponse(data)


def see(request,slug):
    data = dict()
    ProductFormSet = modelformset_factory(Contact, fields=('Nom','post','Tel','email','contact_type','client'), extra=0)
    nadjib = request.POST or None
    print(data)
    client = get_object_or_404(Client_Data, slug=slug)
    formset = ProductFormSet(data=nadjib, queryset=Contact.objects.filter(client=client))

    # if request.method=='POST':
    #  form = Contact_Form(request.POST,instance=client)
    # else:

    for form in formset:
            form.fields['client'].queryset = Contact.objects.filter(client=client.id)

    context = {'form': formset}
    template_name = 'Client_Section/partial_client_contact_form.html'
    data['html_form'] = render_to_string(template_name, context, request=request)
    return JsonResponse(data)
    # return render(request,template_name,context)

# def see(request,slug):
#     data = dict()
#     client = get_object_or_404(Client_Data, slug=slug)
#     print(client.id)
#     contact = Contact.objects.get(client__id=client.id)
#     print(contact)
#     form = Contact_Form(instance=contact)
#     context = {'form':form}
#     template_name = 'Client_Section/partial_client_contact.html'
#     data['html_book_list'] = render_to_string('Client_Section/nadjib.html', {
#         'form': contact
#     })
#     data['html_form'] = render_to_string(template_name, context, request=request)
#     return JsonResponse(data)



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



def save_client_form_update(request, form, template_name):
    data = dict()
    if request.method == 'POST':
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




def client_create(request):
    if request.method == 'POST':
        form = ClientForm(request.POST)
        contact_form = Contact_Form(request.POST)
    else:
        form = ClientForm()
        contact_form = Contact_Form()
    return save_client_form(request, form,contact_form, 'Client_Section/partial_client.html')


def client_update(request,slug):
    client = get_object_or_404(Client_Data, slug=slug)
    if request.method == 'POST':
        form = ClientForm(request.POST, instance=client)
        print(form)

    else:
        form = ClientForm(instance=client)
        print(form)

    return save_client_form_update(request, form,'Client_Section/partial_client_update_update.html')







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



