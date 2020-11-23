# -*- coding: utf-8 -*-
"""
Created on Tue Nov 17 20:43:53 2020

@author: Allan

Midterm - Math Game

Contains
    GameGui:    Primary class that will be used to launch game.
                Launches game window when instance is created.           
    Addition:       Main math problem class for addition problems
    Subtraction:    Subclass of Addition, subtraction problems
    Multiplication: Subclass of Addition, multiplication problems
    Divison:        Subclass of Addition, division problems
"""

import tkinter as tk
import random
import pickle

class GameGui:
    def __init__(self):
        self.__solution = 0 # Initialize solution to problem
        self.__userInput = 0   # Initialize user input for answer
        self.__entryFlag = 0 # Initialize behavior of entry widget. \
                             # 0 = profile/name set\
                             # 1 = math questions\
                             # 2 = prompt user to choose an option
        self.__player = Player()
        self.__playerDictionary = {}

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
        self.lbl_scoreBoard.set('user: '+ self.__player.name + ' score: ' + str(self.__player.score))
        self.lbl_scoreOut = tk.Label(self.main_frame, textvariable = self.lbl_scoreBoard)
        self.lbl_scoreOut.grid(row = 2, column = 0, sticky = 'w')

####### Initialize user answer entry field
        # Event handler - wipe entry field when clicked on
        def clear_label(event):
            self.ent_answer.delete(0, tk.END)
        # Event handler - assign user input to __answer. Behavior changes due to the following flags:
        # 0 = profile/name set\
        # 1 = math questions\
        # 3 = unexpected inputs
        def get_answer(event):
            self.__userInput = self.ent_answer.get()
            self.ent_answer.delete(0, tk.END)

            if self.__entryFlag == 0:
                self.__player.name = self.__userInput
                """
                try to load pickled profile
                """
                self.lbl_string.set('Welcome, ' + self.__player.name)
                self.enable_buttons()
                self.__entryFlag = 3

            # This if statement handles user inputs to math questions
            elif self.__entryFlag == 1:
                if (self.is_true(self.__userInput)):
                    self.lbl_string.set('Correct!')
                    self.__player.correct()
                    self.enable_buttons()
                    self.__entryFlag = 3
                else:
                    self.lbl_string.set('Wrong!')
                    self.__player.wrong()
                    self.enable_buttons()
                    self.__entryFlag = 3

            elif self.__entryFlag == 2:
                self.__player = Player(self.__userInput)
                """
                try to load pickled profile
                """

            elif self.__entryFlag == 3:
                self.lbl_string.set('Input not expected, please select an option') #TODO: disable entry widget

        # initialize entry widget
        self.ent_answer = tk.Entry(self.main_frame)
        self.ent_answer.insert(0,'Enter answer here')
        # set up events to clear widget and get user input
        self.ent_answer.bind("<Button-1>", clear_label)
        self.ent_answer.bind("<Return>", get_answer)
        # place entry widget within main_frame
        self.ent_answer.grid(row = 1, column = 0, sticky = 'w')

####### Set up buttons that generate math questions
        self.btn_addition = tk.Button(self.btn_math_questions, text = '+',command = self.btn_addition)
        self.btn_subtraction = tk.Button(self.btn_math_questions, text = '-', command = self.btn_subtraction)
        self.btn_multiplication = tk.Button(self.btn_math_questions, text = 'x', command = self.btn_multiplication)
        self.btn_division = tk.Button(self.btn_math_questions, text = '/', command = self.btn_division)
        # placing and configuring buttons within frame
        self.btn_addition.grid(row = 0, column = 0,ipadx=25, ipady=5, sticky = 'nsew')
        self.btn_subtraction.grid(row = 0, column = 1,ipadx=25, ipady=5, sticky = 'nsew')
        self.btn_multiplication.grid(row = 0, column = 2,ipadx=25, ipady=5, sticky = 'nsew')
        self.btn_division.grid(row = 0, column = 3,ipadx=25, ipady=5, sticky = 'nsew')

####### Set up buttons for file management (load, save, see all, quit)
        self.btn_read = tk.Button(self.file_io, text = 'Read Saved', width = 10, command = self.btn_read)
        self.btn_write = tk.Button(self.file_io, text = 'Save Game', width = 10, command = self.btn_write)
        self.btn_all = tk.Button(self.file_io, text = 'See All', width = 10)
        self.btn_quit = tk.Button(self.file_io, text = 'Quit', width = 10, command = self.btn_quit)
        # place buttons within file_io frame
        self.btn_read.pack(ipadx = 20)
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
        self.btn_read['state'] = 'disabled'
        self.btn_write['state'] = 'disabled'
        self.btn_all['state'] = 'disabled'

    def enable_buttons(self):
        self.btn_addition['state'] = 'normal'
        self.btn_subtraction['state'] = 'normal'
        self.btn_multiplication['state'] = 'normal'
        self.btn_division['state'] = 'normal'
        self.btn_read['state'] = 'normal'
        self.btn_write['state'] = 'normal'
        self.btn_all['state'] = 'normal'

### Read Save button
    def btn_read(self):
        self.lbl_string.set("What is your name?")
        self.disable_buttons()

### Write Save button
    def btn_write(self):
        # Save profile in dictionary and pickle
        self.__playerDictionary = {self.__player.name,self.__player}
        output_file = open('players.dat','wb')
        pickle.dump(self.__playerDictionary, output_file)
        output_file.close()
        self.lbl_string.set("Profile saved")

### Quit
    def btn_quit(self):
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

"""
Addition Question Class
   Generates a random addition problem of 2 int addends
   between 1 and 10 when instantiated
 2 Attributes:
   __question
   __solution
 1 Method:
   new_prob
"""
class Addition:
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

    def new_prob(self):
        A = random.randint(1,10)
        B = random.randint(1,10)
        self._question = (str(A)+" + "+str(B)+" = ?") #generates string version of problem
        self._solution = A + B #generates correct answer

# Subtraction question object is a subclass of Addition
# Generates a random subtraction problem with int solution > 0
class Subtraction(Addition):
    def __init__(self):
        self.new_prob()
    def new_prob(self):
        A = random.randint(1,10)
        B = random.randint(1,10)
        C = A + B
        self._question = (str(C)+" - "+str(A)+" = ?") #generates string version of problem
        self._solution = B #generates correct answer

# Multiplication question object is a subclass of Addition
# Generates a random multiplication problem with int product > 0
class Multiplication(Addition):
    def new_prob(self):
        A = random.randint(1,10)
        B = random.randint(1,10)
        self._question = (str(A)+" x "+str(B)+" = ?") #generates string version of problem
        self._solution = A*B #generates correct answer

# Division question object is a subclass of Addition
# Generates a random division problem with 
class Division(Addition):
    def new_prob(self):
        A = random.randint(1,10)
        B = random.randint(1,10)
        C = A*B
        self._question = (str(C)+" / "+str(A)+" = ?") #generates string version of problem
        self._solution = B #generates correct answer

class Player:
    def __init__(self,name='-'):
        self.__score = 0 # number of correct
        self.__totalQuestions = 0 # total number of questions attempted
        self.__name = name

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
        return self.__total

    @total.setter
    def total(self,total):
        self.__total = total

    def correct(self):
        self.__score += 1
        self.__totalQuestions += 1

    def wrong(self):
        self.__totalQuestions += 1


test = GameGui()