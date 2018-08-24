# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models

class PdfFiles(models.Model):
	name = models.CharField(max_length=260)
	time = models.DateTimeField(auto_now_add=True)

	class Meta:
		ordering = ["-time"]

	def __str__(self):
		return self.name

class Urls(models.Model):
	path = models.CharField(max_length=1000)
	time = models.DateTimeField(auto_now_add=True)
	alive = models.BooleanField()
	http_code = models.IntegerField()
	pdf_file = models.ForeignKey(PdfFiles, on_delete=models.CASCADE, related_name='urls')

	def __str__(self):
		return self.path

# class UrlsManager(models.Manager):
# 	def get_by_natural_key(self, id, path):
# 		return self.get(id=id, path=path)
