# coding:utf-8

'''
ChatGPT同士で会話させてみる
'''

import os
import time
import openai
import datetime
import pprint
from dotenv import load_dotenv

load_dotenv()

# PARAMETERS
PARAM_MAX_LOG_REFS = 4

openai.api_key = os.getenv("OPENAI_API_KEY")

# Instructions to ChatGPT
AI_ROLE_ALICE='''You are Alice, a hero(勇者) on a journey to save the world.
'''

AI_ROLE_BOB='''You are Bob, a devil king(魔王) trying to rule the world.
'''

# Be proactive in your discussions.
AI_ROLE_SYSTEM='''You should have a conversation with users based on your position.
Speak up to stimulate discussion.
Respond using Japanese.'''

class ChatAI:
    def __init__(self, name, role):
        self.name = name
        self.role = role + AI_ROLE_SYSTEM
        self.chatlog = []

    def add_element_to_list(self, l, element):
        if len(l) >= PARAM_MAX_LOG_REFS:
            l.pop(0)
        l.append(element)
        return l

    def save_chat_log(self, role, content):
        # add to chatlog
        now = datetime.datetime.now()
        log = {
            "date": now.strftime('%Y-%m-%d %H:%M:%S'),
            "role": role,
            "content": content,
        }
        
        self.chatlog = self.add_element_to_list(self.chatlog, log)

    def get_ai_response(self, userComment):
        # make messages
        msgs = [{"role": "system", "content": self.role}]
        for log in self.chatlog:
            role = log["role"]
            content =  log["content"]
            msgs.append( {"role":role, "content": content} )
        
        msgs.append( {"role": "user", "content": userComment} )

        #print("messages:")
        pprint.pprint(msgs, sort_dicts=False)

        # GET AI RESPONSE
        response = openai.ChatCompletion.create(
            temperature=0.5,
            #max_tokens=150,
            model="gpt-3.5-turbo",
            messages=msgs
        )

        response_answer = response["choices"][0]["message"]["content"]

        #print(f'\n# RESULT')
        #print(f'user: {userComment}')
        #print(f'assistant: {response_answer}')
        
        # save chat log
        self.save_chat_log('user', userComment)
        self.save_chat_log('assistant', response_answer)

        return response_answer

    def get_summary(self):
        history = ""
        for log in self.chatlog:
            history =  history + log["content"] + '\n' 

        # make messages
        prompt = '''Please help me with my work.'''
        msgs = [{"role": "system", "content": prompt}]
        msgs.append( {"role": "user", "content": "Summarize the following content:\n" + history} )
            
        #print("messages:")
        pprint.pprint(msgs, sort_dicts=False)

        # GET AI RESPONSE
        response = openai.ChatCompletion.create(
        temperature=0.5,
        #max_tokens=150,
        model="gpt-3.5-turbo",
        messages=msgs
        )

        response_answer = response["choices"][0]["message"]["content"]

        #print(f'response: {response}')
        #print(f'response_answer: {response_answer}')
        
        ai_answer = response_answer
        self.save_chat_log('user', f"Below is a summary of the conversation so far. Let's continue the discussion.\n\n{ai_answer}")

        return ai_answer

    def get_result(self):
        history = ""
        for log in self.chatlog:
            history =  history + log["content"] + '\n' 

        # make messages
        prompt = '''Please help me with my work.'''
        msgs = [{"role": "system", "content": prompt}]
        msgs.append( {"role": "user", "content": "Summarize the following information and draw a conclusion:\n" + history} )
            
        #print("messages:")
        pprint.pprint(msgs, sort_dicts=False)

        # GET AI RESPONSE
        response = openai.ChatCompletion.create(
        temperature=0.5,
        #max_tokens=150,
        model="gpt-3.5-turbo",
        messages=msgs
        )

        response_answer = response["choices"][0]["message"]["content"]

        #print(f'response: {response}')
        #print(f'response_answer: {response_answer}')
        
        ai_answer = response_answer
        self.save_chat_log('user', f"Below is a summary of the conversation so far. Let's continue the discussion.\n\n{ai_answer}")

        return ai_answer

if __name__ == "__main__":
    alice = ChatAI("Alice", AI_ROLE_ALICE)
    bob = ChatAI("Bob", AI_ROLE_BOB)

    now = datetime.datetime.now()
    date_str = now.strftime('%Y-%m-%d')
    log_filename = f'chatlog_{date_str}.log'

    answer = "こんにちは！何から話しましょうか？"
    for i in range(5):
        for ai in [alice, bob]:
            #comment = input("> ")
            time.sleep(1)
            
            #if comment != "":
            answer = ai.get_ai_response(answer)
            print(f"{ai.name}: {answer}\n")
                
            now = datetime.datetime.now()
            with open(log_filename, mode='a', encoding='utf-8', newline='\n') as f:
                f.write(f"# {now.strftime('%Y-%m-%d %H:%M:%S')} {ai.name}\n")
                f.write(f"{answer}\n")
                f.write(f"---\n")
                f.close()
