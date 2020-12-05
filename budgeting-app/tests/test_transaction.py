import unittest
import tkinter as tk

from src import transaction

class TestTransaction(unittest.TestCase):
    def test_user_input_validation(self):
        root = tk.Tk()
        dummyFrame = tk.Frame(root)
        dummyEntry = tk.Entry(root)
        dummyList = []
        date = ("22.2.00")
        amount = 500
        description = ""

        result = transaction.validateUserInput(dummyEntry, dummyEntry, date, amount, description, dummyList, dummyFrame)
        self.assertEqual(isinstance(result, object), True)

if __name__ == "__main__":
    unittest.main()

