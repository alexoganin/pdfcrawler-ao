# -*- coding: utf-8 -*-
from .BaseDataHandler import CBaseDataHandler
from ...models import PdfFiles

class CDetailedDataHandler(CBaseDataHandler):

	type = 'DetailedHandler'

	def _prepareFileInstance(self, row):
		template_dict = self._to_dict(row)
		template_dict['time'] = row.time.strftime("%Y-%m-%d %H:%M:%S")
		template_dict['urls_count'] = row.urls.count()
		template_dict['urls'] = [self._prepareUrlData(u) for u in row.urls.all()]
		return template_dict

	def _prepareUrlInstance(self, row):
		template_dict = self._to_dict(row)
		template_dict['files_count'] = self._get_files_count(row)
		template_dict['files'] = self._get_all_files_by_urls(row)
		return template_dict

	def _prepareUrlData(self, row):
		return self._to_dict(row)

	def _prepareFileData(self, row):
		ret_dict = self._to_dict(row)
		ret_dict['time'] = row.time.strftime("%Y-%m-%d %H:%M:%S")
		return ret_dict

	def _get_files_count(self, url):
		return PdfFiles.objects.filter(urls__path=url.path).count()

	def _get_all_files_by_urls(self, url):
		files = PdfFiles.objects.filter(urls__path=url.path).all()
		return [self._prepareFileData(f) for f in files]
