from PyQt5.QtWidgets import *
from view import *
import csv

QtWidgets.QApplication.setAttribute(QtCore.Qt.AA_EnableHighDpiScaling, True)
QtWidgets.QApplication.setAttribute(QtCore.Qt.AA_UseHighDpiPixmaps, True)


class Account(QMainWindow, Ui_MainWindow):
    """Function to set up the account class.
    """
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.balance = None
        self.setupUi(self)
        self.buttonEnter.clicked.connect(lambda: self.enter())
        self.buttonExit.clicked.connect(lambda: self.exit())
        self.buttonSearch.clicked.connect(lambda: self.account_search())

    def account_search(self):
        """This function searches for the account by taking user's first name, last name, and pin to verify that
        the account exists. If it does not, an error message will appear letting them know that no account exists
        """
        first_name = self.inputFirstName.text().lower()
        last_name = self.inputLastName.text().lower()
        pin = self.inputPIN.text()

        with open("accounts.csv", 'r') as csvfile:
            reader = csv.reader(csvfile)
            for row in reader:
                accounts_first_name, accounts_last_name, accounts_pin, accounts_balance = row

                if accounts_first_name.lower() == first_name and accounts_last_name.lower() == last_name and accounts_pin == pin:
                    self.greetingOutput.setText(f'Welcome {first_name.capitalize()} {last_name.capitalize()}!')
                    self.balance = float(accounts_balance)
                    self.labelOutput.setText(f'Your account balance is: ${self.balance:.2f}')
                    return

        self.greetingOutput.setText(f'There are no accounts with that name and PIN')

    def enter(self):
        """This function allows the user to select what account transactions they would like to complete. If they select
        withdraw, it removes money from their account, deposit adds an amount and the get balance displays the current
        balance in their account.

        """
        amount = float(self.inputAmount.text())
        current_bal = float(self.labelOutput.text().split('$')[1])

        #Part of the function that allows user to withdraw the amount of money
        if self.radioWithdraw.isChecked():
            if amount <= 0:
                self.exit()
                self.labelOutput.setText(f'The amount you wish to withdraw \nis less than or equal to 0')
            elif amount > current_bal:
                self.exit()
                self.labelOutput.setText(f'The amount you wish to withdraw \nis more than the amount in your account')
            else:
                new_bal = current_bal - amount
                self.labelOutput.setText(f'You have withdrawn ${amount:.2f}. \nYour new balance is:${new_bal:.2f}')

        # Part of the function that allows user to deposit the amount of money

        elif self.radioDeposit.isChecked():
            if amount > 0:
                new_bal = current_bal + amount
                self.labelOutput.setText(f'You have deposited ${amount:.2f}. \nYour new balance is: ${new_bal:.2f}')
            else:
                self.exit()
                self.labelOutput.setText(f"The amount entered is invalid. Please try again.")

        """TODO: add function or other method to allow new balance to be saved to .csv
                Test why the radio buttons are not clearing. The code looks correct. 
        """
    def exit(self):
        """Function to clear the previously entered data so new data can be entered and a new account can be searched.
        """
        self.inputFirstName.setText("")
        self.inputLastName.setText("")
        self.inputPIN.setText("")
        self.greetingOutput.setText("")
        self.inputAmount.setText("")
        self.labelOutput.setText("")
        self.radioWithdraw.setChecked(False)
        self.radioDeposit.setChecked(False)
