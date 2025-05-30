## CLASSES ##
# Serves as models for the stored User and Account in the database

class User:
    # 0 = id ; 1 = name ; 2 = password
    def __init__(self, list: list):
        self.user_id = list[0]
        self.name = list[1]
        self.password = list[2]
        self.salt = list[-1]
    def update(self, list: list):
        self.user_id = list[0]
        self.name = list[1]
        self.password = list[2]
        self.salt = list[-1]
    def get_list(self):
        return [self.name, self.password]

class Account:
    # 0 = id ; 1 = name ; 2 = email ; 3 = description ; 4 = password ; last(-1) = user_id
    def __init__(self, list: list):
        self.account_id = list[0]
        self.name = list[1]
        self.email = list[2]
        self.description = list[3]
        self.password = list[4]
        self.user_id = list[-1]
    def update(self, list: list):
        self.account_id = list[0]
        self.name = list[1]
        self.email = list[2]
        self.description = list[3]
        self.password = list[4]
        self.user_id = list[-1]
    def get_list(self):
        return [self.name, self.email, self.description, self.password]