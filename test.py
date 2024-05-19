#!/usr/bin/env python
import unittest
from app import create_app, db
from app.models import User, Challenge, Submission, ActiveChallenge, CompletedChallenge
from config import Config
from flask import url_for

class TestConfig(Config):
    TESTING = True
    SQLALCHEMY_DATABASE_URI = 'sqlite://'
    SERVER_NAME = 'localhost'
    APPLICATION_ROOT = '/'
    PREFERRED_URL_SCHEME = 'http'

class UserModelCase(unittest.TestCase):
    def setUp(self):
        self.app = create_app(TestConfig)
        self.app_context = self.app.app_context()
        self.app_context.push()
        db.create_all()
        self.client = self.app.test_client()

        self.user = User(username='testuser', email='test@example.com')
        self.user.set_password('password')
        db.session.add(self.user)
        db.session.commit()
        self.login()

    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.app_context.pop()

    def login(self):
        self.client.post(url_for('auth.login'), data={
            'username': 'testuser',
            'password': 'password'
        })

    def test_password_hashing(self):
        u = User(username='testuser', email='testuser@example.com')
        u.set_password('cat')
        self.assertFalse(u.check_password('dog'))
        self.assertTrue(u.check_password('cat'))

    def test_avatar(self):
        u = User(username='john', email='john@example.com')
        self.assertEqual(u.avatar(128), ('https://www.gravatar.com/avatar/'
                                         'd4c74594d841139328695756648b6bd6'
                                         '?d=identicon&s=128'))

    def test_create_challenge(self):
        challenge_data = {
            'title': 'Test Challenge',
            'recipe_type': 'Challenge',
            'description': 'This is a test challenge.',
            'is_recipe': True,
            'ingredients': 'Ingredient 1, Ingredient 2',
            'recipe_instructions': 'Step 1, Step 2',
            'cuisine_type': 'North American',
            'cuisine_style': 'Home Cook',
            'difficulty_level': 3,
            'author': self.user
        }
        challenge = Challenge(**challenge_data)
        db.session.add(challenge)
        db.session.commit()

        retrieved_challenge = Challenge.query.filter_by(title='Test Challenge').first()
        self.assertIsNotNone(retrieved_challenge)
        self.assertEqual(retrieved_challenge.description, 'This is a test challenge.')

    def test_view_challenge(self):
        challenge = Challenge(
            title='Test Challenge',
            recipe_type='Challenge',
            description='This is a test challenge.',
            is_recipe=True,
            ingredients='Ingredient 1, Ingredient 2',
            recipe_instructions='Step 1, Step 2',
            cuisine_type='North American',
            cuisine_style='Home Cook',
            difficulty_level=3,
            author=self.user
        )
        db.session.add(challenge)
        db.session.commit()

        response = self.client.get(url_for('main.challenge', challenge_id=challenge.id))
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Test Challenge', response.data)
        self.assertIn(b'Ingredient 1', response.data)
        self.assertIn(b'Step 1', response.data)

    def test_view_non_recipe_challenge(self):
        challenge = Challenge(
            title='Test Non-Recipe Challenge',
            recipe_type='Challenge',
            description='This is a test non-recipe challenge.',
            is_recipe=False,
            ingredients='',
            recipe_instructions='',
            cuisine_type='North American',
            cuisine_style='Home Cook',
            difficulty_level=3,
            author=self.user
        )
        db.session.add(challenge)
        db.session.commit()

        response = self.client.get(url_for('main.challenge', challenge_id=challenge.id))
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Test Non-Recipe Challenge', response.data)
        self.assertNotIn(b'Ingredients', response.data)
        self.assertNotIn(b'Recipe Instructions', response.data)

if __name__ == '__main__':
    unittest.main(verbosity=2)
