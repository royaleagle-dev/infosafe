from django.test import TestCase
from vault.models import Category, Vault

def createCategory(title, description):
		return Category.objects.create(title = title, description = description)


def createVault(title, username, password, email, other_info, category):
	category = createCategory(title = category, description = 'This is a test description for %s'.format(category))
	return Vault.objects.create(title = title, username = username, password = password, email = email, other_info = other_info,
	category = category)

class VaultModelTests(TestCase):

	def test_create_vault(self):
		vault = createVault('test', 'myUsername', 'myPassword', 'email@email.com', 'other information here', 'Testing')
		self.assertIs(vault.__str__(), 'test')

