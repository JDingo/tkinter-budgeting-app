import tkinter as tk

import gui as gui

class User:
    def __init__(self):
        # Muuttujat käyttäjän tiedoille
        self.userName = tk.StringVar()
        self.userAge = tk.StringVar()
        self.userName.set("")
        self.userAge.set("")

        # Muuttujat tuloille ja maksutapahtumien säilyttämiselle
        self.guiIncome = tk.StringVar()
        self.guiExpenses = tk.StringVar()
        totalIncome = 0
        totalExpenses = 0
        incomeString = totalIncome, "€"
        expensesString = totalExpenses, "€"
        self.guiIncome.set(incomeString)
        self.guiExpenses.set(expensesString)

        balanceString = totalIncome + totalExpenses, "€"
        self.balance = tk.StringVar()
        self.balance.set(balanceString)
        self.transactionList = []

userObject = User()
gui = gui.GUI(userObject)
gui.root.minsize(500, 300)
gui.root.mainloop()