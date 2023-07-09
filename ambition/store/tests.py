from http import HTTPStatus

from django.test import TestCase

from store.models import Category

# Create your tests here.


class CategoryViewTest(TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        super().setUpClass()
        for i in range(3):
            category = Category(name=f'카테고리 {i}')
            category.save()

    def test_get(self):
        response = self.client.get('/category')
        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertEqual(len(response.json()['data']['categories']), 3)
