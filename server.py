"""Flask server"""
from json import dumps
### call user_class functions
from server.user_class import token_generate, auth_passwordreset_request, auth_passwordreset_reset
from server.user_class import User, auth_register, auth_login, auth_logout, user_profiles_uploadphoto
from server.user_class import user_profile, user_profile_sethandle, user_profile_setname,\
user_profile_setemail
from server.user_class import admin_userpermission_change, get_user_from_id, users_get_all
###

#Channel Class function
from server.channel_class import channel_invite, channel_details, channel_messages,\
channel_leave, channel_join, channel_addowner, channel_removeowner, channels_list,\
channels_listall, channels_create
##

##message_class function
from server.message import message_send_later, message_send, message_remove, message_edit,\
message_react, message_unreact, message_pin, message_unpin
##

##Standup Functions
from server.standup_functions import standup_start, standup_send, standup_active
##

##Search function
from server.search_function import search
##

from flask import Flask, request, jsonify, send_from_directory
from werkzeug.exceptions import HTTPException
from flask_cors import CORS
from server.access_error import AccessError
import sys

APP = Flask(__name__, static_url_path = '/static/')
CORS(APP)

def sendSuccess(data):
    return dumps(data)

def sendError(code, name, message):
    str1 = " "
    return dumps({
        'code' : code,
        'name': name,
        'message' : str1.join(message)
    }), code

#######################__AUTH_REG__#######################

@APP.route('/auth/register', methods=['POST'])
def user_register():
    """ Function that creates a new user"""

    email = request.form.get('email')
    password = request.form.get('password')
    name_first = request.form.get('name_first')
    name_last = request.form.get('name_last')

    try:
        returnDict = auth_register(email, password, name_first, name_last)
        return sendSuccess({
            'u_id': returnDict['u_id'],
            'token': returnDict['token']
        })
    except ValueError as e:
        return sendError(400, "ValueError", e.args)

@APP.route('/auth/login', methods=['POST'])
def user_login():
    """ Function that logs the user into the system """
    email = request.form.get('email')
    password = request.form.get('password')
    try:
        returnDict = auth_login(email, password)
        return sendSuccess({
            'u_id': returnDict['u_id'],
            'token': returnDict['token']
        })
    except ValueError as e:
        return sendError(400, "ValueError", e.args)

@APP.route('/auth/logout', methods=['POST'])
def user_logout():
    token = request.form.get('token')
    try:
        auth_logout(token)
        return sendSuccess({
            'is_success' : True
        })
    except ValueError:
        return sendSuccess({
            'is_success' : False
        })
    except AccessError:
        return sendSuccess({
            'is_success' : False
        })

@APP.route('/auth/passwordreset/request', methods=['POST'])
def user_password_reset_request():
    email = request.form.get('email')
    try:
        auth_passwordreset_request(email)
        return sendSuccess({

        })
    except ValueError:
        return sendError(400, "ValueError", e.args)

@APP.route('/auth/passwordreset/reset', methods=['POST'])
def user_password_reset():
    reset_code = request.form.get('reset_code')
    new_password = request.form.get('new_password')
    try:
        auth_passwordreset_reset(reset_code, new_password)
        return sendSuccess({

        })
    except ValueError as e:
        return sendError(400, "ValueError", e.args)


#####################__CHANNEL__#############################

@APP.route('/channel/invite', methods=['POST'])
def invite_user():
##This function will let user invite other users to a channel


    input_token = request.form.get("token")
    input_channel_id = request.form.get("channel_id")
    input_u_id = request.form.get("u_id")

    try:
        invite = channel_invite(input_token, input_channel_id, int(input_u_id))
        return sendSuccess({})

    except ValueError as e:
        return sendError(400, "ValueError", e.args)
    except AccessError as a:
        return sendError(401, "AccessError", a.args)

@APP.route('/channel/details', methods=['GET'])
def channel_info():
## This function return the information of a channel

    input_token = request.args.get("token")
    input_channel_id = request.args.get("channel_id")

    try:
        detail = channel_details(input_token, str(input_channel_id))
        return sendSuccess({
            'name' : detail['name'],
            'owner_members': detail['owner_members'],
            'all_members': detail['all_members']
        })
    except ValueError as e:
        return sendError(400, "ValueError", e.args)
    except AccessError as a:
        return sendError(401, "AccessError", a.args)

@APP.route('/channel/messages', methods=['GET'])
def message_of_channel():
## This function return 50 messages of a channel

    input_token = request.args.get("token")
    input_channel_id = request.args.get("channel_id")
    input_start = request.args.get("start")

    try:
        message = channel_messages(input_token, input_channel_id, int(input_start))
        return sendSuccess({
            'messages': message['messages'],
            'start': message['start'],
            'end': message['end']
        })
    except ValueError as e:
        return sendError(400, "ValueError", e.args)
    except AccessError as a:
        return sendError(401, "AccessError", a.args)

@APP.route('/channel/leave', methods=['POST'])
def leave_channel():
## This function let user leave a channe

    token = request.form.get('token')
    channel_id = request.form.get('channel_id')

    try:
        leave = channel_leave(token, channel_id)
        return sendSuccess({})
    except ValueError as e:
        return sendError(400, "ValueError", e.args)


@APP.route('/channel/join', methods=['POST'])
def join_channel():
## This function let user join a channel

    token = request.form.get('token')
    channel_id = request.form.get('channel_id')

    try:
        join = channel_join(token, channel_id)
        return sendSuccess({})
    except ValueError as e:
        return sendError(400, "ValueError", e.args)
    except AccessError as a:
        return sendError(401, "AccessError", a.args)

@APP.route('/channel/addowner', methods=['POST'])
def add_owner():
## this function let owner or dev to add new owner to a channel

    token = request.form.get('token')
    channel_id = request.form.get('channel_id')
    u_id = request.form.get('u_id')

    try:
        add = channel_addowner(token, channel_id, int(u_id))
        return sendSuccess({})
    except ValueError as e:
        return sendError(400, "ValueError", e.args)
    except AccessError as a:
        return sendError(401, "AccessError", a.args)

@APP.route('/channel/removeowner', methods=['POST'])
def re_owner():
## this function remove an owner

    token = request.form.get('token')
    channel_id = request.form.get('channel_id')
    u_id = request.form.get('u_id')

    try:
        remove = channel_removeowner(token, channel_id, int(u_id))
        return sendSuccess({})
    except ValueError as e:
        return sendError(400, "ValueError", e.args)
    except AccessError as a:
        return sendError(401, "AccessError", a.args)

@APP.route('/channels/list', methods=['GET'])
def list_channel():
##this function return a listo channel that the user is part of

    token = request.args.get('token')

    try:
        list_chan = channels_list(token)
        return sendSuccess({
            'channels' : list_chan
        })
    except ValueError as e:
        return sendError(400, "ValueError", e.args)

@APP.route('/channels/listall', methods=['GET'])
def listall_channel():
##this function return a listo channel that the user is part off and public channel

    token = request.args.get('token')

    try:
        listall = channels_listall(token)
        return sendSuccess({
            'channels' : listall
        })
    except ValueError as e:
        return sendError(400, "ValueError", e.args)

@APP.route('/channels/create', methods=['POST'])
def create_channel():
## this function create a channel

    token = request.form.get('token')
    name = request.form.get('name')
    is_public = request.form.get('is_public')

    try:
        channel = channels_create(token, name, is_public)
        return sendSuccess({
            'channel_id' : channel['channel_id']
        })
    except ValueError as e:
        return sendError(400, "ValueError", e.args)


#####################__USER__#############################

@APP.route('/user/profile', methods=['GET'])
def user_profile_show():
    token = request.args.get('token')
    u_id = request.args.get('u_id')
    try:
        returnDict = user_profile(token, int(u_id))
        if returnDict is not None:
            return sendSuccess({
                'u_id' : returnDict['u_id'],
                'email' : returnDict['email'],
                'name_first' : returnDict['name_first'],
                'name_last' : returnDict['name_last'],
                'handle_str' : returnDict['handle_str'],
                'profile_img_url' : returnDict['profile_img_url']
            })
    except ValueError as e:
        return sendError(400, "ValueError", e.args)
    except AccessError as a:
        return sendError(401, "AccessError", a.args)

@APP.route('/user/profile/setname', methods=['PUT'])
def user_profile_changename():
    token = request.form.get('token')
    name_first = request.form.get('name_first')
    name_last = request.form.get('name_last')
    try:
        user_profile_setname(token, name_first, name_last)
        return sendSuccess({

        })
    except ValueError as e:
        return sendError(400, "ValueError", e.args)
    except AccessError as a:
        return sendError(401, "AccessError", a.args)

@APP.route('/user/profile/setemail', methods=['PUT'])
def user_profile_changeemail():
    token = request.form.get('token')
    email = request.form.get('email')
    try:
        user_profile_setemail(token, email)
        return sendSuccess({

        })
    except ValueError as e:
        return sendError(400, "ValueError", e.args)
    except AccessError as a:
        return sendError(401, "AccessError", a.args)

@APP.route('/user/profile/sethandle', methods=['PUT'])
def user_profile_changehandle():
    token = request.form.get('token')
    handle_str = request.form.get('handle_str')
    try:
        user_profile_sethandle(token, handle_str)
        return sendSuccess({

        })
    except ValueError as e:
        return sendError(400, "ValueError", e.args)
    except AccessError as a:
        return sendError(401, "AccessError", a.args)


@APP.route('/user/profiles/uploadphoto', methods=['POST'])
def user_profile_changephoto():
    token = request.form.get('token')
    img_url = request.form.get('img_url')
    x_start = request.form.get('x_start')
    y_start = request.form.get('y_start')
    x_end = request.form.get('x_end')
    y_end = request.form.get('y_end')

    try:
        localhost = str(request.host_url)     
        user_profiles_uploadphoto(token, img_url, int(x_start), int(y_start), int(x_end), int(y_end),localhost)
        return sendSuccess({})
    except ValueError as e:
        return sendError(400, "ValueError", e.args)

@APP.route('/static/<path:path>')
def send_js(path):
    return send_from_directory('',path)



@APP.route('/users/all', methods = ['GET'])
def user_show_all():
    token = request.args.get('token')
    try:
        returnList = users_get_all(token)
        return sendSuccess({
            "users": returnList
        })
    except AccessError as a:
        return sendError(401, "AccessError", a.args)

@APP.route('/admin/userpermission/change', methods=['POST'])
def user_permission_change():
    token = request.form.get('token')
    u_id = request.form.get('u_id')
    permission_id = request.form.get('permission_id')
    try:
        admin_userpermission_change(token, int(u_id), int(permission_id))
        return sendSuccess({

        })
    except ValueError as e:
       return sendError(400, "ValueError", e.args)
    except AccessError as a:
        return sendError(401, "AccessError", a.args)

#######################__MESSAGE__######################
@APP.route('/message/sendlater', methods=['POST'])
def message_later_send():

    token = request.form.get('token')
    channel_id = request.form.get('channel_id')
    message = request.form.get('message')
    time_sent = request.form.get('time_sent')

    try:
        sending = message_send_later(token, channel_id, message, time_sent)
        return sendSuccess({
            'message_id' : sending['message_id']
        })
    except ValueError as e:
        return sendError(400, "ValueError", e.args)
    except AccessError as a:
        return sendError(401, "AccessError", a.args)

@APP.route('/message/send', methods=['POST'])
def send_message():

    token = request.form.get('token')
    channel_id = request.form.get('channel_id')
    message = request.form.get('message')

    try:
        sending = message_send(token, channel_id, message)
        return sendSuccess({
            'message_id' : sending['message_id']
        })
    except ValueError as e:
        return sendError(400, "ValueError", e.args)
    except AccessError as e:
        return sendError(401, "AccessError", a.args)

@APP.route('/message/remove', methods=['DELETE'])
def remove_message():

    token = request.form.get('token')
    message_id = request.form.get('message_id')

    try:
        remove = message_remove(token, int(message_id))
        return sendSuccess({})

    except ValueError as e:
        return sendError(400, "ValueError", e.args)
    except AccessError as a:
        return sendError(401, "AccessError", a.args)

@APP.route('/message/edit', methods=['PUT'])
def edit_message():

    token = request.form.get('token')
    message_id = request.form.get('message_id')
    message = request.form.get('message')

    try:
        edit = message_edit(token, int(message_id), message)
        return sendSuccess({})
    except ValueError as e:
        return sendError(400, "ValueError", e.args)
    except AccessError as a:
        return sendError(401, "AccessError", a.args)

@APP.route('/message/react', methods=['POST'])
def react_message():
    token = request.form.get('token')
    message_id = request.form.get('message_id')
    react_id = request.form.get('react_id')

    try:
        react = message_react(token, int(message_id), int(react_id))
        return sendSuccess({})
    except ValueError as e:
        return sendError(400, "ValueError", e.args)
    except AccessError as a:
        return sendError(401, "AccessError", a.args)

@APP.route('/message/unreact', methods=['POST'])
def unreact_message():
    token = request.form.get('token')
    message_id = request.form.get('message_id')
    react_id = request.form.get('react_id')

    try:
        unreact = message_unreact(token, int(message_id), int(react_id))
        return sendSuccess({})
    except ValueError as e:
        return sendError(400, "ValueError", e.args)
    except AccessError as a:
        return sendError(401, "AccessError", a.args)


@APP.route('/message/pin', methods=['POST'])
def pin_message():
    token = request.form.get('token')
    message_id = request.form.get('message_id')

    try:
        pin = message_pin(token, int(message_id))
        return sendSuccess({})
    except ValueError as e:
        return sendError(400, "ValueError", e.args)
    except AccessError as a:
        return sendError(401, "AccessError", a.args)


@APP.route('/message/unpin', methods=['POST'])
def unpin_message():
    token = request.form.get('token')
    message_id = request.form.get('message_id')

    try:
        unpin = message_unpin(token, int(message_id))
        return sendSuccess({})
    except ValueError as e:
        return sendError(400, "ValueError", e.args)
    except AccessError as a:
        return sendError(401, "AccessError", a.args)

#######################__STANDUP__######################
@APP.route('/standup/start', methods=['POST'])
def standup_start_standup():
    token = request.form.get('token')
    channel_id = request.form.get('channel_id')
    length = request.form.get('length')

    try:
        end_time = standup_start(token, channel_id, int(length))
        return sendSuccess({
            'time_finish': end_time['time_finish']
        })
    except ValueError as e:
        return sendError(400, "ValueError", e.args)
    except AccessError as a:
        return sendError(401, "AccessError", a.args)

@APP.route('/standup/active', methods = ["GET"])
def standup_act():
    token = request.args.get('token')
    channel_id = request.args.get('channel_id')
    try:
        returnDictionary = standup_active(token, channel_id)
        return sendSuccess({
            "is_active" : returnDictionary["is_active"],
            "time_finish" : returnDictionary["time_finish"]
        })
    except ValueError as e:
        return sendError(400, "ValueError", e.args)
    except AccessError as a:
        return sendError(401, "AccessError", a.args)


@APP.route('/standup/send', methods=['POST'])
def standup_send_standup():
    token = request.form.get('token')
    channel_id = request.form.get('channel_id')
    message = request.form.get('message')

    try:
        standup_send(token, channel_id, message)
        return sendSuccess({})
    except ValueError as e:
        return sendError(400, "ValueError", e.args)
    except AccessError as a:
        return sendError(401, "AccessError", a.args)

#######################__SEARCH__######################
@APP.route('/search', methods=['GET'])
def search_search():
    token = request.args.get('token')
    query_str = request.args.get('query_str')

    try:
        searchResult = search(token, query_str)

        return sendSuccess({'messages': searchResult['messages']})
    except ValueError as e:
        return sendError(400, "ValueError", e.args)
    except AccessError as a:
        return sendError(401, "AccessError", a.args)


if __name__ == '__main__':
    APP.run(port=(sys.argv[1] if len(sys.argv) > 1 else 5000), debug=True)
