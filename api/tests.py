from django.test import TestCase
import requests

# Create your tests here.
class TicTacBoardTests(TestCase):
	def test_missing_board_param_status_code(self):
		response = requests.get("http://127.0.0.1:8000?boards=+xzo++o+x")
		self.assertEquals(response.status_code, 400)

	def test_invalid_characters_status_code(self):
		response = requests.get("http://127.0.0.1:8000?board=+xzo++o+x")
		self.assertEquals(response.status_code, 400)

	def test_character_count_status_code(self):
		response = requests.get("http://127.0.0.1:8000?board=+xxo++o+xx")
		self.assertEquals(response.status_code, 400)

	def test_valid_board_status_code(self):
		response = requests.get("http://127.0.0.1:8000?board=+xxo++x+x")
		self.assertEquals(response.status_code, 400)
		
	def test_game_won_status_code(self):
		response = requests.get("http://127.0.0.1:8000?board=xxxo++o+x")
		self.assertEquals(response.status_code, 400)