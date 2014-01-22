from django.contrib import admin
from rbm_website.apps.rbm.models import DBNModel

# The interface for the Admin pages powered by Django
# visit the site /admin to get the pages
class DBNAdmin(admin.ModelAdmin):
    list_display = ('name', 'creator', 'created', 'trained')
    list_filter = ('creator',)
    search_fields = ('name', 'creator')

admin.site.register(DBNModel, DBNAdmin)
