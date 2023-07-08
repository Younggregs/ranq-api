import requests as r
import environ

env = environ.Env()
environ.Env.read_env()

class Email:
    
    @staticmethod
    def send(email, token, page, templateId, title="", name="", pollToken=False):
        link = env('UI_URL') + '/'
        if templateId == 1:
            link = link + page + '?token=' + str(token)
            if pollToken:
                link = link + '&poll=' + str(pollToken)
        elif templateId == 6:
            link = env('UI_URL')
        elif templateId == 3:
            link = env('UI_URL') + '/' + page + '/' + str(token) 
        else:
            link = env('UI_URL') + '/' + str(token)
        
        url = 'https://api.brevo.com/v3/smtp/email'
        headers = {
            "Content-Type": "application/json", 
            "Accept": "application/json",
            "api-key": env('BREVO_API_KEY')
            }
        data = {
            "to": [
                {"email": email, "name": email}
            ],
            "headers": {
                "X-Mailin-custom":"custom_header_1:custom_value_1|custom_header_2:custom_value_2|custom_header_3:custom_value_3",
                "charset":"iso-8859-1"
            },
            "params": {
                "link": link,
                "title": title, 
                "name": name,
            },
            "templateId": templateId,
        } 

        return r.post(url, json = data, headers = headers)