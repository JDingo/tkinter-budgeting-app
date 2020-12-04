# Tuo tkinter-kirjasto GUI:ta varten
from tkinter import *
from tkinter import ttk
from tkinter import messagebox
import operator as operator

# Tuo profile-tiedosto, joka sisältää käyttäjän tietoja
import profile as profile

# Tuo transaction-tiedosto, joka sisältää maksutapahtumiin liittyvät luokat ja metodit
import transaction as transaction

# Tuo sys ohjelman sammuttamista varten
import sys
import datetime as dt

class GUI:
    # Luo popup-ikkuna, jonka jälkeen tuhoa ikkuna ja sammuta ohjelma
    def exit(self):
        messagebox.showinfo("Budjetoija", "Ohjelma sammutetaan.")
        root.destroy()
        sys.exit()

    # Päivitä maksutapahtumat käymällä lista läpi
    # Päivitä käyttöliittymästä overview- ja recent-paneelit
    def addTransaction(self):
        transaction.addTransaction(self.root, self.userData)
        print(self.userData)
        self.sortTransactions()
        self.printTransactions(self.recent)

    # Järjestä maksutapahtumat aikajärjestykseen uusimmasta vanhimpaan tulostusta varten
    def sortTransactions(self):
        self.userData.transactionList.sort(key=operator.attrgetter("date"), reverse=True)

    # Tulosta maksutapahtumat syötetylle ikkunalle masterWindow
    def printTransactions(self, masterWindow):

        # Siivoa annettu raami uudelleenpiirtoa varten
        for widget in masterWindow.winfo_children():
            widget.destroy()

        # Aseta otsikot
        self.recentLabel = ttk.Label(self.recent, text="Viimeaikainen toiminta")
        self.recentLabel.grid(column=0, row=0, columnspan=3)

        self.dateLabel = ttk.Label(self.recent, text="Päivämäärä")
        self.dateLabel.grid(column=0, row=1)
        self.amountLabel = ttk.Label(self.recent, text="Määrä")
        self.amountLabel.grid(column=1, row=1)
        self.descriptionLabel = ttk.Label(self.recent, text="Kuvaus")
        self.descriptionLabel.grid(column=2, row=1)

        totalIncome = 0
        totalExpenses = 0
        for rowIndex, transaction in enumerate(self.userData.transactionList):
            # Päivitä recent-paneeli
            print(transaction.date)
            dateText = transaction.date.strftime("%d/%m/%Y")
            recentItem = ttk.Label(masterWindow, text=dateText)
            recentItem.grid(column=0, row=rowIndex+2)

            amountText = transaction.amount, "€"
            recentItem = ttk.Label(masterWindow, text=amountText)
            recentItem.grid(column=1, row=rowIndex+2)

            recentItem = ttk.Label(masterWindow, text=transaction.description)
            recentItem.grid(column=2, row=rowIndex+2)

            # Päivitä yleiskatsaus paneeli
            if transaction.amount >= 0:
                totalIncome += transaction.amount

            elif transaction.amount < 0:
                totalExpenses += transaction.amount

            else:
                pass
        
        self.userData.guiIncome.set(totalIncome)
        self.userData.guiExpenses.set(totalExpenses)
        self.userData.balance.set(totalIncome + totalExpenses)

    def removeTransactions(self):
        eventWindow = transaction.removeTransactionEventWindow(self.root, self.userData)
        eventWindow.wait_window(eventWindow)
        print("Poistotapahtuma suoritettu!")
        self.sortTransactions()
        self.printTransactions(self.recent)

    def importTranscations(self):
        self.userData.transactionList = transaction.importTransactions(self.userData)
        self.sortTransactions()
        self.printTransactions(self.recent)

    def __init__(self, userObject):
        self.root = root
        root.title("Budjetoija")
        self.userData = userObject

        # Pääraamit ohjelmalle
        self.mainframe = ttk.Frame(self.root, borderwidth=10, relief="raised", padding=(3,3,12,12), width=10, height=10)

        # Paneelit eri osille
        self.info = ttk.Frame(self.mainframe, borderwidth=2, relief="sunken", width=200, height=50)
        self.panel = ttk.Frame(self.mainframe, borderwidth=2, relief="sunken", width=50, height=200)
        self.overview = ttk.Frame(self.mainframe, borderwidth=2, relief="sunken", width=150, height=200)
        self.recent = ttk.Frame(self.mainframe, borderwidth=2, relief="sunken", width=100, height=250)

        # Aseta paneelit
        self.mainframe.grid(column=0, row=0, sticky="nsew")
        self.info.grid(column=0, row=0, columnspan=3, sticky="nsew")
        self.panel.grid(column=0, row=1, sticky="nsew")
        self.overview.grid(column=1, row=1, sticky="nsew")
        self.recent.grid(column=2, row=1, rowspan=2, sticky="nsew")

        # Info-paneelin sisältö
        self.infoLabel = ttk.Label(self.info, text="Info")
        self.infoLabel.grid(column=0, row=0, sticky="nw")

        self.nameLabel = ttk.Label(self.info, textvariable=userObject.userName)
        self.infoName = ttk.Label(self.info, text="Nimi:")
        self.infoName.grid(column=1, row=1, sticky="nw")
        self.nameLabel.grid(column=2, row=1, sticky="nw")

        self.ageLabel = ttk.Label(self.info, textvariable=userObject.userAge)
        self.infoAge = ttk.Label(self.info, text="Ikä")
        self.infoAge.grid(column=1, row=2, sticky="nw")
        self.ageLabel.grid(column=2, row=2, sticky="nw")

        self.editButton = Button(self.info, text="Muokkaa", command = lambda : profile.updateInfo(root, userObject))
        self.editButton.grid(column=1, row=0)

        # Panel-paneelin sisältö
        self.panelLabel = ttk.Label(self.panel, text="Hallintapaneeli")
        self.panelLabel.grid(column=0, row=0)

        self.addTransactionButton = Button(self.panel, text="Lisää transaktio", command=lambda: self.addTransaction())
        self.removeTransactionButton = Button(self.panel, text="Poista transaktio", command=lambda : self.removeTransactions())

        self.importButton = Button(self.panel, text="Tuo tiedosto", command=lambda: self.importTranscations())
        self.exportButton = Button(self.panel, text="Vie tiedosto", command=lambda: transaction.exportTransactions(self.userData))

        self.exitButton = Button(self.panel, text="Poistu", command=self.exit)

        self.testButton = Button(self.panel, text="Testi", command=lambda : self.sortTransactions())

        self.addTransactionButton.grid(column=0, row=1)
        self.removeTransactionButton.grid(column=0, row=2)

        self.importButton.grid(column=0, row=3)
        self.exportButton.grid(column=0, row=4)

        self.exitButton.grid(column=0, row=5)

        self.testButton.grid(column=1, row=5)

        # Overview-paneelin sisältö
        self.overviewLabel = ttk.Label(self.overview, text="Yleiskatsaus")
        self.overviewLabel.grid(column=0, row=0)

        self.incomeLabel = ttk.Label(self.overview, text="Tulot:")
        self.incomeContent = ttk.Label(self.overview, textvariable=userObject.guiIncome)

        self.expensesLabel = ttk.Label(self.overview, text="Menot:")
        self.expensesContent = ttk.Label(self.overview, textvariable=userObject.guiExpenses)

        self.balanceLabel = ttk.Label(self.overview, text="Yhteensä:")
        self.balanceContent = ttk.Label(self.overview, textvariable=userObject.balance)

        self.incomeLabel.grid(column=0, row=1)
        self.incomeContent.grid(column=1, row=1)
        self.expensesLabel.grid(column=0, row=2)
        self.expensesContent.grid(column=1, row=2)
        self.balanceLabel.grid(column=0, row=4)
        self.balanceContent.grid(column=1, row=4)

        # Recent-paneelin sisältö
        self.recentLabel = ttk.Label(self.recent, text="Viimeaikainen toiminta")
        self.recentLabel.grid(column=0, row=0, columnspan=3)

        self.dateLabel = ttk.Label(self.recent, text="Päivämäärä")
        self.dateLabel.grid(column=0, row=1)
        self.amountLabel = ttk.Label(self.recent, text="Määrä")
        self.amountLabel.grid(column=1, row=1)
        self.descriptionLabel = ttk.Label(self.recent, text="Kuvaus")
        self.descriptionLabel.grid(column=2, row=1)

        # Ikkunan koon muutoksen hallinta
        # Ainoastaan recent-paneeli saa lisää tilaa ikkunaa laajennettaessa
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)

        self.mainframe.columnconfigure(0, weight=0)
        self.mainframe.columnconfigure(1, weight=0)
        self.mainframe.columnconfigure(2, weight=1)
        self.mainframe.rowconfigure(0, weight=0)
        self.mainframe.rowconfigure(1, weight=1)

root = Tk()