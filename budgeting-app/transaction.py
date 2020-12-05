# Tuo kirjastot/moduulit käyttöliittymää varten
import tkinter as tk

# Tuo kirjastot/moduulit toiminnallisuutta varten
import datetime as dt
import json as json

# Transaction-luokka mallintaa maksutapahtumia
class Transaction:

    # Luokan attribuutteja on päivämäärä, euromääräinen arvo, kuvaus maksutapahtumasta ja tapahtuman arvon laatu
    def __init__(self, dateObject, amount, description):
        self.date = dateObject
        self.amount = amount

        # Asetetaan maksutapahtumalle arvon laatua vastaava merkitys
        if amount >= 0:
            self.sign = "TULO"
        else:
            self.sign = "MENO"
        self.description = description

# RemoveButton-luokka mallintaa nappia, joka pitää sisällään myös indeksin
# Indeksin avulla nappi on sidottu maksutapahtumalistan maksutapahtumaan, joka voidaan tarvittaessa poistaa indeksin avulla
class RemoveButton:
    def __init__(self, masterWindow, i, toRemoveList):
        self.removeButton = tk.Button(masterWindow, text="X", command = lambda : self.removeTransaction(toRemoveList))
        self.index = i
        self.state = False

    # Maksutapahtuman poistossa asetetaan False indeksin kohdalle
    def removeTransaction(self, transactionList):
        if self.state == False:
            self.removeButton.configure(bg = "red")
            transactionList[self.index] = True
            self.state = not self.state
        elif self.state == True:
            self.removeButton.configure(bg = "SystemButtonFace")
            transactionList[self.index] = False
            self.state = not self.state
        else:
            print("Remove error")

# --- Maksutapahtuman lisäystoiminta --- #

def addTransaction(root, userObject):
    
    def addTransactionEventWindow(root, transactionList):
        window = tk.Toplevel(root)
        window.title("Lisää maksutapahtuma")
        
        dateLabel = tk.Label(window, text="Päivämäärä [dd.mm.yyyy]:")
        dateEntry = tk.Entry(window)

        amountLabel = tk.Label(window, text="Määrä  [xxx.xx]:")
        amountEntry = tk.Entry(window)

        descriptionLabel = tk.Label(window, text="Kuvaus [Vapaaehtoinen]:")
        descriptionEntry = tk.Entry(window)

        addButton = tk.Button(window, text="Lisää transaktio", command = lambda : createTransaction(dateEntry, amountEntry, dateEntry.get(), amountEntry.get(), descriptionEntry.get(), transactionList, window))
        exitButton = tk.Button(window, text="Poistu", command = window.destroy)

        dateLabel.grid(row=0, column=0)
        dateEntry.grid(row=0, column=1)
        amountLabel.grid(row=1, column=0)
        amountEntry.grid(row=1, column=1)
        descriptionLabel.grid(row=2, column=0)
        descriptionEntry.grid(row=2, column=1)

        addButton.grid(row=3, column=0)
        exitButton.grid(row=3, column=1)

        return window

    # Luo maksutapahtuma Transaction-oliona
    def createTransaction(dateEntry, amountEntry, date, amount, description, transactionList, eventWindow):
        error = False
        try:
            amount = float(amount)
            amountEntry.configure(bg="SystemWindow")
        except ValueError:
            amountEntry.configure(bg="salmon")
            eventWindow.bell()
            error = True

        try:
            separatedDate = date.split(".")
            dateObject = dt.datetime(int(separatedDate[2]), int(separatedDate[1]), int(separatedDate[0]))
            dateEntry.configure(bg="SystemWindow")
        except IndexError:
            dateEntry.configure(bg="salmon")
            eventWindow.bell()
            error = True

        if error:
            return None
        else:
            pass

        transactionObject = Transaction(dateObject, amount, description)

        transactionList.append(transactionObject)

        eventWindow.destroy()

    eventWindow = addTransactionEventWindow(root, userObject.transactionList)
    eventWindow.wait_window(eventWindow)
    print("Tapahtuma lisätty!")
    
# --- Maksutapahtumien poistotoiminta --- #

# Luo ikkuna maksutapahtumien poistoa varten
def removeTransactionEventWindow(root, userData):

    # Täytä ikkuna maksutapahtumilla poistoa varten
    def populateRemoveWindow(root, userData, incomeFrame, expensesFrame):
        changedList = userData.transactionList.copy()
        toRemoveList = [False for i in range(len(changedList))]

        incomeListIndex = 1
        expensesListIndex = 1
        for transactionIndex, transaction in enumerate(userData.transactionList):
            if transaction.sign == "TULO":
                removeTransactionButton = RemoveButton(incomeFrame, transactionIndex, toRemoveList)
                printTransactionsToWindow(incomeFrame, transaction, incomeListIndex, removeTransactionButton)
                incomeListIndex +=1
            else:
                removeTransactionButton = RemoveButton(expensesFrame, transactionIndex, toRemoveList)
                printTransactionsToWindow(expensesFrame, transaction, expensesListIndex, removeTransactionButton)
                expensesListIndex +=1

        saveButton = tk.Button(root, text="Tallenna muutokset", command = lambda : returnRemovedTransactionList(root, changedList, toRemoveList, userData))
        saveButton.grid(column=0, row=1, sticky="nw")

    # Poistotapahtuman tallennus päälistaan
    def returnRemovedTransactionList(root, changedList, toRemoveList, userData):
        for index, state in enumerate(toRemoveList):
            if state == True:
                changedList[index] = False
        
        # Karsi kaikki False-arvot eli poistetut maksutapahtumat listasta
        parsedList = list(filter(None, changedList))
        # Tallenna karsittu lista päälistaksi
        userData.transactionList = parsedList
        root.destroy()

    # Tulosta poistotapahtumaikkunalle maksutapahtumat sekä niitä vastaava poistonappi
    def printTransactionsToWindow(masterWindow, transaction, listIndex, removeButton):
        dateText = transaction.date.strftime("%d.%m.%Y")
        recentItem = tk.Label(masterWindow, text=dateText)
        recentItem.grid(column=0, row=listIndex)

        amountText = transaction.amount, "€"
        recentItem = tk.Label(masterWindow, text=amountText)
        recentItem.grid(column=1, row=listIndex)

        recentItem = tk.Label(masterWindow, text=transaction.description)
        recentItem.grid(column=2, row=listIndex)

        removeButton.removeButton.grid(column=3, row=listIndex)
        
    window = tk.Toplevel(root)
    window.title("Poista maksutapahtumia")

    incomeFrame = tk.Frame(window, borderwidth=2, relief="sunken", width=50, height=200)
    expensesFrame = tk.Frame(window, borderwidth=2, relief="sunken", width=50, height=200)
    incomeFrame.grid(column=1, row=1, sticky="nsew")
    expensesFrame.grid(column=2, row=1, sticky="nsew")

    incomeLabel = tk.Label(window, text="Tulot")
    expensesLabel = tk.Label(window, text="Menot")
    incomeLabel.grid(column=1, row=0)
    expensesLabel.grid(column=2, row=0)

    window.columnconfigure(1, weight=1)
    window.columnconfigure(2, weight=1)
    window.rowconfigure(1, weight=1)

    populateRemoveWindow(window, userData, incomeFrame, expensesFrame)

    return window

# --- Ohjelman tallennus tiedostoon ja tuonti tiedostosta --- #

# Ohjelman tietojen vienti json-tiedostoksi
def exportTransactions(userData):
    exportDict = {"name": userData.userName.get(), "age": userData.userAge.get(), "transactions": []}
    with open("transactionData.json","w") as transactionFile:
        for i in userData.transactionList:
            stringDate = i.date.strftime("%d.%m.%Y")
            data = {"date": stringDate, "amount": i.amount, "sign": i.sign, "description": i.description}
            exportDict["transactions"].append(data)

        json.dump(exportDict, transactionFile)

# json-tiedoston tuonti ohjelman tietoihin
def importTransactions(userData):
    transactionsList = []
    with open("transactionData.json","r") as transactionFile:
        jsonFile = json.load(transactionFile)
        userData.userName.set(jsonFile["name"])
        userData.userAge.set(jsonFile["age"])
        for transaction in jsonFile["transactions"]:
            transactionObject = Transaction(transaction["date"], transaction["amount"], transaction["description"])
            transactionsList.append(transactionObject)

    return transactionsList