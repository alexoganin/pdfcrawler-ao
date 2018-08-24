# -*- coding: utf-8 -*-
from django.db.models.query import QuerySet
from django.forms.models import model_to_dict
from ...models import PdfFiles, Urls

class CBaseDataHandler(object):

	file_fields = ['id', 'name', 'time']
	url_fields = ['id', 'path', 'http_code', 'alive']

	def __init__(self, type='json'):
		self._type = type

	def getFormatedData(self, data):
		result = []
		if isinstance(data, QuerySet):
			for row in data:
				result.append(self.convertToDict(row))
		else:
			result = self.convertToDict(data)
		return result

	def convertToDict(self, row):
		return_value = {}
		if isinstance(row, PdfFiles):
			return_value = self._prepareFileInstance(row)
		elif isinstance(row, Urls):
			return_value = self._prepareUrlInstance(row)
		else:
			raise Exception('Not defined object')
		return return_value

	def _prepareFileInstance(self, row):
		raise NotImplementedError

	def _prepareUrlInstance(self, row):
		raise NotImplementedError

	def _to_dict(self, row):
		if isinstance(row, PdfFiles):
			return model_to_dict(row, fields=self.file_fields)
		elif isinstance(row, Urls):
			return model_to_dict(row, fields=self.url_fields)
		else:
			return model_to_dict(row)

