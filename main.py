from kivy.app import App
from kivy.lang import Builder
from kivy.uix.screenmanager import Screen, ScreenManager
from kivy.uix.image import Image
from kivy.uix.behaviors import ButtonBehavior
from hoverable import HoverBehavior
import json, glob, random
from datetime import datetime
from pathlib import Path

Builder.load_file('design.kv')

class LoginScreen(Screen):
	def sign_up(self):
		self.manager.current = "signup_screen"
	
	def login(self, username, password):
		with open ("users.json") as file:
			users = json.load(file)
		if username in users and users[username]["password"] == password:
			self.manager.current = "main_screen"
		else:
			self.ids.login_error.text = "Wrong user or password!"

	def forgot_pass(self):
		self.manager.transition.direction = 'up'
		self.manager.current = "forgot_password" 

class SignUpScreen(Screen):
	def add_user(self, username, password):
		with open ("users.json") as file:
			users = json.load(file)
		users[username] = {'username': username, 'password': password,
							'created': datetime.now().strftime("%Y-%m-%d %H:%M:%S") }
		with open ("users.json", "w") as file:
			json.dump(users, file)
		self.manager.current = "signup_success"

class SignUpSuccess(Screen):
	def back2start(self):
		self.manager.transition.direction = 'right'
		self.manager.current = "login_screen"

class MainScreen(Screen):
	def log_out(self):
		self.manager.transition.direction = 'right'
		self.manager.current = "login_screen"

	def quote(self, feeling):
		available_feels = [Path(filename).stem for filename 
							in glob.glob('quotes/*.txt')]
		
		if feeling.lower() in available_feels:
			with open(f'quotes/{feeling}.txt', encoding="utf8") as file:
				quotes = file.readlines()
				self.ids.quote.text = random.choice(quotes)	
		else:
			self.ids.quote.text = "Try another feeling!"

class ForgotPassword(Screen):
	def back_login(self):
		self.manager.transition.direction = 'down'
		self.manager.current = 'login_screen'

	def retrieve(self, username):
		with open ("users.json") as file:
			users = json.load(file)
		if username in users.keys():
			self.ids.password.text = f"Your password is {users[username]['password']}."
		else:
			self.ids.password.text = "Username not found! Please enter a valid one."	

class RootWidget(ScreenManager):
	pass

class ImageButton (HoverBehavior, ButtonBehavior, Image):
	pass

class MainApp(App):
	def build(self):
		return RootWidget()

if __name__ == "__main__":
	MainApp().run()