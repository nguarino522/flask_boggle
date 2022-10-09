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


    def test_game_route(self):
        """full testing for the game route and functionality"""

        with app.test_client() as client:
            resp = client.get("/game")
            self.assertEqual(resp.status_code, 200)
            self.assertIn('board', session)
            self.assertIsNone(session.get("highscore"))
            self.assertIsNone(session.get("numplays"))


    def test_valid_word(self):
        """test if a word is valid"""

        with app.test_client() as client:
            with client.session_transaction() as session:
                session["board"] = [["C", "A", "T", "T", "T"],
                                    ["C", "A", "T", "T", "T"],
                                    ["C", "A", "T", "T", "T"],
                                    ["G", "A", "T", "T", "T"],
                                    ["C", "A", "T", "T", "T"]]
        resp = client.get("/wordcheck?word=tag")
        self.assertEqual(resp.json['result'], 'ok')


    def test_invalid_word(self):
        """test if a word is invalid and not in app dictionary"""

        self.client.get("/game")
        resp = self.client.get("/wordcheck?word=asdf")
        self.assertEqual(resp.json['result'], 'not-word')


    def test_word_not_on_board(self):
        """test if a word is valid but not found on board"""

        self.client.get("/game")
        resp = self.client.get("/wordcheck?word=peanut")
        self.assertEqual(resp.json['result'], 'not-on-board')
