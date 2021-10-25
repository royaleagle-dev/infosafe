from django.db import models
from django.utils import timezone

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

	def __str__(self):
		return self.title

class Category(models.Model):
	title = models.CharField(max_length = 255)
	description = models.CharField(max_length = 255)

	def __str__(self):
		return self.title

