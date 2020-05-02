from django.contrib import admin

from .models import Article,Achats,Association,Payements

# Register your models here.


admin.site.register(Article)
admin.site.register(Association)
admin.site.register(Achats)
admin.site.register(Payements)

