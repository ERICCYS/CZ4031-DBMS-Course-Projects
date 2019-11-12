import sys
import tkinter as tk
from tkinter import *
from tkinter import messagebox
from pyconnect import DBConnection


class App(object):

    def __init__(self, parent):
        self.root = parent
        self.root.title("Main Frame")
        self.frm_Query = tk.Frame(self.root, width=800, height=150)
        self.frm_Query.pack(side=TOP)
        self.frm_Out = tk.Frame(self.root, width=800, height=150)
        self.frm_Out.pack()
        self.button = tk.Frame(self.root, width=800, height=150)
        self.button.pack(side=BOTTOM)

        self.frm_Q1 = tk.Frame(self.frm_Query, width=100, height=150)
        self.frm_Q1.pack(side=LEFT)
        self.frm_Q2 = tk.Frame(self.frm_Query, width=100, height=150)
        self.frm_Q2.pack(side=RIGHT)

        self.frm_Q3 = tk.Frame(self.frm_Out, width=100, height=150)
        self.frm_Q3.pack(side=LEFT)
        self.frm_oo = tk.Frame(self.frm_Out, width=100, height=150)
        self.frm_oo.pack(side=RIGHT)

        input1 = tk.Label(self.frm_Q1, text='please input your old query:', font=(None, 18))
        input1.pack(side=TOP)
        input2 = tk.Label(self.frm_Q2, text='please input your new query:', font=(None, 18))
        input2.pack(side=TOP)

        self.Q1 = tk.Text(self.frm_Q1, relief=GROOVE, width=30, height=15, borderwidth=5, font=(None, 18))
        self.Q1.pack(side=BOTTOM)
        self.Q2 = tk.Text(self.frm_Q2, relief=RIDGE, width=30, height=15, borderwidth=5, font=(None, 18))
        self.Q2.pack(side=BOTTOM)

        input3 = tk.Label(self.frm_Q3, text='please input your description:', font=(None, 18))
        input3.pack(side=TOP)
        self.Q3 = tk.Text(self.frm_Q3, relief=GROOVE, width=30, height=5, borderwidth=5, font=(None, 18))
        self.Q3.pack()

        out = tk.Label(self.frm_oo, text='OUTPUT', font=(None, 18))
        out.pack(side=TOP)
        
        #self.ooo = tk.Label(self.frm_oo, relief=GROOVE, width=30, height=5, borderwidth=5, font=(None, 18))
        #self.ooo.pack(side = TOP)

        self.output = tk.Text(self.frm_oo, relief=GROOVE, width=30, height=5, borderwidth=5, font=(None, 18))
        self.output.pack(side = BOTTOM)

        view = tk.Button(self.button, text="view output", width=10, height=4, command=self.retrieve_input)
        view.pack(side=LEFT, padx=50,pady=5)

        clear = tk.Button(self.button, text="clear input", width=10, height=4, command=self.clear_input)
        clear.pack(side=LEFT, padx=50,pady=5)

        quit_ = tk.Button(self.button, text="cancel", width=10, height=4, command=self.quitprogram)
        quit_.pack(side=RIGHT, padx=50,pady=5)

    def retrieve_input(self):
        global query_old
        global query_new
        global desc
        global result
        query_old = self.Q1.get("1.0", END)
        query_new = self.Q2.get("1.0", END)
        desc = self.Q3.get("1.0", END)
        result = self.get_output(query_old, query_new, desc)
        self.output.delete("1.0", END)   #Clear the text window so we can write.
        self.output.insert(END,result)

    def clear_input(self):
        self.Q1.delete("1.0", END)
        self.Q2.delete("1.0", END)
        self.Q3.delete("1.0", END) 

    def get_output(self, query_old, query_new, desc):
        connection = DBConnection()
        result_old = connection.execute(query_old)
        result_new = connection.execute(query_new)
        connection.close()
        # TODO: use the vocalizer algo to produce result
        return (str(result_old) + "\n" + str(result_new) + "\n" + desc)

    def quitprogram(self):
        result = messagebox.askokcancel("Quit the game.", "Are you sure?", icon='warning')
        if result == True:
            self.root.destroy()
#			root.update()
#			root.deiconify()		


if __name__ == "__main__":
    root = tk.Tk()
    app = App(root)
    root.geometry('800x600+0+0')
    root.mainloop()
