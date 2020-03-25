from server.channel_class import channels_list, get_channel_list, \
    get_verified_channel_from_id, generate_reacts_dictionary
from server.user_class import get_user_from_token


def search(token, quer_str):
    user = get_user_from_token(token)
    search_result = []
    search_list = []
    channels_dict = channels_list(token)
    for channel in channels_dict:
        search_list.append(channel['channel_id'])

    for channel_id in search_list:
        channel = get_verified_channel_from_id(channel_id, get_channel_list())
        for message in channel.get_mess():
            if quer_str in message.get_message_content():
                message_dict = {
                    'message_id': message.get_message_id(),
                    'u_id': message.get_user_id(),
                    'message': message.get_message_content(),
                    'time_created': int(
                        message.get_time_created().timestamp()),
                    'reacts': [],
                    'is_pinned': message.get_is_pinned()}
                message_dict['reacts'] = generate_reacts_dictionary(
                    user, message)
                search_result.append(message_dict)

    return {'messages': search_result}
