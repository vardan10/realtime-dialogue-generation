import json

transcript = "So I have picked up task 12 which is implementing login with google module in the iOS application I will be exploring how to go about this task and find if there are any SDK is available to integrate single sign on Kevin any updates from the UX team regarding wireframes Hmm no The UX team is currently still working on the app screen design Okay I will check what backend changes will be required for implementing this module and get back to you I will send a mail to you kevin with the backend changes necessary Oh okay I wasnt anticipating"
startTimestamp = 977443200

startTime = 300
endTime = 600

words = []
for word in transcript.split(' '):
    dictionary = {}
    dictionary["startTime"] = str(startTime/1000) + "s"
    dictionary["endTime"] = str(endTime/1000) + "s"
    dictionary["word"] = word
    words.append(dictionary)

    startTime = endTime
    endTime = endTime + 400

json1 = {}
json1["confidence"] = 0.97186122
json1["transcript"] = transcript
json1["startTimestamp"] = startTimestamp
json1["words"] = words

#json_data = json.dumps(json1)

with open('JSONData.json', 'w') as f:
     json.dump(json1, f)