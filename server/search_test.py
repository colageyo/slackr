import pytest
from server.search_function import search
from server.user_class import *
from server.channel_class import *
from server.message import *

def setup():
    data_delete()
    reset_channel_list()
    auth_register("st@unsw.edu","password","Student","Citizen")
    userDict = auth_login("st@unsw.edu",'password')
    channel_id = channels_create(userDict['token'],'Channel1',False)
    return {'token':userDict['token'],'u_id':userDict['u_id'],'channel_id':channel_id['channel_id']}

def test_whole_word():
    setupDict = setup()
    message_id = message_send(setupDict['token'], setupDict['channel_id'], 'word')
    message_send(setupDict['token'], setupDict['channel_id'], 'w0rd')
    searchResult = search(setupDict['token'], "word")
    messages = searchResult['messages']
    assert len(messages) == 1
    assert messages[0]['message_id'] == message_id['message_id']
    assert messages[0]['message'] == 'word'
    
def test_partial_word():
    setupDict = setup()
    message_id = message_send(setupDict['token'], setupDict['channel_id'], 'word')
    message_id2 = message_send(setupDict['token'], setupDict['channel_id'], 'w0rd')
    searchResult = search(setupDict['token'], 'rd')
    messages = searchResult['messages']
    assert len(messages) == 2
    assert messages[0]['message_id'] == message_id['message_id']
    assert messages[0]['message'] == 'word'
    assert messages[1]['message_id'] == message_id2['message_id']
    assert messages[1]['message'] == 'w0rd'
    
def test_private_channel():
    setupDict = setup()
    userDict = auth_register("stu@unsw.edu","password","Student","Citizen")
    channel_id = channels_create(userDict['token'],'Channel2',True)
    message_id = message_send(setupDict['token'], setupDict['channel_id'], 'word')
    message_id2 = message_send(userDict['token'], channel_id['channel_id'], 'w0rd')
    searchResult = search(userDict['token'], 'rd')
    messages = searchResult['messages']
    assert len(messages) == 1
    assert messages[0]['message_id'] == message_id2['message_id']
    assert messages[0]['message'] == 'w0rd'
    
def test_different_channels():
    setupDict = setup()
    channel_id = channels_create(setupDict['token'],'Channel2',True)
    message_id = message_send(setupDict['token'], setupDict['channel_id'], 'word')
    message_id2 = message_send(setupDict['token'], channel_id['channel_id'], 'w0rd')
    searchResult = search(setupDict['token'], 'rd')
    messages = searchResult['messages']
    assert len(messages) == 2
    assert messages[0]['message_id'] == message_id['message_id']
    assert messages[0]['message'] == 'word'
    assert messages[1]['message_id'] == message_id2['message_id']
    assert messages[1]['message'] == 'w0rd'
    
def test_no_search_result():
    setupDict = setup()
    message_id = message_send(setupDict['token'], setupDict['channel_id'], 'word')
    message_id2 = message_send(setupDict['token'], setupDict['channel_id'], 'w0rd')
    searchResult = search(setupDict['token'], 'hi')
    messages = searchResult['messages']
    assert messages == []
