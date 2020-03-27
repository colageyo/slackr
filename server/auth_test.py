from server.user_class import auth_register, token_generate, my_users, auth_login, auth_logout, auth_passwordreset_request, auth_passwordreset_reset, data_delete, get_user_from_token, admin_userpermission_change
import pytest
from server.access_error import AccessError
from server.channel_class import *
     
'''                         TESTING auth_login                   '''

'''Test 1 : correct email and correct password'''
def test_login_corr():
    global my_users
    data_delete()
    user = auth_register("st@unsw.edu","password","Student","Citizen")
    userDict = auth_login("st@unsw.edu",'password')
    assert userDict['u_id'] == user['u_id']
    assert get_user_from_token(userDict['token']) == my_users[0]
    
'''Test 2 : correct email and incorrect password'''
def test_wr_Pass():
    global my_users
    user = {"email" : "st@unsw.edu", "password" : "passwords"}
    
    with pytest.raises(ValueError):
        auth_login(user["email"],user["password"])
        
'''Test 3 : incorrect email and correct password'''
def test_in_email():
    global my_users
    user = {"email" : "stu@unsw.edu", "password" : "passwords"}
    
    with pytest.raises(ValueError):
        auth_login(user["email"],user["password"])
        
'''Test 4 : invalid email and incorrect password'''
def test_wr_pasemail():
    global my_users
    user = {"email" : "1234567", "password" : "4cha"}
    
    with pytest.raises(ValueError):
        auth_login(user["email"],user["password"])
        
'''Test 5 : incorrect email and incorrect password'''
def test_nonEx_email():
    global my_users
    user = {"email" : "Somethingnew@gmail.com", "password" : "abcd1234"}
    
    with pytest.raises(ValueError):
        auth_login(user["email"],user["password"])

'''=============================================================='''
'''                   TESTING auth_logout                        '''

''' Test 1: test with an active token '''
def test_act_tok():
    global my_users
    data_delete() 
    
    auth_register("st@unsw.edu","password","Student","Citizen")
    userDict = auth_login("st@unsw.edu",'password')
    is_success = auth_logout(userDict['token'])
    assert is_success == True
    
   
''' Test 2: test with an inactive token '''
def test_empty_token_list():
    global my_users
    data_delete() 
    
    userDict = auth_register("st@unsw.edu","password","Student","Citizen")
    
    assert auth_logout(userDict['token']) == True
    
    with pytest.raises(AccessError):
        auth_logout("123456")
        
'''=============================================================='''
'''                         TESTING auth_register                '''

''' Test 1: with correct email, password, name_first and name_last '''
def test_regist_corr():
    global my_users
    data_delete()
    user = {"email" : "something123@gmail.com",
    "password" : "PassW0rd",
    "name_first" : "Steve",
    "name_last" : "Chow"}
    
    userDict = auth_register(user["email"],user["password"],user["name_first"],\
    user["name_last"])
    
    userClass = my_users[0]
    
    assert userClass.get_uid() == userDict['u_id']
    assert userClass.get_name_first() == user['name_first']
    
    
''' Test 2: invalid email'''
def test_inV_email():
    global my_users
    data_delete()
    user = {"email" : "emailInvalid##@gmail.vom",
    "password" : "abcd123456",
    "name_first" : "Steve",
    "name_last" : "Chow"}
    
    with pytest.raises(ValueError):
        auth_register(user["email"],user["password"],user["name_first"],\
    user["name_last"])
    
''' Test 3 : email already in use '''
def test_nonE_email():
    global my_users
    data_delete()
    user1 = {"email" : "nonExistEmail@gmail.com",
    "password" : "cabcd123456",
    "name_first" : "Steve",
    "name_last" : "cChaow"}
    
    user2 = {"email" : "nonExistEmail@gmail.com",
    "password" : "abcd123456",
    "name_first" : "Steve",
    "name_last" : "Chaow"}
    
    userDict = auth_register(user1["email"],user1["password"],user1["name_first"],\
    user1["name_last"])
    with pytest.raises(ValueError):
        auth_register(user2["email"],user2["password"],user2["name_first"],\
    user2["name_last"])

''' Test 4 : wrong Password'''
def test_wr_pass():
    global my_users
    data_delete()
    user = {"email" : "ValidEmail@mail.com",
    "password" : "4cha",
    "name_first" : "Steve",
    "name_last" : "Chow"}
    
    with pytest.raises(ValueError):
        auth_register(user["email"],user["password"],user["name_first"],\
    user["name_last"])
    
''' Test 5 : name_first > 50 '''
def test_Fmore50():
    global my_users
    data_delete()
    user = {"email" : "correctEmail@gmail.com",
    "password" : "abcd123456",
    
    "name_first" : "sadfjgsdjfsidfgwgfuiwagfusiufagsfisfisdufsufsifusdfjhshfshfsdj"\
    +"ffshfsdjfsdfsdifvgwaihfvawhfvwycchvwechwcvwhcwfvwefVIFFFWFWFF",
    
    "name_last" : "Chow"}
    
    with pytest.raises(ValueError):
        auth_register(user["email"],user["password"],user["name_first"],\
    user["name_last"])
    
''' Test 6 : name_last > 50 '''
def test_Lmore50():
    global my_users
    data_delete()
    user = {"email" : "correctEmail@gmail.com",
    "password" : "abcd123456",
    
    "name_first" : "Steve",
    
    "name_last" : "sadfjgsdjfsidfgwgfuiwagfusiufagsfisfisdufsufsifusdfjhshfshfsdj"\
    +"ffshfsdjfsdfsdifvgwaihfvawhfvwycchvwechwcvwhcwfvwefVIFFFWFWFF"}
    
    with pytest.raises(ValueError):
        auth_register(user["email"],user["password"],user["name_first"],\
        user["name_last"])
        
''' Test 6 : Same name '''
def test_handle_already_used():
    global my_users
    data_delete()
    auth_register("st@unsw.edu","password","Student","Citizen")
    auth_register("stu@unsw.edu","password","Student","Citizen")
    user = auth_login("stu@unsw.edu",'password')
    
    userClass = get_user_from_token(user['token'])
    # Checking handle
    
    assert(userClass.get_handle_str() == "studentcitizen1")
    
''' Test 6 : Same name(handle generated longer than 20 characters) '''
def test_handle_already_used2():
    global my_users
    data_delete()
    auth_register("st@unsw.edu","password","Studentabcde","Citizen")
    auth_register("stu@unsw.edu","password","Studentabcde","Citizen")
    user = auth_login("stu@unsw.edu",'password')
    
    userClass = get_user_from_token(user['token'])
    # Checking handle
    
    assert(userClass.get_handle_str() == "studentabcdecitizen1")
    
'''=============================================================='''
'''            TESTING admin_userpermission_change              '''
def test_invalid_uid_permission():
    global my_users
    data_delete()
    userDict1 = auth_register("st@unsw.edu","password","Student","Citizen")
    userDict2 = auth_register("stu@unsw.edu","password","Student","Citizen")
    
    with pytest.raises(ValueError):
        admin_userpermission_change(userDict2['token'], 123, 1)
        
    userClass = get_user_from_token(userDict2['token'])
    assert userClass.get_permission_id() == 3
    
def test_invalid_caller():
    global my_users
    data_delete()
    userDict1 = auth_register("st@unsw.edu","password","Student","Citizen")
    userDict2 = auth_register("stu@unsw.edu","password","Student","Citizen")
    
    with pytest.raises(AccessError):
        admin_userpermission_change(userDict2['token'], userDict2['u_id'], 1)
        
    userClass = get_user_from_token(userDict2['token'])
    assert userClass.get_permission_id() == 3

def test_invalid_permission_id():
    global my_users
    data_delete()
    userDict1 = auth_register("st@unsw.edu","password","Student","Citizen")
    userDict2 = auth_register("stu@unsw.edu","password","Student","Citizen")
    
    with pytest.raises(ValueError):
        admin_userpermission_change(userDict1['token'], userDict2['u_id'], 5)
        
    userClass = get_user_from_token(userDict2['token'])
    assert userClass.get_permission_id() == 3
 
def test_admin_change_to_owner():
    global my_users
    data_delete()
    userDict1 = auth_register("st@unsw.edu","password","Student","Citizen")
    userDict2 = auth_register("stu@unsw.edu","password","Student","Citizen")
    userDict3 = auth_register("stus@unsw.edu","password","Student","Citizen")
    admin_userpermission_change(userDict1['token'], userDict2['u_id'], 2)
    
    with pytest.raises(AccessError):
        admin_userpermission_change(userDict2['token'], userDict3['u_id'], 1)
        
    userClass = get_user_from_token(userDict2['token'])
    assert userClass.get_permission_id() == 2
    
def test_admin_change_to_admin():
    global my_users
    data_delete()
    userDict1 = auth_register("st@unsw.edu","password","Student","Citizen")
    userDict2 = auth_register("stu@unsw.edu","password","Student","Citizen")
    userDict3 = auth_register("stus@unsw.edu","password","Student","Citizen")
    channel_id = channels_create(userDict1['token'],'Channel1',False)
    channel_invite(userDict1['token'], channel_id['channel_id'], userDict2['u_id'])
    channel_invite(userDict1['token'], channel_id['channel_id'], userDict3['u_id'])
    admin_userpermission_change(userDict1['token'], userDict2['u_id'], 2)
    admin_userpermission_change(userDict2['token'], userDict3['u_id'], 2)
        
    userClass = get_user_from_token(userDict3['token'])
    assert userClass.get_permission_id() == 2
    
def test_owner_change_to_owner():
    global my_users
    data_delete()
    userDict1 = auth_register("st@unsw.edu","password","Student","Citizen")
    userDict2 = auth_register("stu@unsw.edu","password","Student","Citizen")
    channel_id = channels_create(userDict1['token'],'Channel1',False)
    admin_userpermission_change(userDict1['token'], userDict2['u_id'], 2)
    channel_join(userDict2['token'], channel_id['channel_id'])
    admin_userpermission_change(userDict1['token'], userDict2['u_id'], 1)
    
    userClass = get_user_from_token(userDict2['token'])
    assert userClass.get_permission_id() == 1
    
def test_member_change_to_member():
    global my_users
    data_delete()
    userDict1 = auth_register("st@unsw.edu","password","Student","Citizen")
    userDict2 = auth_register("stu@unsw.edu","password","Student","Citizen")
    userDict3 = auth_register("stus@unsw.edu","password","Student","Citizen")
    
    with pytest.raises(AccessError):
        admin_userpermission_change(userDict2['token'], userDict3['u_id'],3)
    
    userClass = get_user_from_token(userDict3['token'])
    
    assert userClass.get_permission_id() == 3

def test_member_change_to_owner_or_admin():
    global my_users
    data_delete()
    userDict1 = auth_register("st@unsw.edu","password","Student","Citizen")
    userDict2 = auth_register("stu@unsw.edu","password","Student","Citizen")
    userDict3 = auth_register("stus@unsw.edu","password","Student","Citizen")
    
    with pytest.raises(AccessError):
        admin_userpermission_change(userDict2['token'], userDict3['u_id'], 2)
    
    userClass = get_user_from_token(userDict3['token'])
    assert userClass.get_permission_id() == 3

def test_admin_change_owner():
    global my_users
    data_delete()
    userDict1 = auth_register("st@unsw.edu","password","Student","Citizen")
    userDict2 = auth_register("stu@unsw.edu","password","Student","Citizen")
    admin_userpermission_change(userDict1['token'], userDict2['u_id'], 2)
    
    with pytest.raises(AccessError):
        admin_userpermission_change(userDict2['token'], userDict1['u_id'], 2)
        
    userClass = get_user_from_token(userDict1['token'])
    assert userClass.get_permission_id() == 1
    
def test_owner_change_admin_to_member():
    global my_users
    data_delete()
    userDict1 = auth_register("st@unsw.edu","password","Student","Citizen")
    userDict2 = auth_register("stu@unsw.edu","password","Student","Citizen")
    channel_id = channels_create(userDict1['token'],'Channel1',False)
    admin_userpermission_change(userDict1['token'], userDict2['u_id'], 2)
    channel_join(userDict2['token'], channel_id['channel_id'])
    admin_userpermission_change(userDict1['token'], userDict2['u_id'], 3)
    
    userClass = get_user_from_token(userDict2['token'])
    assert userClass.get_permission_id() == 3
    
def test_admint_change_admin_to_admin():
    global my_users
    data_delete()
    userDict1 = auth_register("st@unsw.edu","password","Student","Citizen")
    userDict2 = auth_register("stu@unsw.edu","password","Student","Citizen")
    userDict3 = auth_register("stus@unsw.edu","password","Student","Citizen")

    admin_userpermission_change(userDict1['token'], userDict2['u_id'], 2)
    admin_userpermission_change(userDict1['token'], userDict3['u_id'], 2)
    admin_userpermission_change(userDict2['token'], userDict3['u_id'], 3)
    
    userClass = get_user_from_token(userDict3['token'])
    assert userClass.get_permission_id() == 3
