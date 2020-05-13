from django.shortcuts import render

# Create your views here.
from decimal import Decimal
from django.conf import settings
from decimal import *
from django.shortcuts import render,get_object_or_404,HttpResponse,HttpResponseRedirect
from formtools.wizard.views import SessionWizardView
from .models import Association,Article,Achats,Payements
from django.shortcuts import redirect,reverse
from django.forms import formset_factory
from django.forms import modelformset_factory,formset_factory
from django.http import JsonResponse
from django.forms import formset_factory
from .forms import AchatForm,ArticleForm,AssociationForm,AssociationForm2,Payments_Form,AchatForm2,Payments_Form2
from django.template.loader import render_to_string
from django.views.generic import View
import os
from .utils import render_to_pdf
from django.template.loader import get_template
from Fournis_Section.models import Fournis_Data
from Charge.models import Charge


class GeneratePDF(View):
    def get(self, request, *args, **kwargs):
        template = get_template('proformas/pdf.html')
        context = {
            "invoice_id": 123,
            "customer_name": "John Cooper",
            "amount": 1399.99,
            "today": "Today",
        }
        html = template.render(context)
        pdf = render_to_pdf('proformas/pdf.html', context)
        if pdf:
            response = HttpResponse(pdf, content_type='application/pdf')
            filename = "Invoice_%s.pdf" %("12341231")
            content = "inline; filename='%s'" %(filename)
            download = request.GET.get("download")
            if download:
                content = "attachment; filename='%s'" %(filename)
            response['Content-Disposition'] = content
            return response
        return HttpResponse("Not found")



def payement(request):
    payement = Payements.objects.all()


    pay_dep = Payements.objects.filter(E_S="Dépence")
    pay_vente = Payements.objects.filter(E_S="Vente")
    total = 0
    total_d = 0
    for x in pay_dep:
        total_d = total + x.Montant_HT
    print(total_d)
    total_v =0
    for x in pay_vente:
        total_v = total + x.Montant_HT
    print(total_v)

    diff = total_v - total_d
    context = {'p': payement,'total_d':total_d,'total_v':total_v,'diff':diff}
    return render(request, 'Gestion_Achats/payement/payement_table.html', context)

def payement_charge_delete(request, pk):
    payement = get_object_or_404(Payements, pk=pk)
    data = dict()
    if request.method == 'POST':
        achh = Achats.objects.filter(id=payement.reference).update(Montant_pay=total)
        payement.delete()
        data['form_is_valid'] = True  # This is just to play along with the existing code
        books = Payements.objects.all()
        data['html_book_list'] = render_to_string('Gestion_Achats/payement/partial/partial_payement.html', {
            'payement': payement
        })
    else:
        context = {'obj': payement}
        data['html_form'] = render_to_string('Gestion_Achats/payement/partial/partial_payement_delete.html',
            context,
            request=request,
        )
    return JsonResponse(data)

def payement_delete(request, pk):
    payement = get_object_or_404(Payements, pk=pk)

    if Achats.objects.filter(id=payement.reference):
        achat = get_object_or_404(Achats, pk=payement.reference)
        total =  achat.Montant_pay - payement.Montant_TTC
    data = dict()
    if request.method == 'POST':
        if Achats.objects.filter(id=payement.reference):
         achh = Achats.objects.filter(id=payement.reference).update(Montant_pay=total)

        payement.delete()
        data['form_is_valid'] = True  # This is just to play along with the existing code
        payement = Payements.objects.all()
        data['html_book_list'] = render_to_string('Gestion_Achats/payement/partial/partial_payement.html', {
            'p': payement
        })
    else:
        context = {'obj': payement}
        data['html_form'] = render_to_string('Gestion_Achats/payement/partial/partial_payement_delete.html',
            context,
            request=request,
        )
    return JsonResponse(data)

def save_payements_form(request, form, payement_ttc, id, template_name):
    data = dict()
    if request.method == 'POST':
        if form.is_valid():
            print(id)
            if Achats.objects.filter(id=id):
                achat = get_object_or_404(Achats, pk=id)

                hsab = achat.Montant_pay
                total = hsab -payement_ttc
                ttc_form = form.data['Montant_TTC']
                s = float(total) + float(ttc_form)
                achh = Achats.objects.filter(id=id).update(Montant_pay=s)
                form.save()
            form.save()

            data['form_is_valid'] = True
            payement = Payements.objects.all()
            data['html_book_list'] = render_to_string('Gestion_Achats/payement/partial/partial_partial.html', {
                'payement': payement
            })
        else:
            print(form.errors)
            data['form_is_valid'] = False
    context = {'form': form}
    data['html_form'] = render_to_string(template_name, context, request=request)
    return JsonResponse(data)


def update_payement(request, pk):
    payement = get_object_or_404(Payements, pk=pk)
    payement_ttc = payement.Montant_TTC
    id = payement.reference
    print(id)
    # print(payement_ttc)
    if request.method == 'POST':
        form = Payments_Form2(request.POST,instance=payement)

    else:
        form = Payments_Form2(instance=payement)
    return save_payements_form(request, form, payement_ttc,id, 'Gestion_Achats/payement/payement.html')













def payement_create(request,pk):
    achat = get_object_or_404(Achats,pk=pk)
    # payemnt = Payements.objects.all().values_list('files_id', flat=True)

    if request.method == 'POST':
        form = Payments_Form(request.POST or None,charge=pk)

        Montant_pay = achat.Montant_pay
        # print(Montant_pay)
        montant_ttc = float(form.data['Montant_TTC'])
        Montant_HT = float(form.data['Montant_HT'])
        Montant_pay_aprés = float(Montant_pay) + montant_ttc
        # print(Montant_pay_aprés)
        total = Montant_HT - montant_ttc
        if total < 0:
            error =  "le montant_ttc est superieur que le montant paye "
            return render(request, 'Gestion_Achats/payement/partial_payement_form.html', {'form': form,'errors':error})



        elif(Montant_pay_aprés > Montant_HT):
            error =  "le montant_ttc est superieur que le montant paye 2 "
            return render(request, 'Gestion_Achats/payement/partial_payement_form.html', {'form': form,'errors':error})


        if form.is_valid():
            pay  = form.cleaned_data['Montant_TTC'] + Montant_pay
            print(pay)
            # field_object = Achats._meta.get_field(Montant_pay)
            # print(field_object)
            achh = Achats.objects.filter(id=pk).update(Montant_pay=pay)
            form.save()
            return redirect('view')
        print(form.errors)
    else:

        form = Payments_Form(achat_id=pk)
    return render(request, 'Gestion_Achats/payement/partial_payement_form.html',{'form':form})



def update(request,pk):
    achat = get_object_or_404(Achats, pk=pk)
    # ass = Association.objects.filter(Id_Achats=achat)
    form = modelformset_factory(Association, form=AssociationForm, extra=5,can_delete=True)

    if request.method == 'POST':
       formset = form(request.POST or None)


       if formset.is_valid():
           ht = achat.Montant_HT
           # print(ht)
           error = "la somme des prix est superieur que le montant ht"
           sum = 0
           for x in formset:
               data = x.cleaned_data
               # print(x.Prix_Unitaire)
               # print(data)
               # print(data.get('Prix_Unitaire'))
               # print(data.get('Quantite'))
               if data.get('Prix_Unitaire')  is not None and data.get('Quantite') is not None:
                sum =  sum + (data.get('Prix_Unitaire') * data.get('Quantite'))
                print(data.get('Prix_Unitaire'))
                print(data.get('Quantite'))
           print(sum)

           if (sum > Decimal(ht)):
               print(sum)
               print(' form zawjda !')
               return render(request, 'html_update.html', {'formset': formset, 'errors': error})
           formset.save()
           return redirect('view')
       else:
           # formset._non_form_errors = "Date Exist !"
           print(formset.errors)


    else:
        form = modelformset_factory(Association, form=AssociationForm, extra=5, can_delete=True)
        formset = form(queryset=Association.objects.filter(Id_Achats=achat.id))


    return render(request, 'html_update.html', {'formset': formset})



def step1_ach(request):
    if request.method == 'POST':
      form = AchatForm(request.POST or None)
      if form.is_valid():
             form.save()
             print(form.cleaned_data)
             print(form.cleaned_data.get('Montant_HT'))
             return redirect('step2_ach')
      print(form.errors)
    else:

         form = AchatForm()
    return render(request, 'step1.html', {'form': form,'error':form.errors})


def step2_ach(request):
    if request.method == 'POST':
        nadjib = modelformset_factory(Association, form=AssociationForm2, extra=5,can_delete=True)
        form = nadjib(request.POST)
        # ha = form.cleaned_data
        # id = ha['Id_Achats']
        # ach = get_object_or_404(Achats, pk=id)
        # n = 0
        # for b in form:
        #     a = float(b.data['Prix_Unitaire'])
        #     c = float(b.data['Quantite'])
        #     n = n + (a * c)
        # print(n)
        # if n > ach.Montant_HT:
        #     error = "le montant_ttc est superieur que le montant paye 2 "
        #     return render(request, 'step2.html', {'form': form, 'error': form.errors})

        if form.is_valid():
            form.save()

            return redirect('view')
        else:
            print(form.errors)
            return render(request, 'step2.html', {'formset': form, 'error': form.errors})

    else:
     form = modelformset_factory(Association, form=AssociationForm2, extra=5)
     formset = form(queryset=Association.objects.none())
    # form.fields['Id_Achats'].queryset = Achats.objects.latest('id')
    return render(request, 'step2.html', {'formset': formset,'error':form.errors})


class ContactWizard(SessionWizardView):
    template_name = 'step1.html'
    def get_form(self, step=None, data=None, files=None):

        form = super(ContactWizard, self).get_form(step, data, files)
        # print self['forms']['0'].cleaned_data

        step = step or self.steps.current


        if step == '1':
            form.fields['Id_Achats'].initial = Achats.objects.latest('id')

        return form


    def done(self, form_list, **kwargs):

        for form in form_list:
            print(form.cleaned_data)
            form.save()
        return redirect('nadjib')


def view(request):
    achat = Achats.objects.all()


    name = Achats.objects.all().select_related()
    print(name)


    achat_articl = Achats.objects.all()
    form = modelformset_factory(Association, form=AssociationForm, extra=5,can_delete=True)
    if request.method == 'POST':
        formset = form(request.POST or None)

        print('post')
        print(formset.is_bound)
        print(formset.is_valid)
        print(formset.errors)
        if formset.is_valid():
            print('valide')
            formset.save()
            print(formset.cleaned_data)
            return redirect('view')
    else:
        formset = form(queryset=Association.objects.all())
        print(formset.errors)

    return render(request, 'html.html', {'Achats': achat, 'formset': formset,'as':achat_articl})


def find(request,pk):
    achat = get_object_or_404(Achats, pk=pk)


    return render(request,'html.html',{'achat':achat})

def Article_table(request):
    article = Article.objects.all()
    return render(request,'Gestion_Achats/article/client.html',{'article':article})




def Achats_table(request):
    Achat = Achats.objects.all()
    return render(request,'Gestion_Achats/Achats/client.html',{'Achats':Achat})



def save_Artcile_form(request, form, template_name):
    data = dict()

    if request.method == 'POST':
        if form.is_valid():

            form.save()


            data['form_is_valid'] = True
            articl = Article.objects.all()
            data['html_book_list'] = render_to_string('Gestion_Achats/article/partial_client_c.html', {
                'article': articl
            })
        else:
            print(form.errors)
            data['form_is_valid'] = False
    context = {'form': form}
    data['html_form'] = render_to_string(template_name, context, request=request)
    return JsonResponse(data)




def save_Achats_form(request, form, template_name):
    data = dict()
    if request.method == 'POST':
        if form.is_valid():

            form.save()


            data['form_is_valid'] = True
            achats = Achats.objects.all()
            data['html_book_list'] = render_to_string('Gestion_Achats/Achats/partial_client_c.html', {
                'Achats': achats
            })
        else:
            print(form.errors)
            data['form_is_valid'] = False
    context = {'form': form}
    data['html_form'] = render_to_string(template_name, context, request=request)
    return JsonResponse(data)


def save_Achats_form2(request, form, template_name):
    data = dict()
    if request.method == 'POST':
        if form.is_valid():

            form.save()


            data['form_is_valid'] = True
            achats = Achats.objects.all()
            data['html_book_list'] = render_to_string('Gestion_Achats/Achats/partial_client_c.html', {
                'Achats': achats
            })
        else:
            print(form.errors)
            data['form_is_valid'] = False
    context = {'form': form}
    data['html_form'] = render_to_string(template_name, context, request=request)
    return JsonResponse(data)

def save_article_form_update(request, form, template_name):
    data = dict()
    if request.method == 'POST':
        print(request.method=='POST')
        if form.is_valid():

            form.save()

            data['form_is_valid'] = True
            article = Article.objects.all()
            data['html_book_list'] = render_to_string('Gestion_Achats/article/partial_client_c.html', {
                'article': article
            })
        else:
            print(form.errors)

            data['form_is_valid'] = False
    context = {'form': form}
    data['html_form'] = render_to_string(template_name, context, request=request)
    return JsonResponse(data)


def save_achats_form_update(request, form, template_name):
    data = dict()
    if request.method == 'POST':
        print(request.method=='POST')
        if form.is_valid():

            form.save()

            data['form_is_valid'] = True
            Achat = Achats.objects.all()
            data['html_book_list'] = render_to_string('Gestion_Achats/Achats/partial_client_c.html', {
                'Achats': Achat
            })
        else:
            print(form.errors)

            data['form_is_valid'] = False
    context = {'form': form}
    data['html_form'] = render_to_string(template_name, context, request=request)
    return JsonResponse(data)




def save_achats_form_update_view(request, form, template_name):
    data = dict()
    if request.method == 'POST':
        print(request.method=='POST')
        if form.is_valid():

            form.save()

            data['form_is_valid'] = True
            Achat = Achats.objects.all()
            data['html_book_list'] = render_to_string('Gestion_Achats/Achats/partial_client_c_2.html', {
                'as': Achat
            })
        else:
            print(form.errors)

            data['form_is_valid'] = False
    context = {'form': form}
    data['html_form'] = render_to_string(template_name, context, request=request)
    return JsonResponse(data)


def article_create(request):
    if request.method == 'POST':
        form = ArticleForm(request.POST)

    else:
        form = ArticleForm()
    return save_Artcile_form(request, form, 'Gestion_Achats/article/partial_client.html')


def Achats_create2(request):
    if request.method == 'POST':
        form = AchatForm(request.POST)

    else:
        form = AchatForm()
    return save_Achats_form2(request, form, 'Gestion_Achats/Achats/partial_client2.html')



def Achats_create(request):
    if request.method == 'POST':
        form = AchatForm(request.POST)

    else:
        form = AchatForm()
    return save_Achats_form(request, form, 'Gestion_Achats/Achats/partial_client.html')





def Article_update(request,pk):
    article = get_object_or_404(Article, pk=pk)
    if request.method == 'POST':
        print(request.POST)
        form = ArticleForm(request.POST, instance=article)

    else:
        form = ArticleForm(instance=article)


    return save_article_form_update(request, form,'Gestion_Achats/article/partial_client_update_update.html')



def achat_view_update(request,pk):
    achats = get_object_or_404(Achats, pk=pk)
    if request.method == 'POST':
        print(request.POST)
        form = AchatForm(request.POST, instance=achats)

    else:
        form = AchatForm(instance=achats)

    return save_achats_form_update_view(request, form, 'Gestion_Achats/Achats/partial_client_update_update_view.html')


def Achats_update(request,pk):
    achats = get_object_or_404(Achats, pk=pk)
    if request.method == 'POST':
        print(request.POST)
        form = AchatForm(request.POST, instance=achats)

    else:
        form = AchatForm(instance=achats)


    return save_achats_form_update(request, form,'Gestion_Achats/Achats/partial_client_update_update.html')







def Article_delete(request, pk):
    book = get_object_or_404(Article, pk=pk)
    data = dict()
    if request.method == 'POST':
        book.delete()
        data['form_is_valid'] = True  # This is just to play along with the existing code
        article = Article.objects.all()
        data['html_book_list'] = render_to_string('Gestion_Achats/article/partial_client_c.html', {
            'article': article
        })
    else:
        context = {'obj': book}
        data['html_form'] = render_to_string('Gestion_Achats/article/partial_client_delete.html',
            context,
            request=request,
        )
    return JsonResponse(data)





def Achats_delete(request, pk):
    book = get_object_or_404(Achats, pk=pk)
    data = dict()
    if request.method == 'POST':
        book.delete()
        data['form_is_valid'] = True  # This is just to play along with the existing code
        achats = Achats.objects.all()
        data['html_book_list'] = render_to_string('Gestion_Achats/Achats/partial_client_c_2.html', {
            'as': achats
        })
    else:
        context = {'obj': book}
        data['html_form'] = render_to_string('Gestion_Achats/Achats/partial_client_delete.html',
            context,
            request=request,
        )
    return JsonResponse(data)

# for f in form:
#     data = f.cleaned_data
#     montant = data.get('Prix_Unitaire')
#     quan = data.get('Quantite')
#     TOTAL = montant *quan








