from server.react_class import React


class Message:
    def __init__(self, m_id, u_id, message_content, time_created):
        self.m_id = m_id
        self.u_id = u_id
        self.message_content = message_content
        self.time_created = time_created
        self.reacts = [React()]
        self.is_pinned = False
    
    def get_message_id(self):
        return self.m_id
    def get_user_id(self):
        return self.u_id
    def get_message_content(self):
        return self.message_content
    def get_time_created(self):
        return self.time_created
    def get_reacts(self):
        return self.reacts
    def get_is_pinned(self):
        return self.is_pinned
    
    def change_content(self, message):
        self.message_content = message

    def pinned(self):
        return self.is_pinned == True
    def pin_message(self):
        self.is_pinned = True
    def unpin_message(self):
        self.is_pinned = False


m_id = 0

def get_global_message_id():
    global m_id
    return m_id

def set_global_message_id():
    global m_id
    m_id += 1
    return m_id 
