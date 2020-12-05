# Tuo kirjastot/moduulit käyttöliittymää varten
import tkinter as tk
from tkinter import messagebox

# Tuo kirjastot/moduulit toiminnallisuutta varten
import operator as operator
import profile as profile
import transaction as transaction
import sys as sys
import datetime as dt

class GUI:
    # Luo popup-ikkuna, jonka jälkeen tuhoa ikkuna ja sammuta ohjelma
    def exit(self):
        quitDialog = messagebox.askyesno("Budjetoija", "Oletko varma, että haluat sammuttaa ohjelman? Kaikki tallentamattomat muutokset menetetään.")
        if quitDialog == True:
            root.destroy()
            sys.exit()
        else:
            pass

    # Päivitä maksutapahtumat käymällä lista läpi
    def addTransaction(self):
        transaction.addTransaction(self.root, self.userData)
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

        # Tarkista tämänhetkinen vuosi ja kuukausi
        currentMonthYear = dt.datetime.now().strftime("%m.%Y")

        # Aseta otsikot
        self.recentLabel = tk.Label(masterWindow, text="Viimeaikainen toiminta", font="bold")
        self.recentLabel.grid(column=0, row=0, columnspan=3)
        self.dateLabel = tk.Label(masterWindow, text="Päivämäärä")
        self.dateLabel.grid(column=0, row=1)
        self.amountLabel = tk.Label(masterWindow, text="Määrä")
        self.amountLabel.grid(column=1, row=1)
        self.descriptionLabel = tk.Label(masterWindow, text="Kuvaus")
        self.descriptionLabel.grid(column=2, row=1)

        # Laske uudet arvot käymällä lista läpi
        totalIncome = 0
        totalExpenses = 0
        monthlyIncome = 0
        monthlyExpenses = 0
        for rowIndex, transaction in enumerate(self.userData.transactionList):
            # Tulosta tapahtumat annetulle ikkunalle
            dateText = transaction.date.strftime("%d/%m/%Y")
            recentItem = tk.Label(masterWindow, text=dateText)
            recentItem.grid(column=0, row=rowIndex+2)

            amountText = transaction.amount, "€"
            recentItem = tk.Label(masterWindow, text=amountText)
            recentItem.grid(column=1, row=rowIndex+2)

            recentItem = tk.Label(masterWindow, text=transaction.description)
            recentItem.grid(column=2, row=rowIndex+2)

            # Laske uudet arvot kokonaistulolle ja -menolle (myös kuukausittaille arvoille)
            if transaction.amount >= 0 and transaction.date.strftime("%m.%Y") == currentMonthYear:
                totalIncome += transaction.amount
                monthlyIncome += transaction.amount

            elif transaction.amount >= 0:
                totalIncome += transaction.amount

            elif transaction.amount < 0 and transaction.date.strftime("%m.%Y") == currentMonthYear:
                totalExpenses += transaction.amount
                monthlyExpenses += transaction.amount

            elif transaction.amount < 0:
                totalExpenses += transaction.amount

            else:
                print("Virhe summien laskussa!")
        
        # Aseta uudet arvot StringVar()-muuttujalle
        incomeString = totalIncome, "€"
        expensesString = totalExpenses, "€"
        monthlyIncomeString = monthlyIncome, "€"
        monthlyExpensesString = monthlyExpenses, "€"
        self.userData.guiIncome.set(incomeString)
        self.userData.guiExpenses.set(expensesString)
        self.userData.monthlyIncome.set(monthlyIncomeString)
        self.userData.monthlyExpenses.set(monthlyExpensesString)
        monthlyBalanceString = monthlyIncome + monthlyExpenses, "€"
        balanceString = totalIncome + totalExpenses, "€"
        self.userData.balance.set(balanceString)
        self.userData.monthlyBalance.set(monthlyBalanceString)

    # Maksutapahtumien poisto
    def removeTransactions(self):
        eventWindow = transaction.removeTransactionEventWindow(self.root, self.userData)
        eventWindow.wait_window(eventWindow)
        print("Poistotapahtuma suoritettu!")
        self.sortTransactions()
        self.printTransactions(self.recent)

    # Tiedostosta tuonti
    def importTranscations(self):
        self.userData.transactionList = transaction.importTransactions(self.userData)
        self.sortTransactions()
        self.printTransactions(self.recent)

    def __init__(self, userObject):
        self.root = root
        root.title("Budjetoija")
        self.userData = userObject

        # Pääraamit ohjelmalle
        self.mainframe = tk.Frame(self.root, borderwidth=10, width=10, height=10)

        # Paneelit eri osille
        self.info = tk.Frame(self.mainframe, borderwidth=2, relief="sunken", width=200, height=50)
        self.panel = tk.Frame(self.mainframe, borderwidth=2, relief="sunken", width=50, height=200)
        self.overview = tk.Frame(self.mainframe, borderwidth=2, relief="sunken", width=150, height=200)
        self.recent = tk.Frame(self.mainframe, borderwidth=2, relief="sunken", width=100, height=250)

        # Aseta paneelit
        self.mainframe.grid(column=0, row=0, sticky="nsew", pady=(2,2), padx=(2,2))
        self.info.grid(column=0, row=0, columnspan=3, sticky="nsew", pady=(2,2), padx=(2,2))
        self.panel.grid(column=0, row=1, sticky="nsew", pady=(2,2), padx=(2,2))
        self.overview.grid(column=1, row=1, sticky="nsew", pady=(2,2), padx=(2,2))
        self.recent.grid(column=2, row=1, rowspan=2, sticky="nsew", pady=(2,2), padx=(2,2))

        # Info-paneelin sisältö
        self.infoLabel = tk.Label(self.info, text="Info", font="bold")
        self.infoLabel.grid(column=0, row=0, sticky="nw", pady=(2,2), padx=(2,2))

        self.nameLabel = tk.Label(self.info, textvariable=userObject.userName)
        self.infoName = tk.Label(self.info, text="Nimi:")
        self.infoName.grid(column=1, row=1, sticky="nw")
        self.nameLabel.grid(column=2, row=1, sticky="nw")

        self.ageLabel = tk.Label(self.info, textvariable=userObject.userAge)
        self.infoAge = tk.Label(self.info, text="Ikä")
        self.infoAge.grid(column=1, row=2, sticky="nw")
        self.ageLabel.grid(column=2, row=2, sticky="nw")

        self.editButton = tk.Button(self.info, text="Muokkaa", command = lambda : profile.updateInfo(root, userObject))
        self.editButton.grid(column=1, row=0)

        # Panel-paneelin sisältö
        self.panelLabel = tk.Label(self.panel, text="Hallintapaneeli", font="bold")
        self.panelLabel.grid(column=0, row=0, pady=(2,0), padx=(2,2))

        self.addTransactionButton = tk.Button(self.panel, text="Lisää transaktio", command=lambda: self.addTransaction())
        self.removeTransactionButton = tk.Button(self.panel, text="Poista transaktio", command=lambda : self.removeTransactions())

        self.importButton = tk.Button(self.panel, text="Tuo tiedosto", command=lambda: self.importTranscations())
        self.exportButton = tk.Button(self.panel, text="Vie tiedosto", command=lambda: transaction.exportTransactions(self.userData))

        self.exitButton = tk.Button(self.panel, text="Poistu", command=self.exit)

        self.testButton = tk.Button(self.panel, text="Testi", command=lambda : self.sortTransactions())

        self.addTransactionButton.grid(column=0, row=1, pady=(5,0), padx=(5,5))
        self.removeTransactionButton.grid(column=0, row=2, pady=(1,0), padx=(5,5))

        self.importButton.grid(column=0, row=3, pady=(5,0), padx=(5,5))
        self.exportButton.grid(column=0, row=4, pady=(1,0), padx=(5,5))

        self.exitButton.grid(column=0, row=5, pady=(5,0), padx=(5,5))

        self.testButton.grid(column=0, row=6, pady=(1,5), padx=(5,5))

        # Overview-paneelin sisältö
        self.overviewLabel = tk.Label(self.overview, text="Yleiskatsaus", font="bold")
        self.overviewLabel.grid(column=0, row=0, pady=(2,2), padx=(2,2))

        self.monthlyLabel = tk.Label(self.overview, text="Kuukauden budjetti")
        self.monthlyIncomeLabel = tk.Label(self.overview, text="Tulot:")
        self.monthlyIncomeContent = tk.Label(self.overview, textvariable=userObject.monthlyIncome)
        self.monthlyExpensesLabel = tk.Label(self.overview, text="Menot:")
        self.monthlyExpensesContent = tk.Label(self.overview, textvariable=userObject.monthlyExpenses)
        self.monthlyBalanceLabel = tk.Label(self.overview, text="Yhteensä:")
        self.monthlyBalanceContent = tk.Label(self.overview, textvariable=userObject.monthlyBalance)

        self.monthlyLabel.grid(column=0, row=1, sticky="w")
        self.monthlyIncomeLabel.grid(column=0, row=2)
        self.monthlyIncomeContent.grid(column=1, row=2)
        self.monthlyExpensesLabel.grid(column=0, row=3)
        self.monthlyExpensesContent.grid(column=1, row=3)
        self.monthlyBalanceLabel.grid(column=0, row=4)
        self.monthlyBalanceContent.grid(column=1, row=4)

        self.totalLabel = tk.Label(self.overview, text="Koko budjetti")
        self.monthlyLabel = tk.Label(self.overview, text="Kuukauden budjetti")
        self.incomeLabel = tk.Label(self.overview, text="Tulot:")
        self.incomeContent = tk.Label(self.overview, textvariable=userObject.guiIncome)
        self.expensesLabel = tk.Label(self.overview, text="Menot:")
        self.expensesContent = tk.Label(self.overview, textvariable=userObject.guiExpenses)
        self.balanceLabel = tk.Label(self.overview, text="Yhteensä:")
        self.balanceContent = tk.Label(self.overview, textvariable=userObject.balance)

        self.totalLabel.grid(column=0, row=5, sticky="w", pady=(2,0))
        self.incomeLabel.grid(column=0, row=6)
        self.incomeContent.grid(column=1, row=6)
        self.expensesLabel.grid(column=0, row=7)
        self.expensesContent.grid(column=1, row=7)
        self.balanceLabel.grid(column=0, row=8)
        self.balanceContent.grid(column=1, row=8)

        # Recent-paneelin sisältö
        self.recentLabel = tk.Label(self.recent, text="Viimeaikainen toiminta", font="bold")
        self.recentLabel.grid(column=0, row=0, columnspan=3, pady=(2,2), padx=(2,2))

        self.dateLabel = tk.Label(self.recent, text="Päivämäärä")
        self.dateLabel.grid(column=0, row=1)
        self.amountLabel = tk.Label(self.recent, text="Määrä")
        self.amountLabel.grid(column=1, row=1)
        self.descriptionLabel = tk.Label(self.recent, text="Kuvaus")
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

root = tk.Tk()