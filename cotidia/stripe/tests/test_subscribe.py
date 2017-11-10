import os

from django.test import TestCase, Client
from django.core.urlresolvers import reverse

from cotidia.account import fixtures
from cotidia.testimonial.models import Testimonial
from cotidia.testimonial.factory import TestimonialFactory
from .utils import generate_image_file


class TestimonialAdminTests(TestCase):

    @fixtures.normal_user
    def setUp(self):

        # Create the client and login the user
        self.c = Client()
        self.c.login(
            username=self.normal_user.username,
            password=self.normal_user_pwd)

    def test_subscribe(self):
        """Test that we can subscribe to a plan."""

        url = reverse('testimonial-admin:testimonial-add')

        # Test that the page load first
        response = self.c.get(url)
        self.assertEqual(response.status_code, 200)

        image_file = generate_image_file()

        # Send data
        data = {
            'name': 'Jack Green',
            'role': 'Developer',
            'comment': 'Great work.',
            'photo': image_file,
            'active': True
        }
        response = self.c.post(url, data)
        self.assertEqual(response.status_code, 302)

        # Get the latest added object
        obj = Testimonial.objects.filter().latest('id')
        self.assertEqual(obj.name, data['name'])
        self.assertEqual(obj.role, data['role'])
        self.assertEqual(obj.comment, data['comment'])
        self.assertEqual(obj.photo, data['photo'])
        self.assertEqual(obj.active, data['active'])

    # def test_update_testimonial(self):
    #     """Test that we can update an existing object."""

    #     url = reverse(
    #         'testimonial-admin:testimonial-update',
    #         kwargs={
    #             'pk': self.object.id
    #         }
    #     )

    #     # Test that the page load first
    #     response = self.c.get(url)
    #     self.assertEqual(response.status_code, 200)

    #     image_file = generate_image_file()

    #     # Send data
    #     data = {
    #         'name': 'Jack Green',
    #         'role': 'Developer',
    #         'comment': 'Great work.',
    #         'photo': image_file,
    #         'active': True
    #     }
    #     response = self.c.post(url, data)
    #     self.assertEqual(response.status_code, 302)

    #     # Get the latest added object
    #     obj = Testimonial.objects.get(id=self.object.id)
    #     self.assertEqual(obj.name, data['name'])
    #     self.assertEqual(obj.role, data['role'])
    #     self.assertEqual(obj.comment, data['comment'])
    #     self.assertEqual(obj.photo, data['photo'])
    #     self.assertEqual(obj.active, data['active'])

    # def test_retrieve_testimonial(self):
    #     """Test that we can retrieve an object from its ID."""

    #     url = reverse(
    #         'testimonial-admin:testimonial-detail',
    #         kwargs={
    #             'pk': self.object.id
    #         }
    #     )

    #     # Test that the page load first
    #     response = self.c.get(url)
    #     self.assertEqual(response.status_code, 200)

    # def test_list_testimonial(self):
    #     """Test that we can list objects."""

    #     url = reverse('testimonial-admin:testimonial-list')

    #     # Test that the page load first
    #     response = self.c.get(url)
    #     self.assertEqual(response.status_code, 200)

    # def test_delete_testimonial(self):
    #     """Test that we can delete an object."""

    #     url = reverse(
    #         'testimonial-admin:testimonial-delete',
    #         kwargs={
    #             'pk': self.object.id
    #         }
    #     )

    #     # Test that the page load first
    #     response = self.c.get(url)
    #     self.assertEqual(response.status_code, 200)

    #     # Action detail with POST call
    #     response = self.c.post(url)
    #     self.assertEqual(response.status_code, 302)

    #     # Test that the record has been deleted
    #     obj = Testimonial.objects.filter(id=self.object.id)
    #     self.assertEqual(obj.count(), 0)
