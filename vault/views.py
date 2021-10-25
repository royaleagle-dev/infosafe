from django.shortcuts import render, redirect, get_object_or_404
from . models import Vault, Category 
from django.views import generic

class IndexListView(generic.ListView):
	model = Vault
	context_object_name = 'vaults'
	template_name = 'vault/index.html'

	def get_queryset(self):
		return Vault.objects.all().order_by('-last_edited')


