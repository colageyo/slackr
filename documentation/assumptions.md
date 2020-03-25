# Assumptions
#### Team: T17A-fantastic_5 
Although we are provided with a skeleton of requirements, it is up to our group
to interpret the specifications to best of our abilities. We are aware that our
assumptions may differs from another team with the same specification.

Initially, the assumption is that we are making a program that is a text and
picture based messaging system and there is no voice chat.

We are initially assuming that all functions are working properly for the purpose
of testing and that we know what valid and invalid token, channel_id, u_id, message_id and 
react_id values are. 

### Auth:
- Users will have the ability to register if not an existing user.
- Once the email is registered after sign up, the user cannot sign up again using 
    the same email.
- Slackr is exclusive to UNSW users. In other words, users must have
    a relevant UNSW email to sign up and use Slackr. 

### Channel: 
- Created channels have no existing messages. 
- A user must be in a channel before being added as owners.
- There will always be at least one owner to a channel.
- `channel_listall`:
    - Returns all public and private channels that the user is in. This also includes
    the public channels the user is not a member of.
    - Private servers are hidden if the user is not a participant of the channel.

### Message: 
- `message_sendlater`: Messages will be stored in a waiting list.
- `mesage_remove`: Wiped completely from database or is it hidden from users (can be recovered).
- `message_send`: Assume user has already logged in with a valid token and the channel exist.
- `message_edit`: message_id is always valid.


### User: 
- `user_profiles_uploadphoto`: Users are only able to upload photos in a valid format i.e. .jpeg, .jpg, .png, .gif.
- Users can have the same handle and picture as another user. 
- A token given to the functions will always be valid.

### Standup: 
- The standup is triggered by a single user using some sort of typed up command.
- The `standup_start` function cannot be fully tested in iteration one for it's 
return value as we are unable to return the time when the the standup has 
concluded without implementing the function in some way.
- We are assuming that an invalid channel id is represented using less than 2 integers.
- All channel users can participate in the standup simultaneously.
- `standup_send` cannot be fully tested for the case when the standup time has concluded, as
      we felt like this cannot be tested without a server that would provide us with proper
      time stamps.

### Search: 
- In this iteration, we are assuming that the search function only looks at complete matches 
      and doesn't return partial matches.
- We are also assuming that the search works on both lowercase and upper case strings. 
      For example, searching for 'zebra' will yield the same results as searching for 'Zebra'.
- If the function doesn't find any matches, it returns an empty list.
- The function will raise a Value Error if the input consists of nothing.
- We are not testing for invalid tokens, as we assume that the user that calls for the
      search function within a chat, is already a valid user.
- We are assuming that a message that's marked as 'read' has been viewed by all members of the
      channel.
- We are assuming that inputting just spaces into the search function will raise a value error.

### Admin:
- We are assuming that an invalid user_id is represented with less than 2 integers and an invalid 
      permission_id is any integer other than 1, 2 and 3.
- We are assuming that the only difference between the owners and admins is that the owners
      are the original creators of any give channel.
    