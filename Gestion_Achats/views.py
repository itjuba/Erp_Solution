from django.shortcuts import render

# Create your views here.



from django.shortcuts import render,get_object_or_404,HttpResponse

from .models import Association,Article,Achats
from django.forms import formset_factory
from django.forms import modelformset_factory
from django.http import JsonResponse
from django.forms import formset_factory
from .forms import AchatForm,ArticleForm,AssociationForm
from urllib.parse import parse_qs
import json
from django.contrib import messages
from django.template.loader import render_to_string
# Create your views here.


def view(request):
    achat = Achats.objects.all()
    form = modelformset_factory(Association, form=AssociationForm, extra=5)
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
            return HttpResponse('done')
            print(formset)
    else:
        formset = form(queryset=Association.objects.none())
        print(formset.errors)

    return render(request, 'html.html', {'Achats': achat, 'formset': formset})


def find(request,pk):
    achat = get_object_or_404(Achats, pk=pk)
    return render(request,'html.html',{'achat':achat})

# def view(request):
#     achat = Achats.objects.all()
#     form =  formset_factory(AssociationForm,extra=1)
#
#     if request.method == 'POST':
#       print('post')
#       formset = form(request.POST or None)
#       if formset.is_valid():
#             print('form is vlaid')
#             print(formset)
#             for form in formset:
#                 form.save()
#       else:
#           print(formset.errors)
#
#       return render(request,'html.html',{'Achats':achat,'formset':formset})
#     else:
#         achat = Achats.objects.all()
#         form = formset_factory(AssociationForm, extra=1)
#         return render(request, 'html.html', {'Achats': achat, 'formset': form})
#
#
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






def article_create(request):
    if request.method == 'POST':
        form = ArticleForm(request.POST)

    else:
        form = ArticleForm(request.POST)
    return save_Artcile_form(request, form, 'Gestion_Achats/article/partial_client.html')


def Achats_create(request):
    if request.method == 'POST':
        form = AchatForm(request.POST)

    else:
        form =AchatForm(request.POST)
    return save_Achats_form(request, form, 'Gestion_Achats/Achats/partial_client.html')





def Article_update(request,pk):
    article = get_object_or_404(Article, pk=pk)
    if request.method == 'POST':
        print(request.POST)
        form = ArticleForm(request.POST, instance=article)

    else:
        form = ArticleForm(instance=article)


    return save_article_form_update(request, form,'Gestion_Achats/article/partial_client_update_update.html')



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
        data['html_book_list'] = render_to_string('Gestion_Achats/Achats/partial_client_c.html', {
            'Achats': achats
        })
    else:
        context = {'obj': book}
        data['html_form'] = render_to_string('Gestion_Achats/Achats/partial_client_delete.html',
            context,
            request=request,
        )
    return JsonResponse(data)













