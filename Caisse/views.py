from django.shortcuts import render
from django.shortcuts import render,get_object_or_404,HttpResponse,redirect
from .models import Caisse
from .forms import Caisse_Form,TransactionForm
from django.http import JsonResponse
from django.template.loader import render_to_string
from Transactionb.models import Transactionb



def alim(request, form, template_name):
    data = dict()
    if request.method == 'POST':
        print(request.method=='POST')
        if form.is_valid():

            form.save()

            data['form_is_valid'] = True
        else:
            print(form.errors)

            data['form_is_valid'] = False
    context = {'form': form}
    data['html_form'] = render_to_string(template_name, context, request=request)
    return JsonResponse(data)

def alim_caisse(request):
    if request.method == 'POST':
        form = TransactionForm(request.POST)
    else:
        form = TransactionForm()

    return alim(request, form, 'caisse/partial/partial_alimentation.html')


def caisse_view(request):
    cai = Caisse.objects.all()
    return render(request,'caisse/caisse.html',{'caisse':cai})


def save_caisse_form_create(request, form, template_name):
    data = dict()
    if request.method == 'POST':
        print(request.method=='POST')
        if form.is_valid():

            form.save()

            data['form_is_valid'] = True
            caii = Caisse.objects.all()
            data['html_book_list'] = render_to_string('caisse/partial/partial_caisse.html', {
                'caisse': caii
            })
        else:
            print(form.errors)

            data['form_is_valid'] = False
    context = {'form': form}
    data['html_form'] = render_to_string(template_name, context, request=request)
    return JsonResponse(data)

def caisse_create(request):
    if request.method == 'POST':
        form = Caisse_Form(request.POST)
    else:
        form = Caisse_Form()

    return save_caisse_form_create(request, form, 'caisse/partial/partial_caisse_create.html')




def save_caisse_form_update(request, form, template_name):
    data = dict()
    if request.method == 'POST':
        print(request.method=='POST')
        if form.is_valid():

            form.save()

            data['form_is_valid'] = True
            caii = Caisse.objects.all()
            data['html_book_list'] = render_to_string('caisse/partial/partial_caisse.html', {
                'caisse': caii
            })
        else:
            print(form.errors)

            data['form_is_valid'] = False
    context = {'form': form}
    data['html_form'] = render_to_string(template_name, context, request=request)
    return JsonResponse(data)

def caisse_update(request,pk):
    caisse = get_object_or_404(Caisse,pk=pk)
    if request.method == 'POST':
        form = Caisse_Form(request.POST,instance=caisse)
    else:
        form = Caisse_Form(instance=caisse)

    return save_caisse_form_update(request, form, 'caisse/partial/partial_caisse_update.html')


def caisse_delete(request, pk):
    caisse = get_object_or_404(Caisse, pk=pk)

    data = dict()
    if request.method == 'POST':
        caisse.delete()


        data['form_is_valid'] = True  # This is just to play along with the existing code
        caii = Caisse.objects.all()
        data['html_book_list'] = render_to_string('caisse/partial/partial_caisse.html', {
            'caisse': caii
        })
    else:
        context = {'obj': caisse}
        data['html_form'] = render_to_string('caisse/partial/partial_caisse_delete.html',
            context,
            request=request,
        )
    return JsonResponse(data)
