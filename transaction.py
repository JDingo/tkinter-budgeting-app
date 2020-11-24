# Tuo tkinter-kirjasto GUI:ta varten
from tkinter import *
from tkinter import ttk
from tkinter import messagebox
from tkinter import simpledialog
import datetime as dt

class Transaction:

    def __init__(self, date, amount, description):
        separatedDate = date.split(".")
        print(int(separatedDate[2]), int(separatedDate[1]), int(separatedDate[0]))

        dateObject = dt.datetime(int(separatedDate[2]), int(separatedDate[1]), int(separatedDate[0]))
        self.date = dateObject
        self.amount = amount
        if amount >= 0:
            self.sign = "TULO"
        else:
            self.sign = "MENO"
        self.description = description

# Luo transaction-objekti (maksutapahtuma) ja lisää se transactionList-listaan (maksutapahtumien lista)
def createTransaction(date, amount, description, transactionList, eventWindow):
    transactionObject = Transaction(date, int(amount), description)
    print(transactionObject, transactionObject.date, transactionObject.amount, transactionObject.description)

    transactionList.append(transactionObject)

    eventWindow.destroy()

# Luo ikkuna maksutapahtuman lisäämiseksi
def addTransactionEventWindow(root, transactionList):
    window = Toplevel(root)
    window.title("Lisää maksutapahtuma")
    
    dateLabel = Label(window, text="Päivämäärä [dd.mm.yyyy]:")
    dateEntry = Entry(window)

    amountLabel = Label(window, text="Määrä:")
    amountEntry = Entry(window)

    descriptionLabel = Label(window, text="Kuvaus:")
    descriptionEntry = Entry(window)

    addButton = Button(window, text="Lisää transaktio", command = lambda : createTransaction(dateEntry.get(), amountEntry.get(), descriptionEntry.get(), transactionList, window))
    exitButton = Button(window, text="Poistu", command = window.destroy)

    dateLabel.grid(row=0, column=0)
    dateEntry.grid(row=0, column=1)
    amountLabel.grid(row=1, column=0)
    amountEntry.grid(row=1, column=1)
    descriptionLabel.grid(row=2, column=0)
    descriptionEntry.grid(row=2, column=1)

    addButton.grid(row=3, column=0)
    exitButton.grid(row=3, column=1)

    return window

def removeTransactionEventWindow(root):
    window = Toplevel(root)
    window.title("Poista maksutapahtumia")

    incomeFrame = ttk.Frame(window, borderwidth=2, relief="sunken", width=50, height=200)
    expensesFrame = ttk.Frame(window, borderwidth=2, relief="sunken", width=50, height=200)

    incomeFrame.grid(column=1, row=1)
    expensesFrame.grid(column=2, row=1)

    exitButton = Button(window, text="Poistu", command = window.destroy)
    exitButton.grid(column=0, row=1)

    return window