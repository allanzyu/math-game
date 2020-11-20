# tkinter experiments

import tkinter as tk

class TestGui:
    def __init__(self):
        self.root = tk.Tk()

        tk.mainloop()

class TestObj:
    def __init__(self):
        self.question = 'foo?'
        print(self.question)
        test_method()

    def test_method(self):
        print('bar!')

class TestObj2:
    def __init__(self):
        question = TestObj()
        self.__answer = "bar"
        print(question.question)

test = TestObj()