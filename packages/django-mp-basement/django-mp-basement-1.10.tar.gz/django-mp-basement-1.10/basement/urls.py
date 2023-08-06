
from django.apps import apps
from django.urls import path, include

from basement import views


urlpatterns = [

    path('db/download/', views.download_db, name='download-db')

]

if apps.is_installed('ckeditor_uploader'):
    urlpatterns += [
        path('ckeditor/', include('ckeditor_uploader.urls')),
    ]
