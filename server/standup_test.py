from server.user_class import *
from server.channel_class import *
from server.message_class import *
from server.Error import *
from server.access_error import AccessError
from datetime import datetime,timedelta
from threading import Timer
from server.message import *
from server.standup_functions import *

import pytest

# does not call standup_output_messages properly in test because the data gets cleared when it returns back 
# to the function 
'''=============================================================='''
'''             TESTING standup_start()       '''
def test_standup_start_normal():
	data_delete()
	reset_channel_list()
	authRegisterDict = auth_register("lily565657@unsw.com","quERty6526", "Lily", "Cheung")
	token = authRegisterDict['token']
	u_id = authRegisterDict['u_id']

	channelsCreateDict = channels_create (token, "Channel 1", "True")
	channel_id = channelsCreateDict ['channel_id']
	assert ({'time_finish': int((datetime.now() + timedelta(minutes = 1)).timestamp())} \
		== standup_start(token, channel_id, 60))
	
def test_standup_start_invalid_channel():
	data_delete()
	reset_channel_list()
	authRegisterDict = auth_register("lily565657@unsw.com","quERty6526", "Lily", "Cheung")
	token = authRegisterDict['token']

	channel_id_fake = "24952952906296"

    # Value Error when channel (based on ID) does not exist
	with pytest.raises(ValueError):
		standup_start(token, channel_id_fake, 60)

def test_standup_start_invalid_token():
	data_delete()
	reset_channel_list()
	
	authRegisterDict = auth_register("lily554466@unsw.com","quERty6526", "Lily", "Cheung")
	token1 = authRegisterDict['token']

	authRegisterDict2 = auth_register("lily123@gmail.com","4545rg3eg35yh", "Dollar", "Lilz")
	token2 = authRegisterDict2['token']

	channelsCreateDict = channels_create (token1, "Channel 1", "True")
	channel_id = channelsCreateDict ['channel_id']

    #Access Error when the authorised user is not a member of the channel that the message is within
	with pytest.raises(AccessError):
		standup_start(token2, channel_id, 60)

def test_standup_start_already_running():
	data_delete()
	reset_channel_list()

	authRegisterDict = auth_register("lily565657@unsw.com","quERty6526", "Lily", "Cheung")
	token = authRegisterDict['token']
	u_id = authRegisterDict['u_id']

	channelsCreateDict = channels_create (token, "Channel 1", "True")
	channel_id = channelsCreateDict ['channel_id']

	standup_start(token, channel_id, 60)

	with pytest.raises(ValueError):
		standup_start(token, channel_id, 60)

    #check if the list of messages gets changed
'''=============================================================='''
'''             TESTING standup_send()       '''
def test_standup_send_invalid_channel():
    data_delete()
    reset_channel_list()
    authRegisterDict = auth_register("lily565657@unsw.com","quERty6526", "Lily", "Cheung")
    token = authRegisterDict['token']
    u_id = authRegisterDict['u_id']
    
    channelsCreateDict = channels_create (token, "Channel 1", "True")
    channel_id = channelsCreateDict ['channel_id']
    standup_start(token,channel_id, 60)
    # Value Error when channel (based on ID) does not exist
    with pytest.raises(ValueError):
        standup_send(token, "13245", "test")


def test_standup_send_invalid_token():
    data_delete()
    reset_channel_list()
    authRegisterDict = auth_register("lily565657@unsw.com","quERty6526", "Lily", "Cheung")
    token = authRegisterDict['token']
    u_id = authRegisterDict['u_id']
    
    channelsCreateDict = channels_create (token, "Channel 1", "False")
    authRegisterDict2 = auth_register("lily56557@unsw.com","quERty6526", "Lily", "Cheung")
    channel_id = channelsCreateDict ['channel_id']
    token2 = authRegisterDict2['token']
    standup_start(token,channel_id, 60)
	
    #Access Error when the authorised user is not a member of the channel that the message is within
    with pytest.raises(AccessError):
        standup_send(token2, channel_id, "test")

def test_standup_send_message_exceeded():
    data_delete()
    reset_channel_list()
    authRegisterDict = auth_register("lily565657@unsw.com","quERty6526", "Lily", "Cheung")
    token = authRegisterDict['token']
    u_id = authRegisterDict['u_id']
    
    channelsCreateDict = channels_create (token, "Channel 1", "True")
    channel_id = channelsCreateDict ['channel_id']
    standup_start(token,channel_id, 60)
    #Value Error when message is more than 1000 characters
    with pytest.raises(ValueError):
        standup_send(token, channel_id, "?" * 1001)

def test_standup_send_valid():
    data_delete()
    reset_channel_list()
    authRegisterDict = auth_register("lily565657@unsw.com","quERty6526", "Lily", "Cheung")
    token = authRegisterDict['token']
    u_id = authRegisterDict['u_id']
    
    channelsCreateDict = channels_create (token, "Channel 1", "True")
    channel_id = channelsCreateDict ['channel_id']
    standup_start(token,channel_id, 60)
    assert standup_send(token, channel_id, "test1") == {}
    assert standup_send(token, channel_id, "test2") == {}
    standup_output_message(token, channel_id)
    
    reply = channel_messages(token, channel_id, 0) # dictionary
    reply_messages = reply['messages']  #list
    first_message = reply_messages[0] #dictionary
    assert first_message['message'] == "lilycheung: test1\nlilycheung: test2\n"

def test_standup_send_time_stopped():
    data_delete()
    reset_channel_list()
    authRegisterDict = auth_register("lily565657@unsw.com","quERty6526", "Lily", "Cheung")
    token = authRegisterDict['token']
    u_id = authRegisterDict['u_id']
    
    channelsCreateDict = channels_create (token, "Channel 1", "True")
    channel_id = channelsCreateDict ['channel_id']
#Value Error if the standup time has stopped
    with pytest.raises(ValueError):
        standup_send(token,channel_id,"hello")
        
'''=============================================================='''
'''             TESTING standup_active       '''
def test_standup_active():
    data_delete()
    reset_channel_list()
    authRegisterDict = auth_register("lily565657@unsw.com","quERty6526", "Lily", "Cheung")
    token = authRegisterDict['token']
    u_id = authRegisterDict['u_id']
    channelsCreateDict = channels_create (token, "Channel 1", "True")
    channel_id = channelsCreateDict ['channel_id']
    end_time = standup_start(token,channel_id, 60)
    active = standup_active(token, channel_id)
    
    assert active['is_active'] == True
    assert active['time_finish'] == end_time['time_finish']
    
def test_standup_imactive():
    data_delete()
    reset_channel_list()
    authRegisterDict = auth_register("lily565657@unsw.com","quERty6526", "Lily", "Cheung")
    token = authRegisterDict['token']
    u_id = authRegisterDict['u_id']
    channelsCreateDict = channels_create (token, "Channel 1", "True")
    channel_id = channelsCreateDict ['channel_id']
    active = standup_active(token, channel_id)
    
    assert active['is_active'] == False
    assert active['time_finish'] is None
    
def test_standup_active_invalid_id():
    data_delete()
    reset_channel_list()
    authRegisterDict = auth_register("lily565657@unsw.com","quERty6526", "Lily", "Cheung")
    token = authRegisterDict['token']
    u_id = authRegisterDict['u_id']
    channelsCreateDict = channels_create (token, "Channel 1", "True")
    channel_id = channelsCreateDict ['channel_id']
    standup_start(token,channel_id, 60)
    
    with pytest.raises(ValueError):
        standup_active(token, "132465")
        
def test_standup_active_invalid_token():
    data_delete()
    reset_channel_list()
    authRegisterDict = auth_register("lily565657@unsw.com","quERty6526", "Lily", "Cheung")
    token = authRegisterDict['token']
    u_id = authRegisterDict['u_id']
    channelsCreateDict = channels_create (token, "Channel 1", "True")
    channel_id = channelsCreateDict ['channel_id']
    standup_start(token,channel_id, 60)
    auth_logout(token)
    
    #with pytest.raises(AccessError):
    with pytest.raises(AccessError):
        standup_active(token, channel_id)

