from django.shortcuts import render
from django.shortcuts import render,get_object_or_404,HttpResponse,redirect
from .forms import TransactionForm
from .models import Transactionb
from django.http import JsonResponse
from Gestion_Achats.models import Payements
from django.template.loader import render_to_string
from .forms import Valid

# Create your views here.


def trans_validation(request,pk):
    data = dict()
    Trans = get_object_or_404(Transactionb,id=pk)
    print(Trans)
    if request.method == 'POST':
       form = Valid(request.POST)
       if form.is_valid():
          trans = Transactionb.objects.filter(reference=Trans.reference).update(
             Date_transaction=form.data['Date'],validation=form.data['Validation'])
          data['form_is_valid'] = True
          transb = Transactionb.objects.all()
          data['html_book_list'] = render_to_string('Transactionb/partial/partial_view.html', {
                't': transb
            })

    else:
            form = Valid()
            print(form.errors)
            data['form_is_valid'] = False
            context = {'n': Trans.id,'form':form}
            data['html_form'] = render_to_string('Transactionb/partial/partial_valid.html', context, request=request)
    return JsonResponse(data)


def Transaction_View(request):
    trans = Transactionb.objects.all()
    trans_charge_nv = Transactionb.objects.filter(E_S="Charge",validation__isnull=True)
    trans_charge_nvr = Transactionb.objects.filter(E_S="Charge",validation="rejeté")
    trans_charge_v = Transactionb.objects.filter(E_S="Charge",validation="validé")

    trans_dep_v = Transactionb.objects.filter(E_S="Dépence",validation="validé")
    trans_dep_nv = Transactionb.objects.filter(E_S="Dépence",validation__isnull=True)
    trans_dep_nvr = Transactionb.objects.filter(E_S="Dépence",validation="rejeté")

    trans_vent_v = Transactionb.objects.filter(E_S="Vente",validation="validé")
    trans_vent_nv = Transactionb.objects.filter(E_S="Vente",validation__isnull=True)
    trans_vent_nvr = Transactionb.objects.filter(E_S="Vente",validation="rejeté")

    mt_vent_v = 0
    for x in trans_vent_v:
        mt_vent_v = float(mt_vent_v) + float(x.Montant_HT)

    mt_vent_nv=0
    for x in trans_vent_nv:
        mt_vent_nv = float(mt_vent_nv) + float(x.Montant_HT)

    mt_vent_nvr=0
    for x in trans_vent_nvr:
        mt_vent_nvr = float(mt_vent_nvr) + float(x.Montant_HT)

    mt_dep_v = 0
    for x in trans_dep_v:
        mt_dep_v = float(mt_dep_v) + float(x.Montant_HT)

    mt_dep_nv = 0
    for x in trans_dep_nv:
        mt_dep_nv = float(mt_dep_nv) + float(x.Montant_HT)
    mt_dep_nvr = 0
    for x in trans_dep_nvr:
        mt_dep_nvr = float(mt_dep_nvr) + float(x.Montant_HT)

    mt_charge_nv = 0
    for x in trans_charge_nv:
           mt_charge_nv = float(mt_charge_nv) + float(x.Montant_HT)
    print(mt_charge_nv)

    mt_charge_nvr = 0
    for x in trans_charge_nvr:
           mt_charge_nvr = float(mt_charge_nvr) + float(x.Montant_HT)


    mt_charge_v = 0
    for x in trans_charge_v:
        mt_charge_v = float(mt_charge_v) + float(x.Montant_HT)
    print(mt_charge_v)

    montant_sortie_v = mt_charge_v + mt_dep_v
    montant_sortie_nv = mt_charge_nv + mt_dep_nv + mt_charge_nvr +  mt_dep_nvr
    context = {'t':trans,'mt_vent_v':mt_vent_v,'mt_vent_nv':mt_vent_nv,'mt_dep_v':mt_dep_v,'mt_dep_nv':mt_dep_nv,
               'mt_charge_nv':mt_charge_nv,'mt_charge_v':mt_charge_v,'montant_sortie_v':montant_sortie_v,'montant_sortie_nv':montant_sortie_nv}
    return render(request,'Transactionb/transaction_view.html',context)




def save_trans_form_create(request, form, template_name):
    data = dict()
    if request.method == 'POST':
        print(request.method=='POST')
        if form.is_valid():

            form.save()

            data['form_is_valid'] = True
            transb = Transactionb.objects.all()
            data['html_book_list'] = render_to_string('Transactionb/partial/partial_view.html', {
                't': transb
            })
        else:
            print(form.errors)

            data['form_is_valid'] = False
    context = {'form': form}
    data['html_form'] = render_to_string(template_name, context, request=request)
    return JsonResponse(data)

def trans_create(request):
    if request.method == 'POST':
        form = TransactionForm(request.POST)
    else:
        form = TransactionForm()

    return save_trans_form_create(request, form, 'Transactionb/partial/partial_create.html')


def save_trans_form_update(request, form, template_name):
    data = dict()
    if request.method == 'POST':
        print(request.method=='POST')
        if form.is_valid():

            form.save()

            data['form_is_valid'] = True
            transb = Transactionb.objects.all()
            data['html_book_list'] = render_to_string('Transactionb/partial/partial_view.html', {
                't': transb
            })
        else:
            print(form.errors)

            data['form_is_valid'] = False
    context = {'form': form}
    data['html_form'] = render_to_string(template_name, context, request=request)
    return JsonResponse(data)



def trans_update(request,pk):
    trans = get_object_or_404(Transactionb,pk=pk)
    if request.method == 'POST':
        form = TransactionForm(request.POST,instance=trans)
    else:
        form = TransactionForm(instance=trans)

    return save_trans_form_update(request, form, 'Transactionb/partial/partial_update_t.html')


def trans_delete(request, pk):
    trans = get_object_or_404(Transactionb, pk=pk)

    data = dict()
    if request.method == 'POST':
        trans.delete()


        data['form_is_valid'] = True  # This is just to play along with the existing code
        trans = Transactionb.objects.all()
        data['html_book_list'] = render_to_string('Transactionb/partial/partial_view.html', {
            't': trans
        })
    else:
        context = {'obj': trans}
        data['html_form'] = render_to_string('Transactionb/partial/partial_delete.html',
            context,
            request=request,
        )
    return JsonResponse(data)
