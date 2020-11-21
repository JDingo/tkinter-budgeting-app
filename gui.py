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

def poistu():
    messagebox.showinfo("Budjetoija", "Ohjelma sammutetaan.")
    root.destroy()
    sys.exit()

def paivitaTransaktiot(komento, tulosumma, menosumma):
    if komento == 'lisaa':
        tapahtumaIkkuna = transaktio.lisaaTransaktioGUI(root, maksuTapahtumat)
        tapahtumaIkkuna.wait_window(tapahtumaIkkuna)
        print("Tapahtuma lisätty!")

        for i in range(len(maksuTapahtumat)):
            # Päivitä recent-paneeli
            recentItem = ttk.Label(recent, text=maksuTapahtumat[i].pvm)
            recentItem.grid(column=0, row=i+2)

            maaraTeksti = maksuTapahtumat[i].maara, "€"
            recentItem = ttk.Label(recent, text=maaraTeksti)
            recentItem.grid(column=1, row=i+2)

            recentItem = ttk.Label(recent, text=maksuTapahtumat[i].kuvaus)
            recentItem.grid(column=2, row=i+2)

            # Päivitä yleiskatsaus paneeli
            if maksuTapahtumat[i].maara >= 0:
                tulosumma += maksuTapahtumat[i].maara
                tulot.set(tulosumma)

            elif maksuTapahtumat[i].maara < 0:
                menosumma += maksuTapahtumat[i].maara
                menot.set(menosumma)

            else:
                pass

            yhteensa.set(tulosumma + menosumma)
        
root = Tk()
root.title("Budjetoija")

tulot = StringVar()
menot = StringVar()
tulosumma = 0
menosumma = 0
tulot.set(menosumma)
menot.set(menosumma)

yhteensa = StringVar()
yhteensa.set(tulosumma + menosumma)
maksuTapahtumat = []

# Pääraamit ohjelmalle
mainframe = ttk.Frame(root, borderwidth=10, relief="raised", padding=(3,3,12,12), width=10, height=10)

# Paneelit eri osille
info = ttk.Frame(mainframe, borderwidth=2, relief="sunken", width=200, height=50)
panel = ttk.Frame(mainframe, borderwidth=2, relief="sunken", width=50, height=200)
overview = ttk.Frame(mainframe, borderwidth=2, relief="sunken", width=150, height=200)
recent = ttk.Frame(mainframe, borderwidth=2, relief="sunken", width=100, height=250)

# Aseta paneelit
mainframe.grid(column=0, row=0, sticky="nsew")
info.grid(column=0, row=0, columnspan=3, sticky="nsew")
panel.grid(column=0, row=1, sticky="nsew")
overview.grid(column=1, row=1, sticky="nsew")
recent.grid(column=2, row=1, rowspan=2, sticky="nsew")

# Info-paneelin sisältö
infolabel = ttk.Label(info, text="Info")
infolabel.grid(column=0, row=0, sticky="nw")

nimiLabel = "Nimi: " + profiili.profiiliInfo['Nimi']
infoName = ttk.Label(info, text=nimiLabel)
infoName.grid(column=1, row=1, sticky="nw")

ikaLabel = "Ikä: " + profiili.profiiliInfo['Ika']
infoIka = ttk.Label(info, text=ikaLabel)
infoIka.grid(column=1, row=2, sticky="nw")

ammattiLabel = "Ammatti: " + profiili.profiiliInfo['Ammatti']
infoAmmatti = ttk.Label(info, text=ammattiLabel)
infoAmmatti.grid(column=1, row=3, sticky="nw")

# Panel-paneelin sisältö
panellabel = ttk.Label(panel, text="Hallintapaneeli")
panellabel.grid(column=0, row=0)

lisaa = Button(panel, text="Lisää transaktio", command=lambda: paivitaTransaktiot('lisaa', tulosumma, menosumma))
poista = Button(panel, text="Poista transaktio", command="")

tuo = Button(panel, text="Tuo tiedosto", command="")
vie = Button(panel, text="Vie tiedosto", command="")

poistu = Button(panel, text="Poistu", command=poistu)

testi = Button(panel, text="Testi", command=lambda : print(maksuTapahtumat))

lisaa.grid(column=0, row=1)
poista.grid(column=0, row=2)

tuo.grid(column=0, row=3)
vie.grid(column=0, row=4)

poistu.grid(column=0, row=5)

testi.grid(column=1, row=5)

# Overview-paneelin sisältö
overviewlabel = ttk.Label(overview, text="Yleiskatsaus")
overviewlabel.grid(column=0, row=0)

tulotlabel = ttk.Label(overview, text="Tulot:")
tulotcontent = ttk.Label(overview, textvariable=tulot)

menotlabel = ttk.Label(overview, text="Menot:")
menotcontent = ttk.Label(overview, textvariable=menot)

yhteensalabel = ttk.Label(overview, text="Yhteensä:")
yhteensacontent = ttk.Label(overview, textvariable=yhteensa)

tulotlabel.grid(column=0, row=1)
tulotcontent.grid(column=1, row=1)
menotlabel.grid(column=0, row=2)
menotcontent.grid(column=1, row=2)
yhteensalabel.grid(column=0, row=4)
yhteensacontent.grid(column=1, row=4)

# Recent-paneelin sisältö
recentlabel = ttk.Label(recent, text="Viimeaikainen toiminta")
recentlabel.grid(column=0, row=0, columnspan=3)

pvmLabel = ttk.Label(recent, text="Päivämäärä")
pvmLabel.grid(column=0, row=1)
maaraLabel = ttk.Label(recent, text="Määrä")
maaraLabel.grid(column=1, row=1)
kuvausLabel = ttk.Label(recent, text="Kuvaus")
kuvausLabel.grid(column=2, row=1)

# Ikkunan koon muutoksen hallinta
# Ainoastaan recent-paneeli saa lisää tilaa ikkunaa laajennettaessa
root.columnconfigure(0, weight=1)
root.rowconfigure(0, weight=1)

mainframe.columnconfigure(0, weight=0)
mainframe.columnconfigure(1, weight=0)
mainframe.columnconfigure(2, weight=1)
mainframe.rowconfigure(0, weight=0)
mainframe.rowconfigure(1, weight=1)

window.mainloop()