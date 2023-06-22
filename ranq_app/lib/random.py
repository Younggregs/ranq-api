import secrets
import string

class Random:
    
    @staticmethod
    def generate_random_string(length=19):
        return ''.join(secrets.choice(string.ascii_uppercase + string.digits)
              for i in range(length))