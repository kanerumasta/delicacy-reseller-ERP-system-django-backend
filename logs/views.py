from django.shortcuts import render
from rest_framework.views import APIView
from .models import TransactionLog
from .serializers import LogSerializer
from rest_framework.response import Response
from rest_framework import status

class LogView(APIView):
	def get(self,request):
		try:
			logs = TransactionLog.objects.all().order_by('-timestamp')
			serializer = LogSerializer(logs, many = True)
			return Response(serializer.data, status = status.HTTP_200_OK)
		except Exception as e:
			raise e