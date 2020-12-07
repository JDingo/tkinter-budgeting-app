# Tuo kirjastot/moduulit käyttöliittymää varten
import tkinter as tk

# Tuo kirjastot/moduulit toiminnallisuutta varten
import datetime as dt
import json as json

# Transaction-luokka mallintaa maksutapahtumia
class Transaction:

    # Luokan attribuutteja on päivämäärä, euromääräinen arvo, kuvaus maksutapahtumasta
    def __init__(self, dateObject, amount, description):
        self.date = dateObject
        self.amount = amount
        self.description = description

# RemoveButton-luokka mallintaa nappia, joka pitää sisällään myös indeksin
# Indeksin avulla nappi on sidottu maksutapahtumalistan maksutapahtumaan, 
# joka voidaan tarvittaessa poistaa indeksin avulla
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

# Luo ikkuna maksutapahtuman lisäykselle
def addTransactionEventWindow(root, transactionList):
        window = tk.Toplevel(root)
        window.title("Lisää maksutapahtuma")
        
        dateLabel = tk.Label(window, text="Päivämäärä [dd.mm.yyyy]:")
        dateEntry = tk.Entry(window)
        dateEntry.insert(0, dt.datetime.now().strftime("%d.%m.%Y"))

        amountLabel = tk.Label(window, text="Määrä  [xxx.xx]:")
        amountEntry = tk.Entry(window)

        descriptionLabel = tk.Label(window, text="Kuvaus [Vapaaehtoinen]:")
        descriptionEntry = tk.Entry(window)

        addButton = tk.Button(window, text="Lisää transaktio", command = lambda : validateUserInput(dateEntry, amountEntry, dateEntry.get(), amountEntry.get(), descriptionEntry.get(), transactionList, window))
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

# Käyttäjän syötteen validointi
def validateUserInput(dateEntry, amountEntry, date, amount, description, transactionList, window):
    error = False

    # Varmista syötteen oikeellisuus
    # Värjää virheelliset syötekentät tarvittaessa
    # window.bell() soittaa äänen virheiden sattuessa
    try:
        amount = round(float(amount), 2)
        amountEntry.configure(bg="SystemWindow")
    except:
        amountEntry.configure(bg="salmon")
        window.bell()
        error = True

    try:
        separatedDate = date.split(".")
        dateObject = dt.datetime(int(separatedDate[2]), int(separatedDate[1]), int(separatedDate[0]))
        dateEntry.configure(bg="SystemWindow")
    except:
        dateEntry.configure(bg="salmon")
        window.bell()
        error = True

    if error:
        # Palauta arvo testiä varten ja poistu metodista
        return error
    else:
        transactionObject = createTransaction(dateObject, amount, description, transactionList, window)

        # Palauta olio testiä varten
        return transactionObject

# Luo maksutapahtuma Transaction-oliona
def createTransaction(dateObject, amount, description, transactionList, window):
    # Luo olio, lisää listaan ja tuhoa ikkuna, ohjelma jatkuu main-moduulissa
    transactionObject = Transaction(dateObject, amount, description)
    transactionList.append(transactionObject)
    window.destroy()

    # Palauta olio testiä vartens
    return transactionObject
    
# --- Maksutapahtumien poistotoiminta --- #

# Luo ikkuna maksutapahtumien poistoa varten
def removeTransactionEventWindow(root, userData):

    # Täytä ikkuna maksutapahtumilla poistoa varten
    def populateRemoveWindow(root, userData, incomeFrame, expensesFrame):
        # Luo kopio alkuperäisestä listasta
        # Luo merkintälista, johon merkitään poistettavat maksutapahtumat
        changedList = userData.transactionList.copy()
        toRemoveList = [False for i in range(len(changedList))]

        # Tulostukseen erilliset indeksit, 
        # jotta maksutapahtumat pysyvät järjestyksessä kahdesta eri ikkunasta huolimatta
        incomeListIndex = 0
        expensesListIndex = 0

        # Käy läpi kaikki maksutapahtumat kopiolistasta
        for transactionIndex, transaction in enumerate(changedList):
            if transaction.amount >= 0:
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
        # Jos merkintälistaan on merkattu indeksin kohdalle True,
        # aseta maksutapahtumalistaan False
        for index, state in enumerate(toRemoveList):
            if state == True:
                changedList[index] = False
        
        # Karsi kaikki False-arvot eli poistetut maksutapahtumat listasta
        parsedList = list(filter(None, changedList))

        # Tallenna käsitelty lista käyttäjän maksutapahtumalistaksi
        userData.transactionList = parsedList

        # Tuhoa ikkuna
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

    # Poistoikkunan luonti
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
    
    # Aseta tallenukseen ensiksi käyttäjän ikä
    exportDict = {"name": userData.userName.get(), "age": userData.userAge.get(), "transactions": []}
    with open("transactionData.json","w") as transactionFile:

        # Käy jokainen maksutapahtuma ja lisää ne tallennettavaksi avain-arvo-pareina
        for i in userData.transactionList:
            stringDate = i.date.strftime("%d.%m.%Y")
            data = {"date": stringDate, "amount": i.amount, "description": i.description}
            exportDict["transactions"].append(data)

        # Tallenna json.tiedosto
        json.dump(exportDict, transactionFile)

# json-tiedoston tuonti ohjelman tietoihin
def importTransactions(userData):

    # Luo tyhjä lista, joka palautetaan
    transactionsList = []

    with open("transactionData.json","r") as transactionFile:
        jsonFile = json.load(transactionFile)

        # Tallenna käyttäjälle suoraan käyttäjätiedot
        userData.userName.set(jsonFile["name"])
        userData.userAge.set(jsonFile["age"])

        # Maksutapahtumien tuonnissa ei käydä läpi tietojen oikeellisuutta
        # Oletetaan oikeiksi

        # Käy jokainen tallennettu maksutapahtuma läpi
        # Käsittele jokainen avain-arvo-pari Transaction-olioksi
        # Tallenna ne palautettavaan listaan
        for transaction in jsonFile["transactions"]:
            separatedDate = transaction["date"].split(".")
            dateObject = dt.datetime(int(separatedDate[2]), int(separatedDate[1]), int(separatedDate[0]))
            transactionObject = Transaction(dateObject, transaction["amount"], transaction["description"])
            transactionsList.append(transactionObject)

    return transactionsList