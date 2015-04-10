import subprocess
import json
from websocket import create_connection

class Pushbullet():
	def __init__(self):
		self.user_token = 'YOUR USER TOKEN'
		self.user_token_metadata = json.loads(subprocess.check_output(['curl','--header','Authorization: Bearer '+self.user_token,'https://api.pushbullet.com/v2/users/me']))
		self.user_token_name = self.user_token_metadata['name']
		self.user_token_email = self.user_token_metadata['email']

		self.user_id = self.user_token_metadata['iden']

		self.pt1 = ['curl','--header','Authorization: Bearer '+self.user_token,'-X']

		self.mobile_id = 'MOBILE DEVICES IDEN'
		self.reply_to_number = "Phone Number"
		self.reply_to_name = "Person"

	def push_note(self, title = 'Unspecified', body = 'Unspecified'):
		self.pt2 = [
			'POST',
			'https://api.pushbullet.com/v2/pushes',
			'--header',
			'Content-Type: application/json',
			'--data-binary',
			'{"type": "note", "title": "'+title+'", "body": "'+body+'"}']

		subprocess.call(self.pt1+self.pt2)

	def push_link(self, title, body,url):
		self.pt2 = [
			'POST',
			'https://api.pushbullet.com/v2/pushes',
			'--header',
			'Content-Type: application/json',
			'--data-binary',
			'{"type": "link", "title": "'+title+'", "body": "'+body+'", "url": "'+url+'"}']

		subprocess.call(self.pt1+self.pt2)

	def push_file(self, name, mime, url, body):
		self.pt2 = [
			'POST',
			'https://api.pushbullet.com/v2/pushes',
			'--header',
			'Content-Type: application/json',
			'--data-binary',
			'{"type": "file", "file_name": "'+name+'", "file_mime": "'+mime+'", "file_url": "'+url+'", "body": "'+body+'"}']

		subprocess.call(self.pt1+self.pt2)

	def get_pushes(self, modified_after=0):
		self.pt2 = [
			'GET',
			'https://api.pushbullet.com/v2/pushes?modified_after='+str(modified_after)]
		output = subprocess.check_output(self.pt1+self.pt2)
		output = json.loads(output)
		return output['pushes']

	def push_sms(self, mobile_number, message):
		self.pt2 = [
			'POST',
			'https://api.pushbullet.com/v2/ephemerals',
			'--header',
			'Content-Type: application/json',
			'--data-binary',
			'{"type": "push", "push": {"type": "messaging_extension_reply", "package_name": "com.pushbullet.android", "source_user_iden": "'+self.user_id+'", "target_device_iden": "'+self.mobile_id+'", "conversation_iden": "'+mobile_number+'", "message": "'+message+'"}}']

		subprocess.call(self.pt1+self.pt2)

	def push_delete_all(self,e):
		self.pt2 = [
			'DELETE',
			'https://api.pushbullet.com/v2/pushes']

		subprocess.call(self.pt1+self.pt2)

	def socket_connect(self):
		return create_connection('wss://stream.pushbullet.com/websocket/'+self.user_token)

	def socket_check(self, ws):
		return json.loads(ws.recv())