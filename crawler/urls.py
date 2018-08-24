from django.conf.urls import url
from .views import FileViewApi, FileListViewApi, UrlViewApi, UrlListViewApi, FileView, UrlView, UrlList

urlpatterns = [
	# Api view
	url(r'^files/$', FileListViewApi.as_view()),
	url(r'^files/(?P<id>[0-9]+)/$', FileViewApi.as_view()),
	url(r'^urls/$', UrlListViewApi.as_view()),
	url(r'^urls/(?P<id>[0-9]+)/$', UrlViewApi.as_view()),
	# Front view
	url(r'^fileview/(?P<id>[0-9]+)/$', FileView.as_view()),
	url(r'^urlview/(?P<id>[0-9]+)/$', UrlView.as_view()),
	url(r'^urllist/$', UrlList.as_view()),
]
