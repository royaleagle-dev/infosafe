from django.test import TestCase
from django.urls import reverse
from vault.models import Category, Vault, Keys
from vault.views import edit_keys

def createCategory(title, description):
		return Category.objects.create(title = title, description = description)


def createVault(title, username, password, email, other_info, category):
	category = createCategory(title = category, description = 'This is a test description for %s'.format(category))
	return Vault.objects.create(title = title, username = username, password = password, email = email, other_info = other_info,
	category = category)

class VaultViewTest(TestCase):

    def test_no_vault(self):
        response = self.client.get(reverse('vault:index'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, '')
        self.assertQuerysetEqual(response.context['vaults'], [])

    def test_single_vault(self):
        vault = createVault('test', 'test1', '12345', 'test@t.com', 'other information', 'test')
        response = self.client.get(reverse('vault:index'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, vault.title)
        self.assertQuerysetEqual(response.context['vaults'], [vault])

    def test_multiple_vault(self):
        vault1 = createVault('test', 'test1', '12345', 't@t.com', 'others', 'test1')
        vault2 = createVault('test2', 'test2', '12345', 't@t2.com', 'other2', 'test2')
        response = self.client.get(reverse('vault:index'))
        self.assertEqual(response.status_code, 200)
        self.assertQuerysetEqual(response.context['vaults'], [vault2, vault1])
        self.assertContains(response, 'test')

class VaultDetailViewTest(TestCase):

    def test_vault_detail_show(self):
        vault = createVault('test', 'testme', '12345', 't@t.com', 'other information', 'test')
        url = reverse('vault:detail', args = (vault.id,))
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, vault.title)

class VaultDeleteViewTest(TestCase):

    def test_delete_vault(self):
        vault = createVault('test', 'testme', '12345', 't@t.com', 'other information', 'test')
        url = reverse('vault:delete', args = (vault.id,))
        response = self.client.get(url)
        self.assertEqual(response.status_code, 302)

class VaultSearchViewTest(TestCase):

    def test_search_vault(self):
        vault = createVault('test', 'testme', '12345', 't@t.com', 'other information', 'test')
        url = reverse('vault:search', args = ('test',))
        response = self.client.get(url)
        self.assertQuerysetEqual(response.context['search'], [vault])
        self.assertEqual(response.status_code, 200)

class VaultSettingsViewTest(TestCase):

    def test_settings_show(self):
        response = self.client.get(reverse('vault:settings'))
        self.assertEqual(response.status_code, 200)


class VaultMiscTest(TestCase):

    def test_edit_keys_function(self):
        vault = createVault('test', 'testme', '12345', 't@t.com', 'other information', 'test')
        self.assertEqual(edit_keys(vault, '12345'), True)
    
    def test_unlock_view(self):
        
