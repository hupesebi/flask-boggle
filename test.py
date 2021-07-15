from unittest import TestCase
from app import app
from flask import session
from boggle import Boggle




    # TODO -- write tests for every view function / feature!

class FlaskTests(TestCase):

    def setUp(self):

        self.client = app.test_client()
        app.config['TESTING'] = True

    def test_homepage(self):

        with self.client:
            response = self.client.get('/')
            self.assertIn('board', session)
            self.assertIsNone(session.get('highscore'))
            self.assertIsNone(session.get('nplays'))
            self.assertIn(b'<p>High Score:', response.data)
            self.assertIn(b'Score:', response.data)
            self.assertIn(b'Seconds Left:', response.data)

    def test_valid_word(self):

        with self.client as client:
            with client.session_transaction() as sess:
                sess['board'] = [["H", "E", "L", "L", "O"], 
                                 ["A", "A", "A", "A", "A"], 
                                 ["T", "T", "T", "T", "T"], 
                                 ["T", "T", "T", "T", "T"], 
                                 ["T", "T", "T", "T", "T"]]
        response = self.client.get('/check-word?word=hello')
        self.assertEqual(response.json['result'], 'ok')

    def test_notonboard_word(self):

        self.client.get('/')
        response = self.client.get('/check-word?word=test')
        self.assertEqual(response.json['result'], 'not-on-board')

    def test_not_english_word(self):

        self.client.get('/')
        response = self.client.get(
            '/check-word?word=brrrrrrr')
        self.assertEqual(response.json['result'], 'not-word')