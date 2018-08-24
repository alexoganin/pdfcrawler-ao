# PDFCrawler
ReadME

urls for API:

[GET, POST] /crawler/files/		- file list

[GET] /crawler/files/<file_id>		- get <file_id> information

[GET] /crawler/urls/				- url list

[GET] /crawler/urls/<url_id>		- get <url_id> information

---------------------------------------------------

Handlers:
1. PdfHandler - for split pdf files on part + get urls from each part
2. PrepareDataHandler - for prepeare data for API

http://pdfcrawler-ao.herokuapp.com/

There some problems with upload files on Heroku server. In case when pdf-file contains URL it causes time out worker, maybe it connected with check url avaliable status. On local it works OK.

About models:
There was several ideas how to organize it. First of all it use Model and ModelManager for getting queries for our API. But lack of time forced me to write custom PrepareDataHandler for getting structures of data for Api.

Also there was several ideas to organize API with django-rest-framework


=======
# pdfcrawler-ao
