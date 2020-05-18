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
    return render(request,'Transactionb/transaction_view.html',{'t':trans})




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
