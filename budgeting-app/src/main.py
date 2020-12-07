# Tuo kirjastot/moduulit käyttöliittymää varten
import tkinter as tk
import gui as gui

class User:
    def __init__(self):
        # Muuttujat käyttäjän tiedoille
        self.userName = tk.StringVar()
        self.userAge = tk.StringVar()
        self.userName.set("")
        self.userAge.set("")

        # Muuttujat tuloille ja menoille
        self.guiIncome = tk.StringVar()
        self.guiExpenses = tk.StringVar()
        self.monthlyIncome = tk.StringVar()
        self.monthlyExpenses = tk.StringVar()

        # Luodaan numeeriset arvot ja muutetaan merkkijonoiksi StringVar()-varten
        totalIncome = 0
        totalExpenses = 0
        incomeString = totalIncome, "€"
        expensesString = totalExpenses, "€"

        self.guiIncome.set(incomeString)
        self.guiExpenses.set(expensesString)
        self.monthlyIncome.set(incomeString)
        self.monthlyExpenses.set(expensesString)

        # Muuttujat yhteenvedoille
        balanceString = totalIncome + totalExpenses, "€"
        self.balance = tk.StringVar()
        self.balance.set(balanceString)
        self.monthlyBalance = tk.StringVar()
        self.monthlyBalance.set(balanceString)
        
        # Lista maksutapahtumille
        self.transactionList = []

# Luo User-olio ja liitä se käyttöliittymään
userObject = User()
gui = gui.GUI(userObject)
gui.root.minsize(500, 320)

# Käynnistä TkInter-mainloop
# mainloop tarkastelee käyttäjän syötettä ja päivittää käyttöliittymää tarvittaessa
gui.root.mainloop()