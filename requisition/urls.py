from django.urls import path
from . views import *

urlpatterns = [
    path('requisitions',RequisitionView.as_view()),
    path('items', RequisitionItemView.as_view()),
    path('<int:requisition_id>', RequisitionView.as_view()),
    path('<int:requisition_id>/approve', ApproveRequisitionView.as_view()),
    path('<int:requisition_id>/reject', RejectRequisitionView.as_view()),
    path('<int:requisition_id>/create-order', create_order),
    path('user-requisitions', UserRequisitionsView.as_view(), name='user_requisitions'),
]
