from django.shortcuts import render, redirect, get_object_or_404
from . models import Vault, Category, Keys
from django.views import generic
from cryptography.fernet import Fernet
from django.contrib import messages
from django.http import JsonResponse
from . forms import VaultForm
from django.views import View

def edit_keys(vault_obj, pwd):
	key_obj = Keys.objects.get(vault = vault_obj)
	key = Fernet.generate_key()
	fernet = Fernet(key)
	encode = fernet.encrypt(pwd.encode())
	key_obj.key = key
	key_obj.enc_pwd = encode
	key_obj.save()
	vault_obj.pwd = ''
	vault_obj.save();
	return True;

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
			messages.error(request, "Incorrect Password, Try Again")
			return render(request, "vault/detail.html", {'vault':Vault.objects.get(id=vault)})
	else:
		return redirect('vault:index')

def delete(request, id):
	vault = get_object_or_404(Vault, id=id)
	vault_name = vault.title
	vault.delete()
	messages.success(request, f"Vault --{vault_name}-- was Deleted successfully")
	return redirect("vault:index")

def instant_lock(request):
	vault_id = request.GET.get('id')
	vault = get_object_or_404(Vault, id=vault_id)	
	vault.locked = True
	vault.save()
	return JsonResponse({'status':'locked'})

class AddVault(View):	
	def get(self, request):
		form = VaultForm()
		ctx = {
			'form':form,
		}
		return render(request, "vault/newVault.html", ctx)

	def post(self, request):
		form = VaultForm(request.POST)

		if form.is_valid():
			newVault = Vault(
				title = form.cleaned_data['title'],
				username = form.cleaned_data['username'],
				password = form.cleaned_data['password'],
				email = form.cleaned_data['email'],
				other_info = form.cleaned_data['other_info'],
				category = form.cleaned_data['category'],
				pwd = form.cleaned_data['pwd'],
			)
		newVault.save()

		messages.success(request, "Vault sucessfully added")
		return redirect('vault:index')

def search(request, word):
	search = Vault.objects.filter(title__icontains = word)
	return render(request, "vault/search.html", {'search':search})

def editVault(request, id):
	vault = get_object_or_404(Vault, id=id)
	update_form = VaultForm(request.POST or None, instance = vault)
	if update_form.is_valid():
		update_form.save();
		obj = update_form.save()
		edit = edit_keys(vault, obj.pwd)
		if(edit):
			messages.success(request, "Vault updated successfully")
			return redirect('vault:detail', pk=id)
	return render(request, "vault/editVault.html", {'update_form':update_form})

class Settings(View):
	def get(self, request):
		return render(request, "vault/settings.html")