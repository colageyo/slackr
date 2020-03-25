from server.user_class import User, get_user_from_token, user_valid_token
from server.channel_class import Channel, get_verified_channel_from_id, channel_valid_id, get_channel_list, channel_messages
from server.message_class import Message, get_global_message_id, set_global_message_id
from server.access_error import AccessError
from datetime import datetime, timedelta
from threading import Timer

list_of_messages = []
end_time = datetime.now()

def standup_start(token, channel_id, length):
    global end_time

    sender = get_user_from_token(token)
    sender_uid = sender.get_uid()
    try:
        curr_channel = get_verified_channel_from_id(channel_id,get_channel_list())
    except:
        raise ValueError ("Channel ID is not a valid channel")

    if sender_uid in curr_channel.get_mem_list():
        if not curr_channel.get_active_standup():
            
            curr_channel.set_active_standup(True)
            start_time = datetime.now()
            t = Timer(length, standup_output_message, [token, channel_id], {})
            t.start()
            
            end_time = start_time + timedelta(seconds=length)
            return {
                'time_finish': int(end_time.timestamp())
            }
        else:
            raise ValueError("Standup is already running.")
    else:
        raise AccessError("Authorised user is not a member of the channel.")

def standup_active(token, channel_id):
    global end_time

    if user_valid_token(token) is False:
        raise AccessError("Invalid User Token")

    if get_verified_channel_from_id(channel_id, get_channel_list()).get_active_standup():
        return {
            "is_active" : True,
            "time_finish" : int(end_time.timestamp())
        }
    else :
        return {
            "is_active" : False,
            "time_finish" : None
        }

def standup_send(token, channel_id, message):
    global list_of_messages
    global end_time

    curr_user = get_user_from_token(token)
    
    try:
        curr_channel = get_verified_channel_from_id(channel_id,get_channel_list())
    except:
        raise ValueError ("Channel ID is not a valid channel")
        
    if curr_user.get_uid() in curr_channel.get_mem_list():
        if (len(message) <= 1000):
            if curr_channel.get_active_standup():
                list_of_messages.append({"handle_str": curr_user.get_handle_str(), "message": message})
                return {} 
            else :
                raise ValueError("Standup is not active at the moment")
        else:
            raise ValueError("Message is more that 1000 characters")
    else:
        raise AccessError("The user is not a valid user")
    

def standup_output_message(token, channel_id):
    global list_of_messages

    get_verified_channel_from_id(channel_id, get_channel_list()).set_active_standup(False)
    u_id = get_user_from_token(token).get_uid()
    channel = get_verified_channel_from_id(channel_id, get_channel_list())

    output_string = ""
    
    for dictionary in list_of_messages:
        str1 = dictionary['handle_str']
        str2 = dictionary['message']
        adjusted_string = str1 + ": " + str2 + "\n"
        output_string += adjusted_string
        adjusted_string = ""

    list_of_messages.clear()
    message = Message(set_global_message_id(), u_id, output_string, datetime.now())
    output_string = None
    channel.get_mess().append(message)
