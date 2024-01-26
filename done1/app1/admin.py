from django.contrib import admin

from .models import Person, Requeste, PorteFeuille

# Register your models here.

admin.site.register(Person)
admin.site.register(Requeste)
admin.site.register(PorteFeuille)