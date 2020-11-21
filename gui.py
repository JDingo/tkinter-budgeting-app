# Tuo tkinter-kirjasto GUI:ta varten
from tkinter import *
from tkinter import ttk
from tkinter import messagebox

# Tuo profiili-tiedosto, joka sisältää käyttäjän tietoja
import profile as profiili

# Tuo transaktio-tiedosto, joka sisältää maksutapahtumiin liittyvät luokat ja metodit
import transaktio as transaktio

# Tuo sys ohjelman sammuttamista varten
import sys
        
class GUI():
    def poistu(self):
        messagebox.showinfo("Budjetoija", "Ohjelma sammutetaan.")
        root.destroy()
        sys.exit()

    def paivitaTransaktiot(self, komento, tulosumma, menosumma):
        if komento == 'lisaa':
            tapahtumaIkkuna = transaktio.lisaaTransaktioGUI(root, self.maksuTapahtumat)
            tapahtumaIkkuna.wait_window(tapahtumaIkkuna)
            print("Tapahtuma lisätty!")

            self.menosumma = 0
            self.tulosumma = 0
            for i in range(len(self.maksuTapahtumat)):
                # Päivitä recent-paneeli
                recentItem = ttk.Label(self.recent, text=self.maksuTapahtumat[i].pvm)
                recentItem.grid(column=0, row=i+2)

                maaraTeksti = self.maksuTapahtumat[i].maara, "€"
                recentItem = ttk.Label(self.recent, text=maaraTeksti)
                recentItem.grid(column=1, row=i+2)

                recentItem = ttk.Label(self.recent, text=self.maksuTapahtumat[i].kuvaus)
                recentItem.grid(column=2, row=i+2)

                # Päivitä yleiskatsaus paneeli
                if self.maksuTapahtumat[i].maara >= 0:
                    self.tulosumma += self.maksuTapahtumat[i].maara
                    self.tulot.set(self.tulosumma)

                elif self.maksuTapahtumat[i].maara < 0:
                    self.menosumma += self.maksuTapahtumat[i].maara
                    self.menot.set(self.menosumma)

                else:
                    pass

                self.yhteensa.set(self.tulosumma + self.menosumma)

    def __init__(self, root):
        self.root = root
        root.title("Budjetoija")

        self.tulot = StringVar()
        self.menot = StringVar()
        self.tulosumma = 0
        self.menosumma = 0
        self.tulot.set(self.menosumma)
        self.menot.set(self.menosumma)

        self.yhteensa = StringVar()
        self.yhteensa.set(self.tulosumma + self.menosumma)
        self.maksuTapahtumat = []

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
        self.infolabel = ttk.Label(self.info, text="Info")
        self.infolabel.grid(column=0, row=0, sticky="nw")

        self.nimiLabel = "Nimi: " + profiili.profiiliInfo['Nimi']
        self.infoName = ttk.Label(self.info, text=self.nimiLabel)
        self.infoName.grid(column=1, row=1, sticky="nw")

        self.ikaLabel = "Ikä: " + profiili.profiiliInfo['Ika']
        self.infoIka = ttk.Label(self.info, text=self.ikaLabel)
        self.infoIka.grid(column=1, row=2, sticky="nw")

        self.ammattiLabel = "Ammatti: " + profiili.profiiliInfo['Ammatti']
        self.infoAmmatti = ttk.Label(self.info, text=self.ammattiLabel)
        self.infoAmmatti.grid(column=1, row=3, sticky="nw")

        # Panel-paneelin sisältö
        self.panellabel = ttk.Label(self.panel, text="Hallintapaneeli")
        self.panellabel.grid(column=0, row=0)

        self.lisaa = Button(self.panel, text="Lisää transaktio", command=lambda: self.paivitaTransaktiot('lisaa', self.tulosumma, self.menosumma))
        self.poista = Button(self.panel, text="Poista transaktio", command="")

        self.tuo = Button(self.panel, text="Tuo tiedosto", command="")
        self.vie = Button(self.panel, text="Vie tiedosto", command="")

        self.poistu = Button(self.panel, text="Poistu", command=self.poistu)

        self.testi = Button(self.panel, text="Testi", command=lambda : print(self.maksuTapahtumat))

        self.lisaa.grid(column=0, row=1)
        self.poista.grid(column=0, row=2)

        self.tuo.grid(column=0, row=3)
        self.vie.grid(column=0, row=4)

        self.poistu.grid(column=0, row=5)

        self.testi.grid(column=1, row=5)

        # Overview-paneelin sisältö
        self.overviewlabel = ttk.Label(self.overview, text="Yleiskatsaus")
        self.overviewlabel.grid(column=0, row=0)

        self.tulotlabel = ttk.Label(self.overview, text="Tulot:")
        self.tulotcontent = ttk.Label(self.overview, textvariable=self.tulot)

        self.menotlabel = ttk.Label(self.overview, text="Menot:")
        self.menotcontent = ttk.Label(self.overview, textvariable=self.menot)

        self.yhteensalabel = ttk.Label(self.overview, text="Yhteensä:")
        self.yhteensacontent = ttk.Label(self.overview, textvariable=self.yhteensa)

        self.tulotlabel.grid(column=0, row=1)
        self.tulotcontent.grid(column=1, row=1)
        self.menotlabel.grid(column=0, row=2)
        self.menotcontent.grid(column=1, row=2)
        self.yhteensalabel.grid(column=0, row=4)
        self.yhteensacontent.grid(column=1, row=4)

        # Recent-paneelin sisältö
        self.recentlabel = ttk.Label(self.recent, text="Viimeaikainen toiminta")
        self.recentlabel.grid(column=0, row=0, columnspan=3)

        self.pvmLabel = ttk.Label(self.recent, text="Päivämäärä")
        self.pvmLabel.grid(column=0, row=1)
        self.maaraLabel = ttk.Label(self.recent, text="Määrä")
        self.maaraLabel.grid(column=1, row=1)
        self.kuvausLabel = ttk.Label(self.recent, text="Kuvaus")
        self.kuvausLabel.grid(column=2, row=1)

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
gui = GUI(root)
root.mainloop()