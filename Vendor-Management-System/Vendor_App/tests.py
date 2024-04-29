from rest_framework.test import APITestCase
from rest_framework import status
from django.urls import reverse
from django.contrib.auth.models import User
from .models import Vendor, PurchaseOrder

class APITests(APITestCase):
    def setUp(self):
        self.superuser = User.objects.create_superuser(username='admin', password='admin123', email='admin@example.com')
        self.token = self.obtain_token()

    def obtain_token(self):
        response = self.client.post(reverse('api_token_auth'), {'username': 'admin', 'password': 'admin123'})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        return response.data['token']

    def test_create_vendor(self):
        url = reverse('vendor-list-create')
        data = {'vendor_code': 'V1', 'name': 'Vendor 1', 'contact_details': 'Contact 1', 'address': 'Address 1'}
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token)
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_list_vendors(self):
        url = reverse('vendor-list-create')
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token)
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_retrieve_vendor(self):
        vendor = Vendor.objects.create(name='Test Vendor', contact_details='Test Contact', address='Test Address', vendor_code='V1')
        url = reverse('vendor-retrieve-update-delete', kwargs={'pk': vendor.pk})
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token)
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_update_vendor(self):
        vendor = Vendor.objects.create(name='Test Vendor', contact_details='Test Contact', address='Test Address', vendor_code='V1')
        url = reverse('vendor-retrieve-update-delete', kwargs={'pk': vendor.pk})
        data = {'name': 'Updated Vendor Name'}
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token)
        response = self.client.patch(url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_delete_vendor(self):
        vendor = Vendor.objects.create(name='Test Vendor', contact_details='Test Contact', address='Test Address', vendor_code='V1')
        url = reverse('vendor-retrieve-update-delete', kwargs={'pk': vendor.pk})
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token)
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_create_purchase_order(self):
        vendor = Vendor.objects.create(name='Test Vendor', contact_details='Test Contact', address='Test Address', vendor_code='V1')
        url = reverse('purchase-order-list-create')
        data = {'po_number': 'PO001', 'vendor': vendor.pk, 'order_date': '2023-01-01T12:00:00', 'delivery_date': '2023-01-10T12:00:00', 'status': 'pending'}
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token)
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_list_purchase_orders(self):
        url = reverse('purchase-order-list-create')
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token)
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_retrieve_purchase_order(self):
        vendor = Vendor.objects.create(name='Test Vendor', contact_details='Test Contact', address='Test Address', vendor_code='V1')
        po = PurchaseOrder.objects.create(po_number='PO001', vendor=vendor, status='pending')
        url = reverse('purchase-order-retrieve-update-delete', kwargs={'pk': po.pk})
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token)
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_update_purchase_order(self):
        vendor = Vendor.objects.create(name='Test Vendor', contact_details='Test Contact', address='Test Address', vendor_code='V1')
        po = PurchaseOrder.objects.create(po_number='PO001', vendor=vendor, status='pending')
        url = reverse('purchase-order-retrieve-update-delete', kwargs={'pk': po.pk})
        data = {'status': 'completed'}
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token)
        response = self.client.patch(url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_delete_purchase_order(self):
        vendor = Vendor.objects.create(name='Test Vendor', contact_details='Test Contact', address='Test Address', vendor_code='V1')
        po = PurchaseOrder.objects.create(po_number='PO001', vendor=vendor, status='pending')
        url = reverse('purchase-order-retrieve-update-delete', kwargs={'pk': po.pk})
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token)
