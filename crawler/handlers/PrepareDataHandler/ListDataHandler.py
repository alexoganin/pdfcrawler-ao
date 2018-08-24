# -*- coding: utf-8 -*-
from .BaseDataHandler import CBaseDataHandler

class CListDataHandler(CBaseDataHandler):

	type = 'ListHandler'

	def _prepareFileInstance(self, row):
		template_dict = self._to_dict(row)
		template_dict['time'] = row.time.strftime("%Y-%m-%d %H:%M:%S")
		template_dict['urls_count'] = row.urls.count()
		return template_dict

	def _prepareUrlInstance(self, row):
		template_dict = self._to_dict(row)
		return template_dict
