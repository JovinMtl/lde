"""I want to make a transaction code of 12 caracters"""

from random import choice

from ..models import Recharge


class GenerateCode:
    """Generate a code and inscript in a table of codes that have been
    used successfully with the object(request) of that transaction
    
    It will require the object(Request model) as a parameter
    
    we need to import that model of Codes"""

    def __init__(self) -> None:
        self.input1 = [x for x in range(10)]
        self.input2 = ['a','A','b','B','c','C','d','D','e','E','f','F',
                       'j','J','k','K','l','L','m','M','n','o','O',
                       'p','P','r','R','s','S','t','T',
                       ]
        self.choices = []
        self.code = ""

    def generate(self, table):
        worth = True
        while worth:
            for _ in range(2):
                for _ in range(2):
                    choice1 = choice(self.input1)
                    self.choices.append(choice1)
                for _ in range(3):
                    choice2 = choice(self.input2)
                    self.choices.append(choice2)
                choice1 = choice(self.input1)
                self.choices.append(choice1)
            for element in self.choices:
                self.code += str(element)
            
            if table == 'recharge':
                try:
                    obj = Recharge.objects.get(code_transaction=self.code)
                except Recharge.DoesNotExist:
                    worth = False
                    return self.code
                else:
                    worth = True
    


# jov = GenerateCode()
# code = jov.generate()
# print(f"THe code generated is:\n{code}")