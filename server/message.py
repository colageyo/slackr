""" Message Functions """
from server.message_class import Message, get_global_message_id, set_global_message_id
from server.channel_class import Channel, channel_valid_id, get_verified_channel_from_id, get_channel_list
from server.user_class import get_user_from_token, user_valid_token
from server.standup_functions import standup_start, standup_active, standup_send
from datetime import datetime, timedelta
from threading import Timer
from server.access_error import AccessError
from server.react_class import React, valid_react


"""    Decorators   """
def valid_react_id(function):
    def wrapper(*args, **kwargs):
        react_id = list(args)[2]
        if react_id not in valid_react:
            raise ValueError("Invalid react_id")
        return function(*args, **kwargs)
    return wrapper


def message_exist(function):
    def wrapper(*args, **kwargs):
        channels = get_channel_list()
        message_id = list(args)[1]
        flag = False
        for channel in channels:
            channel_messages = channel.get_mess()
            for message in channel_messages:
                if message_id == message.get_message_id():
                    flag = True
        if flag is False:
            raise ValueError("Message no long exist")
        return function(*args, **kwargs)
    return wrapper


def correct_message_length(function):
    def wrapper(*args, **kwargs):
        message = list(args)[2]
        if len(message) > 1000:
            raise ValueError("Message is more than 1000 characters")
        return function(*args, **kwargs)
    return wrapper


"""    Main message functions     """
@correct_message_length
def message_send_later(token, channel_id, message, time_sent):

    timestamp = float(time_sent)
    time = datetime.fromtimestamp(timestamp)

    if not channel_valid_id(channel_id): 
        raise ValueError("Channel does not exist")

    if not valid_time(time_sent):
        raise ValueError("Time sent is in the past")

    if not authorized_user(token, channel_id):
        raise AccessError("User has not joined the channel")

    time_dif = (time - datetime.now()).total_seconds()
    t = Timer(time_dif, append_message, args=[channel_id, token, set_global_message_id(), message, time])
    t.start()
    return {"message_id": get_global_message_id()}


@correct_message_length
def message_send(token, channel_id, message):

    if not authorized_user(token, channel_id):
        raise AccessError("User has not joined the channel")
       
    time_created = datetime.now()

    return append_message(channel_id, token, set_global_message_id(), message, time_created)


def append_message(channel_id, token, message_id, message, time_created):
    channel_messages = get_channel_messages(channel_id)
    user_id = get_user_from_token(token).get_uid()
    new_message = Message(message_id, user_id, message, time_created)
    channel_messages.append(new_message)

    return {"message_id": message_id} 


@message_exist
def message_remove(token, message_id):

    user_id = get_user_from_token(token).get_uid()
        
    message = get_message_from_m_id(message_id)
    channel = get_verified_channel_from_id(get_channel_from_message(message_id), get_channel_list())
    
    if not channel_owner(user_id, channel):
        if not message_poster(user_id, message):
            raise AccessError("Not authorized user of message")

    channel.get_mess().remove(message)
    return {}


def message_edit(token, message_id, message_str):
    
    if not user_valid_token(token):
        raise AccessError("User is not a valid user")
        
    user_id = get_user_from_token(token).get_uid()
    message = get_message_from_m_id(message_id)
    channel = get_verified_channel_from_id(get_channel_from_message(message_id), get_channel_list())
    
    if not channel_owner(user_id, channel):
        if not message_poster(user_id, message):
            raise AccessError("Not authorized user of message")

    message.change_content(message_str)
    return {}


@valid_react_id
def message_react(token, message_id, react_id):

    user_id = get_user_from_token(token).get_uid()

    if not valid_message_in_channel(user_id, message_id):
        raise ValueError("Invalid message_id with in the user joined channel")

    message = get_message_from_m_id(message_id)

    if already_reacted(user_id, message, react_id):
        raise ValueError("Already contains an active react")

    react = get_react_from_id(message, react_id)
    react.user_react(user_id)

    return {}


@valid_react_id
def message_unreact(token, message_id, react_id):

    user_id = get_user_from_token(token).get_uid()

    if not valid_message_in_channel(user_id, message_id):
        raise ValueError("Invalid message_id with in the user joined channel")

    message = get_message_from_m_id(message_id)

    if not already_reacted(user_id, message, react_id):
        raise ValueError("Does not contain an active react")

    if not user_valid_token(token):
        raise AccessError("User is not a valid user")

    react = get_react_from_id(message, react_id)
    react.user_unreact(user_id)

    return {}


@message_exist
def message_pin(token, message_id):
    user_id = get_user_from_token(token).get_uid()
    
    message = get_message_from_m_id(message_id)
    channel = get_verified_channel_from_id(get_channel_from_message(message_id), get_channel_list())
    
    if not authorized_user(token, channel.get_channel_id()):
        raise AccessError("User is not a member of the channel")
    
    if not user_valid_token(token):
        raise AccessError("User is not a valid user")
    
    if not channel_owner(user_id, channel):
        raise ValueError("The user is not an admin")
    
    if message.pinned():
        raise ValueError("Message is already pinned")
    
    message.pin_message()
    return {}


@message_exist
def message_unpin(token, message_id):
    user_id = get_user_from_token(token).get_uid()
    
    message = get_message_from_m_id(message_id)
    channel = get_verified_channel_from_id(get_channel_from_message(message_id), get_channel_list())
    
    if not authorized_user(token, channel.get_channel_id()):
        raise AccessError("User is not a member of the channel")
    
    if not user_valid_token(token):
        raise AccessError("User is not a valid user")
    
    if not channel_owner(user_id, channel):
        raise ValueError("The user is not an admin")
    
    if not message.pinned():
        raise ValueError("Message is already unpinned")
    
    message.unpin_message()
    return {}

## CHECKER FUNCTIONS START ##

def valid_time(time_sent):
    now = datetime.now()
    time_sent_stamp = datetime.fromtimestamp(float(time_sent))
    time_dif = (now - time_sent_stamp).total_seconds()
    return time_dif < 0


def authorized_user(token, channel_id):
    user_id = get_user_from_token(token)
    channel = get_verified_channel_from_id(channel_id,get_channel_list())
    channel_members = channel.get_mem_list()
    for member in channel_members:
        if user_id.get_uid() == member:
            return True
    return False

def channel_owner(user_id, channel):
    owner_list = channel.get_owner_list()
    for user in owner_list:
        if user_id == user:
            return True
    return False



def valid_message_in_channel(user_id, message_id):
    channel_id = get_channel_from_message(message_id)

    if channel_id is None:
        return False

    channel = get_verified_channel_from_id(channel_id, get_channel_list())
    member_list = channel.get_mem_list()

    for member in member_list:
        if user_id == member:
            return True
    return False


def already_reacted(user_id, message, react_id):
    react = get_react_from_id(message, react_id)
    user_list = react.get_uids()
    if user_id in user_list:
        return True
    else:
        return False

## CHECKER FUNCTIONS END ##

## GETTER FUNCTIONS START ##

def get_channel_messages(channel_id):
    channel = get_verified_channel_from_id(channel_id,get_channel_list())
    return channel.get_mess()

def message_poster(user_id, message):
    u_id = message.get_user_id()
    return user_id == u_id

def get_channel_from_message(message_id):
    channels = get_channel_list()
    flag = False
    for channel in channels:
        messages = channel.get_mess()
        
        for message in messages:
            if message_id == message.get_message_id():
                flag = True
                return channel.get_channel_id()
    return None

def get_message_from_m_id(message_id):

    channel_id = get_channel_from_message(message_id)
    channel_messages = get_channel_messages(channel_id)

    for message in channel_messages:
        if message_id == message.get_message_id():
            return message

def get_react_from_id(message, react_id):
    react_list = message.get_reacts()
    for react in react_list:
        if react_id == react.get_react_id():
            return react

## GETTER FUNCTIONS END ##

