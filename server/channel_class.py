from server.user_class import get_user_from_token, get_user_from_id, User
from server.access_error import AccessError
import uuid
from server.message_class import Message
from datetime import datetime
from server.react_class import React


class Channel:

    def __init__(self, name, channel_id, owner_list, member_list, is_public, message):
        self.name = name
        self.channel_id = channel_id
        self.owner_list = owner_list
        self.member_list = member_list
        self.is_public = is_public
        self.message = message
        self.active_standup = False

    def get_channel_name(self):
        return self.name

    def get_channel_id(self):
        return self.channel_id

    def get_owner_list(self):
        return self.owner_list

    def get_mem_list(self):
        return self.member_list

    def get_is_pub(self):
        return self.is_public

    def get_mess(self):
        return self.message

    def get_active_standup(self):
        return self.active_standup

    def set_active_standup(self, active_standup):
        self.active_standup = active_standup


##Variables
channel_list = []


##

## Main functions
def channel_invite(token, channel_id, u_id):
    global channel_list

    host_user = get_verified_user_from_token(token)
    recipient_user = get_user_from_id(u_id)

    inv_channel = get_verified_channel_from_id(channel_id, channel_list)

    if host_user.get_uid() not in inv_channel.get_mem_list():
        raise AccessError("The host is not in the channel.")

    if recipient_user is None:
        raise ValueError("Invalid Guest.")

    if recipient_user.get_uid() in inv_channel.get_mem_list():
        raise ValueError("The user is already in channel.")

    inv_channel.get_mem_list().append(u_id)

    return {}


def channel_details(token, channel_id):
    global channel_list

    target_channel = get_verified_channel_from_id(channel_id, channel_list)
    user_id = get_verified_user_from_token(token).get_uid()

    if user_id not in target_channel.get_mem_list():
        raise AccessError("The user is not in the channel.")

    list_of_member = generate_list_of_members(target_channel)
    list_of_owner = generate_list_of_owners(target_channel)

    return {'name': target_channel.get_channel_name(),
            'owner_members': list_of_owner,
            'all_members': list_of_member}


def channel_messages(token, channel_id, start):
    
    global channel_list

    channel = get_verified_channel_from_id(channel_id, channel_list)
    u_id = get_verified_user_from_token(token).get_uid()
    user = get_verified_user_from_token(token)
    first_message = len(channel.get_mess()) - start

    if u_id in channel.get_mem_list():
        if start <= len(channel.get_mess()):
            if (len(channel.get_mess()) - start) - 50 >= 0:
                end = start + 50
                last_message = first_message - 50 
            else :
                end = -1
                last_message = 0
            messages = generate_indexed_messages(user, channel, first_message, last_message)
            return {
                "messages": messages,
                "start": start,
                "end": end
            }
        else :
            raise ValueError("The start is greater than cumulative messages")
    else :
        raise AccessError("The user is not in the channel")


def channel_leave(token, channel_id):
    global channel_list
    
    target_channel = get_verified_channel_from_id(channel_id, channel_list)
    mem_id = get_verified_user_from_token(token).get_uid()

    if mem_id in target_channel.get_mem_list():
        (target_channel.get_mem_list()).remove(mem_id)
        if mem_id in target_channel.get_owner_list():
            (target_channel.get_owner_list()).remove(mem_id)
        if len(target_channel.get_owner_list()) == 0:
            channel_list.remove(target_channel)

    else:
        raise ValueError("The user is not in the channel.")

    return {}


def channel_join(token, channel_id):
    target_channel = get_verified_channel_from_id(channel_id, channel_list)

    user = get_verified_user_from_token(token)
    user_id = user.get_uid()

    if user_id in target_channel.get_mem_list():
        raise ValueError("User is already in the channel.")

    if user.get_permission_id() == 1 or user.get_permission_id() == 2:
        target_channel.get_mem_list().append(user_id)
        target_channel.get_owner_list().append(user_id)

    elif user.get_permission_id() == 3 and target_channel.get_is_pub() == True:
        target_channel.get_mem_list().append(user_id)

    else:
        raise AccessError("The Channel is Private.")

    return {}


def channel_addowner(token, channel_id, u_id):
    target_channel = get_verified_channel_from_id(channel_id, channel_list)

    if u_id in target_channel.get_owner_list():
        raise ValueError("This user is already an owner.")

    host_user = get_verified_user_from_token(token)
    host_id = host_user.get_uid()

    if host_id in target_channel.get_owner_list() or \
            (host_user.get_permission_id() == 2 or host_user.get_permission_id() == 1):

        (target_channel.get_owner_list()).append(u_id)

    else:
        raise AccessError("Host User is not authorised.")

    return {}


def channel_removeowner(token, channel_id, u_id):
    target_channel = get_verified_channel_from_id(channel_id, channel_list)

    if u_id not in target_channel.get_owner_list():
        raise ValueError("This user is not an owner of channel.")

    host_user = get_verified_user_from_token(token)

    host_id = host_user.get_uid()

    if host_id in target_channel.get_owner_list() or \
            (host_user.get_permission_id() == 2 or host_user.get_permission_id() == 1):

        target_channel.get_owner_list().remove(u_id)

    else:
        raise AccessError("Host User is not authorised.")

    return {}


def channels_list(token):
    global channel_list

    user = get_verified_user_from_token(token)
    user_id = user.get_uid()

    return_list = []
    for channel in channel_list:
        if user_id in channel.get_mem_list():
            return_list.append({
                'channel_id' : channel.get_channel_id(),
                'name': channel.get_channel_name()
            })
    return return_list


def channels_listall(token):
    global channel_list
    user = get_verified_user_from_token(token)
    user_id = user.get_uid()

    if user.get_permission_id() == 1 or user.get_permission_id() == 2:
        return get_all_channel_name_id(channel_list)
    else:
        return_list = []
        for channel in channel_list:
            if channel.get_is_pub() or (user_id in channel.get_mem_list()):
                return_list.append({
                    'channel_id' : channel.get_channel_id(),
                    'name': channel.get_channel_name()
                    })
        return return_list


def get_all_channel_name_id(channel_list):
    list_return = []
    for channel in channel_list:
        list_return.append({"channel_id": channel.get_channel_id(),\
                        'name': channel.get_channel_name(),
                           })
    return list_return

def channels_create(token, name, is_public):
    global channel_list

    chan_pub = False
    if is_public == "true":
        chan_pub = True

    user = get_verified_user_from_token(token)
    user_id = user.get_uid()
    if len(name) <= 20:
        channel_id = channel_id_generate()
        channel_list.append(Channel(name, channel_id, [user_id], [user_id], chan_pub, []))
        return {"channel_id": channel_id}
    else:
        raise ValueError("Name should have less than 20 characters.")


'''     HELPER FUNCTIONS START    '''

## CHECKER FUNCTIONS START ##

def channel_valid_id(channel_id):
    global channel_list
    for channel in channel_list:
        if channel_id == channel.get_channel_id():
            return True

    return False

def is_user_reacted(u_id, react):
    reacted_user_list = react.get_uids()
    return u_id in reacted_user_list

## CHECKER FUNCTION END ##


## GETTER FUNCTIONS START ##

def get_verified_channel_from_id(channel_id, channel_list):
    for channel in channel_list:
        if channel_id == channel.get_channel_id():
            return channel

    raise ValueError("This channel does not exists.")

def get_verified_user_from_token(token):
    user = get_user_from_token(token)
    if user == None:                                        #pragma: no cover
        raise ValueError("The user does not exists.")
    return user

## GETTER FUNCTION END ##


## HELPER FUNCTIONS START ##

def channel_id_generate():
    channel_id = uuid.uuid1()
    return str(channel_id)

def generate_list_of_members(input_channel):
    list_of_members = []

    for member_id in input_channel.get_mem_list():
        member = get_user_from_id(member_id)
        list_of_members.append({
            "u_id": member.get_uid(),
            "name_first": member.get_name_first(),
            "name_last": member.get_name_last(),
            "profile_img_url" : member.get_profile_img_url()
        })

    return list_of_members


def generate_list_of_owners(input_channel):
    list_of_owners = []
    for owner_id in input_channel.get_owner_list():
        owner = get_user_from_id(owner_id)
        list_of_owners.append({
            "u_id": owner.get_uid(), 
            "name_first": owner.get_name_first(),
            "name_last": owner.get_name_last(),
            "profile_img_url" : owner.get_profile_img_url()
        })

    return list_of_owners

def generate_indexed_messages(user, channel, first_message, last_message):

    messages = []
    output_message = {}

     
    for i in range(last_message, first_message):
        message = channel.get_mess()[i]
        reacts = generate_reacts_dictionary(user, message)
        output_message.update({
            'message_id': message.get_message_id(),
            'u_id': message.get_user_id(),
            'message': message.get_message_content(),
            'time_created': int(message.get_time_created().timestamp()),
            'reacts': reacts,
            'is_pinned': message.get_is_pinned()
        })
        messages.insert(0, output_message)
        output_message = {}
    return messages

def generate_reacts_dictionary(user, message):
    
    output_list = []
    output_dictionary = {}
    message_reacts = message.get_reacts()
    for react in message_reacts:
        if is_user_reacted(user.get_uid(), react):
            reaction = True
        else :
            reaction = False 
        output_dictionary.update({
            "react_id" : react.get_react_id(),
            "u_ids" : react.get_uids(),
            "is_this_user_reacted" : reaction
        })
        output_list.append(output_dictionary)
        output_dictionary = {}
    return output_list

## HELPER FUNCTIONS END ##

'''      HELPER FUNCTION END      '''


def reset_channel_list():
    global channel_list
    channel_list.clear()
    return channel_list

def get_channel_list():
    global channel_list
    return channel_list
