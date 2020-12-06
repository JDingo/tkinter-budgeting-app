import unittest
import tkinter as tk

import json 

from src import transaction

class TestTransaction(unittest.TestCase):

    # Maksutapahtumien datan verifioinnin testaus
    def test_user_input_validation(self):
        root = tk.Tk()
        dummyFrame = tk.Frame(root)
        dummyEntry = tk.Entry(root)
        dummyList = []

        description = ""
        
        # Testidata TestData.json-tiedostossa
        with open("tests/testData.json", "r") as testDataFile:
            testData = json.load(testDataFile)

            # Testaa oikeelliset arvot,
            # metodi ei palauta mitään, odotettu arvo: None
            for amountDataElement in testData["ValidAmounts"]:
                for dateDateElement in testData["ValidDates"]:
                    result = transaction.validateUserInput(dummyEntry, dummyEntry, dateDateElement, amountDataElement, description, dummyList, dummyFrame)
                    self.assertIsNone(result)

            # Testaa viallisia arvoja,
            # metodi palauttaa error-muuttujan, odotettu arvo: True
            for amountDataElement in testData["ValidAmounts"]:
                for dateDateElement in testData["InvalidDates"]:
                    result = transaction.validateUserInput(dummyEntry, dummyEntry, dateDateElement, amountDataElement, description, dummyList, dummyFrame)
                    self.assertTrue(result)

            for amountDataElement in testData["InvalidAmounts"]:
                for dateDateElement in testData["ValidDates"]:
                    result = transaction.validateUserInput(dummyEntry, dummyEntry, dateDateElement, amountDataElement, description, dummyList, dummyFrame)
                    self.assertTrue(result)

            for amountDataElement in testData["InvalidAmounts"]:
                for dateDateElement in testData["InvalidDates"]:
                    result = transaction.validateUserInput(dummyEntry, dummyEntry, dateDateElement, amountDataElement, description, dummyList, dummyFrame)
                    self.assertTrue(result)

if __name__ == "__main__":
    unittest.main()

