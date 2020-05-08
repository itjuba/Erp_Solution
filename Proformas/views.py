from django.shortcuts import render
from .models import Commande,Commande_Designation,Modalite
from django.shortcuts import redirect
from django.template.loader import get_template
from .utils import render_to_pdf
from django.shortcuts import render,get_object_or_404,HttpResponse,HttpResponseRedirect
from django.views.generic import View
from Client_Section.models import Client_Data
import datetime
import threading
from .forms import Commande_Form,Commande_D_Form,Modalite_Form,validat
from django.core.files.storage import FileSystemStorage
from django.http import HttpResponse
from django.forms import modelformset_factory,formset_factory
from django.template.loader import render_to_string
from weasyprint import HTML
from django.core.mail import EmailMessage
import weasyprint
from django.template.loader import render_to_string
from weasyprint import HTML

from django.utils.html import strip_tags
# Create your views here.

def dat_val(request,pk):
    # commande = Commande.objects.filter(id=pk)
    if request.method == 'POST':
        form = validat(request.POST)
        if form.is_valid():
            dat = form.data['Validate_date']
            achh = Commande.objects.filter(id=pk).update(Date_validation=dat,validation=True)
            return redirect('commande')

    else:
        form = validat()
    return render(request,'Proformas/valid.html',{'form':form})



class EmailThread(threading.Thread):
    def __init__(self, subject, html_content, recipient_list, sender):
        self.subject = subject
        self.recipient_list = recipient_list
        self.html_content = html_content
        self.sender = sender
        threading.Thread.__init__(self)

    def run(self):
        msg = EmailMessage(self.subject, self.html_content, self.sender, self.recipient_list)
        msg.attach_file('/tmp/Facture.pdf')
        msg.content_subtype = "html"  # Main content is now text/html
        msg.encoding = 'utf-8'
        msg.send()


def nadjib(subject, html_content, recipient_list, sender):
        EmailThread(subject, html_content, recipient_list, sender).start()



def send_mail(request):
    html_nadjib = render_to_string('Proformas/msg.html')
    to_emails = ['attignadjib@outlook.com']
    subject = "SH INFOR FACTURE"
    nadjib(subject, html_nadjib, to_emails, 'attignadjib@gmail.com')
    # email = EmailMessage(subject, html_nadjib, from_email='attignadjib@gmail.com', to=to_emails)
    # email.attach_file('/tmp/Facture.pdf')
    # email.content_subtype = "html"  # Main content is now text/html
    # email.encoding = 'utf-8'
    # email.send()

    return HttpResponse('SENT')



def html_to_pdf_view(request,pk):
        com = get_object_or_404(Commande,pk=pk)
        if Commande_Designation.objects.filter(Command=pk):
            design = Commande_Designation.objects.filter(Command=com).values_list('Designation', flat=True)
            prix = Commande_Designation.objects.filter(Command=com).values_list('Prix_Unitaire', flat=True)
            qua = Commande_Designation.objects.filter(Command=com).values_list('Quantite', flat=True)
            ht = Commande_Designation.objects.filter(Command=com).values_list('Montant_HT', flat=True)
            tva = Commande_Designation.objects.filter(Command=com).values_list('Montant_TVA', flat=True)
            ttc = Commande_Designation.objects.filter(Command=com).values_list('Montant_TTC', flat=True)
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
            Designation = Designation + " " +  x

        Prix_Uni = 0
        for x in prix:
            Prix_Uni = Prix_Uni + x

        Quantite = 0
        for x in qua:
            Quantite = Quantite + x

        Montant_HT= 0
        for x in ht:
            Montant_HT =Montant_HT +x

        Montant_TVA = 0
        for x in tva:
            Montant_TVA = Montant_TVA +x

        Montant_TTC = 0
        for x in ttc:
                Montant_TTC = Montant_TTC +x




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
        client = com.Client
        client_data = Client_Data.objects.get(id=client.id)
        adresse = client_data.adresse
        NIF = client_data.NIF
        NIS = client_data.NIS
        raison_social = client_data.Raison_social


        context = {
        'Designation': Designation,
        'Prix_Uni': Prix_Uni,
        'Quantite': Quantite,
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

        }
        html_string = render_to_string('Proformas/command.html',context)

        html = HTML(string=html_string,base_url=request.build_absolute_uri())
        html.write_pdf(target='/tmp/Facture.pdf');
        html_nadjib = render_to_string('Proformas/msg.html', context)
        fs = FileSystemStorage('/tmp')
        with fs.open('Facture.pdf') as pdf:
            response = HttpResponse(pdf, content_type='application/pdf')
            response['Content-Disposition'] = 'filename="Facture.pdf"'
            # to_emails = ['attignadjib@outlook.com']
            # subject = "SH INFOR FACTURE"
            # email = EmailMessage(subject, html_nadjib, from_email='attignadjib@gmail.com', to=to_emails)
            # email.attach_file('/tmp/Facture.pdf')
            # email.content_subtype = "html"  # Main content is now text/html
            # email.encoding = 'utf-8'
            # email.send()
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
        form = Commande_Form(request.POST or None)
        if form.is_valid():
            form.save()
            return redirect('step2')
        print(form.errors)
    else:

        form = Commande_Form()
    return render(request, 'Proformas/steps/step1.html', {'form': form})


def step2(request):
    if request.method == 'POST':
        nadjib = modelformset_factory(Commande_Designation, form=Commande_D_Form, extra=5, can_delete=True)
        form = nadjib(request.POST)

        if form.is_valid():
            form.save()

            return redirect('step3')
        else:
            print(form.errors)
            return render(request, 'Proformas/steps/step2.html', {'formset': form, 'error': form.errors})

    else:
      ss = modelformset_factory(Commande_Designation, form=Commande_D_Form, extra=5)
      formset = ss(queryset=Commande.objects.none())
    return render(request, 'Proformas/steps/step2.html', {'formset': formset})

