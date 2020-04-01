from django.shortcuts import render,get_object_or_404

from .models import Client_Data
from .forms import ClientForm
from django.http import JsonResponse
from django.template.loader import render_to_string
# Create your views here.


def home(request):
    return render(request,'Client_Section/home_client.html',{'client':client})


def client(request):
    client = Client_Data.objects.all()
    return render(request,'Client_Section/client.html',{'client':client})



def save_client_form(request, form, template_name):
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
            data['form_is_valid'] = False
    context = {'form': form}
    data['html_form'] = render_to_string(template_name, context, request=request)
    return JsonResponse(data)




def client_create(request):
    if request.method == 'POST':
        form = ClientForm(request.POST)
    else:
        form = ClientForm()
    return save_client_form(request, form, 'Client_Section/partial_client.html')


def client_update(request, slug):
    book = get_object_or_404(Client_Data, slug=slug)
    print(book.slug)
    if request.method == 'POST':
        form = ClientForm(request.POST, instance=book)
    else:
        form = ClientForm(instance=book)
    return save_client_form(request, form, 'Client_Section/partial_client_update.html')







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



