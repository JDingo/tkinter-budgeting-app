# Tuo tkinter-kirjasto GUI:ta varten
from tkinter import *
from tkinter import ttk
from tkinter import messagebox
from tkinter import simpledialog

class Transaktio:

    def __init__(self, pvm, maara, kuvaus):
        self.pvm = pvm
        self.maara = maara
        if maara >= 0:
            self.luokka = "TULO"
        else:
            self.luokka = "MENO"
        self.kuvaus = kuvaus

def luoTransaktio(pvm, maara, kuvaus, lista, ikkuna):
    transaktio = Transaktio(pvm, int(maara), kuvaus)
    print(transaktio, transaktio.pvm, transaktio.maara, transaktio.kuvaus)

    lista.append(transaktio)

    ikkuna.destroy()

def lisaaTransaktioGUI(root, lista):
    ikkuna = Toplevel(root)
    ikkuna.title("Lisää maksutapahtuma.")
    
    pvmLabel = Label(ikkuna, text="Päivämäärä [dd.mm.yyyy]:")
    pvmEntry = Entry(ikkuna)

    maaraLabel = Label(ikkuna, text="Määrä:")
    maaraEntry = Entry(ikkuna)

    kuvausLabel = Label(ikkuna, text="Kuvaus:")
    kuvausEntry = Entry(ikkuna)

    lisaaNappi = Button(ikkuna, text="Lisää transaktio", command = lambda : luoTransaktio(pvmEntry.get(), maaraEntry.get(), kuvausEntry.get(), lista, ikkuna))
    poistuNappi = Button(ikkuna, text="Poistu", command = ikkuna.destroy)

    pvmLabel.grid(row=0, column=0)
    pvmEntry.grid(row=0, column=1)
    maaraLabel.grid(row=1, column=0)
    maaraEntry.grid(row=1, column=1)
    kuvausLabel.grid(row=2, column=0)
    kuvausEntry.grid(row=2, column=1)

    lisaaNappi.grid(row=3, column=0)
    poistuNappi.grid(row=3, column=1)

    return ikkuna