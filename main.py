import requests
import json
import time
import random
#Static Variables
TimesExiled = 0
TimesIterated = 0

#Variables
BlackListedGroupId = 1234567890 #The ID of the group youd like the exclude the user ID's From.
BlackListedUserIds = {123456789,1234567890} #The User ID's you'd like to exclude from the group.
CheckFrequency = 120 #How frequently the program will check the group & kick banned members.
Cookies = "" #The cookie you can find under Ctrl+I -> Storage -> Cookies -> .ROBLOSECURITY
#Everything Else (only modify this stuff if you know what you're doing)
Session = requests.Session()
Session.cookies[".ROBLOSECURITY"] = Cookies

def ReValidateSession():
    SessionRequest1 = Session.post(
        url="https://auth.roblox.com/"
    )
    if "X-CSRF-Token" in SessionRequest1.headers:  # check if token is in response headers
        Session.headers["X-CSRF-Token"] = SessionRequest1.headers["X-CSRF-Token"]  # store the response header in the session
        print("Generated New Token")

def DeletePosts(GroupId,UserId):
    DeleteResponse = Session.delete(
        url="https://groups.roblox.com/v1/groups/"+str(GroupId)+"/wall/users/"+str(UserId)+"/posts"
    )
    print(DeleteResponse)
    if DeleteResponse != 200:
        if DeleteResponse == 403:
            print("ReValidating Session & Retrying.")
            ReValidateSession()
            DeletePosts(GroupId,UserId)
    else:
        print("Successfully filtered wall posts.")

def FilterWall():
    for UUID in BlackListedUserIds:
        DeletePosts(BlackListedGroupId,UUID)

def KickUser(GroupId,UserId):
    Request = Session.delete("https://groups.roblox.com/v1/groups/"+str(GroupId)+"/users/"+str(UserId))
    if Request != 200:
        if Request == 403:
            ReValidateSession()
            KickUser(GroupId,UserId)

#Runtime
ReValidateSession()

while True:

    TimesIterated = TimesIterated+1
    print("Checking for Iteration | "+str(TimesIterated))
    if TimesIterated % 10 == 0 and TimesIterated != 0:
        ReValidateSession()
    FilterWall()
    for UUID in BlackListedUserIds:
        UserGroupsDataRAW = requests.get("https://groups.roblox.com/v2/users/"+str(UUID)+"/groups/roles")
        UserGroupsData = UserGroupsDataRAW.json()
        for Item in UserGroupsData["data"]:
            Group = Item["group"]
            Id = Group["id"]
            if BlackListedGroupId == Id:
                TimesExiled= TimesExiled+1
                print("Match | "+str(TimesExiled)+" | Found; Exiling.")
                KickUser(BlackListedGroupId,UUID)
                
    time.sleep(CheckFrequency)
