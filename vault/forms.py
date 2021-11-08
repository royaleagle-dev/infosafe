from django import forms
from . models import Vault

class VaultForm(forms.ModelForm):
	
	#meta information for the model
	class Meta:
		model = Vault
		exclude = ['date_created', 'last_edited', 'locked']
