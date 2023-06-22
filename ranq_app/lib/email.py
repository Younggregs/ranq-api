import requests as r
import environ

env = environ.Env()
environ.Env.read_env()

class Email:
    def __init__(self, email, token, page, templateId):
        self.email = email
        self.link = env('UI_URL') + '/' + page + '?token=' + str(token)
        self.templateId = templateId

    def send(self):
        url = 'https://api.brevo.com/v3/smtp/email'
        headers = {
            "Content-Type": "application/json", 
            "Accept": "application/json",
            "api-key": env('BREVO_API_KEY')
            }
        data = {
            "to": [
                {"email": self.email, "name": self.email}
            ],
            "headers": {
                "X-Mailin-custom":"custom_header_1:custom_value_1|custom_header_2:custom_value_2|custom_header_3:custom_value_3",
                "charset":"iso-8859-1"
            },
            "params": {
                "link": self.link
            },
            "templateId": self.templateId,
        } 

        return r.post(url, json = data, headers = headers)