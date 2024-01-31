from django.urls import path
from .views import *
urlpatterns = [
	path('', LogView.as_view()),
]