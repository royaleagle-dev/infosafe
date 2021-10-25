from django.urls import path
#from . models import Vault, Category
from . import views

app_name = 'vault'

urlpatterns = [
	path('', views.IndexListView.as_view(), name = 'index'),
]