from django.shortcuts import render
from .models import Commande,Commande_Designation,Modalite,Facture
from django.shortcuts import redirect
from django.template.loader import get_template
from .utils import render_to_pdf
from django.shortcuts import render,get_object_or_404,HttpResponse,HttpResponseRedirect
from django.views.generic import View
from django.http import JsonResponse
from Client_Section.models import Client_Data
from decimal import Decimal
from django.urls import reverse
import datetime
import threading
from .forms import Commande_Form,Commande_D_Form,Modalite_Form,validat,Commande_Form2,Facture_Form,Facture_Form2,Commande_Form_step,Commande_D_Form2,Commande_D_Form_p,Commande_Formna
from django.core.files.storage import FileSystemStorage
from django.http import HttpResponse
from django.forms import modelformset_factory,formset_factory
from django.template.loader import render_to_string
from weasyprint import HTML
from django.core.mail import EmailMessage
import weasyprint
from django.template.loader import render_to_string
from weasyprint import HTML
from .forms import Payments_Form_facture
import json
import simplejson
from django.core import serializers


from django.utils.html import strip_tags
# Create your views here.

def update2(request,pk):
        commande = get_object_or_404(Commande, pk=pk)
    
        form = Commande_Form2(instance=commande)
        forms = modelformset_factory(Commande_Designation, form=Commande_D_Form_p, extra=0, can_delete=True)
        formset = forms(queryset=Commande_Designation.objects.filter(Command=commande.id),form_kwargs={'com':commande})

        return render(request,'Proformas/steps/testupdate2.html',{'form':form,'formset':formset})


def update2post(request,pk):
    
    data = dict()
    if request.method == 'POST' and request.is_ajax:
        
        commande = get_object_or_404(Commande, id=pk)
      
        form = Commande_Formna(request.POST,instance=commande)
        if form.is_valid():
         form.save()

        else:
            print(form.errors)
          
            data['errors'] = form.errors
    return JsonResponse(data)


def update1(request,pk):
    print('update 1')
    data_dict = dict()
    satas = dict()
    commande = get_object_or_404(Commande, id=pk)
    forms = modelformset_factory(Commande_Designation, form=Commande_D_Form2, extra=0,can_delete=True)
    formset = forms(request.POST or None,form_kwargs={'com':commande})
    if request.method == 'POST' and request.is_ajax:
       if formset.is_valid():
           ht = commande.Montant_HT
           error = "la somme des prix doit etre égale au montant ht de la commande !" + ' Montant HT:'  + ' ' + str(ht)
           sum = 0
           for x in formset:
               data = x.cleaned_data

               if data.get('Prix_Unitaire')  is not None and data.get('Quantite') is not None:
                sum =  sum + (float(Decimal(data.get('Prix_Unitaire'))) * float(Decimal(data.get('Quantite'))))
           
           print(sum)
           if (sum != Decimal(ht)):
               print('makach kifeh')
               data['errors'] = "kbir alih ! 7"
               print('errors')
               return JsonResponse(data)
           else:
                
                formset.save()
        
                html = render_to_string(
                template_name='Proformas/steps/partial_step.html',
                context={"formset": formset}
                )
                print('update')
                data_dict = {"html_from_view": html}
                return JsonResponse(data_dict)
       else:
            print(formset.errors)
    return JsonResponse(data_dict)
                
      
        
           

def test(request):
    
    nadjib = modelformset_factory(Commande_Designation, form=Commande_D_Form, extra=1, can_delete=True)
    formset = nadjib(queryset=Commande.objects.none())
    if request.method == 'POST' and request.is_ajax:
            print('post test 1')
            
            
            print(request.POST)
            
            
            form_c = Commande_Form_step(request.POST or None)
            if form_c.is_valid():
                print('form valide !')
                form_c.save()
                print('commande saved !')
            else:
                print(form_c.errors.as_text())
                data = dict()
                data['errors'] = form_c.non_field_errors()

                return JsonResponse(data)
   
    form = Commande_Form_step()
    return render(request,'Proformas/steps/test.html',{'form':form,'formset':formset})

    #return render(request,'Proformas/steps/test.html',{'formset':formset,'form':form})



def test2(request):
    print('test2')
    if request.method == 'POST' and request.is_ajax:
        nadjib = modelformset_factory(Commande_Designation, form=Commande_D_Form, extra=1, can_delete=True)
        form = nadjib(request.POST)
        if form.is_valid():
                print("form is valide")
                commandes = Commande.objects.latest('id')
                print(commandes.id)
                print('nadjibo')
                res = 0
                for x in form:
                    data = x.cleaned_data
                    commande = get_object_or_404(Commande,id=commandes.id)
                    print(commande)
                    # print(data.get('Prix_Unitaire'))
                    res = res + (float(Decimal(int(data.get('Prix_Unitaire')))) * float(Decimal(int(data.get('Quantite')))))
                if res != commande.Montant_HT:
                        print('not equal')
                        print('res = ')
                        print(res)
                        er = 'la somme des prix doit etre égale au montant ht de la commande ! ' + ' ' + str(commande.Montant_HT)
                        dat = dict()
                        dat['errors'] = er
                        print(er)
                        return JsonResponse(dat)
                   
                form.save()
                print('before redirect')
                return HttpResponseRedirect(reverse('update2', args=[commande.id]))
                print('after redirect')
        else:
            print(form.errors)
            data = dict()
            data['errors'] = form.errors.as_text()
            return JsonResponse(data)

    return redirect('test')







def update_com_d(request,pk):
    commande = get_object_or_404(Commande, pk=pk)
    print(commande)
    form = modelformset_factory(Commande_Designation, form=Commande_D_Form2, extra=1,can_delete=True)

    if request.method == 'POST':
       formset = form(request.POST or None,form_kwargs={'com':commande})


       if formset.is_valid():
           ht = commande.Montant_HT
           error = "la somme des prix doit etre égale au montant ht de la commande !" + ' Montant HT:'  + ' ' + str(ht)
           sum = 0
           for x in formset:
               data = x.cleaned_data

               if data.get('Prix_Unitaire')  is not None and data.get('Quantite') is not None:
                sum =  sum + (float(Decimal(data.get('Prix_Unitaire'))) * float(Decimal(data.get('Quantite'))))

           print(sum)
           print(Decimal(ht))
           if (sum != Decimal(ht)):
               return render(request, 'html_update.html', {'formset': formset, 'errors': error})
           formset.save()
           return redirect('commande')
       else:
           # formset._non_form_errors = "Date Exist !"
           print(formset.errors)


    else:
        form = modelformset_factory(Commande_Designation, form=Commande_D_Form_p, extra=1, can_delete=True)
        formset = form(queryset=Commande_Designation.objects.filter(Command=commande.id),form_kwargs={'com':commande})


    return render(request, 'Proformas/commande_d_update.html', {'formset': formset})



def is_valid_queryparam(param):
    return param != '' and param is not None


def ajax_live(request):
    ctx = {}
    url_parameter = request.GET.get("q", 'None')
    if url_parameter:
        if Facture.objects.filter(Titre_facture__icontains=url_parameter):
            artists = Facture.objects.filter(Titre_facture__icontains=url_parameter)

        elif Facture.objects.filter(Date__icontains=url_parameter):
            artists = Facture.objects.filter(Date__icontains=url_parameter)
        elif Client_Data.objects.filter(Raison_social__iexact=url_parameter).exists():
                Client_Data.objects.get(Raison_social__iexact=url_parameter)
                # client = get_object_or_404(Client_Data,Raison_social__iexact=url_parameter)
                client = Client_Data.objects.get(Raison_social__iexact=url_parameter)
                artists = Facture.objects.filter(commande__Client=client)
        else:
            artists = ""
    else:
        artists = Facture.objects.all()
        print(artists)

    if request.is_ajax():
        if not artists:
            print('here')
            html = render_to_string(
                template_name="Proformas/facture/ajax_errors.html",
                context={"artists": artists ,'er' :'not found'}
            )

            data_dict = {"html_from_view": html}
            print(data_dict)

            return JsonResponse(data=data_dict, safe=False)

        html = render_to_string(
            template_name="Proformas/facture/ajax.html",
            context={"artists": artists}
        )

        data_dict = {"html_from_view": html}
        print(data_dict)

        return JsonResponse(data=data_dict, safe=False)














def payement_c(request,pk):
    facture = get_object_or_404(Facture,pk=pk)
    # p = Payements.objects.all().values_list('files_id', flat=True)

    if request.method == 'POST':
        form = Payments_Form_facture(request.POST or None,facture=pk)

        if form.is_valid():
            facture = Facture.objects.filter(id=pk).update(Date_payement=form.data['Date'])
            facture = Facture.objects.filter(id=pk).update(Etat=True)
            form.save()
            return redirect('facture')
        print(form.errors)
    else:

        form = Payments_Form_facture(facture=pk)
    return render(request, 'Gestion_Achats/payement/partial_payement_form.html',{'form':form})



def html_to_pdf_view_facture(request, pk):
    id_com = Facture.objects.get(id=pk)
    com = get_object_or_404(Commande, id=id_com.commande.id)

    if Commande_Designation.objects.filter(Command=com):
        design = Commande_Designation.objects.filter(Command=com).values_list('Designation', flat=True)
        prix = Commande_Designation.objects.filter(Command=com).values_list('Prix_Unitaire', flat=True)
        qua = Commande_Designation.objects.filter(Command=com).values_list('Quantite', flat=True)
        # ht = Commande_Designation.objects.filter(Command=com).values_list('Montant_HT', flat=True)
        # tva = Commande_Designation.objects.filter(Command=com).values_list('Montant_TVA', flat=True)
        # ttc = Commande_Designation.objects.filter(Command=com).values_list('Montant_TTC', flat=True)
    else:
        design = ""
        prix = ""
        qua = ""
        ht = ""
        tva = ""
        ttc = ""

    Designation = ''
    for x in design:
        print(x)
        Designation = Designation +  '-' + x +  " ,"

    # Prix_Uni = 0
    # for x in prix:
    #     Prix_Uni = Prix_Uni + x

    # Quantite = 0
    # for x in qua:
    #     Quantite = Quantite + x

    # Montant_HT = 0
    # for x in ht:
    #     Montant_HT = Montant_HT + x
    #
    # Montant_TVA = 0
    # for x in tva:
    #     Montant_TVA = Montant_TVA + x
    #
    # Montant_TTC = 0
    # for x in ttc:
    #     Montant_TTC = Montant_TTC + x

    if Modalite.objects.filter(Command=com.id).exists():
        mod = Modalite.objects.get(Command=com.id)
        modalite_payement = mod.modalite_payement
        print(modalite_payement)
        Arret_Facture = mod.Arret_Facture
        Formation = mod.Formation
        Period_Réalisation = mod.Period_Réalisation
        Echéancier_payement = mod.Echéancier_payement
        Debut_realsiation = mod.Debut_realsiation
        Garantie = mod.Garantie
    else:
        modalite_payement = ''
        print(modalite_payement)
        Arret_Facture = ''
        Formation = ''
        Period_Réalisation = ''
        Echéancier_payement = ''
        Debut_realsiation = ''
        Garantie = ''

    Montant_HT = id_com.Montant_HT
    Montant_TVA = id_com.Montant_TVA
    Montant_TTC = id_com.Montant_TTC


    Numero_com = id_com.Numero_facture
    client = com.Client
    client_data = Client_Data.objects.get(id=client.id)
    adresse = client_data.adresse
    NIF = client_data.NIF
    NIS = client_data.NIS
    AI =  client_data.AI
    raison_social = client_data.Raison_social
    rc = client_data.RC

    context = {
        'Designation': Designation,
        'Prix_Uni': prix,
        'Quantite': qua,
        'Montant_HT': Montant_HT,
        'Montant_TVA': Montant_TVA,
        'Montant_TTC': Montant_TTC,
        'Numero_com': Numero_com,
        'adresse': adresse,
        'NIF': NIF,
        'NIS': NIS,
        'AI':AI,
        'raison_social': raison_social,
        'Date': id_com.Date,
        'modalite_payement': modalite_payement,
        'Arret_Facture': Arret_Facture,
        'Formation': Formation,
        'Echéancier_payement': Echéancier_payement,
        'Period_Réalisation': Period_Réalisation,
        'Debut_realsiation': Debut_realsiation,
        'Garantie': Garantie,
        'rc':rc

    }
    html_string = render_to_string('Proformas/facture_pdf.html', context)

    html = HTML(string=html_string, base_url=request.build_absolute_uri())
    html.write_pdf(target='/tmp/{username}.{filename}'.format(username=raison_social,filename='facture')+ '.pdf');
    html_nadjib = render_to_string('Proformas/msg.html', context)
    fs = FileSystemStorage('/tmp')
    with fs.open('{username}.{filename}'.format(username=raison_social,filename='facture')+ '.pdf') as pdf:
        response = HttpResponse(pdf, content_type='application/pdf')
        response['Content-Disposition'] = 'filename="Facture.pdf"'
    return response


def save_facture_form(request, form, template_name):
    data = dict()
    if request.method == 'POST':
        print(request.method=='POST')
        if form.is_valid():

            form.save()

            data['form_is_valid'] = True
            f = Facture.objects.all()
            data['html_book_list'] = render_to_string('Proformas/facture/partial/partial_facture2.html', {
                'facture': f
            })
        else:
            print(form.errors)

            data['form_is_valid'] = False
    context = {'form': form}
    data['html_form'] = render_to_string(template_name, context, request=request)
    return JsonResponse(data)


def facture_update(request,pk):
    facture = get_object_or_404(Facture, pk=pk)
    if request.method == 'POST':
        print(request.POST)
        form = Facture_Form2(request.POST, instance=facture)

    else:
        form = Facture_Form2(instance=facture)


    return save_facture_form(request, form,'Proformas/facture/partial/partial_facture_model.html')



def facture_delete(request,pk):
    facture = get_object_or_404(Facture, pk=pk)
    print(facture)
    data = dict()
    if request.method == 'POST':
        facture.delete()
        data['form_is_valid'] = True  # This is just to play along with the existing code
        f = Facture.objects.all()
        data['html_book_list'] = render_to_string('Proformas/facture/partial/partial_facture.html', {
            'facture': f
        })
    else:
        context = {'facture': facture,'id':pk}
        data['html_form'] = render_to_string('Proformas/facture/partial/partial_delete.html',
            context,
            request=request,
        )
    return JsonResponse(data)

def facture_view(request):
    factur = Facture.objects.all()

    factur_pay = Facture.objects.filter(Etat=True)
    factur_np = Facture.objects.filter(Etat=False)
    mhtg_p = 0
    mhtg_np = 0
    mhtg = 0
    for x in factur_pay:
        mhtg_p = mhtg_p + x.Montant_HT
    for x in factur_np:
        mhtg_np = mhtg_np + x.Montant_HT
    for x in factur:
        mhtg = mhtg + x.Montant_HT

    print(mhtg_p)
    print(mhtg_np)
    print(mhtg)
    context = {'facture':factur,
               'mhtg_p':mhtg_p,
               'mhtg_np':mhtg_np,
               'mhtg':mhtg}

    return render(request,'Proformas/facture/partial_view.html',context)



def Facture_create(request,pk):
    command = get_object_or_404(Commande,pk=pk)
    # payemnt = Payements.objects.all().values_list('files_id', flat=True)

    if request.method == 'POST':
        form = Facture_Form(request.POST or None,fac=pk)

        ttc = command.Montant_TTC

        if float(form.data['Montant_TTC']) > float(ttc):
            error =  "le montant_ttc est superieur que le montant TTC de la commande "
            return render(request, 'Proformas/facture/facture_form.html', {'form': form,'errors':error})


        if form.is_valid():
            form.save()
            return redirect('commande')
        print(form.errors)
    else:

        form = Facture_Form(fac=pk)
    return render(request, 'Proformas/facture/facture_form.html',{'form':form})




def commande_deletee(request,pk):
        commande = get_object_or_404(Commande, pk=pk)
        data = dict()
        if request.method == 'POST':
            commande.delete()
            data['form_is_valid'] = True  # This is just to play along with the existing code
            com = Commande.objects.all()
            data['html_book_list'] = render_to_string('Proformas/partial/partial_proformas.html', {
                'c': com
            })
        else:
            context = {'obj': commande}
            data['html_form'] = render_to_string('Proformas/partial/parital_delete.html',
                                                 context,
                                                 request=request,
                                                 )
        return JsonResponse(data)


def dat_val(request,pk):
    commande = get_object_or_404(Commande,pk=pk)
    if request.method == 'POST':
      form = Commande_Form2(request.POST, instance=commande)
    else:
        form = Commande_Form2(instance=commande)

    return valid_save(request, form, pk, 'Proformas/partial/partial_valid.html')

def valid_save(request, form,pk, template_name):
        commande = Commande.objects.filter(id=pk)
        data = dict()
        if request.method == 'POST':
            if form.is_valid():
                dat = form.data['Date_validation']
                achh = Commande.objects.filter(id=pk).update(Date_validation=dat, validation=True)
                data['form_is_valid'] = True
                command = Commande.objects.all()
                data['html_book_list'] = render_to_string('Proformas/partial/partial_proformas.html', {
                'c': command
            })
            else:
                print(form.errors)
                data['form_is_valid'] = False
        context = {'form': form}
        data['html_form'] = render_to_string('Proformas/partial/partial_valid.html',context,
                                             request=request,
                                             )
        return JsonResponse(data)


# def dat_val(request,pk):
#     # commande = Commande.objects.filter(id=pk)
#     if request.method == 'POST':
#         form = validat(request.POST)
#         if form.is_valid():
#             dat = form.data['Validate_date']
#             achh = Commande.objects.filter(id=pk).update(Date_validation=dat,validation=True)
#             return redirect('commande')
#
#     else:
#         form = validat()
#     return render(request,'Proformas/valid.html',{'form':form})
#


class EmailThread(threading.Thread):
    def __init__(self, subject, html_content, recipient_list, sender,name):
        self.subject = subject
        self.recipient_list = recipient_list
        self.html_content = html_content
        self.sender = sender
        threading.Thread.__init__(self)
        self.name= name

    def run(self):
        msg = EmailMessage(self.subject, self.html_content, self.sender, self.recipient_list)
        msg.attach_file('/tmp/{username}.{filename}'.format(username=self.name,filename='proformas')+ '.pdf')
        msg.content_subtype = "html"  # Main content is now text/html
        msg.encoding = 'utf-8'
        if(msg.send()):
            print('yes')
            return HttpResponse('SENT')



# def send_mail(request,pk):
#     commande = get_object_or_404(Commande,id=pk)
#     name  = commande.Client.Raison_social
#     html_nadjib = render_to_string('Proformas/msg.html',{'raison_social':name,'Date':datetime.date.today()})
#     to_emails = ['attignadjib@outlook.com']
#     subject = "SH INFOR FACTURE"
#     sender = 'attignadjib@gmail.com'
#     # EmailThread(subject, html_nadjib, to_emails, sender, name).start()
#     if(EmailThread(subject, html_nadjib, to_emails, sender, name).start()):
#      return HttpResponse('SENT')
#     else:
#         return HttpResponse('not sent')


def send_mail(request,pk):
        commande = get_object_or_404(Commande,id=pk)
        name  = commande.Client.Raison_social
        html_nadjib = render_to_string('Proformas/msg.html',{'raison_social':name,'Date':datetime.date.today()})
        to_emails = ['attignadjib@outlook.com']
        subject = "SH INFOR FACTURE"
        sender = 'attignadjib@gmail.com'
        msg = EmailMessage(subject, html_nadjib, sender, to_emails)
        msg.attach_file('/tmp/{username}.{filename}'.format(username=name, filename='proformas') + '.pdf')
        msg.content_subtype = "html"  # Main content is now text/html
        msg.encoding = 'utf-8'
        try:
            msg.send()
            return HttpResponse('sent')
        except Exception as e:
            return HttpResponse('Not sent')



def html_to_pdf_view(request,pk):
        com = get_object_or_404(Commande,pk=pk)
        if Commande_Designation.objects.filter(Command=pk):
            design = Commande_Designation.objects.filter(Command=com).values_list('Designation', flat=True)
            prix = Commande_Designation.objects.filter(Command=com).values_list('Prix_Unitaire', flat=True)
            qua = Commande_Designation.objects.filter(Command=com).values_list('Quantite', flat=True)
            # ht = Commande_Designation.objects.filter(Command=com).values_list('Montant_HT', flat=True)
            # tva = Commande_Designation.objects.filter(Command=com).values_list('Montant_TVA', flat=True)
            # ttc = Commande_Designation.objects.filter(Command=com).values_list('Montant_TTC', flat=True)
        else :
           design = ""
           prix = ""
           qua = ""
           ht = ""
           tva = ""
           ttc = ""

        Designation = ''
        for x in design:

            print(x)
            Designation = Designation +  '-' + x +  " ,"

        # Prix_Uni = 0
        # for x in prix:
        #     Prix_Uni = Prix_Uni + x

        # Quantite = 0
        # for x in qua:
        #     Quantite = Quantite + x

        # Montant_HT= 0
        # for x in ht:
        #     Montant_HT =Montant_HT +x

        # Montant_TVA = 0
        # for x in tva:
        #     Montant_TVA = Montant_TVA +x

        # Montant_TTC = 0
        # for x in ttc:
        #         Montant_TTC = Montant_TTC +x

        Montant_HT = com.Montant_HT
        Montant_TVA = com.Montant_TVA
        Montant_TTC = com.Montant_TTC




        if Modalite.objects.filter(Command=com.id).exists():
            mod = Modalite.objects.get(Command=com.id)
            modalite_payement = mod.modalite_payement
            print(modalite_payement)
            Arret_Facture = mod.Arret_Facture
            Formation = mod.Formation
            Period_Réalisation = mod.Period_Réalisation
            Echéancier_payement = mod.Echéancier_payement
            Debut_realsiation = mod.Debut_realsiation
            Garantie = mod.Garantie
        else:
            modalite_payement  = ''
            print(modalite_payement)
            Arret_Facture = ''
            Formation = ''
            Period_Réalisation = ''
            Echéancier_payement = ''
            Debut_realsiation = ''
            Garantie = ''

        Numero_com  = com.Numero_commande
        datee = com.Date
        client = com.Client
        client_data = Client_Data.objects.get(id=client.id)
        adresse = client_data.adresse
        NIF = client_data.NIF
        NIS = client_data.NIS
        raison_social = client_data.Raison_social


        context = {
        'Designation': Designation,
        'Prix_Uni': prix,
        'Quantite': qua,
        'Montant_HT': Montant_HT,
        'Montant_TVA': Montant_TVA,
        'Montant_TTC': Montant_TTC,
        'Numero_com': Numero_com,
        'adresse': adresse,
        'NIF': NIF,
        'NIS': NIS,
        'raison_social': raison_social,
        'Date': datetime.date.today(),
        'modalite_payement':modalite_payement,
        'Arret_Facture':Arret_Facture,
        'Formation': Formation,
        'Echéancier_payement':Echéancier_payement,
        'Period_Réalisation':Period_Réalisation,
        'Debut_realsiation':Debut_realsiation,
        'Garantie':Garantie,
        'date':datee,

        }
        html_string = render_to_string('Proformas/command.html',context)

        html = HTML(string=html_string,base_url=request.build_absolute_uri())
        html.write_pdf(target='/tmp/{username}.{filename}'.format(username=raison_social,filename='proformas')+ '.pdf');
        html_nadjib = render_to_string('Proformas/msg.html', context)
        fs = FileSystemStorage('/tmp')
        with fs.open('{username}.{filename}'.format(username=raison_social,filename='proformas')+ '.pdf') as pdf:
            response = HttpResponse(pdf, content_type='application/pdf')
            response['Content-Disposition'] = 'filename="Proformas.pdf"'
        return response





def Commande_view(request):
    command = Commande.objects.all()
    return render(request, 'Proformas/command_view.html', {'c': command})


def step3(request):
    if request.method == 'POST':
        form = Modalite_Form(request.POST or None)
        if form.is_valid():
            form.save()
            return redirect('commande')
        print(form.errors)
    else:

        form = Modalite_Form()
    return render(request, 'Proformas/steps/step3.html', {'form': form})


def step1(request):
    if request.method == 'POST':
        form = Commande_Form_step(request.POST or None)
        if form.is_valid():
            form.save()
            return redirect('step2')
        print(form.errors)
    else:

        form = Commande_Form_step()
    return render(request, 'Proformas/steps/step1.html', {'form': form})


# def step2(request):
#         # print('in')
#         commande = Commande.objects.latest('id')
#         if request.method == 'POST':
#             # print('post')
#             if request.POST['designation'] and request.POST['prix'] and request.POST['quantite']  and request.POST['mnt_ht'] and request.POST['mnt_tva'] and request.POST['mnt_ttc']:
#                 # print('get')
#                 print(request.POST)
#                 res = 0
#                 for des,prix,q,mht,mtva,ttc in zip(request.POST.getlist('designation'),request.POST.getlist('prix'),request.POST.getlist('quantite'),request.POST.getlist('mnt_tva'),request.POST.getlist('mnt_ht'),request.POST.getlist('mnt_ttc')):
#                      # print('in for')
#                      cd = Commande_D_Form({'Designation':des,'Prix_Unitaire':prix,'Quantite':q,'Montant_HT':mht,'Montant_TVA':mtva,'Montant_TTC':ttc , 'Command' : commande},instance=Commande_Designation())
#                      # print('hna')
#                      res = res + float(prix) * float(q)
#                 if res > commande.Montant_TTC:
#                          er = 'la somme des prix est sup que le montant tt de la commande '
#                          return render(request, 'Proformas/steps/step2.html', {'com': commande, 'ers': er})
#
#                 else:
#                          if cd.is_valid():
#                              # print('valide')
#                              cd.save()
#                          else:
#                              # print(cd.errors)
#                              er = 'data exists '
#                              return render(request, 'Proformas/steps/step2.html', {'com': commande, 'ers': er})
#                 return redirect('step3')
#
#             else:
#                 er = 'check yout inputs :'
#
#                 return render(request, 'Proformas/steps/step2.html', {'com': commande ,'ers' :er})
#         print('ici')
#         return render(request, 'Proformas/steps/step2.html',{'com': commande} )



def step2(request):
    nadjib = modelformset_factory(Commande_Designation, form=Commande_D_Form, extra=1, can_delete=True)

    if request.method == 'POST':
        form = nadjib(request.POST)

        if form.is_valid():
            commande = Commande.objects.last
            res = 0
            for x in form:
                data = x.cleaned_data
                commande = get_object_or_404(Commande,id=data.get('Command').id)
                # print(data.get('Prix_Unitaire'))
                res = res + (float(Decimal(int(data.get('Prix_Unitaire')))) * float(Decimal(int(data.get('Quantite')))))
            if res != commande.Montant_HT:
                print(res)
                er = 'la somme des prix doit etre égale au montant ht de la commande ! ' + ' ' + str(commande.Montant_HT)
                return render(request, 'Proformas/steps/step2.html', {'formset': form, 'com': commande, 'ers': er})
            else:
                form.save()

            return redirect('step3')
        else:
            print(form.errors)
            return render(request, 'Proformas/steps/step2.html', {'formset': form, 'error': form.errors})

    else:
      # ss = modelformset_factory(Commande_Designation, form=Commande_D_Form, extra=1,c)
      formset = nadjib(queryset=Commande.objects.none())
    return render(request, 'Proformas/steps/step2.html', {'formset': formset})

def save_commande_form_update(request, form, template_name):
    data = dict()
    if request.method == 'POST':
        print(request.method=='POST')
        if form.is_valid():

            form.save()

            data['form_is_valid'] = True
            commande = Commande.objects.all()
            data['html_book_list'] = render_to_string('Proformas/partial/partial_proformas.html', {
                'c': commande
            })
        else:
            print(form.errors)

            data['form_is_valid'] = False
    context = {'form': form}
    data['html_form'] = render_to_string(template_name, context, request=request)
    return JsonResponse(data)

def commande_update(request,pk):
    commande = get_object_or_404(Commande,pk=pk)
    if request.method == 'POST':
        form = Commande_Form2(request.POST,instance=commande)
    else:
        form = Commande_Form2(instance=commande)

    return save_commande_form_update(request, form, 'Proformas/partial/parital_commande_update.html')
