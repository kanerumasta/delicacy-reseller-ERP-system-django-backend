from django.urls import path
from . views import *
urlpatterns = [
    
    path('purchase-orders', PurchaseOrderView.as_view()),
    path('purchase-orders/order-items', PurchaseOrderItemView.as_view()),
   
    path('purchase-order/receive/<str:order_code>', received_order),
    path('purchase-order/add-to-inventory/<str:order_code>', add_to_inventory),

]
