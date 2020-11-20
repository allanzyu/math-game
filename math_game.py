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

class GameGui:
    def __init__(self):
        self.__solution = 0 # Initialize solution to problem
        self.__userInput = 0   # Initialize user input for answer

####### Create root window widget
        self.root = tk.Tk()
        self.root.title('Math Game!')

####### Create frames
        self.btn_math_questions = tk.Frame(self.root)
        self.main_frame = tk.Frame(self.root)
        self.file_io = tk.Frame(self.root)

####### Initialize user answer entry field
        # Event handler - wipe entry field when clicked on
        def clear_label(event):
            self.ent_answer.delete(0, tk.END)
        # Event handler - assign user input to __answer
        def get_answer(event):
            self.__userInput = self.ent_answer.get()
            self.ent_answer.delete(0, tk.END)
        # initialize entry widget
        self.ent_answer = tk.Entry(self.main_frame)
        self.ent_answer.insert(0,'Enter answer here')
        # set up events to clear widget and get user input
        self.ent_answer.bind("<Button-1>", clear_label)
        self.ent_answer.bind("<Return>", get_answer)
        # place entry widget within main_frame
        self.ent_answer.grid(row = 1, column = 0, sticky = 'w')

####### Initialize label widget, main method to communicate with user
        self.lbl_string = tk.StringVar()
        self.lbl_string.set('Welcome to Math Game!')
        self.lbl_out = tk.Label(self.main_frame, textvariable = self.lbl_string)
        self.lbl_out.grid(row = 0, column = 0, sticky = 'w')

####### Set up buttons that generate math questions
        self.btn_addition = tk.Button(self.btn_math_questions, text = '+',command = self.btn_addition)
        self.btn_subtraction = tk.Button(self.btn_math_questions, text = '-', command = self.btn_subtraction)
        self.btn_multiplication = tk.Button(self.btn_math_questions, text = 'x', command = self.btn_multiplication)
        self.btn_division = tk.Button(self.btn_math_questions, text = '/', command = self.btn_division)
        # placing and configuring buttons within frame
        self.btn_addition.grid(row = 0, column = 0,ipadx=15, ipady=5, sticky = 'nsew')
        self.btn_subtraction.grid(row = 0, column = 1,ipadx=15, ipady=5, sticky = 'nsew')
        self.btn_multiplication.grid(row = 0, column = 2,ipadx=15, ipady=5, sticky = 'nsew')
        self.btn_division.grid(row = 0, column = 3,ipadx=15, ipady=5, sticky = 'nsew')

####### placing the frames
        self.main_frame.grid(row = 0, column = 0, sticky = 'w')
        self.btn_math_questions.grid(row = 1, column = 0, sticky = 'sw')

####### Main tkinter Loop
        tk.mainloop()

### Addition question button
    def btn_addition(self):
        problem = Addition()
        self.lbl_string.set(problem.question)
        self.__solution = problem.solution

### Subtraction question button
    def btn_subtraction(self):
        problem = Subtraction()
        self.lbl_string.set(problem.question)
        self.__solution = problem.solution

### Multiplication question button
    def btn_multiplication(self):
        problem = Multiplication()
        self.lbl_string.set(problem.question)
        self.__solution = problem.solution

### Division question button
    def btn_division(self):
        problem = Division()
        self.lbl_string.set(problem.question)
        self.__solution = problem.solution
"""
# Addition question object
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
        self.__question = 'foo'
        self.__solution = 0
        self.new_prob()

    @property
    def question(self):
        return self.__question

    @question.setter
    def question(self,question):
        self.__question = question

    @property
    def solution(self):
        return self.__solution

    @solution.setter
    def solution(self, solution):
        self.__solution = solution

    def new_prob(self):
        A = random.randint(1,10)
        B = random.randint(1,10)
        self.question = (str(A)+" + "+str(B)+" = ?") #generates string version of problem
        self.solution = A + B #generates correct answer

# Subtraction question object is a subclass of Addition
# Generates a random subtraction problem with int solution > 0
class Subtraction(Addition):
    def new_prob(self):
        A = random.randint(1,10)
        B = random.randint(1,10)
        C = A + B
        self.question = (str(C)+" - "+str(A)+" = ?") #generates string version of problem
        self.solution = B #generates correct answer

# Multiplication question object is a subclass of Addition
# Generates a random multiplication problem with int product > 0
class Multiplication(Addition):
    def new_prob(self):
        A = random.randint(1,10)
        B = random.randint(1,10)
        self.question = (str(A)+" x "+str(B)+" = ?") #generates string version of problem
        self.solution = A*B #generates correct answer

# Division question object is a subclass of Addition
# Generates a random division problem with 
class Division(Addition):
    def new_prob(self):
        A = random.randint(1,10)
        B = random.randint(1,10)
        C = A*B
        self.question = (str(C)+" / "+str(A)+" = ?") #generates string version of problem
        self.solution = B #generates correct answer

test = GameGui()