# -*- coding: utf-8 -*-
from __future__ import unicode_literals
import json
from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, JsonResponse
from django.core.serializers.json import DjangoJSONEncoder
from django.db.models import Count
from django.views import View
from django.views.generic import ListView
from .models import PdfFiles, Urls
from .handlers.PdfFileHandler import CPdfFileHandler
from .handlers.PrepareDataHandler.HandlerFactory import CHandlerFactory, CDetailedDataHandler, CListDataHandler


class BaseView(View):
	def get(self, request):
		# raise MethodNotAllowed
		pass

	def post(self, request):
		pass

	def put(self, request):
		pass

	def delete(self, request):
		pass


class FileListViewApi(ListView):

	model = PdfFiles
	queryset = PdfFiles.objects.annotate(urls_count=Count('urls'))

	def get(self, request, *args, **kwargs):
		# json_data = json.dumps(list(self.get_queryset().values()), cls=PdfFileJsonEncoder)
		dataHandler = CHandlerFactory.getHandlerInstance(CListDataHandler.type)
		data = dataHandler.getFormatedData(self.get_queryset())
		json_data = json.dumps(data, cls=DjangoJSONEncoder)
		return JsonResponse(json_data, safe=False, content_type="application/json")

	def post(self, request):
		files = request.FILES.getlist('pdf_file')
		pdf_handler = CPdfFileHandler()
		pdf_handler.process(files)
		return HttpResponse('Add new file here')


class FileViewApi(View):
	def get(self, request, id):
		file_data = get_object_or_404(PdfFiles, pk=id)
		data_handler = CHandlerFactory.getHandlerInstance(CDetailedDataHandler.type)
		data = data_handler.getFormatedData(file_data)
		json_data = json.dumps(data, cls=DjangoJSONEncoder)
		return JsonResponse(json_data, safe=False)


class UrlListViewApi(ListView):
	model = Urls
	queryset = Urls.objects.all()

	def get(self, request, *args, **kwargs):
		dataHandler = CHandlerFactory.getHandlerInstance(CListDataHandler.type)
		data = dataHandler.getFormatedData(self.get_queryset())
		json_data = json.dumps(data, cls=DjangoJSONEncoder)
		return JsonResponse(json_data, safe=False)


class UrlViewApi(View):
	def get(self, request, id):
		url_data = get_object_or_404(Urls, pk=id)
		data_handler = CHandlerFactory.getHandlerInstance(CDetailedDataHandler.type)
		data = data_handler.getFormatedData(url_data)
		json_data = json.dumps(data, cls=DjangoJSONEncoder)
		return JsonResponse(json_data, safe=False)


class FileView(View):
	def get(self, request, id):
		get_object_or_404(PdfFiles, pk=id)
		return render(request, "crawler/file_viewer.html", {'id': id})


class UrlView(View):
	def get(self, request, id):
		get_object_or_404(Urls, pk=id)
		return render(request, "crawler/url_viewer.html", {'id': id})


class UrlList(View):
	def get(self, request):
		return render(request, "crawler/url_list.html", {})

