import pytest
from server.message import message_send_later, message_send, message_remove, message_edit, message_react, message_unreact, message_pin, message_unpin, get_message_from_m_id
from server.access_error import AccessError
from datetime import datetime
from server.user_class import *
from server.channel_class import *

def setup():
    data_delete()
    reset_channel_list()
    auth_register("st@unsw.edu","password","Student","Citizen")
    userDict = auth_login("st@unsw.edu",'password')
    channel_id = channels_create(userDict['token'],'Channel1',False)
    return {'token':userDict['token'],'u_id':userDict['u_id'],'channel_id':channel_id['channel_id']}
    
''' ============================================================== '''
'''             TESTING message_send_later                      '''
""" Test 1: standard operation, expecting no error"""
def test_normal_sendlater():
    setupDict = setup()
    message = 'A new message'
    time_sent = 1605305395
    
    message_id = message_send_later(setupDict['token'], setupDict['channel_id'], message, time_sent)
    '''send_later_message = send_later[0]
    
    assert send_later_message['message'] == message
    assert send_later_message['token'] == setupDict['token']
    assert send_later_message['time_sent'] == datetime.fromtimestamp(float(time_sent))'''

""" Test 2: invalid time_sent, expecting ValueError"""
def test_time_sent_past():
    setupDict = setup()
    message = 'hello'
    time_sent = 1564
    
    with pytest.raises(ValueError) as excinfo:
        message_send_later(setupDict['token'], setupDict['channel_id'], message, time_sent)
        
    assert excinfo.type == ValueError
    
''' Test 3: invalid message, expecting ValueError'''
def test_long_message_send_later():
    setupDict = setup()
    message = "A" * 1001
    time_sent = 1605305395
    
    with pytest.raises(ValueError) as excinfo:
        message_send_later(setupDict['token'], setupDict['channel_id'], message, time_sent)
        
    assert excinfo.type == ValueError

""" Test 4: invalid channel, expecting ValueError"""
def test_invalid_channel():
    setupDict = setup()
    message = "Hello world"
    time_sent = 1605305395
    
    with pytest.raises(ValueError) as excinfo:
        message_send_later(setupDict['token'], "1234", message, time_sent)
        
    assert excinfo.type == ValueError

""" Test 5: user not in channel, expecting AccessError"""
def test_user_not_in_channel_later():
    setupDict = setup()
    auth_register("stu@unsw.edu","password","Student","Citizen")
    userDict = auth_login("stu@unsw.edu",'password')
    message = "Hello world"
    time_sent = 1605305395
    
    with pytest.raises(AccessError) as excinfo:
        message_send_later(userDict['token'], setupDict['channel_id'], message, time_sent)
    assert excinfo.type == AccessError
''' ============================================================== '''
'''                     TESTING message_send                    '''
''' Test 1: Test if the message has been successfully sent to the channel'''
def test_normal():
    global my_users
    setupDict = setup()
    message = 'A new message'
    message_id = message_send(setupDict['token'], setupDict['channel_id'], message)
    
    reply = channel_messages(setupDict['token'], setupDict['channel_id'], 0) # dictionary
    reply_messages = reply['messages']  #list
    first_message = reply_messages[0] #dictionary
    assert first_message['message'] == message

''' Test 2: Test successfully raise error'''
def test_long_message():
    global my_users
    setupDict = setup()
    message = "A" * 1001
    
    with pytest.raises(ValueError) as excinfo:
        message_send(setupDict['token'], setupDict['channel_id'], message)
    assert excinfo.type == ValueError

""" Test 3: user not in channel, expecting AccessError"""
def test_user_not_in_channel():
    global send_later
    setupDict = setup()
    auth_register("stu@unsw.edu","password","Student","Citizen")
    userDict = auth_login("stu@unsw.edu",'password')
    message = "Hello world"
    
    with pytest.raises(AccessError) as excinfo:
        message_send(userDict['token'], setupDict['channel_id'], message)
        
    assert excinfo.type == AccessError
''' =============================================================== '''
'''                 TESTING message_remove                          '''
""" Test 1: All valid inputs, no expecting error"""
def test_standard_remove():
    global send_later
    setupDict = setup()
    message_send(setupDict['token'], setupDict['channel_id'],'hello')
    message = message_send(setupDict['token'], setupDict['channel_id'],'A new message')
    message_remove(setupDict['token'], message['message_id'])
    start = 0
    reply = channel_messages(setupDict['token'], setupDict['channel_id'], start) # dictionary
    reply_messages = reply['messages']  #list
    for messageDict in reply_messages:
        assert message['message_id'] != messageDict['message_id']

""" Test 2: Invalid message, expecting ValueError"""
def test_invalid_message():
    global send_later
    setupDict = setup()
    message = message_send(setupDict['token'], setupDict['channel_id'],'A new message')
    message_remove(setupDict['token'], message['message_id'])
    with pytest.raises(ValueError) as excinfo:
        message_remove(setupDict['token'], message['message_id'])
    assert excinfo.type == ValueError

""" Test 3: User not the poster of the message and not owner or admin"""
def test_invalid_poster():
    global send_later
    setupDict = setup()
    message = message_send(setupDict['token'], setupDict['channel_id'],'A new message')
    auth_register("stu@unsw.edu","password","Student","Citizen")
    userDict = auth_login("stu@unsw.edu",'password')
    channel_invite(setupDict['token'],setupDict['channel_id'],userDict['u_id'])
    
    with pytest.raises(AccessError, match=r'Not authorized user of message') as excinfo:
        message_remove(userDict['token'], message['message_id'])
    assert excinfo.type == AccessError

""" Test 4: User not in channel"""
def test_unauthorized_user():
    global send_later
    setupDict = setup()
    message = message_send(setupDict['token'], setupDict['channel_id'],'A new message')
    auth_register("stu@unsw.edu","password","Student","Citizen")
    userDict = auth_login("stu@unsw.edu",'password')
    
    with pytest.raises(AccessError, match=r'Not authorized user of message') as excinfo:
        message_remove(userDict['token'], message['message_id'])
    assert excinfo.type == AccessError
    
""" Test 5: user did not send message but is owner """
def test_owner_not_poster_but_owner():
    global send_later
    setupDict = setup()
    auth_register("stu@unsw.edu","password","Student","Citizen")
    userDict = auth_login("stu@unsw.edu",'password')
    channel_invite(setupDict['token'],setupDict['channel_id'],userDict['u_id'])
    message_send(setupDict['token'], setupDict['channel_id'],'hello')
    message = message_send(userDict['token'], setupDict['channel_id'],'A new message')
    message_remove(setupDict['token'], message['message_id'])
    
    start = 0
    reply = channel_messages(setupDict['token'], setupDict['channel_id'], start) # dictionary
    reply_messages = reply['messages']  #list
    for messageDict in reply_messages:
        assert message['message_id'] != messageDict['message_id']
        
def test_message_creator_remove():
    global send_later
    setupDict = setup()
    auth_register("stu@unsw.edu","password","Student","Citizen")
    userDict = auth_login("stu@unsw.edu",'password')
    channel_invite(setupDict['token'],setupDict['channel_id'],userDict['u_id'])
    message_send(setupDict['token'], setupDict['channel_id'],'hello')
    message = message_send(userDict['token'], setupDict['channel_id'],'A new message')
    message_remove(userDict['token'], message['message_id'])
    
    start = 0
    reply = channel_messages(setupDict['token'], setupDict['channel_id'], start) # dictionary
    reply_messages = reply['messages']  #list
    for messageDict in reply_messages:
        assert message['message_id'] != messageDict['message_id']
    
''' ================================================================== '''
'''                     TESTING message_edit                           '''
def test_standard_edit():
    global my_users
    setupDict = setup()
    message_id = message_send(setupDict['token'], setupDict['channel_id'], 'A new message')
    
    message_edit(setupDict['token'], message_id['message_id'], "Hello")
    start = 0
    reply = channel_messages(setupDict['token'], setupDict['channel_id'], start) # dictionary
    reply_messages = reply['messages']  #list
    first_message = reply_messages[0] #dictionary
    assert first_message['message'] == "Hello"
    
def test_not_poster_but_is_owner():
    global my_users
    setupDict = setup()
    auth_register("stu@unsw.edu","password","Student","Citizen")
    userDict = auth_login("stu@unsw.edu",'password')
    channel_invite(setupDict['token'],setupDict['channel_id'],userDict['u_id'])
    message_id = message_send(userDict['token'], setupDict['channel_id'], 'A new message')
    
    message_edit(setupDict['token'], message_id['message_id'], "Hello")
    start = 0
    reply = channel_messages(setupDict['token'], setupDict['channel_id'], start) # dictionary
    reply_messages = reply['messages']  #list
    first_message = reply_messages[0] #dictionary
    
    assert first_message['message'] == "Hello"

def test_not_owner_or_poster():
    global my_users
    setupDict = setup()
    auth_register("stu@unsw.edu","password","Student","Citizen")
    userDict = auth_login("stu@unsw.edu",'password')
    channel_invite(setupDict['token'],setupDict['channel_id'],userDict['u_id'])
    message_id = message_send(setupDict['token'], setupDict['channel_id'], 'A new message')
    
    with pytest.raises(AccessError, match=r'Not authorized user of message') as excinfo:
        message_edit(userDict['token'], message_id['message_id'], "Hello")
    assert excinfo.type == AccessError

def test_invalid_token():
    global my_users
    setupDict = setup()
    message_id = message_send(setupDict['token'], setupDict['channel_id'], 'A new message')
    auth_logout(setupDict['token'])
    with pytest.raises(AccessError, match=r'User is not a valid user') as excinfo:
        message_edit(setupDict['token'], message_id['message_id'], "Hello")
    assert excinfo.type == AccessError
    
def test_message_creator():
    global my_users
    setupDict = setup()
    auth_register("stu@unsw.edu","password","Student","Citizen")
    userDict = auth_login("stu@unsw.edu",'password')
    channel_invite(setupDict['token'],setupDict['channel_id'],userDict['u_id'])
    message_id = message_send(userDict['token'], setupDict['channel_id'], 'A new message')
    
    message_edit(userDict['token'], message_id['message_id'], "Hello")
    start = 0
    reply = channel_messages(setupDict['token'], setupDict['channel_id'], start) # dictionary
    reply_messages = reply['messages']  #list
    first_message = reply_messages[0] #dictionary
    
    assert first_message['message'] == "Hello"

''' ================================================================== '''
'''                     TESTING message_react                          '''
def test_standard_react():
    global my_users
    setupDict = setup()
    message_id = message_send(setupDict['token'], setupDict['channel_id'], "Hello")
    react_id = 1
    message_react(setupDict['token'], message_id['message_id'], react_id)
    message = get_message_from_m_id(message_id['message_id'])
    reacts = message.get_reacts()
    assert setupDict['u_id'] in reacts[0].get_uids()
    
    auth_register("stu@unsw.edu","password","Student","Citizen")
    userDict = auth_login("stu@unsw.edu",'password')
    channel_invite(setupDict['token'],setupDict['channel_id'],userDict['u_id'])
    message_react(userDict['token'], message_id['message_id'], react_id)
    
    assert userDict['u_id'] in reacts[0].get_uids()
    
def test_invalid_message_id():
    global my_users
    setupDict = setup()
    message_id = message_send(setupDict['token'], setupDict['channel_id'], "Hello")
    react_id = 1
    
    with pytest.raises(ValueError, match=r'Invalid message_id') as excinfo:
        message_react(setupDict['token'], "123", react_id)
    assert excinfo.type == ValueError

def test_invalid_react_id():
    global my_users
    setupDict = setup()
    message_id = message_send(setupDict['token'], setupDict['channel_id'], "Hello")
    react_id = 0
    
    with pytest.raises(ValueError, match=r'Invalid react_id') as excinfo:
        message_react(setupDict['token'], message_id['message_id'], react_id)
    assert excinfo.type == ValueError

def test_already_reacted():
    global my_users
    setupDict = setup()
    message_id = message_send(setupDict['token'], setupDict['channel_id'], "Hello")
    react_id = 1
    message_react(setupDict['token'], message_id['message_id'], react_id)
    message = get_message_from_m_id(message_id['message_id'])
    reacts = message.get_reacts()
    assert setupDict['u_id'] in reacts[0].get_uids()
    
    with pytest.raises(ValueError, match=r'Already contains an active react') as excinfo:
        message_react(setupDict['token'], message_id['message_id'], react_id)
    assert excinfo.type == ValueError
    
def test_react_not_in_channel():
    global my_users
    setupDict = setup()
    userDict = auth_register("stu@unsw.edu","password","Student","Citizen")
    message_id = message_send(setupDict['token'], setupDict['channel_id'], "Hello")
    react_id = 1
    message_react(setupDict['token'], message_id['message_id'], react_id)
    message = get_message_from_m_id(message_id['message_id'])
    reacts = message.get_reacts()
    assert setupDict['u_id'] in reacts[0].get_uids()
    
    with pytest.raises(ValueError, match=r'Invalid message_id with in the user joined channel') as excinfo:
        message_react(userDict['token'], message_id['message_id'], react_id)
    assert excinfo.type == ValueError
    
''' ================================================================== '''
'''                   TESTING message_unreact                          '''
def test_standard_unreact():
    global my_users
    setupDict = setup()
    message_id = message_send(setupDict['token'], setupDict['channel_id'], "Hello")
    react_id = 1
    message_react(setupDict['token'], message_id['message_id'], react_id)
    message = get_message_from_m_id(message_id['message_id'])
    reacts = message.get_reacts()
    
    auth_register("stu@unsw.edu","password","Student","Citizen")
    userDict = auth_login("stu@unsw.edu",'password')
    channel_invite(setupDict['token'],setupDict['channel_id'],userDict['u_id'])
    message_react(userDict['token'], message_id['message_id'], react_id)
    
    message_unreact(userDict['token'], message_id['message_id'], react_id)
    assert userDict['u_id'] not in reacts[0].get_uids()

def test_invalid_message_id_unreact():
    global my_users
    setupDict = setup()
    message_id = message_send(setupDict['token'], setupDict['channel_id'], "Hello")
    react_id = 1
    message_react(setupDict['token'], message_id['message_id'], react_id)
    
    with pytest.raises(ValueError, match=r'Invalid message_id') as excinfo:
        message_unreact(setupDict['token'], "123", react_id)
    assert excinfo.type == ValueError

def test_invalid_unreact_id():
    global my_users
    setupDict = setup()
    message_id = message_send(setupDict['token'], setupDict['channel_id'], "Hello")
    react_id = 0
    message_react(setupDict['token'], message_id['message_id'], 1)
    
    with pytest.raises(ValueError, match=r'Invalid react_id') as excinfo:
        message_unreact(setupDict['token'], message_id['message_id'], react_id)
    assert excinfo.type == ValueError

def test_no_reacts():
    global my_users
    setupDict = setup()
    message_id = message_send(setupDict['token'], setupDict['channel_id'], "Hello")
    react_id = 1
    
    with pytest.raises(ValueError, match=r'Does not contain an active react') as excinfo:
        message_unreact(setupDict['token'], message_id['message_id'], react_id)
    assert excinfo.type == ValueError
    
def test_invalid_token_unreact():
    global my_users
    setupDict = setup()
    message_id = message_send(setupDict['token'], setupDict['channel_id'], "Hello")
    react_id = 1
    message_react(setupDict['token'], message_id['message_id'], 1)
    auth_logout(setupDict['token'])
    with pytest.raises(AccessError, match=r'User is not a valid user') as excinfo:
        message_unreact(setupDict['token'], message_id['message_id'], react_id)
    assert excinfo.type == AccessError
    
''' ================================================================== '''
'''                        TESTING message_pin                         '''
def test_standard_pin():
    global my_users
    setupDict = setup()
    message_id = message_send(setupDict['token'], setupDict['channel_id'], "Hello")
    message_pin(setupDict['token'], message_id['message_id'])
    message = get_message_from_m_id(message_id['message_id'])
    
    assert message.is_pinned == True

def test_invalid_message_id_pin():
    global my_users
    setupDict = setup()
    message_id = message_send(setupDict['token'], setupDict['channel_id'], "Hello")
    
    with pytest.raises(ValueError, match=r'Message no long exist') as excinfo:
        message_pin(setupDict['token'], "123")
    assert excinfo.type == ValueError
    
    message = get_message_from_m_id(message_id['message_id'])
    assert message.is_pinned == False
    
def test_not_admin_pin():
    global my_users
    setupDict = setup()
    message_id = message_send(setupDict['token'], setupDict['channel_id'], "Hello")
    
    auth_register("stu@unsw.edu","password","Student","Citizen")
    userDict = auth_login("stu@unsw.edu",'password')
    channel_invite(setupDict['token'],setupDict['channel_id'],userDict['u_id'])
    
    with pytest.raises(ValueError, match=r'The user is not an admin') as excinfo:
        message_pin(userDict['token'], message_id['message_id'])
    assert excinfo.type == ValueError
    
    message = get_message_from_m_id(message_id['message_id'])
    assert message.is_pinned == False

def test_already_pinned():
    global my_users
    setupDict = setup()
    message_id = message_send(setupDict['token'], setupDict['channel_id'], "Hello")
    message_pin(setupDict['token'], message_id['message_id'])
    
    with pytest.raises(ValueError, match=r'Message is already pinned') as excinfo:
        message_pin(setupDict['token'], message_id['message_id'])
    assert excinfo.type == ValueError

def test_unauthorized():
    global my_users
    setupDict = setup()
    message_id = message_send(setupDict['token'], setupDict['channel_id'], "Hello")
    
    auth_register("stu@unsw.edu","password","Student","Citizen")
    userDict = auth_login("stu@unsw.edu",'password')
    
    with pytest.raises(AccessError, match=r'User is not a member of the channel') as excinfo:
        message_pin(userDict['token'], message_id['message_id'])
    assert excinfo.type == AccessError
    
    message = get_message_from_m_id(message_id['message_id'])
    assert message.is_pinned == False
    
def test_invalid_token_pin():
    global my_users
    setupDict = setup()
    message_id = message_send(setupDict['token'], setupDict['channel_id'], "Hello")
    message_pin(setupDict['token'], message_id['message_id'])
    auth_logout(setupDict['token'])
    with pytest.raises(AccessError, match=r'User is not a valid user') as excinfo:
        message_pin(setupDict['token'], message_id['message_id'])
    assert excinfo.type == AccessError

''' ================================================================== '''
'''                      TESTING message_unpin                         '''
def test_standard_unpin():
    global my_users
    setupDict = setup()
    message_id = message_send(setupDict['token'], setupDict['channel_id'], "Hello")
    message_pin(setupDict['token'], message_id['message_id'])
    message = get_message_from_m_id(message_id['message_id'])
    
    assert message.is_pinned == True
    
    message_unpin(setupDict['token'], message_id['message_id'])
    assert message.is_pinned == False

def test_invalid_message_id_unpin():
    global my_users
    setupDict = setup()
    message_id = message_send(setupDict['token'], setupDict['channel_id'], "Hello")
    message_pin(setupDict['token'], message_id['message_id'])
    message = get_message_from_m_id(message_id['message_id'])
    
    with pytest.raises(ValueError, match=r'Message no long exist') as excinfo:
        message_unpin(setupDict['token'], "123")
    assert excinfo.type == ValueError
    
    assert message.is_pinned == True

def test_not_admin_unpin():
    global my_users
    setupDict = setup()
    message_id = message_send(setupDict['token'], setupDict['channel_id'], "Hello")
    
    auth_register("stu@unsw.edu","password","Student","Citizen")
    userDict = auth_login("stu@unsw.edu",'password')
    channel_invite(setupDict['token'],setupDict['channel_id'],userDict['u_id'])
    message = get_message_from_m_id(message_id['message_id'])
    message_pin(setupDict['token'], message_id['message_id'])
    
    with pytest.raises(ValueError, match=r'The user is not an admin') as excinfo:
        message_unpin(userDict['token'], message_id['message_id'])
    assert excinfo.type == ValueError
    
    assert message.is_pinned == True

def test_already_unpinned():
    global my_users
    setupDict = setup()
    message_id = message_send(setupDict['token'], setupDict['channel_id'], "Hello")
    message = get_message_from_m_id(message_id['message_id'])
    
    with pytest.raises(ValueError, match=r'Message is already unpinned') as excinfo:
        message_unpin(setupDict['token'], message_id['message_id'])
    assert excinfo.type == ValueError
    
    assert message.is_pinned == False

def test_unauthorized_unpin():
    global my_users
    setupDict = setup()
    message_id = message_send(setupDict['token'], setupDict['channel_id'], "Hello")
    
    auth_register("stu@unsw.edu","password","Student","Citizen")
    userDict = auth_login("stu@unsw.edu",'password')
    
    message_pin(setupDict['token'], message_id['message_id'])
    
    message = get_message_from_m_id(message_id['message_id'])
    
    with pytest.raises(AccessError, match=r'User is not a member of the channel') as excinfo:
        message_unpin(userDict['token'], message_id['message_id'])
    assert excinfo.type == AccessError
    
    assert message.is_pinned == True
    
def test_invalid_token_unpin():
    global my_users
    setupDict = setup()
    message_id = message_send(setupDict['token'], setupDict['channel_id'], "Hello")
    
    message_pin(setupDict['token'], message_id['message_id'])
    
    message = get_message_from_m_id(message_id['message_id'])
    auth_logout(setupDict['token'])
    with pytest.raises(AccessError, match=r'User is not a valid user') as excinfo:
        message_unpin(setupDict['token'], message_id['message_id'])
    assert excinfo.type == AccessError
    
    assert message.is_pinned == True
