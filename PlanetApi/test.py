import unittest
import json
from app import app


class TestRoutes(unittest.TestCase):
    # User registration params
    first_name = "test6"
    last_name = "user"
    email = "{}@mailinator.com".format(first_name)
    password = 'password'
    # Add planet params
    planet_name = '331h'
    planet_type = 'Class M'
    home_star = 'Proxima Centurai'
    mass = '567e8'
    radius = '356e4'
    distance = '456e560'
    # update planet params
    update_planet_name = planet_name + "_update"
    planet_id = 9

    def setUp(self):
        self.app = app.test_client()
        self.app.testing = True

    def test_home_page(self):
        response = self.app.get('/')
        data = json.loads(response.data.decode('utf-8'))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['message'], 'Welcome to Planetary API!')

    def test_get_all_planets(self):
        response = self.app.get('/planets')
        data = json.loads(response.data.decode('utf-8'))
        self.assertEqual(response.status_code, 200)
        self.assertTrue(len(data) > 0)  # Ensure data is returned

    def test_register_user(self):
        response = self.app.post('/register',
                                 data={'first_name': self.first_name,
                                       'last_name': self.last_name,
                                       'email': self.email,
                                       'password': self.password})
        data = json.loads(response.data.decode('utf-8'))

        print(data)

        self.assertEqual(response.status_code, 201)
        self.assertEqual(data['message'], 'User created successfully')

    def test_user_login(self):
        response = self.app.post('/login', data={'email': self.email, 'password': self.password})
        data = json.loads(response.data.decode('utf-8'))
        self.assertEqual(response.status_code, 200)
        self.assertTrue('access_token' in data)  # Ensure access token is returned
        print(data['access_token'])

    def test_add_planet(self):
        headers = {
            'Authorization': 'Bearer ' + self.user_login(),
        }
        response = self.app.post('/add_planet', headers=headers,
                                 data={'planet_name': self.planet_name,
                                       'planet_type': self.planet_type,
                                       'home_star': self.home_star,
                                       'mass': self.mass,
                                       'radius': self.radius,
                                       'distance': self.distance})
        print(response)
        data = json.loads(response.data.decode('utf-8'))
        print(data)
        self.assertEqual(response.status_code, 201)

    def test_update_planet(self):
        headers = {
            'Authorization': 'Bearer ' + self.user_login(),
        }
        response = self.app.post('/add_planet', headers=headers,
                                 data={'planet_id': self.planet_id,
                                       'planet_name': self.update_planet_name,
                                       'planet_type': self.planet_type,
                                       'home_star': self.home_star,
                                       'mass': self.mass,
                                       'radius': self.radius,
                                       'distance': self.distance})
        print(response)
        data = json.loads(response.data.decode('utf-8'))
        print(data)
        self.assertEqual(response.status_code, 201)

    def test_delete_planet(self):
        headers = {
            'Authorization': 'Bearer ' + self.user_login(),
        }
        response = self.app.delete('/remove_planet/{}'.format(5), headers=headers)
        data = json.loads(response.data.decode('utf-8'))
        self.assertEqual(response.status_code, 202)
        self.assertTrue(len(data) > 0)  # Ensure data is returned

    def user_login(self):
        response = self.app.post('/login', data={'email': self.email, 'password': self.password})
        data = json.loads(response.data.decode('utf-8'))
        return data['access_token']


if __name__ == '__main__':
    test_order = ['test_home_page', 'test_get_all_planets', 'test_register_user', 'test_user_login', 'test_add_planet',
                  'test_update_planet', 'test_delete_planet']
    loader = unittest.TestLoader()
    loader.sortTestMethodsUsing = lambda x, y: test_order.index(x) - test_order.index(y)
    unittest.main()
