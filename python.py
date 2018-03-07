import json
import datetime
import flask
import sys
import requests
from nltk.tokenize import sent_tokenize
from nltk.tokenize import word_tokenize
app = flask.Flask(__name__)


SpeakerTime = 5

words = []
firstTimestamp = []
transcript = []
speakerNames = []
wordsWithTimestamp = []

@app.route("/",methods=["POST"])
def speechData():
    data = {"success": False}

    if flask.request.method == "POST":
        content = flask.request.json
        data['success'] = True
        storeSpeechData(content,firstTimestamp,words)
        transcript.append(content['transcript'])

    return flask.jsonify(data)

@app.route("/speakerData",methods=["POST"])
def speakerData():
    data = {"success": False}

    if flask.request.method == "POST":
        content = flask.request.json
        speakerNames.append(content['speaker'])

    return flask.jsonify(data)



@app.route("/finalProcessing",methods=["POST"])
def finalProcessing():

    # Punctuation
    finalTranscript = doPunctuation(' '.join(transcript).rstrip())
    
    #correct punctuation (Dont require this if punctuator is good)
    finalTranscript = correctPunctuation(finalTranscript)

    #Split Sentences
    sentences = splitIntoSentences(finalTranscript)

    #loop Through sentences and assign timestamp to words
    counter= 0
    for sentence in sentences:
        tempList = []
        for word in sentence.split(' '):
            tempList.append({'time':words[counter]['time'],"word":word})
            counter += 1
        wordsWithTimestamp.append(tempList)

    # create a dialogue
    dialogue = getDialogue(wordsWithTimestamp)

    data = {"success": True}
    return flask.jsonify(data)



def getDialogue(wordswithtimestamp):
    initialTime = datetime.datetime.fromtimestamp(1519560060) - datetime.datetime.fromtimestamp(1519560060)
    mainList = []
    currentList = []
    counter = 0
    
    for sentence in wordswithtimestamp:
        sentenceLength = len(sentence)
        flag = False

        ActualSentence = ''
        for index,word in enumerate(sentence):
            ActualSentence += word['word'] + " "
            
            # Better Logic required
            if (word['time'].total_seconds() - initialTime.total_seconds()) > SpeakerTime:
                if index < (sentenceLength/2):
                    flag = True
        
        if flag:
            initialTime + datetime.timedelta(seconds=SpeakerTime*1000)
            mainList.append({'sentence':currentList,'speaker':speakerNames[counter]})
            counter += 1
            currentList = []
            currentList.append(ActualSentence)
        else:
            currentList.append(ActualSentence)
    
    
    print(mainList,file=sys.stderr)
    return mainList



def splitIntoSentences(finalTranscript):
    return sent_tokenize(finalTranscript)



def doPunctuation(data):
    # url = "http://bark.phon.ioc.ee/punctuator"
    # return requests.post(url)
    return "Hi Kevin Good morning, Hi Rohan Good morning. Do we have everyone on the call? Yes, I have the complete off shore mobile development team. With me Great Lets get started. We have been planning version 2 of our mobile apps and in the last week me and Rohan, sat together and worked on the back log items as well as added a few new features to the sprint. I hope everyone has gone through the sprint plan and assigned tasks So Lets quickly share updates on current tasks. Rohan. Why dont you go first, Yes, sure kevin. So I have picked up task 12, which is implementing login with google module in the iOS application. I will be exploring how to go about this task and find if there are any SDK, is available to integrate single sign on Kevin, any updates from the UX team regarding wireframes, Hmm, no, The UX team is currently still working on the app screen design. Okay, I will check what backend changes will be required for implementing this module and get back to you. I will send a mail to you kevin with the backend changes necessary. Oh okay, I wasnt, anticipating "



def correctPunctuation(text):
    sentences = sent_tokenize(text)
    ignoreWords = ['hi','yes','no','okay','hmm','no']
    newText = ''

    for sentence in sentences:
        counter = 0
        fullstopPostition = 0
        commaPosition = -1
        
        wordList = word_tokenize(sentence)
        for index,word in enumerate(wordList):
            currentWord = word
            if word.lower() in ignoreWords:
                newText += currentWord + ' '
                continue

            if word == '.':
                fullstopPostition = counter
            elif word == ',':
                commaPosition = counter

                if not fullstopPostition == -1:
                    if commaPosition-fullstopPostition < 6 and commaPosition-fullstopPostition > 0:
                        currentWord = '.'
                if wordList[index+1].lower() in ignoreWords:
                    currentWord = '.'

            newText += currentWord + ' '
            counter += 1

    return (newText.replace(' ,',',').replace(' .','.').replace(' ?','?'))



def storeSpeechData(data,firstTimestamp,words):
    startTimestamp = datetime.datetime.fromtimestamp(data['startTimestamp'])

    if not firstTimestamp:
        firstTimestamp.append(startTimestamp)

    for word in data['words']:
        wordStartTime = float(word['startTime'][:-1])
        wordTime = startTimestamp + datetime.timedelta(seconds=wordStartTime)
        CorrectTime = wordTime - firstTimestamp[0]
        words.append({"word":word['word'],"time": CorrectTime })



if __name__ == "__main__":
    app.config['JSON_AS_ASCII'] = False
    app.run(host="0.0.0.0")