from django.shortcuts import render,get_object_or_404,HttpResponse,redirect
from .models import Charge
from .forms import ChargeForm
from django.http import JsonResponse
from .forms import Payments_charge_Form
from django.template.loader import render_to_string
from .forms import Payments_charge_Form
# Create your views here.


def Chareg_view(request):
    charge = Charge.objects.all()
    return  render(request,'charge_view.html',{'c':charge})



def save_charge_form_create(request, form, template_name):
    data = dict()
    if request.method == 'POST':
        print(request.method=='POST')
        if form.is_valid():

            form.save()

            data['form_is_valid'] = True
            charge = Charge.objects.all()
            data['html_book_list'] = render_to_string('charge/partial/partial_view_charge.html', {
                'c': charge
            })
        else:
            print(form.errors)

            data['form_is_valid'] = False
    context = {'form': form}
    data['html_form'] = render_to_string(template_name, context, request=request)
    return JsonResponse(data)

def charge_create(request):
    if request.method == 'POST':
        form = ChargeForm(request.POST)
    else:
        form = ChargeForm()

    return save_charge_form_create(request, form, 'charge/partial/partial_create.html')



def save_charge_form_update(request, form, template_name):
    data = dict()
    if request.method == 'POST':
        print(request.method=='POST')
        if form.is_valid():

            form.save()

            data['form_is_valid'] = True
            charge = Charge.objects.all()
            data['html_book_list'] = render_to_string('charge/partial/partial_view_charge.html', {
                'c': charge
            })
        else:
            print(form.errors)

            data['form_is_valid'] = False
    context = {'form': form}
    data['html_form'] = render_to_string(template_name, context, request=request)
    return JsonResponse(data)

def charge_update(request,pk):
    charge = get_object_or_404(Charge,pk=pk)
    if request.method == 'POST':
        form = ChargeForm(request.POST,instance=charge)
    else:
        form = ChargeForm(instance=charge)

    return save_charge_form_update(request, form, 'charge/partial/partial_update.html')


def charge_delete(request, pk):
    book = get_object_or_404(Charge, pk=pk)
    data = dict()
    if request.method == 'POST':
        book.delete()
        data['form_is_valid'] = True  # This is just to play along with the existing code
        charge = Charge.objects.all()
        data['html_book_list'] = render_to_string('charge/partial/partial_view_charge.html', {
            'c': charge
        })
    else:
        context = {'obj': book}
        data['html_form'] = render_to_string('charge/partial/partial_charge_delete.html',
            context,
            request=request,
        )
    return JsonResponse(data)


def payement_charge_create(request,pk):
    charge = get_object_or_404(Charge,pk=pk)
    # payemnt = Payements.objects.all().values_list('files_id', flat=True)

    if request.method == 'POST':
        form = Payments_charge_Form(request.POST or None,charge=pk)

        Montant_pay = charge.Montant
        Montant_HT = float(form.data['Montant_HT'])


        total = float(Montant_HT)  - float(Montant_pay)
        if total < 0:
            error =  "le montant ht est superieur que le montant de la charge "
            return render(request, 'Gestion_Achats/payement/partial_payement_form.html', {'form': form,'errors':error})



        if form.is_valid():
            pay  = form.cleaned_data['Montant_TTC'] + Montant_pay

            form.save()
            return redirect('charge_view')
        print(form.errors)
    else:

        form = Payments_charge_Form(charge=pk)
    return render(request, 'Gestion_Achats/payement/partial_payement_form.html',{'form':form})

