from django.test import TestCase
from vault.models import Category, Vault, Keys
from cryptography.fernet import Fernet

def createCategory(title, description):
		return Category.objects.create(title = title, description = description)


def createVault(title, username, password, email, other_info, category):
	category = createCategory(title = category, description = 'This is a test description for %s'.format(category))
	return Vault.objects.create(title = title, username = username, password = password, email = email, other_info = other_info,
	category = category)

def createKey(vault, enc_pwd):
	key = Fernet.generate_key()
	fernet = Fernet(key)
	enc_pwd = fernet.encrypt(enc_pwd.encode())
	return Keys.objects.create(vault = vault, key = key, enc_pwd = enc_pwd)

class VaultModelTests(TestCase):

	def test_create_vault(self):
		vault = createVault('test', 'myUsername', 'myPassword', 'email@email.com', 'other information here', 'Testing')
		self.assertIs(vault.__str__(), 'test')

class KeysModelTests(TestCase):

	def test_create_keys(self):
		vault = createVault('TestVault', 'Ayotunde', '12345', 'ay@email.com', 'other info goes here', 'testing');
		key = createKey(vault, '12345')
		self.assertIs(key.__str__(), vault.title)

class CategoryModelTests(TestCase):

	def test_create_category(self):
		category = createCategory('test', 'already tested')
		self.assertIs(category.__str__(), category.title)


