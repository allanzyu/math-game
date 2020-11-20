# -*- coding: utf-8 -*-
"""
Created on Tue Nov 17 20:43:53 2020

@author: Allan

Midterm - Math Game


"""

import tkinter as tk
import random

class GameGui:
    def __init__(self):
        self.__solution = 0 # Initialize solution to problem
        self.__answer = 0   # Initialize user input for answer

        # create root window widget
        self.root = tk.Tk()
        self.root.title('Math Game!')

        # Initialize label widget to display welcome message
        self.lbl_string = tk.StringVar()
        self.lbl_string.set('Welcome to Math Game!')
        self.lbl_out = tk.Label(self.root, textvariable = self.lbl_string)

        # Initialize buttons
        self.btn_addition = tk.Button(self.root, text = '+',command = self.btn_addition)
        self.btn_subtraction = tk.Button(self.root, text = '-', command = self.btn_subtraction)
        self.btn_multiplication = tk.Button(self.root, text = 'x', command = self.btn_multiplication)
        self.btn_division = tk.Button(self.root, text = '/', command = self.btn_division)

        ### Initialize user answer entry field ###
        # Event handler - wipe entry field when clicked on
        def clear_label(event):
            self.ent_answer.delete(0, tk.END)
        # Event handler - assign user input to __answer
        def get_answer(event):
            self.__answer = self.ent_answer.get()
            self.ent_answer.delete(0, tk.END)
        self.ent_answer = tk.Entry(self.root)
        self.ent_answer.insert(0,'Enter answer here')
        self.ent_answer.bind("<Button-1>", clear_label)
        self.ent_answer.bind("<Return>", get_answer)

        # pack dat shit
        self.lbl_out.pack()
        self.ent_answer.pack()
        self.btn_addition.pack()
        self.btn_subtraction.pack()
        self.btn_multiplication.pack()
        self.btn_division.pack()

        tk.mainloop()

    ### Addition question button
    def btn_addition(self):
        problem = Addition()
        self.lbl_string.set(problem.question)
        self.__solution = problem.solution

    def btn_subtraction(self):
        problem = Subtraction()
        self.lbl_string.set(problem.question)
        self.__solution = problem.solution

    def btn_multiplication(self):
        problem = Multiplication()
        self.lbl_string.set(problem.question)
        self.__solution = problem.solution

    def btn_division(self):
        problem = Division()
        self.lbl_string.set(problem.question)
        self.__solution = problem.solution

# Addition question object
#   Generates a random addition problem of 2 int addends
#   between 1 and 10 when instantiated
# 2 Attributes:
#   __question
#   __solution
# 1 Method:
#   new_prob
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