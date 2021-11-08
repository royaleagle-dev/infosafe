from django.shortcuts import render, redirect, get_object_or_404
from . models import Vault, Category, Keys
from django.views import generic
from cryptography.fernet import Fernet
#import base64
from django.contrib import messages

from django.http import HttpResponse
from django.http import JsonResponse

from . forms import VaultForm

class IndexListView(generic.ListView):
	model = Vault
	context_object_name = 'vaults'
	template_name = 'vault/index.html'

	def get_queryset(self):
		return Vault.objects.all().order_by('-last_edited')

class VaultDetailView(generic.DetailView):
	model = Vault
	context_object_name = 'vault'
	template_name = 'vault/detail.html'

def unlock(request):
	if request.method == 'POST':
		pwd = request.POST.get('key')
		vault = request.POST.get('vault')
		select_key = Keys.objects.filter(vault__id = vault)[:1]
		for item in select_key:
			select_key = item
		encode_decode_key = select_key.key
		enc_pwd = select_key.enc_pwd
		fernet = Fernet(encode_decode_key)
		decode = fernet.decrypt(enc_pwd).decode()
		if decode == pwd:
			#unlock vault
			vault = Vault.objects.get(id = vault)
			vault.locked = False
			vault.save()
			ctx = {
					'vault':vault,
			}
			return render(request, "vault/detail.html", ctx)
		else:
			#come here later
			return render(request, "vault/detail.html", {'vault':Vault.objects.get(id=vault)})
	else:
		return redirect('vault:index')

def delete(request, id):
	vault = get_object_or_404(Vault, id=id)
	vault_name = vault.title
	vault.delete()
	messages.success(request, f"Vault {vault_name} was Deleted successfully")
	return redirect("vault:index")


def instant_lock(request):
	vault_id = request.GET.get('id')
	vault = get_object_or_404(Vault, id=vault_id)	
	vault.locked = True
	vault.save()
	return JsonResponse({'status':'locked'})

def addVault(request):
	form = VaultForm()
	ctx = {
		'form':form,
	}
	return render(request, "vault/newVault.html", ctx)