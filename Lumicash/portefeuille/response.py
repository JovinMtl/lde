"""THis is about the response to send back"""
import requests

class Answer:
    """Answer that the owner has approved to pay.
    say the user with phone number XXXXXX has approved the payment of 
    XXXXX amount.
    This information could be used for the requester(server) to search
    into his database the corresponding entry and act accordingly"""
    def __init__(self, phone_number, amount, status_code,\
                 code_transaction) -> None:
        self.data = {
            'phone_number': phone_number,
            'amount' : amount,
            'code_transaction': code_transaction,
            'status_code' : status_code,
        }
        self.url_server = 'http://127.0.0.1:8002/jov/api/reque//answer/'
    
    def reply(self):
        response = requests.post(self.url_server, self.data)
        if response.status_code == 200:
            print(f"The answer has been well delivered: \
                  {response.json()}")
            return 25
        else:
            return 21