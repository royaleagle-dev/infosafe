from django.contrib import admin
from . models import Vault, Category, Keys

# Register your models here.

admin.site.register(Vault)
admin.site.register(Category)
admin.site.register(Keys)
