from django.shortcuts import render

# Create your views here.



from django.shortcuts import render,get_object_or_404,HttpResponse,HttpResponseRedirect
from formtools.wizard.views import SessionWizardView
from .models import Association,Article,Achats
from django.shortcuts import redirect,reverse
from django.forms import formset_factory
from django.forms import modelformset_factory,formset_factory
from django.http import JsonResponse
from django.forms import formset_factory
from .forms import AchatForm,ArticleForm,AssociationForm,AssociationForm2
from django.template.loader import render_to_string

from Fournis_Section.models import Fournis_Data


def update(request,pk):
    achat = get_object_or_404(Achats, pk=pk)
    # ass = Association.objects.filter(Id_Achats=achat)
    form = modelformset_factory(Association, form=AssociationForm, extra=5,can_delete=True)
    # formset = form(queryset=Association.objects.filter(Id_Achats=achat.id))

    if request.method == 'POST':
       formset = form(request.POST or None)
       if formset.is_valid():
           formset.save()
           return redirect('view')


    else:
        form = modelformset_factory(Association, form=AssociationForm, extra=5, can_delete=True)
        formset = form(queryset=Association.objects.filter(Id_Achats=achat.id))


    return render(request, 'html_update.html', {'formset': formset})



def step1(request):
    if request.method == 'POST':
      form = AchatForm(request.POST or None)
      if form.is_valid():
             form.save()
             print(form.cleaned_data)
             print(form.cleaned_data.get('Montant_HT'))
             return redirect('step2')
      print(form.errors)
    else:

         form = AchatForm()
    return render(request, 'step1.html', {'form': form,'error':form.errors})


def step2(request):
    if request.method == 'POST':
        nadjib = modelformset_factory(Association, form=AssociationForm2, extra=5,can_delete=True)
        form = nadjib(request.POST)

        if form.is_valid():
            form.save()

            return redirect('view')
        else:
            print(form.errors)


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
    # for p in Achats.objects.raw('SELECT Id_Fournis_id,id FROM Gestion_Achats_achats'):
    #    print(p.Montant_TTC)
    #    print(p.Id_Fournis_id)


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








