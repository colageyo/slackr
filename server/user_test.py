from server.user_class import user_profile, user_profile_sethandle, user_profile_setname, user_profile_setemail, auth_register, my_users, data_delete, auth_login, users_get_all, get_user_from_token
import pytest
from server.access_error import AccessError

'''                       TESTING user_profile                   '''
# Testing the function with correct inputs
def test_correct_profile():
    global my_users
    data_delete()
    auth_register("st@unsw.edu","password","Student","Citizen")
    userDict = auth_login("st@unsw.edu",'password')
    # Testing user_profile
    profile = user_profile(userDict['token'], userDict['u_id'])
    
    assert(profile['email'] == 'st@unsw.edu')
    assert(profile['name_first'] == 'Student')
    assert(profile['name_last'] == 'Citizen')
    assert(profile['handle_str'] == 'studentcitizen')
    
# Testing the function with an invalid u_id
def test_invalid_id():
    global my_users
    data_delete()
    auth_register("st@unsw.edu","password","Student","Citizen")
    user = auth_login("st@unsw.edu",'password')
    
    # Testing user_profile
    with pytest.raises(ValueError):
        user_profile(user['token'], '546')

# Testing the function with no inputs
def test_no_inputs_profile():
    
    # Testing user_profile
    with pytest.raises(AccessError):
        user_profile("", "")
        
'''=============================================================='''
'''               TESTING user_profile_sethandle                 '''
# Testing function with correct inputs
def test_correct_sethandle():
    global my_users
    data_delete()
    auth_register("st@unsw.edu","password","Student","Citizen")
    user = auth_login("st@unsw.edu",'password')
    
    # Changing user's handle
    user_profile_sethandle(user['token'],"Apple")
    
    # Checking handle
    profile = user_profile(user['token'], user['u_id'])
    assert(profile['handle_str'] == "Apple")
    
# Testing function with a handle longer than 20 characters
def test_handle_too_long():
    global my_users
    data_delete()
    auth_register("st@unsw.edu","password","Student","Citizen")
    user = auth_login("st@unsw.edu",'password')
    
    # Changing user's handle
    with pytest.raises(ValueError):
        user_profile_sethandle(user['token'],"abcdefghijklmnopqrstuvwxyz")
    
    # Checking handle
    profile = user_profile(user['token'], user['u_id'])
    assert(profile['handle_str'] == "studentcitizen")
    
# Testing function with no inputs
def test_no_inputs_handle():
    global my_users
    data_delete()
    auth_register("st@unsw.edu","password","Student","Citizen")
    user = auth_login("st@unsw.edu",'password')
    
    # Changing user's handle
    with pytest.raises(AccessError):
        user_profile_sethandle("","")
    
    # Checking handle
    profile = user_profile(user['token'], user['u_id'])
    assert(profile['handle_str'] == "studentcitizen")
    
def test_20_users():
    global my_users
    data_delete()
    for i in range(0,19):
        string = "st" + str(i) + "@unsw.edu.au"
        user = auth_register(string,"password","Studentabcde","Citizen")
        userDict = user_profile(user['token'], user['u_id']);
        handle = "studentabcdecitize"
        if i == 0:
            handle += "n"
        elif i >= 1 and i < 10:
            handle += "n" + str(i)
        else:
            handle += str(i)
        assert handle == userDict['handle_str']

def test_same_handle():
    global my_users
    data_delete()
    user1 = auth_register("st@unsw.edu","password","Student","Citizen")
    user2 = auth_register("stu@unsw.edu","password","jono","huang")
    
    # Changing user's handle
    with pytest.raises(ValueError):
        user_profile_sethandle(user2['token'],"studentcitizen")
    # Checking handle
    
'''=============================================================='''
'''                TESTING user_profile_setname                  '''
# Testing function with correct inputs
def test_correct_name():
    global my_users
    data_delete()
    auth_register("st@unsw.edu","password","Student","Citizen")
    user = auth_login("st@unsw.edu",'password')
    
    # Changing user's email
    user_profile_setname(user['token'],'Citizen','Student')
    
    # Testing user_profile
    profile = user_profile(user['token'], user['u_id'])
    assert(profile['name_first'] == 'Citizen')
    assert(profile['name_last'] == 'Student')
    
# Testing function with invalid last name
def test_invalid_last_name():
    global my_users
    data_delete()
    auth_register("st@unsw.edu","password","Student","Citizen")
    user = auth_login("st@unsw.edu",'password')
    
    last_name = "abcdefghijklmnopqrstuvwxyzabcdefghijklmnopqrstuvwxyz"
    
    # Changing user's name
    with pytest.raises(ValueError):
        user_profile_setname(user['token'],'Student',last_name)
    
    # Checking email
    profile = user_profile(user['token'], user['u_id'])
    assert(profile['name_last'] == 'Citizen')
    assert(profile['name_first'] == 'Student')
    
# Testing function with invalid first name
def test_invalid_first_name():
    global my_users
    data_delete()
    auth_register("st@unsw.edu","password","Student","Citizen")
    user = auth_login("st@unsw.edu",'password')
    
    
    first_name = "abcdefghijklmnopqrstuvwxyzabcdefghijklmnopqrstuvwxyz"
    
    # Changing user's name
    with pytest.raises(ValueError):
        user_profile_setname(user['token'],first_name,'Citizen')
    
    # Checking name
    profile = user_profile(user['token'], user['u_id'])
    assert(profile['name_last'] == 'Citizen')
    assert(profile['name_first'] == 'Student')

# Testing function with no inputs
def test_name_no_inputs():
    global my_users
    data_delete()
    auth_register("st@unsw.edu","password","Student","Citizen")
    user = auth_login("st@unsw.edu",'password')
    
    
    # Changing user's name
    with pytest.raises(AccessError):
        user_profile_setname("","","")
    
    # Checking name
    profile = user_profile(user['token'], user['u_id'])
    assert(profile['name_last'] == 'Citizen')
    assert(profile['name_first'] == 'Student')
    
'''=============================================================='''
'''                TESTING user_profile_setemail                 '''
# Testing function with correct inputs
def test_correct_email():
    global my_users
    data_delete()
    auth_register("st@unsw.edu","password","Student","Citizen")
    user = auth_login("st@unsw.edu",'password')
    
    
    # Changing user's email
    user_profile_setemail(user['token'],'student@unsw.edu')
    
    # Testing user_profile
    profile = user_profile(user['token'], user['u_id'])
    assert(profile['email'] == 'student@unsw.edu')
    
# Testing function with invalid email address
def test_invalid_email():
    global my_users
    data_delete()
    auth_register("st@unsw.edu","password","Student","Citizen")
    user = auth_login("st@unsw.edu",'password')
    
    
    # Changing user's email
    with pytest.raises(ValueError):
        user_profile_setemail(user['token'],"asouhd")
    
    # Checking email
    profile = user_profile(user['token'], user['u_id'])
    assert(profile['email'] == 'st@unsw.edu')
    
# Testing function with email address that's already in use
def test_email_used():
    global my_users
    data_delete()
    auth_register("st@unsw.edu","password","Student","Citizen")
    user = auth_login("st@unsw.edu",'password')
    
    
    # Creating user 2
    user2 = auth_register("haha@gmail.com", "Lilyisthebest555", "John", "Smith")
    token2 = user2['token']
    
    # Changing user's email
    with pytest.raises(ValueError):
        user_profile_setemail(user['token'],"haha@gmail.com")
    
    # Checking email
    profile = user_profile(user['token'], user['u_id'])
    assert(profile['email'] == 'st@unsw.edu')
    
# Testing function with no inputs
def test_email_no_inputs():
    global my_users
    data_delete()
    auth_register("st@unsw.edu","password","Student","Citizen")
    user = auth_login("st@unsw.edu",'password')
    
    
     # Changing user's email
    with pytest.raises(AccessError):
        user_profile_setemail("","")
    
    # Checking email
    profile = user_profile(user['token'], user['u_id'])
    assert(profile['email'] == 'st@unsw.edu')
    
'''=============================================================='''
'''                     TESTING user_all                         '''
# Testing function with correct inputs
def test_correct_user_all():
    global my_users
    data_delete()
    user1 = auth_register("st@unsw.edu","password","Student","Citizen")
    user2 = auth_register("stu@unsw.edu","password","Citizen","Student")
    users = users_get_all(user1['token']);
    
    userDict1 = users[0]
    userDict2 = users[1]
    
    assert userDict1['email'] == "st@unsw.edu"
    assert userDict1['name_first'] == "Student"
    assert userDict2['email'] == "stu@unsw.edu"
    assert userDict2['name_first'] == "Citizen"

