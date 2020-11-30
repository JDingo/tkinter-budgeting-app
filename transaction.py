# Tuo tkinter-kirjasto GUI:ta varten
from tkinter import *
from tkinter import ttk
from tkinter import messagebox
from tkinter import simpledialog
import datetime as dt
import json

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

class RemoveButton:
    def __init__(self, masterWindow, i, transactionList):
        self.removeButton = Button(masterWindow, text="X", command = lambda : self.removeTransaction(transactionList))
        self.index = i

    def removeTransaction(self, transactionList):
        del transactionList[self.index]

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

# Luo ikkuna maksutapahtumien poistoa varten
def removeTransactionEventWindow(root, systemObject):
    window = Toplevel(root)
    window.title("Poista maksutapahtumia")

    incomeFrame = ttk.Frame(window, borderwidth=2, relief="sunken", width=50, height=200)
    expensesFrame = ttk.Frame(window, borderwidth=2, relief="sunken", width=50, height=200)
    incomeFrame.grid(column=1, row=1, sticky="nsew")
    expensesFrame.grid(column=2, row=1, sticky="nsew")

    incomeLabel = ttk.Label(window, text="Tulot")
    expensesLabel = ttk.Label(window, text="Menot")
    incomeLabel.grid(column=1, row=0)
    expensesLabel.grid(column=2, row=0)

    window.columnconfigure(1, weight=1)
    window.columnconfigure(2, weight=1)
    window.rowconfigure(1, weight=1)

    exitButton = Button(window, text="Poistu", command = window.destroy)
    exitButton.grid(column=0, row=1, sticky="nw")

    populateRemoveWindow(window, systemObject, incomeFrame, expensesFrame)

    return window

# Täytä ikkuna maksutapahtumilla poistoa varten
def populateRemoveWindow(root, systemObject, incomeFrame, expensesFrame):
    print(systemObject.transactionList)

    incomeListIndex = 1
    expensesListIndex = 1
    for transactionIndex, transaction in enumerate(systemObject.transactionList):
        if transaction.sign == "TULO":
            removeTransactionButton = RemoveButton(incomeFrame, transactionIndex, systemObject.transactionList)
            printTransactionsToWindow(incomeFrame, transaction, incomeListIndex, removeTransactionButton)
            incomeListIndex +=1
        else:
            removeTransactionButton = RemoveButton(expensesFrame, transactionIndex, systemObject.transactionList)
            printTransactionsToWindow(expensesFrame, transaction, expensesListIndex, removeTransactionButton)
            expensesListIndex +=1

    # for i, transaction in enumerate(incomeList):
    #     dateText = transaction.date.strftime("%d/%m/%Y")
    #     recentItem = ttk.Label(incomeFrame, text=dateText)
    #     recentItem.grid(column=0, row=i)

    #     amountText = transaction.amount, "€"
    #     recentItem = ttk.Label(incomeFrame, text=amountText)
    #     recentItem.grid(column=1, row=i)

    #     recentItem = ttk.Label(incomeFrame, text=transaction.description)
    #     recentItem.grid(column=2, row=i)

    # for i, transaction in enumerate(expensesList):
    #     dateText = transaction.date.strftime("%d.%m.%Y")
    #     recentItem = ttk.Label(expensesFrame, text=dateText)
    #     recentItem.grid(column=0, row=i)

    #     amountText = transaction.amount, "€"
    #     recentItem = ttk.Label(expensesFrame, text=amountText)
    #     recentItem.grid(column=1, row=i)

    #     recentItem = ttk.Label(expensesFrame, text=transaction.description)
    #     recentItem.grid(column=2, row=i)

def printTransactionsToWindow(masterWindow, transaction, listIndex, removeButton):
    dateText = transaction.date.strftime("%d/%m/%Y")
    recentItem = ttk.Label(masterWindow, text=dateText)
    recentItem.grid(column=0, row=listIndex)

    amountText = transaction.amount, "€"
    recentItem = ttk.Label(masterWindow, text=amountText)
    recentItem.grid(column=1, row=listIndex)

    recentItem = ttk.Label(masterWindow, text=transaction.description)
    recentItem.grid(column=2, row=listIndex)

    removeButton.removeButton.grid(column=3, row=listIndex)
        

# Ohjelman tietojen vienti json-tiedostoksi
def exportTransactions(transactionsList, userName, userAge):
    exportDict = {"name": userName.get(), "age": userAge.get(), "transactions": []}
    with open("transactionData.json","w") as transactionFile:
        for i in transactionsList:
            stringDate = i.date.strftime("%d.%m.%Y")
            data = {"date": stringDate, "amount": i.amount, "sign": i.sign, "description": i.description}
            exportDict["transactions"].append(data)

        json.dump(exportDict, transactionFile)

# json-tiedoston tuonti ohjelman tietoihin
def importTransactions(transactionsList, userName, userAge):
    transactionsList = []
    with open("transactionData.json","r") as transactionFile:
        jsonFile = json.load(transactionFile)
        print(jsonFile)
        userName.set(jsonFile["name"])
        userAge.set(jsonFile["age"])
        for transaction in jsonFile["transactions"]:
            transactionObject = Transaction(transaction["date"], transaction["amount"], transaction["description"])
            transactionsList.append(transactionObject)

    return transactionsList