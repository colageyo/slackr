###### General Refactoring

1. Moved all files into server folder and fixed the importing 

2. Fixed any circular importing issues 

3. Got rid of "import *" from all files 

###### Refractoring of channel_class.py

1. Used Top Down Thinking principle to group the getting user from token and the 
authenticating if user exists in one helper function `get_verified_user_from_token`. 
    - Avoided repeating a complex process for every main functions (DRY). 
    Reduced the complexity of the main functions overall by reducing the use of 
    if/else (use for authentication) hence KISS (state that more complex = more bug).
    - `get_verified_user_from_token` is reuseable and very useful for other non 
    channel function. 
    - Design smell:rigidity, viscosity, immobility

2. Used Top Down Thinking principle for the process of getting channel from it 
id and validating if its a existed channel using `get_verified_channel_from_id`.
    - Avoided repeating a complex process for every main functions (DRY). 
    - Reduced the complexity of the main functions overall by reducing the use of 
    if/else (use for authentication) and hence KISS (which states that more complex a system
implies potential for more bugs) 
    - `get_verified_channel_from_id` is reuseable and useful for other non 
    channel function. 
    - Design smell: rigidity, viscosity, immobility

3. Broke down and rewrote `channel_invite` to reduce the repetition of authenticating
user and channel for a second time in this function.
    - used KISS to reduce the amount of if/else statement and therefore reduce potential bugs. 
    - Design smell: needless complexity

4. Used KISS principle to reduce the amount of if/else statement in 
`channels_list` and `channels_listall`. 
    - Design smell: needless complexity

5. Created `append_channel_id_name(list_of_chan, name, chan_id)` to use 
in `generate_list` and `generate_listall` channels to avoid the repetition of 
a complex appending function. 
    - DRY and Top Down Thinking. 
    - Design smell: viscosity, ridigity, immobility, opacity

6. Created a function `get_all_channel_name_id` to get all created channel(id,name) 
of the app to use in `listall_channel`. We only used it once 
but this helper function has the potential to be used for other purposes. Hence,
 it is a separate function. 
    - Design smell: immobility

7. Broke down and rewrote `channels_create` to reduce the complexity by reducing 
the amount of use of if/else statement. 
    - KISS. 
    - Design smell: needless complexity

8. Rewrote the function `channel_messages` using the Top-down thinking principle.
    - The function was broken down into 3 different parts:
        - what is called by the frontend
        - generating the messages list
        - generating the reacts list
This has made the function considerably more readable and easier to adjust. 
Hence, the function also adhering to the KISS principle.

###### Refactoring of user_class.py

1. Created a decorator function such as `authorise_token(token)`, to reduce the 
repetition of code in terms of raising an AccessError if the token is not valid. 
Hence, adhering to the DRY software engineering principle.

2. Changed the `user_valid_password` function so now the length of the password 
is adjustable, making the function more reusable.

3. Changed the `user_valid_name` function so now the max_length of name is 
adjustable, making the function more reusable.

4. Created additional helper function (`generate_users_all` and 
`make_user_owner_in_all_channels`) to make the functions `admin_permissions_change()` 
and `users_get_all` more readable, maintainable and extensible.

###### Refactoring of message.py

1. Implemented a general `append_message` function to handle `message_send` and `message_sendlater` (DRY principle)

2. Created a decorator function such as `correct_message_length` to reduce amount of code repetition in order to raise the ValueError message.

3. Created a decorator function such as `message_exist` to eliminate repetition of code raising error messages.