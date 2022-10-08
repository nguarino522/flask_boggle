from unittest import TestCase
from app import app
from flask import session
from boggle import Boggle


class FlaskTests(TestCase):

    # TODO -- write tests for every view function / feature!

    def setUp(self):
        """set before each test"""

        self.client = app.test_client()
        app.config['TESTING'] = True

    def test_homepage(self):
        """testing the default base route"""

        with app.test_client() as client:
            resp = client.get('/')
            self.assertEqual(resp.status_code, 200)
            self.assertIn(b'input id="startbtn', resp.data)

    def test_game_route(self):
        """full testing for the game route and functionality"""

        with app.test_client() as client:
            resp = client.get("/game")
            self.assertEqual(resp.status_code, 200)
            self.assertIsNone(session.get("highscore"))
            self.assertIsNone(session.get("numplays"))
            #self.assertIn(b'<p>High Score:', resp.data)