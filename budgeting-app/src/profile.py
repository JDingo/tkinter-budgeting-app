# Tuo kirjastot/moduulit käyttöliittymää varten
import tkinter as tk

def updateInfo(root, userObject):
    # Käyttäjätietojen muutosikkuna
    def editInfoEventWindow(root, userName, userAge):
        window = tk.Toplevel(root)
        window.title("Muokkaa tietoja")

        nameLabel = tk.Label(window, text="Nimi:")
        nameEntry = tk.Entry(window)

        ageLabel = tk.Label(window, text="Ika:")
        ageEntry = tk.Entry(window)

        confirmButton = tk.Button(window, text="OK", command = lambda : editInfo(nameEntry.get(), ageEntry.get(), userName, userAge, window))

        nameLabel.grid(column=0, row=0)
        nameEntry.grid(column=1, row=0)

        ageLabel.grid(column=0, row=1)
        ageEntry.grid(column=1, row=1)

        confirmButton.grid(column=0, row=2)

        return window

    # Aseta annetut parametrit StringVar-tyypin muuttujiin
    # StringVar päivittää tiedot automaattisesti käyttöliittymään
    def editInfo(name, age, userName, userAge, window):
        userName.set(name)
        userAge.set(age)
        window.destroy()

    # Luo ikkuna
    eventWindow = editInfoEventWindow(root, userObject.userName, userObject.userAge)
    # Jatka, kun aiemmin luotu ikkuna tuhotaan
    eventWindow.wait_window(eventWindow)