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
            cais = Caisse()
            cais.ES = "Alimentation"
            cais.Date = form.cleaned_data['Date']
            cais.Montant = form.cleaned_data['Montant_TTC']
            cais.Nature = "Alimentation"
            cais.save()
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

def alim_caisse(request):
    if request.method == 'POST':
        form = TransactionForm(request.POST)
    else:
        form = TransactionForm()

    return alim(request, form, 'caisse/partial/partial_alimentation.html')


def caisse_view(request):
    cai = Caisse.objects.all()

    pay_char = Caisse.objects.filter(ES="Charge")
    print(pay_char)
    pay_v = Caisse.objects.filter(ES="Vente")
    print(pay_v)
    # pay_vente = Caisse.objects.filter(ES="Dépence")
    pay_entree= Caisse.objects.filter(ES="Alimentation")
    print(pay_entree)

    total_v = 0
    for x in pay_v:
        total_v = total_v + x.Montant

    print(total_v)

    total_c = 0
    for x in pay_char:
        total_c = total_c + x.Montant
    print(total_c)

    total_e = 0
    for x in pay_entree:
        total_e = total_e + x.Montant
    print(total_e)

    return render(request,'caisse/caisse.html',{'caisse':cai,'entree':total_e+total_v,'sortie':total_c,'dif':total_v+total_e-total_c})


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
