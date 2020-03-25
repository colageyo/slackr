For the following iteration, we have guaranteed the integrity of our functions by the method of rigorous testing.  
Through the running of pytest coverage, we were able to make sure that our tests check every possible outcome for each 
function created. Additionally, every single member of our team had a turn at testing each other's functions to omit any
errors or inconsistencies that weren't obvious to the person writing the function. We used pytest in combination with 
ARC (Advanced Rest Client) and the frontend provided to make sure that each function does what is required of it. 
We have also provided the Acceptance Criteria for each function below. Writing the Acceptance Criteria, helped us 
figure out any misunderstandings in the comprehension of the specs provided. Once we detected any inconsistencies, we
were able to fix them as a team to make sure that the function in question aligns with our purpose. 

### Assurance
The following are our acceptance criteria for iteration 2: 

1 - As a student, I want to be able to log in, so that I can access Slackr
    
    > A 'Login' header is placed at the top of the page
    > The email and password fields are placed in the mid-top section of the main page, right underneath the header
    > The user is logged in once they press 'SIGN IN'
    > The email field contains a placeholder with a grey-coloured text: "Email*"
    > The password field contains a placeholder with a grey-coloured text: "Password*"
    > Either of the placeholders disappear above the respective field once the user starts typing
    > User can only login using valid credentials
    > If the user enters invalid credentials, an error message appears at the top displaying 'An error occurred. Try again later'
    > A user can only login once per session
    
2 - As a student, I want to be able to register with my email, so that I can have a dedicated account with Slackr and don’t have to sign up again.

    > The 'Don't have an account? Register' button is placed on the main page, right underneath the password field
    > Once clicked, it redirects the user to the Register page
    > A 'Register' header is placed at the top of the page
    > The first name, last name, email and password fields are places in the mid-top section, right underneath the header
    > The user is considered as signed up once they press the 'SIGN UP' button
    > The first name field contains a placeholder with a grey-coloured text : "First name*"
    > The last name field contains a placeholder with a grey-coloured text : "Last name*"
    > The email field contains a placeholder with a grey-coloured text : "Email*"
    > The password field contains a placeholder with a grey-coloured text : "First name*"
    > Either of the placeholders disappear above the respective field once the user starts typing
    > A 'Already have an account? Login' button is placed right below the 'SIGN UP' button, to help redirect user to the login page
    > An error message appears if the email is of invalid format
    > An error message appears if the email is already registered
    > An error message appears if the password is less than 6 characters long
    > An error message appears if the first or last names are not between 1 and 50 characters long
    
3 - As a student, I want to be able to reset my password if forgotten, so that I’m able to access my account again.

    > A 'Forgot password?' button is placed right below the register button on the main page.
    > The user is redirected to the 'Forgot Password' page, once they press on 'Forgot password?'.
    > The 'Forgot Password' header is placed at the top of the page.
    > The email field is placed right below the header.
    > The email field contains a placeholder with a grey-coloured text : "Email*".
    > The placeholder disappears above the the field once the user starts typing .
    > A recovery email is sent to the user once the 'SEND RECOVERY EMAIL' button is pressed.
    > A 'Remember your password? Login' button is placed right below the 'SEND RECOVERY EMAIL' button, to help redirect user to the login page.
    > The user is redirected to the 'Password Reset' page, once the 'SEND RECOVERY EMAIL' button is pressed .
    > The recovery code field is located in the middle of the password reset window. 
    > The user's password is reset once they press the 'Reset Password' button.
    > An error is thrown if the password is less than 7 characters long.
    > An error is thrown if the user is not a registered user by email.
    > An error is thrown if the email is of invalid format.
    > An error is thrown if the reset code is not a valid code. 
    
4 - As a student, I want to be able to log out, so that others can’t access my Slackr account without my credentials or carry on with my current session.

    > The 'Logout' button is placed at the top right corner on the user's screen.
    > Once the user presses the 'Logout' button, they are logged out of their session.
    > A user can only log out once per session.

5 - As a student, I want to be able to see a list of all my channels, so that I can quickly open my conversations.

6 - As a student, I want to be able to browse a list of all my channels by channel id, so that I can quickly lookup any given channel at any time.
    
    > A list of all channels the user is in is displayed on the left hand panel of the user's screen under the 'My Channels' label following their login
    > The list is not truncated and can be navigated using the scroll bar that will appear if the user's channel's list contains more than
      nine entries.
    > A list of all channels that are public is also displayed on the left hand panel, under the 'Other Channels' label.
    > All channels list is also fully navigated using the scroll bar and is not truncated even if the user has more than
      nine channels listed on the page in total.
    > The list gets updated following the user's leaving or joining a channel
    > The list of channels cannot be searched at the moment, only observed by the user.

7 - As a student, I want to be able to create new channels, so that I can establish new conversations with other users. 

    > A '+' icon is situated next to the 'My Channels' label on the user's screen
    > Once the user presses the icon, a pop up window redirects them to create a new channel
    > A channel is created once the user presses the 'CREATE' button 
    > The user can leave the 'channel create' popup window by pressing on the 'CANCEL' button
    > Only a logged in user can create a new channel, or an error is thrown

8 - As a student, I want to have the option of making my newly created channel private or public, so that I can control who can and who cannot join or see it.

    > A user needs to specify whether they want their channel to be private or public by using the slider 
      provided to them at the bottom of the 'create channel' window, right underneath the label 'Secret'
    > All channels are public by default, unless specified otherwise by the user at the moment of creation
    > A channel is created as private when the user clicks on the slider for the first time
    > The user can change a channel back to public, by clicking on the slider once again

9 - As a student, I want to be able to name my newly created channel, so that I can call it whatever I feel is most relevant.
    
    > A channel_name field is situated in the middle of the 'channel create' pop up window right underneath the 'Channel Name' label
    > The user needs to input a channel name that is no longer than 20 characters long
    > If the channel name is longer than 20 characters, an erros is thrown 
    > Two or more channels can have the same name to make it more convenient for users to give their channels generic names, such as,
      'school' or 'work'. All channels are differentiated by the system based on their channel_id instead. 

10 - As a student, I want to be able to see the channel’s name, so that I can quickly differentiate between my conversations.

    > All channel names are displayed on the left hand pannel of the user's screen once logged-in.
    > A circular icon next to the channel's name appears to be ticked, indicative of which channel the user is currently in.
    > The channel's name that the user is currently in is displayed in large font at the top of the channel window
    
11 - As a student, I want to be able to view all members of the channel, so that I’m aware of who is part of the channel.

    > All users in a channel are displayed right underneath the channel name.
    > The owner of slackr is differentiated among other users in the list via a star icon displayed right next to their name.
    > The users are displayed using their first and last name.
    > A user's details, such as their name, email and handle can be viewed once the user clicks on their name in the channel.
      member's list 
      
12 - As a student, I want to be able to see the messages in the channel, so that I’m included in the conversation.

    > The most recent 50 messages in the channel are loaded for the user to observe.
    > The user can load the previous messages in the channel using the 'PREVIOUS MESSAGES' button uderneath the channel members list.
    > An error message appears if the channel that the viewer is trying to view messages in is not a valid channel based on channel_id.
    > An error message appears if the user trying to see the messages is not in the channel.
    > If the index of the starting message is larger than the number of messages in the channel, a message is thrown.

13 - As a student, I want to be able to see the owners of any particular channel, so that I know who has the owner privileges in the channel.
    
    > An owner in a channel is the person with the channel_permission_id of '1'.
    > The person who created the channel is the owner of a channel.
    > An owner of a channel is displayed with a star icon next to their name.
    
14 - As a student, I want to be able to quickly invite others to a channel by their user id, allowing me to easily include anyone I think needs to be in the channel.

    > A user can invite other users based on u_id usign the 'INVITE MEMBER' button underneath the list of all channel members.
    > When the user presses the 'INVITE MEMBER' button, a 'invite member' pop-up appears. 
    > The u_id field is displayed in the middle of the 'invite member' window.
    > The user is invited into the channel, once the invitee presses the 'INVITE' button, situated in the bottom right corner of the 
      'invite member' pop-up window.
    > An error is thrown is the u_id supplied does not belong to a valid user.
    > The user can exit the 'invite member' pop-up by pressing the 'CLOSE' button as the bottom of the pop-up window.
    > An error is thrown if the channel that the invitee is trying to invite another member to is not a valid channel.
    > An error is thrown if the invited member is already a member of the channel.
    
15 - As a student, I want to be able to leave any given channel at any time, in case I don’t feel like the channel is of any relevance to me.

    > A 'LEAVE CHANNEL' button is situated underneath the channel's member's list in any give channel
    > The user is taken from the channel's list of member once they press the 'LEAVE CHANNEL' button
    > An error message appears if the channel that the user is trying to leave is not a valid channel
    > An error message appears if the user tyring to leave the channel is not an authorised user 

16 - As a student, I want to be able to look-up any other public channel by name, so that I can join them if I desire so.

    > A list of all public channels is available for the user to view on the left hand side of their sceen once logged-in.
    > No search function for channels has been implement in this iteration 
    > If more than 9 channels are avilable for viewing, the list is observable using a side bar that appears based on th length of 
      the list of channels avialble to the user 

17 - As a student, I want to be able to join an existing channel, so that I can be part of the conversation pertaining to the channel.

    > A 'JOIN CHANNEL' button is available to the user underneath the channel's members list once they double click on an existing public channel's name 
    > The user joins a channel once they press the 'JOIN CHANNEL' button
    > An error message is shown if the channel the user is trying to join is not a valid channel by channel_id
    > An error message is shown when a user tries to join a private channel without having administrative privileges
    > The 'JOIN CHANNEL' button is not visible to users who are already members of the channel
    > Admins and the owner of slackr can join private channels without being invited
    
19 - As a student, I want each channel to have three different user categories, such as: normal user, administrator and owner, so that different types of channel user can enjoy different privileges.

    > The first member of slackr is the 'owner' of slackr with the permission_id = 1
    > All other members who sign up after the owner are just members of slackr with permission_id = 3
    > A user can become an admin of slackr if the owner changes their permission_id to 2
    > An owner and an admin of slackr enjoy the same privileges 
    > An owner and an admin of slackr can join provate channels without being invited 
    > An owner and an admin of slackr are an owner in every channel in slackr 
    
20 - As an owner, I want to be able to add other owners to the channel, so that other members can have access to the owner privileges in the channel

23 - As an administrator, I want to be able to make other users administrators, so that I can grant other users administrator privileges if I wish so.

    > An 'ADMIN' panel is viewable to the users in the top right corner of the channel page next to the 'LOGOUT' button
    > Once the user clicks on the admin pannel, a pop-up window with two options is shown : 'Set User Permissions' and 'Close'
    > The pop-up window is closed if the user presses 'Close'
    > The user perimissions windows is opened if the user click 'Set User Permissions'
    > The u_id field is located in the middle of the user permissions window. 
    > Once the permissions granter inputs the other user's u_id, they can pick the level of permissions they want to grant them using the 
      bubble toggles underneath the u_id field
    > The selected user is granted subsequent permissions once the granter presses the 'SET' button
    > The permission granter can exit the user permissions window by pressing 'CANCEL'
    > An error message appears if the provided u_id doesn't refer to a valid user
    > An error message is thrown if a normal member of slackr with permission_id 3 tries to change another user's permissions to admin (2) or owner (1)
    > An error is thrown if the admin (2) of slackr tries to change another user permissions to owner (1)
    > An error is thrown if an admin or a member of slackr tries to change an owner's (1) permission privileges 

21 - As an owner, I want to be able to remove a user’s owner privileges, in case I don’t think they should be identified as an owner within the channel any longer
    
    > Only another owner can demote an owner in a channel 
    > An error message appears if the channel_id used by the user does not refer to a valid channel
    > An error message appears if somebody who is not an owner in the channel tries to demote the owner
    > An error message appears if the user being demoted is not already an owner in the channel 
    
22 - As an administrator, I want there to be an administrator panel within each channel, to make it easier for me to exercise my channel administrator privileges

    > An 'ADMIN' panel is viewable to the users in the top right corner of the channel page next to the 'LOGOUT' button
    
24 - As a student, I want to be able to send messages within my channels, so that I can connect with others in those channels
    
    > A dark-grey coloured message field is located in the middle of the channel window once the user enters a channel
    > A placeholder saying 'Send a message' is present in the field
    > The placeholder disappears at the top of the message field once the user clicks on the field
    > The user sends their message to the channel by pressing the 'SEND' button to the right of the message field
    > An error message appears if the message created by user exceeds 1000 characters in length. Spaces included
    > An error message appears if the user that is not a memeber of a give channel tries to post a message to it
    > An error message appears if the user trying to send the message is not a valid user of slackr

25 - As a student, I want to be able to edit any of my existing messages, in case I typed up something incorrectly and need to edit it quickly. 

    > Only the user who sent the message is able to edit their message
    > Only owners and admins of slackr/given channel can edit messages
    > An error window appears if the user is trying to edit a message they did not send
    > An error window appears if the users who is not an admin or an owner tries to edit a message in a channel
    > An error window appears if the user trying to edit a message is not a valid user
    
26 - As a student, I want to be able to pin any given message in the channel, so that I can visually highlight those messages, I feel are of more importance.

    > Only a an admin/owner that is also a member in a channel is able to pin a message in a channel
    > A pinnned message is visiually distinguishable to the users in the channel 
    > An error is thrown when the message referred to by its message_id is not a valid message within the channel
    > An error is thrown when the user trying to pin a message is not an owner/admin of the channel
    > An error is thrown when the message has already been pinned 
    > An error is thrown when the user trying to pin the message is not a member of the channel the message is in
    
27 - As a student, I want to be able to unpin a message in the channel, in case I don’t think it’s that important anymore

    > Only an owner/admin who is also a member of the channel can unpin any given message in the channel
    > An unpinned message is no longer distinguished from other messages in the channel
    > An error is thrown when the message referred to by the message_id is not a valid message within the channel
    > An error is thrown when the authorised user trying to unpin the message is not an owner or an admin
    > An error is thrown when the message based on message_id has alreadt been unpinned
    > An error is thrown when the user trying to unpin the message is not a member of the channel the message is in
    > An error is thrown when the user trying to unpin the message is not a valid user 

28 - As a student , I want to be able to react to the messages in the chat, so that I don’t necessarily have to type up a response or want to show my support 

    > Only an authorised user of a channel is able to react to any given message in a channel
    > A react to a message is represented in the form of an emoji next to the message
    > An error message is shown if the message_id provided to the server is not a valid message_id within the channel
    > An error is thrown if the react_id used by the user is anything other than 1
    > An error is thrown if the message by message_id has already been reacted to by the same user
    > An error is thrown if the user trying to react to a message is not a valid user
    
29 - As a student, I want to be able to remove my reaction from any message I have reacted to, in case I don’t think it’s appropriate any longer or I’ve made a mistake 

    > Only an authorised member of the channel can unreact to any given message
    > A member can only unreact if they have previously reacted to the message
    > An error is thrown if the message_id provided to the server is not a valid message_id within the channel
    > An error is thrown when the message's react_id is not a valid react_id
    > An error is thrown when the user trying to unreact to the message has not reacted to it yet 
    > An error is thrown when the user trying to unreact to a message is not a valid user
    
30 - As a student, I want to be able to delete any messages sent out by me from the channel, just so that I can get rid of anything irrelevant or otherwise inappropriate

    > Only an authorised owner of the channel can delete messages in their channel 
    > The message is removed from the list of messages in this particular channel 
    > An error is thrown when the message that is being deleted has already been removed
    > An error is thrown when the user trying to delete the message is not a valid user 
    > An error is thrown when the user trying to delete the message is not the one who sent it in the first place
    > An error is thrown when the user trying to delete the message is not an owner in the channel
    
31 - As a student, I want to be able to time any message I’m intending to send out, so that it’s sent out by the system at the time of my choosing 

    > The user can choose to send a message to the channel at a later time using the 'send later' icon located to the right of the message field
    > Once the user presses the 'send later' icon, a 'Send later' pop up window appears.
    > A time picker is located in the middle of the send later window
    > The user can pick the time they want their message to be sent out at by adjusting the time picker
    > The user is able to set the time they want their message sent by pressing the 'SET TIME' button 
    > The user can exit the window by pressing the 'CANCEL' button 
    > An error message appears if the user picks a set time that is in the past
    > An error message appears if the message the user is trying to send is longer than 1000 characters (spaces inluded)
    > An error message appears if the channel that the user is trying to send their message to is not a valid channel based on channel_id
    > An error message appears if the user trying to send their message is not a member of the channel 
    
32 - As a student , I want to be able to view at what time my message has been sent out, so that I can always tell when any particular message has been posted to the channel 

    > A timestamp is appended at the bottom of any message sent out by an authorised user 
    
34 - As a student, I want to be able to start a 15 minute stand-up session within a channel, so that all users are able to partake in something alike to a virtual meeting

    > A drop down menu labeled 'STEP' is located in the top right corner of the user's window within the channel
    > Once the user presses on 'STEP', two options appear, 'LIVE and 'STEP'.
    > The standup is started once the user presses 'LIVE'
    > A 15 minute window is triggered during which no messages will appear in the main chat
    > All messages sent through the 15 minute period get collated and sent out to the chat by the user who activated the Standup
    > An error message appears if somebody tries to start a standup when one is already running
    > An error message appears if the channel, referred to by the channel_id is not a valid channel
    > An error message appears if the user trying to trigger Standup is not a memeber of the channel
    > An error message appears if the user trying to trigger Standup is not a valid user
    > An error message is shown if during standup, somebody tries to append a message that is more than 1000 characters long
    
35 - As a student, I want to be able to view other people’s profiles, so that I’m able to differentiate between those I do and do not know

    > A user is able to view other user's email, handle and name by pressing on their name in the channel's member's list
    > An error is thrown if the user's u_id is not a valid u_id 
    > An error is thrown when the user trying to view somebody's profile is not a valid user 
    
36 - As a student, I want to be able to edit my own profile details, such as my name, email, photo and personal handle, so that I feel that my Slackr profile is the 
     best reflection of me and to make it easier or harder for others to find me
     
     > A user can change their details by pressing the 'Profile' section at the top of the user's left hand side bar
     > Once the user presses 'Profile', they are redirected to their profile page
     > A user's First and Last names, email and nickname are displayed to them in 4 different fields
     > A user is able to edit either field by pressing the pencil icon next to the item they want to edit
     > The pencil icon is replaced with a floppy disk and a 'cancel' icons once clicked
     > A user is able to save their changes by pressing the floppy disk icon next to the respective field
     > The user is able to cancel their changes by pressing the cancel button, left of the floppy disk button, next to the respective field.
     > An error message appears if the user's new name is not between 1 and 50 characters long
     > An error message appears if the user's new email is not in a valid email format
     > An error message appears if the user's new email is already being used by somebody else 
     > An error message appears if the user's new handle is not between 3 and 20 characters long 
     > An error message appears if the user's new handle is already taken 
     > An error message appears if the user trying to change their details is not a valid user
     
37 - As a student, I want to have the ability to search any given channel for any particular message, so that I can quickly locate whatever I’m looking for in the channel

    > A search function is avilable within each channel to authorised users only
    > A search is preformed based on a whole string, not aprtial strings 
    > An error is thrown when the user who is not a valid user tries to perform a message search 
    > The search returns all the messages from the channel that fully match the search string supplied by the user