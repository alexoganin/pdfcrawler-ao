# -*- coding: utf-8 -*-
import os
import re
import requests
import shutil
import magic
import PyPDF2
from uuid import uuid4
from django.core.exceptions import ValidationError
from pdfcrawler.settings import MEDIA_ROOT
from ..models import PdfFiles, Urls


class CPdfFileHandler(object):
	def __init__(self):
		self._support_mimetype = ['application/pdf']
		self._upload_file_list = []
		self._saved_files = []
		self._file_folder = os.path.join(MEDIA_ROOT, str(uuid4()))

	def process(self, files):
		self._files = files
		self._save_files()
		self._validate_files()
		self._process_urls()
		self._save_to_db()
		self._delete_files()
		return

	def _save_files(self):
		if not len(self._files):
			raise ValidationError('Pdf file filed is empty', code='invalid')
		try:
			os.makedirs(self._file_folder)
		except OSError as e:
			raise OSError('Coudn\'t create a directory for files, error: %s' % str(e))

		for f in self._files:
			with open(os.path.join(self._file_folder, f.name), 'wb+') as current_file:
				for chunk in f.chunks():
					current_file.write(chunk)


	def _validate_files(self):
		for file_path in self._get_files_path_list():
			mimetype = magic.from_file(file_path, mime=True)
			if mimetype not in self._support_mimetype:
				raise ValidationError('File \'%s\' is not pdf format, it has %s mimetype' %
									  (os.path.basename(file_path), mimetype))


	def _process_urls(self):
		saved_files = []
		for f in self._get_files_path_list():
			with open(f, 'rb') as pdf_file_object:
				pdf_reader = PyPDF2.PdfFileReader(pdf_file_object)
				urls = self._get_urls(pdf_reader, os.path.basename(f))
				saved_files.append({
					"file": os.path.basename(f),
					"urls": urls
				})
		self._saved_files = saved_files
		return saved_files

	def _save_to_db(self):
		for file_data in self._saved_files:
			pdf_file_row = PdfFiles(name=file_data.get('file', ''))
			pdf_file_row.save()
			for url_data in file_data.get('urls'):
				url_row = Urls(path=url_data.get('path'), alive=url_data.get('alive'),
							   http_code=url_data.get('http_code'), pdf_file=pdf_file_row)
				url_row.save()

	def _delete_files(self):
		shutil.rmtree(self._file_folder)

	def _get_files_path_list(self):
		files = []
		for (dirpath, dirnames, filenames) in os.walk(self._file_folder):
			files.extend(filenames)
		return [os.path.join(self._file_folder, f) for f in files]

	def _get_urls(self, pdf_reader, file_name):

		def check_url(location):
			try:
				r = requests.head(location)
				status = False if r.status_code >= 400 else True
				return status, r.status_code
			except requests.ConnectionError:
				return False, 400  # in cause when the host can't be reach

		def get_url_template(url):
			print 'url: ' + url
			alive, http_code = check_url(url)
			print alive, http_code
			print '-------------------------'
			return {
				"path": url,
				"alive": alive,
				"http_code": http_code
			}

		regex = re.compile(
			r'^(?:http|ftp)s?://'  # http:// or https://
			r'(?:(?:[A-Z0-9](?:[A-Z0-9-]{0,61}[A-Z0-9])?\.)+(?:[A-Z]{2,6}\.?|[A-Z0-9-]{2,}\.?)|'  # domain...
			r'localhost|'  # localhost...
			r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})'  # ...or ip
			r'(?::\d+)?'  # optional port
			r'(?:/?|[/?]\S+)$', re.IGNORECASE)

		urls = []
		for page_num in range(0, 20 if pdf_reader.numPages > 20 else pdf_reader.numPages):
			page = pdf_reader.getPage(page_num)
			page_buffer = page.extractText().replace("\r", " ").replace("\n", " ")
			word_list = page_buffer.split()
			current_url_list = [word for word in word_list if re.match(regex, word)]
			urls.extend(current_url_list)
		urls = list(set([url.strip('.') for url in urls if url]))		# Leave only uniq url values
		return [get_url_template(url) for url in urls]