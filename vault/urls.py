from django.urls import path
#from . models import Vault, Category
from . import views

app_name = 'vault'

urlpatterns = [
	path('', views.IndexListView.as_view(), name = 'index'),
	path('<int:pk>/', views.VaultDetailView.as_view(), name = 'detail'),
	path('unlock/', views.unlock, name = 'unlock'),
	path('delete/<int:id>', views.delete, name = 'delete'),
	path('instant_lock', views.instant_lock, name = 'instant_lock'),
	path('addVault', views.addVault, name = 'addVault')
]