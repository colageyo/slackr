valid_react = [1]

class React:
    def __init__(self):
        self.react_id = 1
        self.u_ids = []

    def get_react_id(self):
        return self.react_id
    def get_uids(self):
        return self.u_ids

    def user_react(self, user_id):
        self.u_ids.append(user_id)
    def user_unreact(self, user_id):
        self.u_ids.remove(user_id)
