import requests as r
import os
import environ

env = environ.Env()
environ.Env.read_env()

class Email:
    def __init__(self, email, token, name):
        self.email = email
        self.name = name
        self.token = token

    def send(self):
        url = 'https://api.sendinblue.com/v3/smtp/email/'
        headers = {
            "Content-Type": "application/json", 
            "Accept": "application/json",
            "api-key": os.getenv('BREVO_API_KEY')
            }
        data = {
            "to": [
                {"email": self.email, "name": self.name}
            ],
            "headers": {
                "newKey": "New Value"
            },
            "params": {
                "token": self.token
            },
            "templateId": 1
        } 

        return r.post(url, json = data, headers = headers)