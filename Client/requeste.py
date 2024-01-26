import requests
from requests.exceptions import JSONDecodeError


class UserBrowising:

    def __init__(self):
        # Data to be sent
        self.data = {
            'username': 'jovino',
            # 'password': 'done',
            'password': 'done1234',
            'amount_t_cred' : 14000,
        }
        self.data_new_user = {
            'username': 'jovin',
            'password': 'done1234',
        }
        self.data_fund = {
            'username': 'jovino',
            'password': 'done1234',
            'receiver_number':62111333,
            'amount_to_send':500,
        }
        self.data_lumi = {
            'username': 'Lde',
            'password': 'done1234',
            'debtor_number':62111333,
            'amount_to_pay':500,
        }
        self.data_fund_upload = {
            'username': 'jovin',
            'password': 'done1234',
            'amount_to_deb': 2000,
            'number_to_deb': 62111333

        }

        # URL of the server
        self.url = 'http://127.0.0.1:8000/jov/api/lo/'
        self.link = 'http://127.0.0.1:8000/jov/api/check/'
        self.urlFund = 'http://127.0.0.1:8002/jov/api/fund/'
        self.userLink = 'http://127.0.0.1:8000/jov/api/reque//8/approve/'
        self.linkManageUser = 'http://127.0.0.1:8002/jov/api/user/'
        self.askFundLink = 'http://127.0.0.1:8002/jov/api/reque//'
        self.askLumiFund = 'http://127.0.0.1:8000/power/give_not_owner/'
        self.cookies = ""
        self.response = requests.models.Response()
        
    def injira(self):
        # Sending the data
        self.response = requests.post(self.url, data=self.data)
        # Checking the response
        if self.response.status_code == 200:
            self.cookies = self.response.cookies
            return self.cookies
        return ({"Failed to connect"})

    def check(self):
        self.response = requests.get(self.link, cookies=self.cookies)
        if self.response.status_code == 200:
            return self.response.json()

    def askFund(self):
        self.response = requests.post(self.askLumiFund, self.data_lumi, \
                                      cookies=self.cookies)
        if self.response.status_code == 200:
            return self.response.json()
        return (f"THe Funding failed: {self.response.reason}")
    
    def uploadFund(self):
        self.response = requests.post(self.askFundLink,\
                                       self.data_fund_upload, \
                                        cookies=self.cookies)
        if self.response.status_code == 200:
            return self.response.json()
        return (f"THe Funding To your accound failed: {self.response.reason}")
        
    
    def onUsers(self, method):
        self.injira()
        if method == 'get':
            self.response = requests.get(self.userLink,\
                                         cookies=self.cookies)
            if self.response.status_code == 200:
                return self.response.json()
            return self.response.status_code
        if method == 'post':
            self.response = requests.post(self.userLink, data=self.data, \
                                         cookies=self.cookies)
            if self.response.status_code == 200:
                return self.response.json()
            return self.response.status_code
    
    def addUser(self):
        self.response = requests.post(self.linkManageUser, \
                                       self.data_new_user)
        if self.response.status_code == 200:
            print("Operation Done successfully")
            try:
                return self.response.json()
            except JSONDecodeError:
                return f"The SERVER says that '{self.response.text}'"
        return f"THis user {self.data_new_user['username']} \
already exist. Please try a new one."


browising = UserBrowising()
# cookies = browising.injira()
# response = browising.check()
# response = browising.askFund() 
response = browising.uploadFund() #client1 approving Lumicash to pay Lde
# response = browising.onUsers('get')
# response = browising.addUser()
print(f"Your answer is: {response}")