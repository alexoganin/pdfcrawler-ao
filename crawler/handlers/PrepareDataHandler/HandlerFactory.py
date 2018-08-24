# -*- coding: utf-8 -*-
from .DetailedDataHanlder import CDetailedDataHandler
from .ListDataHandler import CListDataHandler


class CHandlerFactory(object):
	@staticmethod
	def getHandlerInstance(type):
		if type == CDetailedDataHandler.type:
			return CDetailedDataHandler()
		elif type == CListDataHandler.type:
			return CListDataHandler()