from django.shortcuts import render
from .models import Commande,Commande_Designation,Modalite
from django.shortcuts import redirect
from django.template.loader import get_template
from .utils import render_to_pdf
from django.shortcuts import render,get_object_or_404,HttpResponse,HttpResponseRedirect
from django.views.generic import View
from Client_Section.models import Client_Data
import datetime
from .forms import Commande_Form,Commande_D_Form,Modalite_Form
from django.core.files.storage import FileSystemStorage
from django.http import HttpResponse
from django.template.loader import render_to_string
from weasyprint import HTML
# Create your views here.

def html_to_pdf_view(request,pk):
        com = get_object_or_404(Commande,pk=pk)
        com_d = Commande_Designation.objects.get(Command=com)

        Designation = com_d.Designation
        Prix_Uni = com_d.Prix_Unitaire
        Quantite = com_d.Quantite
        Montant_HT = com_d.Montant_HT
        Montant_TVA = com_d.Montant_TVA
        Montant_TTC = com_d.Montant_TTC


        client = com.Client
        print(client)
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
        'adresse': adresse,
        'NIF': NIF,
        'NIS': NIS,
        'raison_social': raison_social,
        'Date': datetime.date.today(),

        }
        html_string = render_to_string('Proformas/command.html',context)

        html = HTML(string=html_string,base_url=request.build_absolute_uri())
        html.write_pdf(target='/tmp/mypdf.pdf');

        fs = FileSystemStorage('/tmp')
        with fs.open('mypdf.pdf') as pdf:
          response = HttpResponse(pdf, content_type='application/pdf')
          response['Content-Disposition'] =  'filename="Commande.pdf"'
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
        form = Commande_D_Form(request.POST or None)
        if form.is_valid():
            form.save()
            return redirect('step3')
        print(form.errors)
    else:

        form = Commande_D_Form()
    return render(request, 'Proformas/steps/step2.html', {'form': form})
