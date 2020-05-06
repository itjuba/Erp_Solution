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
from django.forms import modelformset_factory,formset_factory

from django.template.loader import render_to_string
from weasyprint import HTML
# Create your views here.

def html_to_pdf_view(request,pk):
        com = get_object_or_404(Commande,pk=pk)
        design = Commande_Designation.objects.filter(Command=com).values_list('Designation', flat=True)
        prix = Commande_Designation.objects.filter(Command=com).values_list('Prix_Unitaire', flat=True)
        qua = Commande_Designation.objects.filter(Command=com).values_list('Quantite', flat=True)
        ht = Commande_Designation.objects.filter(Command=com).values_list('Montant_HT', flat=True)
        tva = Commande_Designation.objects.filter(Command=com).values_list('Montant_TVA', flat=True)
        ttc = Commande_Designation.objects.filter(Command=com).values_list('Montant_TTC', flat=True)
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
        nadjib = modelformset_factory(Commande_Designation, form=Commande_D_Form, extra=5, can_delete=True)
        form = nadjib(request.POST)

        if form.is_valid():
            form.save()

            return redirect('step3')
        else:
            print(form.errors)

    form = modelformset_factory(Commande_Designation, form=Commande_D_Form, extra=5)
    formset = form(queryset=Commande.objects.none())
    return render(request, 'Proformas/steps/step2.html', {'formset': formset, 'error': form.errors})

