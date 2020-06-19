from io import BytesIO
from django.http import HttpResponse
from django.template.loader import get_template
from django.conf import settings
import os
from random import randint
from xhtml2pdf import pisa
from datetime import datetime
from django.utils.text import slugify
import random
import string

def render_to_pdf(template_src, context_dict={}):
    template = get_template(template_src)
    html  = template.render(context_dict)
    result = BytesIO()
    pdf = pisa.pisaDocument(BytesIO(html.encode("ISO-8859-1")), result,link_callback=fetch_resources)
    if not pdf.err:
        return HttpResponse(result.getvalue(), content_type='application/pdf')
    return None

def fetch_resources(uri, rel):
        path = os.path.join(settings.STATIC_ROOT, uri.replace(settings.STATIC_URL, ""))

        return path




def unique_slug_generator(instance, new_slug=None):

    if new_slug is not None:
        slug = new_slug
    else:
        slug = slugify(datetime.now().year)


    crypt = "{slug}-{randstr}".format(
                    slug=slug,
                    randstr=randint(1000000, 1999000)
                )
    return crypt

