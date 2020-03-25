from server.user_class import *
from server.message import *
from server.channel_class import *
import pytest
import uuid

## Note: cannot cover user == None attributes because the token cannot be decoded in auth functions.
## However, asserts are implemented.

'''             TESTS FOR CHANNEL FUNCTIONS         '''
'''=============================================================='''
'''             TESTING channel_invite        '''
# Test 1: Test with correct inputs
def test_invite_corr_input():
	global channel_list
	global my_users
	reset_channel_list()
	data_delete()

	authRegisterDict = auth_register("lily554466@unsw.com","quERty6526", "Lily", "Cheung")
	token1 = authRegisterDict['token']

	authRegisterDict2 = auth_register("lily123@gmail.com","4545rg3eg35yh", "Dollar", "Lilz")
	u_id2= authRegisterDict2 ['u_id']

	channelsCreateDict = channels_create (token1, "Channel 1", "true")
	channel_id_1 = channelsCreateDict ['channel_id']

	new_invite = channel_invite(token1,channel_id_1,u_id2)

	channel_test = get_verified_channel_from_id(channel_id_1,channel_list)

	assert u_id2 in channel_test.get_mem_list()

	assert new_invite == {}


# Test 2: Wrong Channel ID
# 	This function test for exception when an invalid channel id is passed into the function
def test_invite_wrong_channel_id():
	global channel_list
	global my_users
	reset_channel_list()
	data_delete()

	authRegisterDict = auth_register("lily554466@unsw.com","quERty6526", "Lily", "Cheung")
	token1 = authRegisterDict['token']

	authRegisterDict2 = auth_register("lily123@gmail.com","4545rg3eg35yh", "Dollar", "Lilz")
	u_id2= authRegisterDict2 ['u_id']

	channel_id = '2341345'

	with pytest.raises(ValueError):
		channel_invite(token1,channel_id,u_id2)

# Test 3: Wrong User ID
# 	this function test for exception when an invalid user id is passed into the
# 	function
def test_invite_wrong_u_id():
	global channel_list
	global my_users
	reset_channel_list()
	data_delete()

	details = auth_register("lily123@unsw.edu","4545DFHUgnww", "Dollar", "Lilz")
	dummy_token = details['token']

	u_id = "45945924294942"

	channelsCreateDict = channels_create (dummy_token, "Channel 1", "true")
	channel_id = channelsCreateDict ['channel_id']

	with pytest.raises(ValueError):
		channel_invite(dummy_token,channel_id,u_id) 

def test_invite_host_not_in_mem_list():
	global channel_list
	global my_users
	reset_channel_list()
	data_delete()

	authRegisterDict = auth_register("lily554466@unsw.com","quERty6526", "Lily", "Cheung")
	token1 = authRegisterDict['token']

	authRegisterDict2 = auth_register("lily123@gmail.com","4545rg3eg35yh", "Dollar", "Lilz")
	u_id2= authRegisterDict2 ['u_id']

	dict4 = auth_register("lily7777123@gmail.com","how35yh", "Dollar", "Lilz")
	token4 = dict4['token']

	channelsCreateDict = channels_create (token1, "Channel 1", "true")
	channel_id = channelsCreateDict ['channel_id']

	with pytest.raises(AccessError):
		channel_invite(token4,channel_id,u_id2) 

def test_recipient_already_member():
	global channel_list
	global my_users
	reset_channel_list()
	data_delete()

	authRegisterDict = auth_register("lily554466@unsw.com","quERty6526", "Lily", "Cheung")
	token1 = authRegisterDict['token']

	authRegisterDict2 = auth_register("lily123@gmail.com","4545rg3eg35yh", "Dollar", "Lilz")
	u_id2= authRegisterDict2 ['u_id']

	channelsCreateDict = channels_create (token1, "Channel 1", "true")
	channel_id_1 = channelsCreateDict ['channel_id']

	new_invite = channel_invite(token1,channel_id_1,u_id2)

	with pytest.raises(ValueError):
		channel_invite(token1,channel_id_1,u_id2) 

'''=============================================================='''
'''             TESTING channel_details        '''
def test_channel_details_corr_inputs():
	global channel_list
	global my_users
	reset_channel_list()
	data_delete()
	#reset u_id

	#setup
	dict1 = auth_register("whyisifailing@unsw.com","quERty6526", "Lily", "Cheung")
	tok1 = dict1['token']
	u_id1= dict1['u_id']

	user_class = get_user_from_id(u_id1)
	assert user_class != None 

	dict2 = auth_register("stooge@gmail.com","how35yh", "Dollar", "Lilz")
	token2 = dict2['token']
	u_id2= dict2['u_id']

	channel = channels_create(token2, "Fourth Channel", "true")
	channel_id = channel['channel_id']

	channel_class = get_verified_channel_from_id(channel_id, channel_list)
	assert (channel_class != None)

	channel_join(tok1, channel_id)

	#print(channel_details(tok1, channel_id)) 
	# test correct return
	assert channel_details(tok1, channel_id) == {'name': 'Fourth Channel', 
		'owner_members': [{
			'u_id': u_id2, 
			'name_first': 'Dollar', 
			'name_last': 'Lilz', 
			'profile_img_url': None},
			{'u_id': u_id1, 
			'name_first': 'Lily', 
			'name_last': 'Cheung', 
			'profile_img_url': None}], 
		'all_members': [{
			'u_id': u_id2, 
			'name_first': 'Dollar', 
			'name_last': 'Lilz', 
			'profile_img_url': None}, 
			{'u_id': u_id1, 
			'name_first': 'Lily', 
			'name_last': 'Cheung', 
			'profile_img_url': None}]}
			
def test_details_uid_not_member():
	global channel_list
	global my_users
	reset_channel_list()
	data_delete()
	#setup
	dict1 = auth_register("whyisifailing@unsw.com","quERty6526", "Lily", "Cheung")
	tok1 = dict1['token']
	u_id1= dict1['u_id']

	dict4 = auth_register("lily7777123@gmail.com","how35yh", "Dollar", "Lilz")
	token4 = dict4['token']
	u_id4= dict4['u_id']

	channel = channels_create(token4, "Fourth Channel", "true")
	channel_id = channel['channel_id']

	channel_class = get_verified_channel_from_id(channel_id, channel_list)
	assert (channel_class != None)

	# test raise
	with pytest.raises(AccessError):
		channel_details(tok1,channel_id) 

def test_details_channel_doesnt_exist(): 
	global channel_list
	global my_users
	reset_channel_list()
	data_delete()

	dict1 = auth_register("whyisifailing@unsw.com","quERty6526", "Lily", "Cheung")
	tok1 = dict1['token']

	channel_id = '1242424'
	with pytest.raises(ValueError):
		channel_details(tok1,channel_id) 

'''=============================================================='''
'''             TESTING channel_messages        '''


'''test 1: test with correct input 1 message'''
def test_message_message_corr():
	global channel_list
	global my_users
	reset_channel_list()
	data_delete()

	authRegisterDict = auth_register("lily565657@unsw.com","quERty6526", "Lily", "Cheung")
	token = authRegisterDict['token']
	u_id = authRegisterDict ['u_id']

	channelsCreateDict = channels_create (token, "Channel 1", "true")
	channel_id = channelsCreateDict ['channel_id']

	mess_id = message_send(token,channel_id,"hello world")
	message_react(token, mess_id['message_id'], 1)

	target_channel = get_verified_channel_from_id(channel_id,channel_list)
	assert len(target_channel.get_mess()) == 1

	message = channel_messages(token, channel_id, 0)
	assert len (message['messages']) == 1
	assert message['end'] == -1

''' test 2: test with correct input and 70 messages'''
def test_message_message_corr70():
	global channel_list
	global my_users
	reset_channel_list()
	data_delete()

	authRegisterDict = auth_register("lily565657@unsw.com","quERty6526", "Lily", "Cheung")
	token = authRegisterDict['token']
	u_id = authRegisterDict ['u_id']

	channelsCreateDict = channels_create (token, "Channel 1", "true")
	channel_id = channelsCreateDict ['channel_id']

	counter = 0
	for counter in range (0,70):
		mess_id = message_send(token,channel_id,str(counter))
		counter += 1
	target_channel = get_verified_channel_from_id(channel_id,channel_list)
	assert len(target_channel.get_mess()) == 70

	message = channel_messages(token, channel_id, 3)
	assert len (message['messages']) == 50
	assert message['end'] == 53

''' test 3: test with in start > len(message)'''
def test_message_bigger_start():
	global channel_list
	global my_users
	reset_channel_list()
	data_delete()

	authRegisterDict = auth_register("lily565657@unsw.com","quERty6526", "Lily", "Cheung")
	token = authRegisterDict['token']
	u_id = authRegisterDict ['u_id']

	channelsCreateDict = channels_create (token, "Channel 1", "true")
	channel_id = channelsCreateDict ['channel_id']

	counter = 0
	for counter in range (0,30):
		mess_id = message_send(token,channel_id,str(counter))
		counter += 1
	target_channel = get_verified_channel_from_id(channel_id,channel_list)
	assert len(target_channel.get_mess()) == 30

	with pytest.raises(ValueError,match = "The start is greater than cumulative messages"):
		message = channel_messages(token, channel_id, 31)



'''test 4: user is not in the channel'''
def test_message_user_not_in():
	global channel_list
	global my_users
	reset_channel_list()
	data_delete()

	authRegisterDict = auth_register("lily565657@unsw.com","quERty6526", "Lily", "Cheung")
	token = authRegisterDict['token']
	u_id = authRegisterDict['u_id']
	
	authRegisterDict1 = auth_register("Steven3147@gmail.com","123456", "Steven", "Trinh")
	token1 = authRegisterDict1['token']
	u_id1 = authRegisterDict1['u_id']


	channelsCreateDict = channels_create (token, "Channel 1", "true")
	channel_id = channelsCreateDict ['channel_id']

	counter = 0
	for counter in range (0,30):
		mess_id = message_send(token,channel_id,str(counter))
		counter += 1
	target_channel = get_verified_channel_from_id(channel_id,channel_list)
	assert len(target_channel.get_mess()) == 30

	with pytest.raises(AccessError):
		message = channel_messages(token1, channel_id, 25)
			
'''test 5: test non exist channel'''
def test_message_non_channel():
	global channel_list
	global my_users
	reset_channel_list()
	data_delete()

	authRegisterDict = auth_register("lily565657@unsw.com","quERty6526", "Lily", "Cheung")
	token = authRegisterDict['token']
	u_id = authRegisterDict['u_id']
		
	channelsCreateDict = channels_create (token, "Channel 1", "true")
	channel_id = channelsCreateDict ['channel_id']
	channel_id_fake = 12334534647
	counter = 0
	for counter in range (0,30):
		mess_id = message_send(token,channel_id,str(counter))
		counter += 1
	target_channel = get_verified_channel_from_id(channel_id,channel_list)
	assert len(target_channel.get_mess()) == 30

	with pytest.raises(ValueError):
		message = channel_messages(token, channel_id_fake, 25)

'''test 6: non existed user'''
def test_message_non_user():
	global channel_list
	global my_users
	reset_channel_list()
	data_delete()

	authRegisterDict = auth_register("lily565657@unsw.com","quERty6526", "Lily", "Cheung")
	token = authRegisterDict['token']
	u_id = authRegisterDict['u_id']
	fake_token = "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ1X2lkIjoiYzFjZWIzNjktNjQ5NS00ZjBkLThkOGEtOTczOTQxNDc3MjNhIiwidGltZV9zdGFtcCI6NDM0ODA5fQ.Bos3FvaoWJFvVPtrr7Csv4ELjIOJ6KD_AaUUHULyF0k"

	channelsCreateDict = channels_create (token, "Channel 1", "true")
	channel_id = channelsCreateDict ['channel_id']

	counter = 0
	for counter in range (0,30):
		mess_id = message_send(token,channel_id,str(counter))
		counter += 1
	target_channel = get_verified_channel_from_id(channel_id,channel_list)
	assert len(target_channel.get_mess()) == 30

	with pytest.raises(ValueError):
		message = channel_messages(fake_token, channel_id, 25)

	
'''=============================================================='''
'''             TESTING channel_leave        '''
''' Test 1 : Test with correct inputs'''
''' This function have no outputs we have not implemented the actual function so
	we cant test for the functions features '''

def test_leave_corr_inputs():
	global channel_list
	global my_users
	reset_channel_list()
	data_delete()

	authRegisterDict = auth_register("lily565657@unsw.com","quERty6526", "Lily", "Cheung")
	token = authRegisterDict['token']
	u_id = authRegisterDict ['u_id']

	assert get_user_from_token(token) != None

	channelsCreateDict = channels_create (token, "Channel 1", "true")
	channel_id = channelsCreateDict ['channel_id']

	assert get_verified_channel_from_id(channel_id,channel_list) != None

	assert (channels_listall(token) == [{"channel_id": channel_id, "name":"Channel 1"}])

	#call channel_leave
	channel_leave(token, channel_id)

	# check that value error is raised once channel does not exist anymore
	# channel id should not exist
	with pytest.raises(ValueError):
		get_verified_channel_from_id(channel_id,channel_list)

''' Test 2 : Test invalid channel Id'''
''' This function test for ValueError when given an invalid id'''

def test_leave_invalid_channel_id():
	global channel_list
	global my_users
	reset_channel_list()
	data_delete()

	authRegisterDict = auth_register("lily@unsw.com","quERty6526", "Lily", "Cheung")
	token = authRegisterDict['token']
	channel_id = "0000000000000"

def test_leave_not_a_member():
	global channel_list
	global my_users
	reset_channel_list()
	data_delete()

	authRegisterDict = auth_register("lily565657@unsw.com","quERty6526", "Lily", "Cheung")
	token = authRegisterDict['token']
	u_id = authRegisterDict ['u_id']

	authRegisterDict1 = auth_register("Steven3147@gmail.com","123456", "Steven", "Trinh")
	token1 = authRegisterDict1['token']
	u_id1 = authRegisterDict1['u_id']

	channelsCreateDict = channels_create (token, "Channel 1", "true")
	channel_id = channelsCreateDict ['channel_id']

	with pytest.raises(ValueError):
		channel_leave(token1, channel_id)

def test_leave_owner():
	global channel_list
	global my_users
	reset_channel_list()
	data_delete()

	authRegisterDict = auth_register("lily565657@unsw.com","quERty6526", "Lily", "Cheung")
	token = authRegisterDict['token']
	u_id = authRegisterDict ['u_id']

	authRegisterDict2 = auth_register("marina@gmail.com","45445454225", "Dollar", "Lilz")
	token2 = authRegisterDict2['token']
	u_id2= authRegisterDict2 ['u_id']

	channelsCreateDict = channels_create (token, "Channel 1", "true")
	channel_id = channelsCreateDict ['channel_id']

	channel_join(token2, channel_id)

	channel_class = get_verified_channel_from_id(channel_id,channel_list)
	assert len(channel_class.get_owner_list()) == 1 

	channel_leave(token2, channel_id)

	assert u_id2 not in channel_class.get_mem_list() 
	assert u_id2 not in channel_class.get_owner_list() 

	channel_leave(token, channel_id)
	assert len(channel_class.get_owner_list()) == 0
	

	# with pytest.raises(ValueError):
	# 	get_verified_channel_from_id(channel_id,channel_list)


'''=============================================================='''
'''             TESTING channel_join       '''
''' Test 1 : Test with correct inputs'''
def test_join_corr_inputs():
	global channel_list
	global my_users
	reset_channel_list()
	data_delete()

	authRegisterDict = auth_register("lily565657@unsw.com","quERty6526", "Lily", "Cheung")
	token = authRegisterDict['token']
	u_id = authRegisterDict ['u_id']

	channelsCreateDict = channels_create (token, "Channel 1", "true")
	channel_id = channelsCreateDict ['channel_id']

	assert (channels_listall(token) == [{"channel_id": channel_id, "name":"Channel 1"}])

	authRegisterDict2 = auth_register("marina@gmail.com","45445454225", "Dollar", "Lilz")
	token2 = authRegisterDict2['token']
	u_id2= authRegisterDict2 ['u_id']

	user_class2 = get_user_from_id(u_id2)
	num = user_class2.get_permission_id() 
	assert num != '1'

	channel_join(token2,channel_id)

	channel_test = get_verified_channel_from_id(channel_id,channel_list)

	assert (u_id2 in channel_test.get_mem_list())

	assert (u_id2 not in channel_test.get_owner_list())


''' Test 2 : Test invalid channel Id'''
''' This function test for ValueError when given an invalid id'''
def test_join_wrong_channel_id():

	authRegisterDict = auth_register("lily@unsw.com","quERty6526", "Lily", "Cheung")
	token = authRegisterDict['token']

	channel_id = "000000000"

	with pytest.raises(ValueError):
		channel_join(token,channel_id)

def test_join_not_admin_or_private_channel():
	global channel_list
	global my_users
	reset_channel_list()
	data_delete()

	authRegisterDict = auth_register("jono@unsw.com","quERty6526", "Lily", "Cheung")
	token1 = authRegisterDict['token']
	u_id1= authRegisterDict ['u_id']

	authRegisterDict2 = auth_register("marina@gmail.com","45445454225", "Dollar", "Lilz")
	token2 = authRegisterDict2['token']
	u_id2= authRegisterDict2 ['u_id']


	channelsCreateDict = channels_create (token1, "Channel 1", "False")
	channel_id = channelsCreateDict ['channel_id']

	with pytest.raises(AccessError):
		channel_join(token2,channel_id)

def test_join_user_already_member():
	global channel_list
	global my_users
	reset_channel_list()
	data_delete()

	authRegisterDict = auth_register("lily565657@unsw.com","quERty6526", "Lily", "Cheung")
	token = authRegisterDict['token']
	u_id = authRegisterDict ['u_id']

	channelsCreateDict = channels_create (token, "Channel 1", "true")
	channel_id = channelsCreateDict ['channel_id']

	assert (channels_listall(token) == [{"channel_id": channel_id, "name":"Channel 1"}])

	authRegisterDict2 = auth_register("marina@gmail.com","45445454225", "Dollar", "Lilz")
	token2 = authRegisterDict2['token']
	u_id2= authRegisterDict2 ['u_id']

	channel_join(token2,channel_id)

	with pytest.raises(ValueError):
		channel_join(token2,channel_id)
	
'''=============================================================='''
'''             TESTING channel_addowner        '''
# normal case
def test_channel_addowner_normal():
	global channel_list
	global my_users
	reset_channel_list()
	data_delete()

	authRegisterDict = auth_register("jono@unsw.com","quERty6526", "Lily", "Cheung")
	token1 = authRegisterDict['token']
	u_id1= authRegisterDict ['u_id']

	authRegisterDict2 = auth_register("marina@gmail.com","45445454225", "Dollar", "Lilz")
	token2 = authRegisterDict2['token']
	u_id2= authRegisterDict2 ['u_id']

	channelsCreateDict = channels_create (token1, "Channel 1", "true")
	channel_id_1 = channelsCreateDict ['channel_id']

	#setup: assuming token1 member is already an owner
		#add 2nd member
	channel_join (token2, channel_id_1)
	channel_addowner(token1, channel_id_1, u_id2)

	#iterate through members list to see he exists in members
	channel_test = get_verified_channel_from_id(channel_id_1,channel_list)


	assert (u_id2 in channel_test.get_mem_list())

	assert (u_id2 in channel_test.get_owner_list())

# value error when channel (based on ID) does not exist
def test_channel_addowner_no_channelid():
	global channel_list
	global my_users
	reset_channel_list()
	data_delete()

	authRegisterDict = auth_register("jono3@unsw.com","quERty6526", "Lily", "Cheung")
	token1 = authRegisterDict['token']
	u_id1= authRegisterDict ['u_id']

	authRegisterDict2 = auth_register("marina33@gmail.com","45445454225", "Dollar", "Lilz")
	token2 = authRegisterDict2['token']
	u_id2= authRegisterDict2 ['u_id']

	channelsCreateDict = channels_create (token1, "Channel 1", "true")
	channel_id_1 = channelsCreateDict ['channel_id']

	channel_join (token2, channel_id_1)

	bad_chan_id = "0405454"

	with pytest.raises(ValueError):
		channel_addowner (token1, bad_chan_id, u_id2)

# value error when user with u_id is already owner of the channel
def test_channel_addowner_already_owner():
	global channel_list
	global my_users
	reset_channel_list()
	data_delete()

	authRegisterDict = auth_register("jono2@unsw.com","quERty6526", "Lily", "Cheung")
	token1 = authRegisterDict['token']
	u_id1= authRegisterDict ['u_id']

	channelsCreateDict = channels_create (token1, "Channel 11", "true")
	channel_id_1 = channelsCreateDict ['channel_id']

	with pytest.raises(ValueError):
		channel_addowner (token1, channel_id_1, u_id1)


# access error when authorised user not an owner of slackr, or owner of channel
def test_channel_addowner_no_slackr():
	global channel_list
	global my_users
	reset_channel_list()
	data_delete()

	authRegisterDict = auth_register("jono1@unsw.com","quERty6526", "Lily", "Cheung")
	token1 = authRegisterDict['token']
	u_id1= authRegisterDict ['u_id']

	authRegisterDict2 = auth_register("marina1@gmail.com","45445454225", "Dollar", "Lilz")
	token2 = authRegisterDict2['token']
	u_id2= authRegisterDict2 ['u_id']

	authRegisterDict3 = auth_register("lisa@gmail.com","45445454225", "Dererr", "Lilz")
	token3 = authRegisterDict3['token']
	u_id3= authRegisterDict3 ['u_id']

	channelsCreateDict = channels_create (token1, "Channel 1", "true")
	channel_id_1 = channelsCreateDict ['channel_id']
	#setup:  only token1 is member and owner
	channel_join(token2, channel_id_1)
	channel_join(token3, channel_id_1)

	# token 2 trying to make token 3 owner
	with pytest.raises(AccessError):
		channel_addowner(token2, channel_id_1, u_id3)

'''=============================================================='''
'''             TESTING channel_removeowner        '''
# normal case
def test_channel_removeowner_normal():
	global channel_list
	global my_users
	reset_channel_list()
	data_delete()

	#Token
	authRegisterDict = auth_register("lily554466@unsw.com","quERty6526", "Lily", "Cheung")
	token1 = authRegisterDict['token']
	u_id1 = authRegisterDict ['u_id']

	authRegisterDict2 = auth_register("lily123@gmail.com","4545rg3eg35yh", "Dollar", "Lilz")
	token2 = authRegisterDict2['token']
	u_id2 = authRegisterDict2 ['u_id']

	#Channel ID
	channelsCreateDict = channels_create (token1, "Fine", "true")
	channel_id_1 = channelsCreateDict ['channel_id']

	channelsCreateDict2 = channels_create(token2, "Other Channel", False)
	channel_id_2 = channelsCreateDict2 ['channel_id']

	#setup: add token 2, make owner and then remove ownership of token 2
	channel_join (token2, channel_id_1)
	channel_addowner(token1, channel_id_1, u_id2)
	channel_removeowner (token1, channel_id_1, u_id2)

	channel_test = get_verified_channel_from_id(channel_id_1,channel_list)

	assert( u_id2 not in channel_test.get_owner_list())
	

# value error when channel (based on ID) does not exist
def test_channel_removeowner_no_channel_id():
	global channel_list
	global my_users
	reset_channel_list()
	data_delete()
	#Token
	authRegisterDict = auth_register("lilyhuh@unsw.com","quERty6526", "Lily", "Cheung")
	token1 = authRegisterDict['token']

	authRegisterDict2 = auth_register("lily124545453@gmail.com","4545rg3eg35yh", "Dollar", "Lilz")
	u_id2 = authRegisterDict2 ['u_id']

	#Channel ID
	channelsCreateDict = channels_create (token1, "Chan55nel 1", "true")
	channel_id_1 = channelsCreateDict ['channel_id']

	dne_channel = "328942394"

	with pytest.raises(ValueError):
		channel_removeowner (token1, dne_channel, u_id2)

# value error when user with u_id is not owner of the channel
# normal member of channel attempt to remove ownership of an owner
def test_channel_removeowner_not_owner1():
	global channel_list
	global my_users
	reset_channel_list()
	data_delete()
	#Token
	authRegisterDict = auth_register("lilywhy@unsw.com","quERty6526", "Lily", "Cheung")
	token1 = authRegisterDict['token']
	u_id1 = authRegisterDict ['u_id']

	authRegisterDict2 = auth_register("weguae@gmail.com","4545rg3eg35yh", "Dollar", "Lilz")
	token2 = authRegisterDict2['token']

	#Channel ID
	channelsCreateDict = channels_create (token1, "Channel 1", "true")
	channel_id_1 = channelsCreateDict ['channel_id']

	channel_join (token2, channel_id_1)

	with pytest.raises(AccessError):
		channel_removeowner(token2, channel_id_1, u_id1)

def test_channel_removeowner_not_owner2():
	global channel_list
	global my_users
	reset_channel_list()
	data_delete()

	#Token
	authRegisterDict = auth_register("lily554466@unsw.com","quERty6526", "Lily", "Cheung")
	token1 = authRegisterDict['token']
	u_id1 = authRegisterDict ['u_id']

	authRegisterDict2 = auth_register("lily123@gmail.com","4545rg3eg35yh", "Dollar", "Lilz")
	token2 = authRegisterDict2['token']
	u_id2 = authRegisterDict2 ['u_id']

	#Channel ID
	channelsCreateDict = channels_create (token1, "Fine", "true")
	channel_id_1 = channelsCreateDict ['channel_id']

	#setup: add token 2, make owner and then remove ownership of token 2
	channel_join (token2, channel_id_1)
	with pytest.raises(ValueError):
		channel_removeowner(token1, channel_id_1, u_id2)
		
'''=============================================================='''
'''             TESTING channel_list        '''

''' TESTS FOR CHANNELS_LIST '''
# channels_list shows the list of all the channels the user is a part of

def test_channels_list_normal():
	global channel_list
	global my_users
	reset_channel_list()
	data_delete()

	authRegisterDict = auth_register("li54466@unsw.com","quERty6526", "Lily", "Cheung")
	token1 = authRegisterDict['token']
	u_id1 = authRegisterDict['u_id']

	authRegisterDict2 = auth_register("l123@gmail.com","4545rg3eg35yh", "Dollar", "Lilz")
	token2 = authRegisterDict2['token']


	channelsCreateDict = channels_create (token1, "Channel 5", "true")
	channel_id_1 = channelsCreateDict ['channel_id']

	channelsCreateDict2 = channels_create(token2, "Other Channel 2", False)
	channel_id_2 = channelsCreateDict2 ['channel_id']

	channel_invite(token2, channel_id_2, u_id1)
	assert channels_list(token1) == [{'channel_id':channel_id_1,\
		'name': "Channel 5"},{'channel_id':channel_id_2, 'name':"Other Channel 2"}]


# no channels
def test_channels_list_no_channels():
	global channel_list
	global my_users
	reset_channel_list()
	data_delete()
	#setup: a token without any channels made
	no_chann = auth_register("sanaislif444e3@unsw.com","4gjejhgjWWW", "Sana", "Minatozaki")
	no_chann_token = no_chann['token']
	assert (channels_list(no_chann_token) == [])


'''=============================================================='''
'''             TESTING channel_listall        '''

### channels_listall should include all the channels the user is not a part of
### only testing to see if it displays all channels, else tested above
### Assumption: does not display private channel unless already a participant
###     - Third channel should not be listed since user is not a member and channel is private
def test_channels_listall_normal():
	global channel_list
	global my_users
	reset_channel_list()
	data_delete()

	#Set up
	authRegisterDict = auth_register("lil6767676767y@unsw.com","quERty6526", "Lily", "Cheung")
	token1 = authRegisterDict['token']
	u_id1= authRegisterDict ['u_id']

	authRegisterDict2 = auth_register("lily6566123@gmail.com","43e44Ttr45", "Dollar", "Lilz")
	token2 = authRegisterDict2['token']
	u_id2= authRegisterDict2 ['u_id']

	authRegisterDict4 = auth_register("momoisli33fe@unsw.com","4gjejhgjWWW", "Momo", "Hirai")
	token4 = authRegisterDict4['token']
	u_id4 =  authRegisterDict4 ['u_id']

	channelsCreateDict = channels_create (token1, "Channel 1", "true")
	channel_id_1 = channelsCreateDict ['channel_id']

	channelsCreateDict2 = channels_create(token2, "Other Channe2", False)
	channel_id_2 = channelsCreateDict2 ['channel_id']

	channelsCreateDict4 = channels_create(token4, "Fourth Channe4", "true")
	channel_id_4 = channelsCreateDict4 ['channel_id']

	#token 2 invites id1 to channel
	channel_invite(token2, channel_id_2, u_id1)
	channel_join(token1, channel_id_4)

	assert (channels_listall(token1) == [{'channel_id':channel_id_1 , 'name': "Channel 1"},{'channel_id':channel_id_2, 'name':"Other Channe2"},{'channel_id':channel_id_4, 'name':"Fourth Channe4"}])

def test_listall_normal_slackr_owner():
	global channel_list
	global my_users
	reset_channel_list()
	data_delete()

	#Set up
	authRegisterDict = auth_register("lil6767676767y@unsw.com","quERty6526", "Lily", "Cheung")
	token1 = authRegisterDict['token']
	u_id1= authRegisterDict ['u_id']
	user = get_user_from_id(u_id1)
	user.set_permission_id(3)

	authRegisterDict2 = auth_register("lily6566123@gmail.com","43e44Ttr45", "Dollar", "Lilz")
	token2 = authRegisterDict2['token']
	u_id2= authRegisterDict2 ['u_id']

	channelsCreateDict = channels_create (token1, "Channel 1", "true")
	channel_id_1 = channelsCreateDict ['channel_id']

	channelsCreateDict2 = channels_create(token2, "Other Channe2", False)
	channel_id_2 = channelsCreateDict2 ['channel_id']

	assert (channels_listall(token1) == [{'channel_id':channel_id_1 , 'name': "Channel 1"}])

'''=============================================================='''
'''             TESTING channel_create        '''
def test_channels_create_normal():
	reset_channel_list()
	data_delete()

	global my_users
	global channel_list
	reset_channel_list()
	details = auth_register("student3333@unsw.edu","4545DFHUgnww", "Dollar", "Lilz")
	dummy_token = details['token']
	dummy_uid = details['u_id']

	# before creating channel
	assert (channels_list(dummy_token) == [])

	# after creating channel
	newChannel = channels_create(dummy_token, 'Best Channel', "true")
	new_chan_id = newChannel ['channel_id']

	chan = get_verified_channel_from_id(new_chan_id, channel_list)
	assert (chan.get_active_standup() == False)

	# assert channel id is not null
	assert (channels_list(dummy_token) == [{'channel_id':new_chan_id, 'name':"Best Channel"}])
	

#value error if name is more than 20 characters long
def test_channels_create_twenty_characters():
	reset_channel_list()
	data_delete()

	global my_users
	global channel_list
	details = auth_register('student333@unsw.edu',"4545DFHUgnww", "Dollar", "Lilz")
	dummy_token = details['token']

   # with pytest.raises(ValueError, match=r"*Channel name exceeded 20 characters*"):
	#    channels_create(dummy_token, "This is more than 20 characters", "true")

	with pytest.raises(ValueError):
		channels_create(dummy_token, "This is more than 20 characters", "true")

'''=============================================================='''
'''             TESTING channel_id_generate        '''
def test_channel_id_generate():
	global my_users
	reset_channel_list()
	data_delete()

	assert channel_id_generate() != None
'''=============================================================='''
'''             TESTING channel_valid_id       '''
def test_channel_valid_id():
	global my_users
	reset_channel_list()
	data_delete()

	authRegisterDict = auth_register("lil6767676767y@unsw.com","quERty6526", "Lily", "Cheung")
	token1 = authRegisterDict['token']
	u_id1= authRegisterDict ['u_id']

	channelsCreateDict = channels_create (token1, "Channel 1", "true")
	channel_id_1 = channelsCreateDict ['channel_id']

	assert channel_valid_id(channel_id_1) == True

def test_channel_not_valid_id():
	global my_users
	reset_channel_list()
	data_delete()

	channel_id_1 = "22852868268"

	assert channel_valid_id(channel_id_1) == False
	
