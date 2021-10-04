from django.contrib.auth import get_user_model
from rest_framework.test import APITestCase

from backend.app.models import Recipes

User = get_user_model()


class RecipesAPITestCase(APITestCase):
    def detUp(self):
        user_obj = User(username='testuser',
                        email='test@test.com',
                        first_name='Testname',
                        last_name='Testov',
                        )
        user_obj.set_password('Tel-555555')
        user_obj.save()
        recipes = Recipes.objects.create(
            user=user_obj,
            tags=[1, 2],
            image="data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABAgMAAABieywaAAAACVBMVEUAAAD///9fX1/S0ecCAAAACXBIWXMAAA7EAAAOxAGVKw4bAAAACklEQVQImWNoAAAAggCByxOyYQAAAABJRU5ErkJggg==",
            name='string',
            text='string',
            cooking_time=1,
            #     ingredients={[
            #         {
            #             "id": 1123,
            #             "amount": 10
            #         }
            #     ],
            #
            # }
        )

    def test_single_user(self):
        user_count = User.objects.count()
        self.assertEqual(user_count,1)
