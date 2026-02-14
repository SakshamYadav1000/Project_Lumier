import datetime
import webbrowser
import time
import random
import pyttsx3
import os
import json

class Lumier:
    def __init__(self,name):
        self.name=name
    
#for_user:
    def show_time(self):
        now=datetime.datetime.now()
        print(f"Current time is {now.strftime('%H:%M:%S')}")
    
    def search(self):
        query=input("What you want to search: ")
        url=f"http://www.google.com/search?q={query}"
        webbrowser.open(url)
        print("Searching google for you....")
    
    def calculate(self):
        try:
            expression=input("Enter the maths equation: ")
            result=eval(expression)
            print(f"The result is: {result}")
        except:
            print("OOps! That expression was invalid!")
    
    def speak(self,message=None):
        engine=pyttsx3.init()
        if message is None:
            message=input("Provide a message: ")
        engine.say(message)
        engine.runAndWait()
    
    def timer(self):
        seconds=int(input("Enter the time in seconds: "))
        time.sleep(seconds)
        self.speak("Time's up!")
        print("Time's up...")
    
    def joke(self):
        jokes=["What did one snowman say to the other snowman? It smells like carrots over here!","Why did Beethoven get rid of his chickens? All they ever said was, 'Bach, Bach, Bach!'","What did 20 do when it was hungry? Twenty-eight.","Why is grass so dangerous? Because it's full of blades!","Why are mountains so funny? They're hill areas.","Why wasn't the cactus invited to hang out with the mushrooms? He wasn't a fungi.","Why shouldn't you fundraise for marathons? They just take the money and run."]
        chosen_joke=random.choice(jokes)
        print(chosen_joke)
        self.speak(chosen_joke)

    def remember(self):
        os.makedirs("memory",exist_ok=True)
        note=input("What should i remember? ")
        with open("memory/memory.txt","a") as file:
            file.write(note+"\n")
        print("Okay I will remember that")
    
    def note(self):
        os.makedirs("notes",exist_ok=True)
        ask=input("Do you want to create a note or read a existing note? ")
        if(ask.lower()=="create"):
            title=input("What is the title: ")
            content=input("What is the content: ")
            filename=(f"notes/{title}.txt")
            with open(filename,"w") as file:
                file.write(f"{title}\n{content}")
        elif(ask.lower()=="read"):
            title=input("Enter the title you want to read: ")
            filename=(f"notes/{title}.txt")
            try:
                with open(f"notes/{title}.txt") as file:
                    content=file.read()
                    if(content.strip()==""):
                        print("There is nothing in notes!!")
                    else:
                        print("The content is: ")
                        print(content)
            except FileNotFoundError:
                print("File Not Found!!")
    
    def recall(self):
        mode=input("What do you want me recall? Memory or fact? ").lower()
        if mode=="memory":
            try:
                with open("memory/memory.txt") as file:
                    lines=file.readlines()
                    if not lines:
                        print("i dont remember anything yet.")
                    else:
                        for line in lines:
                            print("- "+line.strip())
            except FileNotFoundError:
                print("i dont have any memories yet.")
        elif mode=="fact":
            query=input("Which fact do you want me recall? ").lower()
            os.makedirs("knowledge",exist_ok=True)
            facts=self.load_facts()
            if facts:
                if query in facts:
                    print(facts[query])
                else:
                    print(f"{query} not found!!")
            else:
                print("No facts avaiable!!")
        else:
            print("Invalid!!") 

    def learn(self):
        os.makedirs("knowledge",exist_ok=True)
        facts=self.load_facts()
        topic=input("Enter the topic: ")
        definition=input("Enter the definition: ")
        facts[topic]=definition
        with open("knowledge/facts.json","w") as file:
            json.dump(facts,file,indent=4)

    def forget(self):
        query=input("What do you want me to forget? ").lower()
        facts=self.load_facts()
        if facts:
            if query in facts:
                del facts[query]
                with open("knowledge/facts.json","w") as file:
                    json.dump(facts,file,indent=4)
                print(f"The {query} has been forgotten")
            else:
                print(f"The {query} do not exist!!")
        else:
            print("The facts does not exist!!")
    
    def list_facts(self):
        facts=self.load_facts()
        if facts:
            for topic,definition in facts.items():
                print(f"Topic: {topic}")
                print(f"Definition {definition}")
                print("-"*30)
        else:
            print("No facts to list!!")
    
    def exit(self):
        print(f"Shuting down... GoodBye!")
        input("Press Enter to Exit")

#for_backend:

    def greet(self):
        greetings = ["Hey there, {user}! Nice to see you.","Hello {user}, how can I help you today?","Welcome back, {user}!","Hi {user}! I'm here if you need anything.","Greetings, {user}! Let's get started."]
        greet = random.choice(greetings)
        name = getattr(self, "user", "there")
        print(greet.format(user=name))

    def welcome_user(self):
        self.get_user_name()
        print("-" * 44)
        print("\U0001F31F Lumire this side!! \U0001F31F")
        self.greet()
        print("Here's what I can help you with:\n")
        print("\U0001F9E0 Memory        \U0001F552 Time       \U0001F4AC Speak")
        print("\U0001F4DD Notes         \U0001F3B2 Joke       \U0001F50D Search")
        print("\U0001F4DA Learn Facts   \U0001F9EE Calculator \U0001F4C1 Recall")
        print("\nReady when you are!")
        print("-" * 44)

    def get_user_name(self):
        os.makedirs(f"user",exist_ok=True)
        filepath=("user/profile.txt")
        if os.path.exists(filepath):
            with open(filepath) as file:
                name=file.read().strip()
                self.user=name
                print(f"Welcome!! {name}")
        else:
            name=input("Hey whats your name? ")
            with open(filepath,"w") as file:
                file.write(name)
                self.user=name
            print(f"Heyy nice to meet you {name} i've saved your profile!")
    
    def remember_last_command(self):
        filepath=("user/last_command.txt")
        if os.path.exists(filepath):
            with open(filepath) as file:
                last=file.read().strip()
            if last:
                print(f"Last time you used the {last} command.")
                run=input(f"Do you want to repeat {last} command?(yes/no): ").lower()
                if run=="yes":
                    if hasattr(self,last):
                        func=getattr(self,last)
                        if callable(func):
                            func()
            else:
                print("No last command was found!!")
        else:
            print("No memory of the last command!!")
    
    def load_facts(self):
        filepath=("knowledge/facts.json")
        if os.path.exists(filepath):
            with open(filepath) as file:
                facts=json.load(file)
                return facts
        else:
            return {} 

    def command_map(self):
        return {"greet": ["greet", "say hi", "hello", "hey"],
        "show_time": ["time", "clock", "what's the time"],
        "calculate": ["calculate", "math", "solve"],
        "remember": ["remember", "note this", "store"],
        "recall": ["recall", "what did you remember", "memory", "fact"],
        "introduce": ["introduce", "who are you"],
        "search": ["search", "google", "find this"],
        "speak": ["speak", "say", "talk"],
        "timer": ["timer", "alarm", "remind me"],
        "joke": ["joke", "make me laugh", "funny"],
        "note": ["note", "write down", "create note"],
        "exit": ["exit", "quit", "close"]}
    
    def detect_mood(self,cmd):
        moods={"happy": ["excited", "thrilled", "joy", "yeyey", "yippy", "!!!"],"sad": ["i don't care", "why this always", "so done", "i don't want this"],"tired": ["exhausted","i want to sleep", "i don't want to do anything", "..."]}
        for mood,keywords in moods.items():
            if any (keyword in cmd for keyword in keywords):
                print(f"it sounds like you are {mood}.")
                self.log_mood(cmd,mood)
                return

    def log_mood(self,mood_text,mood_type):
        now=datetime.datetime.now()
        timestamp=now.strftime("%Y-%m-%d %H:%M:%S")
        entry=(f"{timestamp} {mood_type} : {mood_text}\n")
        with open("user/mood.txt","a") as file:
            file.write(entry)


    def closest_match(self, cmd):
        from difflib import get_close_matches

        all_keywords = []
        for keywords in self.command_map().values():
            all_keywords.extend(keywords)

        matches = get_close_matches(cmd, all_keywords, n=1, cutoff=0.3)

        if matches:
            matched_keyword = matches[0]
        
            for command, keywords in self.command_map().items():
                if matched_keyword in keywords:
                    print(f"Did you mean: '{matched_keyword}'?")
                    return command 

        return None
    
#future:
    def refelect_mood(self):
        pass