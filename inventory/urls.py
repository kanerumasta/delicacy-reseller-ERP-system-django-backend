from django.urls import path
from . views import *


urlpatterns = [

    #manage delicacies endpoint
    path('delicacies', DelicaciesView.as_view()),
    path('delicacies/<int:delicacy_id>',DelicaciesView.as_view()),
  
    path('variations', VariationView.as_view()),
    path('variations/<int:variation_id>', VariationView.as_view()),

    path('', InventoryView.as_view()),

    path('total-low-stock-items',get_total_low_stock_items),
    path('total-out-of-stock-items',get_total_out_of_stock_items),

    path('check_delicacy_name/', CheckDelicacyNameView.as_view(), name='check_delicacy_name'),
    path('get_out_of_stock_items',get_out_of_stock_items),
    path('get_low_stock_items',get_low_stock_items),
    path('get_expired_items',get_expired_items),

    #manage inventory item endpoint
    path('items', ItemView.as_view()),
    path('items/<int:item_id>',ItemView.as_view()),

    path('get_delicacy_name/<int:delicacy_id>', get_delicacy_name),

    path('suppliers', SupplierView.as_view())

]
