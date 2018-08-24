# -*- coding: utf-8 -*-
from django.core.serializers.json import DjangoJSONEncoder
from .models import PdfFiles, Urls


class PdfFileJsonEncoder(DjangoJSONEncoder):
	def __make_decoding(self):
		return ""

	def default(self, obj):
		print type(obj)
		if isinstance(obj, PdfFiles):
			return self.__make_decoding(obj)
		return super(PdfFileJsonEncoder, self).default(obj)
