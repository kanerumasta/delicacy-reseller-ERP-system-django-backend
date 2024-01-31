from django.contrib import admin
from . models import *

admin.site.register(PurchaseOrder)
admin.site.register(PurchaseOrderItem)