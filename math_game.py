# -*- coding: utf-8 -*-
"""
Created on Tue Nov 17 20:43:53 2020

@author: Allan

Midterm - Math Game

Contains
    GameGui:        Primary class that will be used to launch game.
                    Launches game window when instance is created.
    Base:           Superclass that contains getters and setters for
                    math problem subclasses.
    Addition:       Subclass of Base, addition problems
    Subtraction:    Subclass of Base, subtraction problems
    Multiplication: Subclass of Base, multiplication problems
    Divison:        Subclass of Base, division problems
    Player:         Class that contains player attributes
"""

import tkinter as tk
import tkinter.messagebox
import random
import pickle

class GameGui:
    def __init__(self):
        self.__solution = 0 # Initialize solution to problem
        self.__userInput = 0   # Initialize user input for answer
        self.__entryFlag = 0    # Initialize behavior of entry widget. \
                                # 0 = profile/name set
                                # 1 = math questions
                                # 2 = load profile
                                # 3 = unexpected inputs
                                # 4 = new player creation
        self.__player = Player()
        self.__playerDictionary = {}

        self.load_file() #load players.dat on startup

####### Create root window widget
        self.root = tk.Tk()
        self.root.title('Math Game!')

####### Create frames
        self.btn_math_questions = tk.Frame(self.root)
        self.main_frame = tk.Frame(self.root)
        self.file_io = tk.Frame(self.root)

####### Initialize label widget, main method to communicate with user
        self.lbl_string = tk.StringVar()
        self.lbl_string.set('Welcome to Math Game! Please enter your name.')
        self.lbl_out = tk.Label(self.main_frame, textvariable = self.lbl_string)
        self.lbl_out.grid(row = 0, column = 0, sticky = 'w')
        self.lbl_scoreBoard = tk.StringVar()
        self.lbl_scoreOut = tk.Label(self.main_frame, textvariable = self.lbl_scoreBoard)
        self.lbl_scoreOut.grid(row = 2, column = 0, sticky = 'w')

####### Initialize user answer entry field
        # Event handler - wipe entry field when clicked on
        def clear_label(event):
            self.ent_answer.delete(0, tk.END)
        # Event handler - assign user input to __answer. Behavior changes due to the following flags:
        # 0 = profile/name set
        # 1 = math questions
        # 2 = load profile
        # 3 = unexpected inputs
        # 4 = new player creation
        def get_answer(event):
            self.__userInput = str(self.ent_answer.get()) # get input
            self.ent_answer.delete(0, tk.END) # clear input widget

            if self.__entryFlag == 0:
                if self.__userInput in self.__playerDictionary:
                    self.__player = self.__playerDictionary[self.__userInput]
                else:
                    self.__player = Player(self.__userInput)
                    self.__playerDictionary[self.__player.name] = self.__player                 
                self.lbl_string.set('Welcome, ' + self.__player.name + '. Select a math problem below.')
                self.lbl_scoreBoard.set('user: '+ self.__player.name + '     score: ' + str(self.__player.score))
                self.enable_buttons()
                self.__entryFlag = 3

            # This if statement handles user inputs to math questions
            elif self.__entryFlag == 1:
                if (self.is_true(self.__userInput)):
                    self.lbl_string.set('Correct!')
                    self.__player.correct()
                    self.lbl_scoreBoard.set('user: '+ self.__player.name + '     score: ' + str(self.__player.score))
                    self.enable_buttons()
                    self.__entryFlag = 3
                else:
                    self.lbl_string.set('Wrong!')
                    self.__player.wrong()
                    self.lbl_scoreBoard.set('user: '+ self.__player.name + '     score: ' + str(self.__player.score))
                    self.enable_buttons()
                    self.__entryFlag = 3

            # This if statement handles loading profiles, loads if profile exists
            elif self.__entryFlag == 2:
                if self.__userInput in self.__playerDictionary:
                    self.__player = self.__playerDictionary[self.__userInput]
                    self.lbl_string.set('Welcome, ' + self.__player.name)
                    self.lbl_scoreBoard.set('user: '+ self.__player.name + '     score: ' + str(self.__player.score))
                    self.enable_buttons()
                else:
                    self.lbl_string.set('Profile not found')
                    self.enable_buttons()

            # This if statement handles all cases when input is not expected
            elif self.__entryFlag == 3:
                self.lbl_string.set('Input not expected, please select an option') #TODO: disable entry widget

            # This if statement handles new player creation, only creates new if player doesn't already exist
            elif self.__entryFlag == 4:
                if self.__userInput in self.__playerDictionary:
                    self.lbl_string.set('Player already exists')
                    self.__entryFlag = 3
                    self.enable_buttons()
                else:
                    self.__player = Player(self.__userInput)    
                    self.__playerDictionary[self.__userInput] = self.__player  
                    self.lbl_string.set('Welcome, ' + self.__player.name + '. Select a math problem below.')
                    self.lbl_scoreBoard.set('user: '+ self.__player.name + '     score: ' + str(self.__player.score))
                    self.enable_buttons()
                    self.__entryFlag = 3

        # initialize entry widget
        self.ent_answer = tk.Entry(self.main_frame)
        self.ent_answer.insert(0,'Enter answer here')
        # set up events to clear widget and get user input
        self.ent_answer.bind("<Button-1>", clear_label)
        self.ent_answer.bind("<Return>", get_answer)
        # place entry widget within main_frame
        self.ent_answer.grid(row = 1, column = 0, sticky = 'w')

####### Set up buttons that generate math questions
        self.btn_addition = tk.Button(self.btn_math_questions, text = 'Addition',command = self.btn_addition)
        self.btn_subtraction = tk.Button(self.btn_math_questions, text = 'Subtraction', command = self.btn_subtraction)
        self.btn_multiplication = tk.Button(self.btn_math_questions, text = 'Multiplication', command = self.btn_multiplication)
        self.btn_division = tk.Button(self.btn_math_questions, text = 'Division', command = self.btn_division)
        # placing and configuring buttons within frame
        self.btn_addition.grid(row = 0, column = 0,ipadx=25, ipady=5, sticky = 'nsew')
        self.btn_subtraction.grid(row = 0, column = 1,ipadx=25, ipady=5, sticky = 'nsew')
        self.btn_multiplication.grid(row = 0, column = 2,ipadx=25, ipady=5, sticky = 'nsew')
        self.btn_division.grid(row = 0, column = 3,ipadx=25, ipady=5, sticky = 'nsew')

####### Set up buttons for file management (load, save, see all, quit)
        self.btn_new = tk.Button(self.file_io, text = 'New Player', width = 10, command = self.btn_new)
        self.btn_load = tk.Button(self.file_io, text = 'Load Profile', width = 10, command = self.btn_load)
        self.btn_write = tk.Button(self.file_io, text = 'Save Game', width = 10, command = self.btn_write)
        self.btn_all = tk.Button(self.file_io, text = 'See All', width = 10, command = self.btn_all)
        self.btn_quit = tk.Button(self.file_io, text = 'Quit', width = 10, command = self.btn_quit)
        # place buttons within file_io frame
        self.btn_new.pack(ipadx = 20)
        self.btn_load.pack(ipadx = 20)
        self.btn_write.pack(ipadx = 20)
        self.btn_all.pack(ipadx = 20)
        self.btn_quit.pack(ipadx = 20)

####### Placing the frames
        self.main_frame.grid(row = 0, column = 0, padx = 20, pady = 20 ,sticky = 'w')
        self.btn_math_questions.grid(row = 1, column = 0, sticky = 'sw')
        self.file_io.grid(row = 0, column = 1,sticky = 'e')

####### Main tkinter Loop
        self.disable_buttons() # start with all buttons disabled
        tk.mainloop()

### disable/enable all buttons
    def disable_buttons(self):
        self.btn_addition['state'] = 'disabled'
        self.btn_subtraction['state'] = 'disabled'
        self.btn_multiplication['state'] = 'disabled'
        self.btn_division['state'] = 'disabled'
        self.btn_new['state'] = 'disabled'
        self.btn_load['state'] = 'disabled'
        self.btn_write['state'] = 'disabled'
        self.btn_all['state'] = 'disabled'

    def enable_buttons(self):
        self.btn_addition['state'] = 'normal'
        self.btn_subtraction['state'] = 'normal'
        self.btn_multiplication['state'] = 'normal'
        self.btn_division['state'] = 'normal'
        self.btn_new['state'] = 'normal'
        self.btn_load['state'] = 'normal'
        self.btn_write['state'] = 'normal'
        self.btn_all['state'] = 'normal'

### New Player button
    def btn_new(self):
        self.lbl_string.set("What is your name?")
        self.__entryFlag = 4
        self.disable_buttons()

### Read Save button
    def btn_load(self):
        self.lbl_string.set("What is your name?")
        self.__entryFlag = 2
        self.disable_buttons()

### Write Save button
    def btn_write(self):
        # Save profile in dictionary and pickle
        del self.__playerDictionary[self.__player.name]
        self.__playerDictionary[self.__player.name] = self.__player  
        output_file = open('players.dat','wb')
        pickle.dump(self.__playerDictionary, output_file)
        output_file.close()
        self.lbl_string.set("Profile saved")

### See All users
    def btn_all(self):
        outString = ''
        for entry in self.__playerDictionary:
            profile = self.__playerDictionary[entry]
            if profile.total > 0:
                rawPercentScore = 100*profile.score/profile.total
                percentScore = '{:.2f}'.format(rawPercentScore)
            else:
                percentScore = "N/A"
            outString = outString + "Name: " + profile.name + \
                        "    Score: " + str(profile.score) + \
                        "    Percent Correct: " + percentScore + '%\n'
        tkinter.messagebox.showinfo('All Players',outString)
        
### Quit
    def btn_quit(self):
        self.__playerDictionary[self.__player.name] = self.__player  
        output_file = open('players.dat','wb')
        pickle.dump(self.__playerDictionary, output_file)
        output_file.close()
        self.root.destroy()

### Addition question button
    def btn_addition(self):
        problem = Addition()
        self.lbl_string.set(problem.question)
        self.__solution = problem.solution
        self.disable_buttons()
        self.__entryFlag = 1

### Subtraction question button
    def btn_subtraction(self):
        problem = Subtraction()
        self.lbl_string.set(problem.question)
        self.__solution = problem.solution
        self.disable_buttons()
        self.__entryFlag = 1

### Multiplication question button
    def btn_multiplication(self):
        problem = Multiplication()
        self.lbl_string.set(problem.question)
        self.__solution = problem.solution
        self.disable_buttons()
        self.__entryFlag = 1

### Division question button
    def btn_division(self):
        problem = Division()
        self.lbl_string.set(problem.question)
        self.__solution = problem.solution
        self.disable_buttons()
        self.__entryFlag = 1

### Check if user input matches solution
    def is_true(self,userInput):
        errorFlag = True
        while (errorFlag):
            try:
                if str(userInput) == str(self.__solution):
                    return True
                else:
                    return False
            except:
                self.lbl_string.set("something went wrong")

### load players.dat, creates .dat if it doesn't exist
    def load_file(self, file = 'players.dat'):
        try:
            inputFile = open(file,'rb')
            self.__playerDictionary = pickle.load(inputFile)
            inputFile.close()
        except:
            outputFile = open(file,'wb')
            pickle.dump(self.__playerDictionary, outputFile)
            outputFile.close()


# Base class contains setters and getters for 
# subclass math problems.
class Base:
    def __init__(self):
        self._question = 'foo'
        self._solution = 0
        self.new_prob()

    @property
    def question(self):
        return self._question

    @question.setter
    def question(self,question):
        self._question = question

    @property
    def solution(self):
        return self._solution

    @solution.setter
    def solution(self, solution):
        self._solution = solution

# Addition is a subclass of Base
# Generates a random subtraction problem with int solution > 0
class Addition(Base):
    def new_prob(self):
        A = random.randint(1,10)
        B = random.randint(1,10)
        self._question = (str(A)+" + "+str(B)+" = ?") #generates string version of problem
        self._solution = A + B #generates correct answer

# Subtraction is a subclass of Base
# Generates a random subtraction problem with int solution > 0
class Subtraction(Base):
    def __init__(self):
        self.new_prob()
    def new_prob(self):
        A = random.randint(1,10)
        B = random.randint(1,10)
        C = A + B
        self._question = (str(C)+" - "+str(A)+" = ?") #generates string version of problem
        self._solution = B #generates correct answer

# Multiplication is a subclass of Base
# Generates a random multiplication problem with int product > 0
class Multiplication(Base):
    def new_prob(self):
        A = random.randint(1,10)
        B = random.randint(1,10)
        self._question = (str(A)+" x "+str(B)+" = ?") #generates string version of problem
        self._solution = A*B #generates correct answer

# Division is a subclass of Base
# Generates a random division problem with int solution > 0
class Division(Base):
    def new_prob(self):
        A = random.randint(1,10)
        B = random.randint(1,10)
        C = A*B
        self._question = (str(C)+" / "+str(A)+" = ?") #generates string version of problem
        self._solution = B #generates correct answer

# Player class has 3 attributes:
#   score, name, total
# 2 methods:
#   correct, wrong
class Player:
    def __init__(self,name='-'):
        self.__score = 0 # number of correct
        self.__totalQuestions = 0 # total number of questions attempted
        self.__name = name # player name

    @property
    def score(self):
        return self.__score

    @score.setter
    def score(self,score):
        self.__score = score

    @property
    def name(self):
        return self.__name

    @name.setter
    def name(self,name):
        self.__name = name

    @property
    def total(self):
        return self.__totalQuestions

    @total.setter
    def total(self,total):
        self.__total = total

    def correct(self):
        self.__score += 1
        self.__totalQuestions += 1

    def wrong(self):
        self.__totalQuestions += 1


test = GameGui()