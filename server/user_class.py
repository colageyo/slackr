""" This file contains the class USER """
import jwt
import re
import hashlib
import uuid
import random
from server.access_error import AccessError
import yagmail
from datetime import datetime
import sys
import urllib.request
from PIL import Image


class User: 

    def __init__(self, tokens, u_id, email, password, name_first, name_last, \
        handle_str, permission_id, reset_code, profile_img_url):
        
        self.tokens = tokens
        self.u_id = u_id
        self.email = email
        self.password = password
        self.name_first = name_first
        self.name_last = name_last
        self.handle_str = handle_str
        self.permission_id = permission_id
        self.profile_img_url = profile_img_url


    def get_email(self):
        return self.email
    def get_password(self):
        return self.password
    def get_uid(self):
        return self.u_id 
    def get_handle_str(self):
        return self.handle_str
    def get_reset_code(self):
        return self.reset_code                      #pragma: no cover
    def get_tokens(self):
        return self.tokens
    def get_name_first(self):
        return self.name_first
    def get_name_last(self):
        return self.name_last
    def get_permission_id(self):
        return self.permission_id
    def get_profile_img_url(self):
        return self.profile_img_url
    
    def set_password(self, password):
        self.password = password                    #pragma: no cover
    def set_reset_code(self, reset_code):
        self.reset_code = reset_code                #pragma: no cover
    def set_handle_str(self, handle_str):
        self.handle_str = handle_str
    def set_name_first(self, name_first):
        self.name_first = name_first
    def set_name_last(self, name_last):
        self.name_last = name_last
    def set_email(self, email):
        self.email = email
    def set_permission_id(self, permission_id):
        self.permission_id = permission_id
    def set_profile_img_url(self, profile_img_url):
        self.profile_img_url = profile_img_url      #pragma: no cover

    
my_users = []
my_request_codes = []
SECRET = 'Rayden'
handle_str_ext = 0
my_uid = 0

##  DECORATORS START ##
def authorise_token(function):
    def wrapper(*args, **kwargs):
        argsList = list(args)
        if not user_valid_token(argsList[0]):
            raise AccessError("Invalid User Token")
        return function(*args, **kwargs)
    return wrapper
## DECORATORS END ##

def data_delete():
    global my_users
    global handle_str_ext
    handle_str_ext = 0
    my_users.clear()
    return my_users

def auth_register(email, password, name_first, name_last):
    global my_users
    if (user_valid_email(email)):
        if (user_unique_email(email)):
            if (user_valid_password(password, 6)):
                if (user_valid_name(name_first, 50) and user_valid_name(name_last, 50)):
                    u_id = user_id_generate()
                    token = token_generate(u_id)
                    handle_str = user_handle_generate(name_first, name_last)
                    my_users.append(User([token], u_id, email, hash_value(password),\
                        name_first, name_last, handle_str, 3, None, None))
                    if (len(my_users) == 1):
                        get_user_from_token(token).set_permission_id(1)
                    return {"u_id" : u_id, "token": token}
                else :
                    raise ValueError("Invalid First or Last Name")
            else :
                 raise ValueError("Invalid Password")
        else :
            raise ValueError("This User Already Exists")
    else :
        raise ValueError("Invalid Email Format")


def auth_login(email, password):
    global my_users
    if (user_valid_email(email)):
        if (get_user_by_email(email) is not None):
            if (get_user_by_email(email).get_password() == hash_value(password)):
                    token = token_generate(get_user_by_email(email).get_uid())
                    get_user_by_email(email).get_tokens().append(token)
                    return {'u_id' : get_user_by_email(email).get_uid(), 'token': token }
            else :
                raise ValueError("Invalid Password Entered")
        else :
            raise ValueError("A User With This Email Does Not Exist")
    else :
        raise ValueError("Invalid Email Format")

@authorise_token            
def auth_logout(token):
    get_user_from_token(token).get_tokens().remove(token)
    return True
 
#pragma: no cover
def auth_passwordreset_request(email):
    if not user_unique_email(email):                                        #pragma: no cover
        reset_code = request_code_generate()                                
        send_email(email, message = reset_code)                             
        get_user_by_email(email).set_reset_code(hash_value(reset_code))     
        return True                                                         
    else :                                                                  #pragma: no cover
        raise ValueError                                                    #pragma: no cover

#pragma: no cover
def auth_passwordreset_reset(reset_code, new_password):
    global my_users                                                          #pragma: no cover
    for user in my_users:                                                    #pragma: no cover
        if (user.get_reset_code() == hash_value(reset_code)):                
            if (user_valid_password(new_password, 6)):                          
                user.set_password(hash_value(new_password))                 
                return True                                                  
            else :                                                           
                raise ValueError("Invalid Password")                         
    else :                                                                   #pragma: no cover
        raise ValueError("Please enter a valid reset code")                  #pragma: no cover

@authorise_token
def user_profile(token, u_id):
    global my_users
    if (user_valid_uid(u_id)):
        return { 'u_id' : u_id,
                'email' : get_user_from_id(u_id).get_email(), 
                'name_first' : get_user_from_id(u_id).get_name_first(),
                'name_last' : get_user_from_id(u_id).get_name_last(),
                'handle_str' : get_user_from_id(u_id).get_handle_str(),
                'profile_img_url' : get_user_from_id(u_id).get_profile_img_url()
                }
    else:
        raise ValueError("Invalid User ID")

@authorise_token
def user_profile_setname(token, name_first, name_last):
    global my_users
    if (user_valid_name(name_first, 50)):
        if(user_valid_name(name_last, 50)):
            get_user_from_token(token).set_name_first(name_first)
            get_user_from_token(token).set_name_last(name_last)
            return True
        else :
            raise ValueError("Invalid Last Name")
    else :
        raise ValueError("Invalid First Name")

@authorise_token
def user_profile_setemail(token, email):
    global my_users
    if (user_valid_email(email)):
        if (user_unique_email(email)):
            get_user_from_token(token).set_email(email)
            return True
        else :
            raise ValueError("User With This Email Already Exists")
    else :
        raise ValueError("Invalid Email Format")

@authorise_token
def user_profile_sethandle(token, handle_str):
    global my_users
    if (user_valid_handle_str(handle_str)):
        get_user_from_token(token).set_handle_str(handle_str)
        return True
    else :
        raise ValueError("Choose a Different Handle")

@authorise_token
def user_profiles_uploadphoto(token, img_url, x_start, y_start, x_end, y_end, local_host):
    global my_users                                                                     #pragma: no cover
    user = get_user_from_token(token)                                                   #pragma: no cover
    user_id = user.get_uid()                                                            #pragma: no cover

    user_image = str(user_id) +"image.jpg"                                              #pragma: no cover
    path = './static/'+ user_image                                                      #pragma: no cover

    if not img_url.endswith('.jpg'):                                                    #pragma: no cover
        raise ValueError("the file is not a .JPG")

    picture = urllib.request.urlopen(img_url)                                           #pragma: no cover
    if (picture.getcode() != 200):                                                      #pragma: no cover
        raise ValueError("HTTP status over 200")

    urllib.request.urlretrieve(img_url,path)                                            #pragma: no cover
    
    imageObject = Image.open(path)                                                      #pragma: no cover
    width, height = imageObject.size                                                    #pragma: no cover
    if (x_start > width) or (x_end > width) or (y_end > height) or (y_start > height)\
            or (x_start >= x_end) or (y_start >= y_end):                                #pragma: no cover
        raise ValueError("Invalid crop dimension")

    cropped = imageObject.crop((x_start, y_start, x_end, y_end))                        #pragma: no cover
    cropped.save(path)                                                                  #pragma: no cover
    
    us_img_url = local_host +'static/' +user_image                                      #pragma: no cover
    user.set_profile_img_url(us_img_url)                                                #pragma: no cover


@authorise_token
def users_get_all(token):
    global my_users
    return generate_users_all()

@authorise_token
def admin_userpermission_change(token, u_id, permission_id):
    global my_users
    user = get_user_from_token(token)

    if (user_valid_uid(u_id)): 
        if (user_valid_permission_id(permission_id)):
            if (user.get_permission_id() == 1):
                get_user_from_id(u_id).set_permission_id(permission_id)
                if permission_id == 1 or permission_id == 2:
                    make_user_owner_in_all_channels(u_id)
                return True
            if (user.get_permission_id() == 2):
                if (permission_id == 1):
                    raise AccessError("As an Admin, You Can Not Change Other Users to Owners")
                if (user_is_not_an_owner(u_id)):
                    get_user_from_id(u_id).set_permission_id(permission_id)
                    if permission_id == 2:
                        make_user_owner_in_all_channels(u_id)
                    return True
                else :
                    raise AccessError("As An Admin, You Can Not Change An Owner's Privileges")
            else:
                    raise AccessError("As a Member, You Can Not Change Anyone's Privileges")
        else :
            raise ValueError("Your Permission ID is Invalid")
    else :
        raise ValueError("Invalid User ID")


## CHECKER FUNCTIONS START ##
def user_unique_email(email):
    global my_users
    for user in my_users:
        if (user.get_email() == email):
            return False
    return True

def user_valid_email(email):
    regex = '^\w+([\.-]?\w+)*@\w+([\.-]?\w+)*(\.\w{2,3})+$'
    if (re.search(regex,str(email))):
        return True
    return False

def user_valid_password(password, password_length):
    if (len(str(password)) > password_length or len(str(password)) == password_length):
        return True
    return False

def user_valid_name(name, name_max_length):
    if (len(str(name)) > 1 and len(str(name)) < name_max_length):
        return True
    return False

def user_valid_token(token):
    for user in my_users:
        for tokens in user.get_tokens():
            if tokens == token:
                return True
    return False

def user_valid_uid(u_id):
    for user in my_users:
        if user.get_uid() == u_id:
            return True
    return False

def user_valid_handle_str(handle_str):
    for user in my_users:
        if user.get_handle_str() != handle_str:
            if (len(str(handle_str)) <= 20 and len(str(handle_str)) >= 3):
                return True
        else:
            return False

def user_valid_permission_id(permission_id):
    if (permission_id == 1 or permission_id == 2 or permission_id == 3):
        return True
    return False

def user_is_not_an_owner(u_id):
    user = get_user_from_id(u_id)
    if user.get_permission_id() == 1:
        return False
    return True


## CHECKER FUNCTIONS END ##

## GET USER FUNCTIONS START ##
def get_user_by_email(email):
    global my_users
    for user in my_users:
        if (user.get_email() == email):
            return user
    return None

def get_user_from_token(token):
    global SECRET
    decoded = jwt.decode(token, SECRET, algorithms = ['HS256'])
    return get_user_from_id(decoded['u_id'])


def get_user_from_id(u_id):
    global my_users
    for user in my_users:
        if (int(u_id) == user.get_uid()):
            return user
    return None

## GET USER FUNCTIONS END ##


## HELPER FUNCTIONS START ##
def send_email(to_email, message):
    
    sender_email = 'fantastic.five.gr@gmail.com'            #pragma: no cover
    password = 'Rayden123'                                  #pragma: no cover
    
    yag = yagmail.SMTP(sender_email, password)              #pragma: no cover
    yag.send(                                               #pragma: no cover
        to = to_email,
        subject = "Your Slackr Password Reset Code",
        contents = str(message)
    )
    
def user_id_generate():
    global my_uid
    my_uid += 1
    return my_uid

def handle_numbers_generator():
    global handle_str_ext
    handle_str_ext += 1
    return handle_str_ext

def user_handle_generate(name_first, name_last):
    global my_users
    handle_str = (name_first + name_last).lower()
    handle_str = handle_str[:20]
    for i in my_users:
        if i.get_handle_str() == handle_str:
            number = str(handle_numbers_generator())
            if (len(handle_str + number) > 20):
                handle_str = handle_str[:18]
            handle_str = handle_str + number
    return str(handle_str)
        
def token_generate(u_id):
    global SECRET
    payload = {
        'u_id' : u_id,  
        'time_stamp' : datetime.now().microsecond 
    }
    return jwt.encode(payload, SECRET, algorithm ='HS256').decode('utf-8')

def hash_value(value):
    return hashlib.sha256(value.encode()).hexdigest()

def request_code_generate():
    global my_request_codes                                 #pragma: no cover
    new_code = str(random.randint(100, 10000))              #pragma: no cover
    for i in my_request_codes:                              #pragma: no cover
        if i == hash_value(new_code):
            return request_code_generate()
    my_request_codes.append(hash_value(new_code))           #pragma: no cover
    return new_code                                         #pragma: no cover

def generate_users_all():
    global my_users
    all_users = []
    my_dictionary = {}

    for user in my_users:
        my_dictionary.update({
            "u_id" : user.get_uid(),
            "email" : user.get_email(),
            "name_first" : user.get_name_first(),
            "name_last" : user.get_name_last(),
            "handle_str" : user.get_handle_str(),
            "profile_img_url" : user.get_profile_img_url()
        })
        all_users.append(my_dictionary)
        my_dictionary = {}
    return all_users

def make_user_owner_in_all_channels(u_id):
    global my_users
    import server.channel_class

    channel_list = server.channel_class.get_channel_list()

    for channel in channel_list:
        if u_id in channel.get_mem_list():
            if u_id not in channel.get_owner_list():
                channel.get_owner_list().append(u_id)

    return True
## HELPER FUNCTIONS END ##
