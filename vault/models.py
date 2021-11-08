from django.db import models
from django.utils import timezone
from datetime import datetime, timedelta

from django.db.models.signals import post_save
from django.dispatch import receiver
from cryptography.fernet import Fernet

# Create your models here.

class Vault(models.Model):
	title = models.CharField(max_length = 255)
	username = models.CharField(max_length = 255, default = '')
	password = models.CharField(max_length = 255, default = '')
	email = models.EmailField(default = 'mail@email.com')
	other_info = models.TextField(max_length = 10000, default = '')
	date_created = models.DateTimeField(default = timezone.now)
	last_edited = models.DateTimeField(auto_now = True)
	category = models.ForeignKey('Category', on_delete = models.CASCADE)
	locked = models.BooleanField(default = True)
	pwd = models.CharField(max_length = 255)

	def __str__(self):
		return self.title

class Keys(models.Model):
	vault = models.ForeignKey('Vault', on_delete = models.CASCADE)
	key = models.BinaryField(max_length = 255)
	enc_pwd = models.BinaryField(max_length = 255)

	def __str__(self):
		return self.vault.title

def create_keys(sender, instance, created, **kwargs):
	if created:
		key = Fernet.generate_key()
		fernet = Fernet(key);
		enc_pwd = fernet.encrypt(instance.pwd.encode())
		Keys.objects.create(vault = instance, key = key, enc_pwd = enc_pwd)
		instance.pwd = ''
		instance.save()

post_save.connect(create_keys, sender = Vault)


class Category(models.Model):
	title = models.CharField(max_length = 255)
	description = models.CharField(max_length = 255)

	def __str__(self):
		return self.title