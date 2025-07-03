
from django.test import TestCase
from django.urls import reverse
from restaurant.models import Menu  # Adjust the import based on your project structure
from restaurant.serializers import MenuSerializer  # Adjust the import based on your project structure

class MenuViewTest(TestCase):

    def setUp(self):
        # Create test instances of the Menu model
        self.menu1 = Menu.objects.create(name="Burger", price=5.99)
        self.menu2 = Menu.objects.create(name="Pizza", price=7.99)
        self.menu3 = Menu.objects.create(name="Salad", price=4.99)

    def test_getall(self):
        # Use the test client to retrieve the Menu objects
        response = self.client.get(reverse('menu-list'))  # Adjust 'menu-list' to your URL name

        # Serialize the data
        expected_data = MenuSerializer(Menu.objects.all(), many=True).data
        
        # Assertions to check if the response data matches the expected data
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data, expected_data)