from django.shortcuts import render

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



def create_client(request):
    data = dict()

    if request.method == 'POST':
        form = ClientForm(request.POST)
        if form.is_valid():
            form.save()
            data['form_is_valid'] = True
            books = Client_Data.objects.all()
            data['html_book_list'] = render_to_string('Client_Section/partial_client_c.html', {
                'client': books
            })
        else:
            data['form_is_valid'] = False
    else:
        form = ClientForm()

    context = {'form': form}
    data['html_form'] = render_to_string('Client_Section/partial_client.html',
                                         context,
                                         request=request
                                         )
    return JsonResponse(data)