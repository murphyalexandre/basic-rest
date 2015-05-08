import unittest
import json

from app import app, db
from app.models import Car


class BasicRestTestCase(unittest.TestCase):
    """ Basic tests for our basic-rest app """

    def add_car(self, title, message, user):
        post = Post(
            title=title,
            message=message,
            user=user
        )

        db.session.add(post)
        db.session.commit()

        return post

    def get_json_headers(self, json_data):
        headers = [('Content-Type', 'application/json')]
        headers.append(('Content-Length', len(json_data)))

        return headers

    def setUp(self):
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///'
        app.config['TESTING'] = True
        self.app = app.test_client()
        db.create_all()

        # Create one car
        car = Car(
                description="Test",
                cylinders=6,
                make="Make",
                model="Model",
                year=2014,
                owner="Someone",
                image="http://sunshinedrugs.com/wp-content/uploads/2015/03/55BuickStudioShoot__0031EDIT2.jpg"
        )

        db.session.add(car)
        db.session.commit()

    def tearDown(self):
        db.drop_all()

    # TESTS
    def test_car_list(self):
        rv = self.app.get('/api/v1/cars', follow_redirects=True)

        self.assertEqual(rv.status_code, 200)

        # We only have the latest 5 posts
        self.assertIn(b'Test', rv.data)
        self.assertIn(b'Make', rv.data)
        self.assertIn(b'Model', rv.data)
        self.assertIn(b'Someone', rv.data)

    def test_car(self):
        rv = self.app.get('/api/v1/cars/1', follow_redirects=True)

        self.assertEqual(rv.status_code, 200)

        # We only have the latest 5 posts
        self.assertIn(b'Test', rv.data)
        self.assertIn(b'Make', rv.data)
        self.assertIn(b'Model', rv.data)
        self.assertIn(b'Someone', rv.data)

    def test_car_invalid_id(self):
        rv = self.app.get('/api/v1/cars/0', follow_redirects=True)

        self.assertEqual(rv.status_code, 404)

    def test_new_car(self):
        data = {
            "description": "Another",
            "cylinders": 8,
            "make": "Ford",
            "model": "Taurus",
            "year": 2013,
            "owner": "Else",
            "image": "http://sunshinedrugs.com/wp-content/uploads/2015/03/55BuickStudioShoot__0031EDIT2.jpg"
        }
        json_data = json.dumps(data)

        rv = self.app.post('/api/v1/cars', headers=self.get_json_headers(json_data), data=json_data)

        self.assertEqual(rv.status_code, 200)

        # We only have the latest 5 posts
        self.assertIn(b'Another', rv.data)
        self.assertIn(b'Ford', rv.data)
        self.assertIn(b'Taurus', rv.data)
        self.assertIn(b'Else', rv.data)

    def test_new_car_missing_data(self):
        data = {
            "description": "Another",
            "cylinders": 8,
            "make": "Ford"
        }
        json_data = json.dumps(data)

        rv = self.app.post('/api/v1/cars', headers=self.get_json_headers(json_data), data=json_data)

        self.assertEqual(rv.status_code, 400)

    def test_update_car(self):
        data = {
            "id": 1,
            "description": "Another",
            "cylinders": 8,
            "make": "Ford",
            "model": "Taurus",
            "year": 2013,
            "owner": "Else",
            "image": "http://sunshinedrugs.com/wp-content/uploads/2015/03/55BuickStudioShoot__0031EDIT2.jpg"
        }
        json_data = json.dumps(data)

        rv = self.app.put('/api/v1/cars/1', headers=self.get_json_headers(json_data), data=json_data)

        self.assertEqual(rv.status_code, 200)

        # We only have the latest 5 posts
        self.assertIn(b'Another', rv.data)
        self.assertIn(b'Ford', rv.data)
        self.assertIn(b'Taurus', rv.data)
        self.assertIn(b'Else', rv.data)

    def test_update_car_invalid_id(self):
        data = {
            "id": 0,
            "description": "Another",
            "cylinders": 8,
            "make": "Ford",
            "model": "Taurus",
            "year": 2013,
            "owner": "Else",
            "image": "http://sunshinedrugs.com/wp-content/uploads/2015/03/55BuickStudioShoot__0031EDIT2.jpg"
        }
        json_data = json.dumps(data)

        rv = self.app.put('/api/v1/cars/0', headers=self.get_json_headers(json_data), data=json_data)

        self.assertEqual(rv.status_code, 404)

    def test_partial_update_car(self):
        data = {
            "id": 1,
            "description": "Update",
            "make": "Toyota",
            "model": "Corolla"
        }
        json_data = json.dumps(data)

        rv = self.app.put('/api/v1/cars/1', headers=self.get_json_headers(json_data), data=json_data)

        self.assertEqual(rv.status_code, 200)

        # We only have the latest 5 posts
        self.assertIn(b'Update', rv.data)
        self.assertIn(b'Toyota', rv.data)
        self.assertIn(b'Corolla', rv.data)

    def test_delete_car(self):
        rv = self.app.delete('/api/v1/cars/1')

        self.assertEqual(rv.status_code, 204)

        rv = self.app.get('/api/v1/cars', follow_redirects=True)

        self.assertEqual(rv.status_code, 200)

        # We only have the latest 5 posts
        self.assertNotIn(b'Test', rv.data)
        self.assertNotIn(b'Make', rv.data)
        self.assertNotIn(b'Model', rv.data)
        self.assertNotIn(b'Someone', rv.data)

    def test_delete_car_invalid_id(self):
        rv = self.app.delete('/api/v1/cars/0')

        self.assertEqual(rv.status_code, 404)


if __name__ == '__main__':
    unittest.main()
