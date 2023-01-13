from rest_framework.test import APITestCase, APIRequestFactory, force_authenticate
from rest_framework_simplejwt.views import TokenObtainPairView

from product.models import *
from product.views import CategoryAPIView, ProductAPIView
from django.contrib.auth import get_user_model
User = get_user_model()


class CategoryTest(APITestCase):
    """
    Test category view
    """

    def setUp(self):
        self.factory = APIRequestFactory()
        self.setup_category()
        self.user = self.setup_user()



    def setup_user(self):
        return User.objects.create_user('test@test.com', '1', is_active=True)




    def setup_category(self):
        # list_of_category = [Category('category1'), Category('category2'), Category('category3')]

        list_of_category = []
        for i in range(1, 100):
            list_of_category.append(Category(f'category{i}'))
        print(list_of_category)
        Category.objects.bulk_create(list_of_category)
        # Category.objects.create(title='category1')
        # Category.objects.create(title='category2')
        # Category.objects.create(title='category3')

    def test_get_category(self):
        request = self.factory.get('product/category/')
        view = CategoryAPIView.as_view({'get': 'list'})
        response = view(request)

        assert response.status_code == 200
        assert Category.objects.count() == 99
        assert Category.objects.first().title == 'category1'

    def test_post_category(self):
        data = {
            'title': 'test'
        }
        request = self.factory.post('product/category/', data)
        force_authenticate(request, user=self.user)
        view = CategoryAPIView.as_view({'post': 'create'})
        response = view(request)
        print(response.status_code)
        assert response.status_code == 201
        assert Category.objects.filter(title='test').exists()


class ProductTest(APITestCase):
    """
    Test category view
    """

    def setUp(self):
        self.factory = APIRequestFactory()
        self.setup_category()
        self.user = self.setup_user()
        self.setup_product()
        self.access_token = self.setup_user_token()

    def setup_user_token(self):
        data = {
            'email': 'test@test.com',
            'password': '1'
        }
        request = self.factory.post('account/login/', data)
        view = TokenObtainPairView.as_view()

        response = view(request)
        return response.data['access']

    def setup_user(self):
        return User.objects.create_user('test@test.com', '1', is_active=True)

    def setup_category(self):
        Category.objects.create(title='test_product1')

    def setup_product(self):
        products = [
            Product(owner=self.user, category=Category.objects.first(), price=20, image='test', title='test'),
            Product(owner=self.user, category=Category.objects.first(), price=20, image='test', title='test2')
        ]
        Product.objects.bulk_create(products)

    def test_get_product(self):
        request = self.factory.get('product/')
        view = ProductAPIView.as_view({'get': 'list'})
        response = view(request)

        assert response.status_code == 200
        # assert Category.objects.count() == 99
        # assert Category.objects.first().title == 'category1'

    def test_post_product(self):
        image = open('media/images/b4cd7935.jpg', 'rb')
        data = {
            # 'owner_id': self.user.id,
            'category': Category.objects.first().title,
            'title': 'test_post',
            'price': 20,
            'image': image
        }
        print("DATA", data)
        request = self.factory.post('product/', data, HTTP_AUTHORIZATION='Bearer ' + self.access_token)
        image.close()
        view = ProductAPIView.as_view({'post': 'create'})
        #
        response = view(request)
        # print(response.data)
        # assert response.status_code == 201
        # assert Product.objects.count() == 2
        # assert Category.objects.filter(title='test').exists()