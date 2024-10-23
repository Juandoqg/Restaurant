from django.test import TestCase, Client
from django.urls import reverse
from myapp.models import User

class CreateUserViewTests(TestCase):

    def setUp(self):
        self.client = Client()
        self.url = reverse('createUser')  
        self.admin_user = User.objects.create_superuser(username='admin', password='admin123', email='admin@example.com')

    def test_create_user_get_request(self):
        self.client.login(username='admin', password='admin123')
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'createUser.html')

    def test_create_user_post_request_valid(self):
        self.client.login(username='admin', password='admin123')
        response = self.client.post(self.url, {
            'username': 'newuser',
            'password': 'newpassword',
            'name': 'New',
            'lastname': 'User',
            'email': 'newuser@example.com',
            'document': '123456789', 
            'date': '2024-01-01',      
            'Tipo': 'Mesero'
        })
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'createUser.html')
        self.assertTrue(response.context['success'])  # Verifica el valor en el contexto
        self.assertTrue(User.objects.filter(username='newuser').exists())

    def test_create_user_post_request_invalid(self):
        self.client.login(username='admin', password='admin123')
        response = self.client.post(self.url, {
            'username': '',
            'password': '',
            'name': '',
            'lastname': '',
            'email': '',
            'document': '',  
            'date': '',      
            'Tipo': 'Mesero'
        })
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'createUser.html')
        self.assertContains(response, 'error')  # Cambia esto si usas mensajes
        self.assertFalse(User.objects.filter(username='').exists())
