from django.contrib import admin
from rbm_website.apps.rbm.models import DBNModel

class DBNAdmin(admin.ModelAdmin):
    list_display = ('name', 'creator', 'created', 'trained')
    list_filter = ('creator',)
    search_fields = ('name', 'creator')

admin.site.register(DBNModel, DBNAdmin)
