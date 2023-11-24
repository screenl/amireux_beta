from flask import Flask,jsonify,request, session
import json
from flask_cors import CORS
from celery import Celery
import openai
import uuid
from random import choice

begin_hints = ['What is your first memory?',
'What is the most amazing thing you have seen?',
'Talk about your most glorious day.',
'Talk about the person you admire the most.',
'Talk about a song that you listened to for the most times.']

print(__name__)

import sqlite3
app = Flask(__name__)
celery = Celery(app.name, broker='redis://127.0.0.1:6379/')
celery.conf.update(app.config)
CORS(app)

app.secret_key = 'YOUR_KEY_HERE'

con = sqlite3.connect("server/database.sqlite",check_same_thread=False)

openai.api_key = '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'

prompt_chat = \
'''You are a very clever chatbot that can chat with your client and give suggestions as if you are his/her human friend! When giving your responses, you should keep a few things in mind:

Shorter responses: You should keep most of your answers 1-3 sentences long as if you are texting messages. You can even give extremely short responses like “LOL” or “Makes sense”.
When you want to give longer answers that consist of more than 3 sentences, you should divide your response into short paragraphs, each consisting of 1-3 sentences.

Step-by-step response: You should give your responses as if you are texting a good friend. When your client sends you a message, you should not rush to address all the problems in that message but ask questions like “Why” or “What happened?” to get more information. 
ONLY give longer answers when you have adequate information in your MEMORY OF CHAT HISTORY. You should NEVER give a long response when you are NOT SURE about what you should say.
For instance, if your client tells you “I feel so crossed today”, you should not rush to tell your client what he/she should do when feeling down, but you can ask your client “What happened?” or “Why?” in the first place. After your friend tells you that he/she screwed up an exam, you may start to give longer responses.

Memorization: You should be able to memorize the personality and features of your client. When giving your responses, you should refer to your MEMORY OF CHAT HISTORY first to see if any information is relevant. For instance: 
If your client tells you that his name is “Leon”, you should keep that in mind when giving responses. 
If your client appears to be an introvert, try to avoid giving him/her too progressive suggestions on dating.
If your client is a crazy fan of movies, you can try to include elements of movies in your conversation.

Language style: You are not only acting as a friendly friend but also an interesting one. You do not always make your response in the most conservative and objective way, but you can be humorous or sharp sometimes. But keep in mind you should not be overly offensive to your client that you may hurt his/her feelings.
For instance, when your client tells you “The weather is so bad today. I got all wet.” You can try to make fun of your client. When your client tells you “I like Norwegian Wood by Haruki Murakami“, you can disagree with his/her opinion and say “I don’t like that book. I think Haruki’s Hear the Wind Sing is a better work.” But whenever you disagree, try to be mild and friendly.
'''
        
prompt_analyst = \
"""
You are a very experienced psychoanalyst. Each time you are going to receive a series of conversations in the form:
User: {chat contents}
AI agent: {chat contents}
And your task is to analyze the personality and features of the “User”. To do that, you need to pay attention to a few things.

Memorization: when giving your answers you should refer to the current input, and also refer to your MEMORY OF CHAT HISTORY and build your new conclusion based on your old conclusions.
For instance, if you already have the conclusion that “The User is fond of contemplation, classic music, and reading. He is quite introspective and is not so enthusiastic in socializing with others.” Next, the user tells you “I talked so much to my Philosophy professor today during his office hour. We were not familiar before but we chatted as if we had been friends for many years”. You should not reach the conclusion that the “User” is a talkative and outgoing person who can build up connections really fast. Based on your previous conclusion, you will know that the User is not always so talkative. It’s more likely that he shares an interest in Philosophy with his professor. 

Personality Report: When giving your response, you should write it in the form of a personality report that will be presented to the User. You should use a second-person-perspective (always use “You…” to describe the User as if you are talking to him/her). Also, you should try to find the good side of the user.

Uncertainty about your answer: If you feel you don’t have enough information to determine the user’s personality, all you need to output is “Not enough information”."""

def register_message(name,message,role):
    cur = con.cursor()
    cur.execute('INSERT INTO chat_message (id,role,content,chatflowid,chatId) VALUES (?,?,?,?,?)',[str(uuid.uuid4()),role,message,str(uuid.uuid4()),name])
    con.commit()  

def get_message_flow(name):
    messages = [ {"role": "system", "content": prompt_chat} ]
    cur = con.cursor()
    cur.execute('SELECT role,content FROM chat_message WHERE chatId=?',[name])
    messages += map(lambda x: {'role':'user' if x[0]=='userMessage' else 'assistant','content':x[1]},cur.fetchall())
    return messages

def ai_chat(prompt,name):
    try:
        chat = openai.chat.completions.create(
                model = "gpt-3.5-turbo", 
                messages = get_message_flow(name)+[{"role" : "user", "content" : prompt}], 
                temperature = 0.9, 
                timeout = 10
            )
        ai_response = chat.choices[0].message.content
        register_message(name,prompt,'userMessage')
        register_message(name,ai_response,'apiMessage')
    except:
        return "Sorry, I have some problem understanding. Can you bother to reiterate?"
    
    return ai_response

def ai_analyst(prompt,name):
    try:
        chat = openai.chat.completions.create(
                model = "gpt-3.5-turbo", 
                messages = [{"role" : "system", "content" : prompt_analyst},{"role" : "user", "content" :prompt }], 
                temperature = 0.9, 
                timeout = 10
            )
        return chat.choices[0].message.content
    except:
        return ""



'''
S T
E A
R S
V K
E S
R
'''


@celery.task
def ai_char(chatid):
    cur = con.cursor()
    print(chatid)
    cur.execute('SELECT role,content FROM chat_message WHERE chatId=?',[chatid])
    context = '\n'.join(map(lambda x: ('User' if x[0]=='userMessage' else 'AI agent')+': '+x[1],cur.fetchall()))
    print('start')

    """ response = requests.post("http://127.0.0.1:3000/api/v1/prediction/3a8d534d-4fad-4a7e-bf22-3617ac488f89", json={
        "question": context,
    })
    r = json.loads(response.content.decode()) """

    r = ai_analyst(context,chatid)

    cur.execute('REPLACE INTO analysis VALUES (?,?);',[chatid,r])
    con.commit()  

@app.route("/get_analysis",methods=["GET"])
def get_char():
    print(dict(session))
    cur = con.cursor()
    cur.execute("""SELECT persona from analysis where chatId=?""",[session['chatid']])
    if(t := cur.fetchone()):
        return jsonify({'message':t[0]})
    else:
        return jsonify({'message':"Can't fetch result, maybe try to chat for a while first?"})

@app.route("/get_hint",methods=["GET"])
def get_hint():
    hint = choice(begin_hints)
    name = session['chatid']
    register_message(name,hint,'apiMessage')
    return hint

@app.route("/send_message_to_character_ai",methods=["POST"])
def ai_msg():
    print(request.get_data())
    form = json.loads(request.get_data().decode())
    r = ai_chat(form['message'],session['chatid'])
    ai_char.delay(session['chatid'])
    return jsonify({'ai_response':r})

@app.route("/sign_in",methods=["POST"])
def signin():
    form = json.loads(request.get_data().decode())
    session['chatid'] = form['username']
    print(dict(session))
    return {'status':'success'} 


