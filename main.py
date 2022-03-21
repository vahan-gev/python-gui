from turtle import clear
from PySide6 import QtCore, QtWidgets
from PySide6.QtGui import QIcon
from random import randint
import hashlib
import sys
import os, os.path
import sqlite3
from sqlite3 import Error

# Variable Declaring
currency = "$"
version = "3.0"
if os.path.exists('database'):
    entries = os.listdir('database/')
else:
    print("First Start")
    print("Creating directory...")
    os.mkdir('database')
    print("Done...")
    print("Creating File data.sqlite")
    f = open("data.sqlite", "w")
    f.close()
    print("Done creating database file")
accounts = list()
active_account = None
administrators = [8665726578]
headingStyle = '''
    font-size: 18px;
'''
inputStyle = '''
    border: none;
    height: 40px;
    font-size: 18px;
    border-radius: 2px;
    padding-left: 10px;
'''
buttonStyle = '''
    border: none;
    height: 40px;
    font-size: 18px;
    border-radius: 5px;
    padding-left: 10px;
    background-color: #404EED;
    color: white;
    font-weight: bold;
'''
accountButton = '''
    border: none;
    height: 40px;
    font-size: 18px;
    border: 0.5px solid gray;
    border-radius: 5px;
    padding-left: 10px;
    color: black;
'''
def GET_USER_PASS_FROM_DATA_BY_ID(id):
    sqliteConnection = sqlite3.connect('./database/data.sqlite')
    cursor = sqliteConnection.cursor()
    cursor.execute("SELECT * FROM users WHERE id=?", (id,))
    rows = cursor.fetchall()
    for row in rows:
        return row[5]

def GET_USER_BY_ID(id):
    sqliteConnection = sqlite3.connect('./database/data.sqlite')
    cursor = sqliteConnection.cursor()
    cursor.execute("SELECT * FROM users WHERE id=?", (id,))
    rows = cursor.fetchall()
    for row in rows:
        return row

def CHECK_IF_USER_EXISTS(id):
    sqliteConnection = sqlite3.connect('./database/data.sqlite')
    cursor = sqliteConnection.cursor()
    cursor.execute("SELECT * FROM users WHERE id=?", (id,))
    cursor.execute('select exists(select 1 from users where id = ?)', (id,))
    [exists] = cursor.fetchone() 
    if exists:
        return True
    else:
        return False

def UPDATE_USER_BALANCE(account, target_id, money):
    sqliteConnection = sqlite3.connect('./database/data.sqlite')
    cursor = sqliteConnection.cursor()
    cursor.execute("UPDATE users SET balance = ? WHERE id = ?", (account.balance, account.id,))
    target_user = GET_USER_BY_ID(target_id)
    user = Account(target_user[0], target_user[1], target_user[2], target_user[3], target_user[4], target_user[5], target_user[6])
    user.addMoney(money)
    cursor.execute("UPDATE users SET balance = ? WHERE id = ?", (user.balance, user.id,))
    sqliteConnection.commit()
    return True
  

def REGISTER_NEW_ACCOUNT(name, surname, age, gender, id, pin, balance):
    try:
        sqliteConnection = sqlite3.connect('./database/data.sqlite')
        cursor = sqliteConnection.cursor()
        cursor.execute("INSERT INTO users (name, surname, age, gender, id, pin, balance) values (?, ?, ?, ?, ?, ?, ?)",
            (name, surname, age, gender, id, pin, balance))
        sqliteConnection.commit()
        print("New Account Registered Successfully")
        cursor.close()
    except sqlite3.Error as error:
        print("Failed to register an account: ", error)
    finally:
        if (sqliteConnection):
            sqliteConnection.close()
            print("The SQLite connection is closed")

def INITIATE_ACCOUNT(account):
    return Account(account[0], account[1], account[2], account[3], account[4], account[5], account[6])

def GET_ALL_ACCOUNTS():
    sqliteConnection = sqlite3.connect('./database/data.sqlite')
    cursor = sqliteConnection.cursor()
    cursor.execute("SELECT * FROM users")
    rows = cursor.fetchall()
    for row in rows:
        new_account = INITIATE_ACCOUNT(row)
        accounts.append(new_account)
    return accounts
   

def generateRandomID(n):
    range_start = 10**(n-1)
    range_end = (10**n)-1
    return randint(range_start, range_end)

class RegisterWindow(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Registration")
        self.setIcon()
        self.resize(400, 100)
        self.confirmationWindow = None
        self.nameText = QtWidgets.QLabel("Name")
        self.nameText.setStyleSheet(headingStyle)
        self.name = QtWidgets.QLineEdit(placeholderText="Enter your name")
        self.name.setStyleSheet(inputStyle)
        self.surnameText = QtWidgets.QLabel("Surname")
        self.surnameText.setStyleSheet(headingStyle)
        self.surname = QtWidgets.QLineEdit(placeholderText="Enter your surname")
        self.surname.setStyleSheet(inputStyle)
        self.ageText = QtWidgets.QLabel("Age")
        self.ageText.setStyleSheet(headingStyle)
        self.age = QtWidgets.QLineEdit(placeholderText="Enter your age")
        self.age.setStyleSheet(inputStyle)
        self.genderText = QtWidgets.QLabel("Gender")
        self.genderText.setStyleSheet(headingStyle)
        self.gender = QtWidgets.QComboBox()
        self.gender.setStyleSheet(inputStyle)
        self.gender.addItems(["Male", "Female"])
        self.idText = QtWidgets.QLabel("ID")
        self.idText.setStyleSheet(headingStyle)
        self.id = QtWidgets.QLineEdit(placeholderText="Enter your ID")
        self.id.setStyleSheet(inputStyle)
        self.pinText = QtWidgets.QLabel("PIN")
        self.pinText.setStyleSheet(headingStyle)
        self.pin = QtWidgets.QLineEdit(placeholderText="Enter your pin")
        self.pin.setEchoMode(QtWidgets.QLineEdit.Password)
        self.pin.setStyleSheet(inputStyle)
        self.register = QtWidgets.QPushButton("Register")
        self.register.setStyleSheet(buttonStyle)
        self.layout = QtWidgets.QVBoxLayout(self)
        self.layout.addWidget(self.nameText)
        self.layout.addWidget(self.name)
        self.layout.addWidget(self.surnameText)
        self.layout.addWidget(self.surname)
        self.layout.addWidget(self.ageText)
        self.layout.addWidget(self.age)
        self.layout.addWidget(self.genderText)
        self.layout.addWidget(self.gender)
        self.layout.addWidget(self.pinText)
        self.layout.addWidget(self.pin)
        self.layout.addWidget(self.register)
        self.register.clicked.connect(self.registerAccount)
    def setIcon(self):
        appIcon = QIcon("icon.png")
        self.setWindowIcon(appIcon)

    def showdialog(self, id):
        msg = QtWidgets.QMessageBox()
        msg.setIcon(msg.Information)
        msg.setText("New Account Registered Successfully")
        msg.setInformativeText("To enter your account use the ID {} and the pin that you selected. Save your ID for future logins".format(id))
        msg.setWindowTitle("Success")
        msg.setStandardButtons(msg.Ok)
        msg.exec()
    @QtCore.Slot()
    def registerAccount(self):
        newID = generateRandomID(10)
        if self.name.text() != "" and self.surname.text() != "" and self.age.text() != "" and self.pin.text() != "":
            REGISTER_NEW_ACCOUNT(self.name.text(), self.surname.text(), self.age.text(), self.gender.currentText(), newID, hashlib.md5(self.pin.text().encode()).hexdigest(), 0)
            self.showdialog(newID)
            self.destroy()

class LoginForm(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Bank System v{}".format(version))
        self.setIcon()
        self.window = None
        self.welcome = QtWidgets.QLabel("Welcome User. Login using your credentials")
        self.welcome.setStyleSheet(headingStyle);
        self.id = QtWidgets.QLineEdit(placeholderText="Enter your ID")
        self.id.setStyleSheet(inputStyle)
        self.pin = QtWidgets.QLineEdit(placeholderText="Enter your pin")
        self.pin.setStyleSheet(inputStyle)
        self.pin.setEchoMode(QtWidgets.QLineEdit.Password)
        self.login = QtWidgets.QPushButton("Sign in")
        self.login.setStyleSheet(buttonStyle)
        self.register = QtWidgets.QPushButton("Don't have account yet. Register")
        self.register.setStyleSheet(buttonStyle)
        self.layout = QtWidgets.QVBoxLayout(self)
        self.layout.addWidget(self.welcome)
        self.layout.addWidget(self.id)
        self.layout.addWidget(self.pin)
        self.layout.addWidget(self.login)
        self.layout.addWidget(self.register)
        self.login.clicked.connect(self.loginAction)
        self.register.clicked.connect(self.registerAction)

    def setIcon(self):
        appIcon = QIcon("icon.png")
        self.setWindowIcon(appIcon)

    def showdialog(self, text):
        msg = QtWidgets.QMessageBox()
        msg.setText(text)
        msg.setWindowTitle("Alert")
        msg.setStandardButtons(msg.Ok)
        msg.exec()

    @QtCore.Slot()
    def registerAction(self):
        if self.window is None:
            self.window = RegisterWindow()
            self.window.show()
        else:
            self.window = None

    @QtCore.Slot()
    def loginAction(self):
        if self.id.text() != "" and self.pin.text() != "":
            account = GET_USER_BY_ID(self.id.text())
            password = account[5]
            if password == hashlib.md5(self.pin.text().encode()).hexdigest():
                global active_account
                active_account = Account(account[0], account[1], account[2], account[3], account[4], account[5], account[6])
                if self.window is None:
                    self.window = AccountWindow(active_account)
                    self.window.show()
                    self.close()
                else:
                    self.window = None
            else:
                self.showdialog("Incorrect password or user does not exist")
        else:
            self.showdialog("ID or/and Pin fields cannot be empty")

class AdminPanel(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Admin Panel")
        self.resize(400, 100)
        self.setIcon()
        self.accountWindow = None
        self.layout = QtWidgets.QVBoxLayout(self)
        alls = GET_ALL_ACCOUNTS()
        self.heading = QtWidgets.QLabel("List of all registered accounts")
        self.heading.setStyleSheet('''
                font-size: 24px;
                font-weight: bold;
        ''')
        self.layout.addWidget(self.heading)
        for account in alls:
            self.account = QtWidgets.QPushButton("[{}] {} {}: ${}".format(account.id, account.name, account.surname, account.balance))
            self.account.setStyleSheet(accountButton);
            self.layout.addWidget(self.account)
        self.search = QtWidgets.QPushButton("Search")
        self.search.setStyleSheet(buttonStyle)
        self.back = QtWidgets.QPushButton("Back")
        self.back.setStyleSheet(buttonStyle)
        self.layout.addWidget(self.search)
        self.layout.addWidget(self.back)
        self.back.clicked.connect(self.goBack)
   
    @QtCore.Slot()
    def goBack(self):
        if self.accountWindow is None:
            self.accountWindow = AccountWindow(active_account   )
            self.accountWindow.show()
            global accounts
            accounts = list()   
            self.close()
        else:
            self.accountWindow = None    
    def setIcon(self):
        appIcon = QIcon("icon.png")
        self.setWindowIcon(appIcon)

class MoneyTransactionForm(QtWidgets.QWidget):
    def __init__(self, account, balanceText):
        super().__init__()
        self.setWindowTitle("Send money")
        self.resize(400, 100)
        self.setIcon()
        self.account = account
        self.balanceText = balanceText
        self.id = QtWidgets.QLineEdit(placeholderText="Enter the ID of the user")
        self.id.setStyleSheet(inputStyle)
        self.money = QtWidgets.QLineEdit(placeholderText="Enter the amount of money you would like to send")
        self.money.setStyleSheet(inputStyle)
        self.pin = QtWidgets.QLineEdit(placeholderText="Confirm your password")
        self.pin.setStyleSheet(inputStyle)
        self.pin.setEchoMode(QtWidgets.QLineEdit.Password)
        self.send = QtWidgets.QPushButton("Confirm")
        self.send.setStyleSheet(buttonStyle)
        self.layout = QtWidgets.QVBoxLayout(self)
        self.layout.addWidget(self.id)
        self.layout.addWidget(self.money)
        self.layout.addWidget(self.pin)
        self.layout.addWidget(self.send)
        self.send.clicked.connect(self.sendMoney)

    @QtCore.Slot()
    def sendMoney(self):
        if self.account.id != "" and self.money.text() != "" and self.id.text() and self.pin.text():
            password = self.account.pin
            if password == hashlib.md5(self.pin.text().encode()).hexdigest():  
                if CHECK_IF_USER_EXISTS(self.id.text()):
                    if self.account.removeMoney(self.money.text()):
                        if UPDATE_USER_BALANCE(self.account, self.id.text(), self.money.text()):
                            self.showdialog("${} sent from: {} to account {}".format(self.money.text(), self.account.id, self.id.text()), "Success")
                            self.balanceText.setText("Your Balance: ${}".format(self.account.balance))
                            self.destroy()
                        else:
                            self.showdialog("Something went wrong", "Error")
                    else:
                        self.showdialog("You don't have enough money to make this transaction", "Insufficient funds")
                else:
                    self.showdialog("User does not exist", "Error")
            else:
                self.showdialog("Incorrect password", "Error")

    def showdialog(self, text, title):
        msg = QtWidgets.QMessageBox()
        msg.setText(text)
        msg.setWindowTitle(title)
        msg.setStandardButtons(msg.Ok)
        msg.exec()

    def setIcon(self):
        appIcon = QIcon("icon.png")
        self.setWindowIcon(appIcon)

class AccountWindow(QtWidgets.QWidget):
    def __init__(self, account):
        super().__init__()
        self.setWindowTitle("Dashboard")
        self.resize(400, 100)
        self.setIcon()
        self.transactionWindow = None
        self.loginWindow = None
        self.adminPanel = None
        self.account = account
        self.welcome = QtWidgets.QLabel("Welcome back, {}".format(self.account.name))
        self.welcome.setStyleSheet(headingStyle);
        self.balance = QtWidgets.QLabel("Your Balance: ${}".format(self.account.balance))
        self.balance.setStyleSheet(headingStyle);
        self.send = QtWidgets.QPushButton("Send Money")
        self.send.setStyleSheet(buttonStyle)
        self.logout = QtWidgets.QPushButton("Log Out")
        self.logout.setStyleSheet(buttonStyle)
        self.logout.clicked.connect(self.logoutFunction)
        self.layout = QtWidgets.QVBoxLayout(self)
        self.layout.addWidget(self.welcome)
        self.layout.addWidget(self.balance)
        self.layout.addWidget(self.send)
        self.send.clicked.connect(self.openTransactionWindow)
        if self.account.id in administrators:
            self.admin = QtWidgets.QPushButton("Admin Panel")
            self.admin.setStyleSheet(buttonStyle)
            self.layout.addWidget(self.admin)
            self.admin.clicked.connect(self.openAdminPanel)
        self.layout.addWidget(self.logout)
    @QtCore.Slot()
    def openAdminPanel(self):
        if self.adminPanel is None:
            self.adminPanel = AdminPanel()
            self.adminPanel.show()
            self.close()
        else:
            self.adminPanel = None
        #print(active_account.id)

    @QtCore.Slot()
    def logoutFunction(self):
        if self.loginWindow is None:
            self.loginWindow = LoginForm()
            self.loginWindow.show()
            self.close()
        else:
            self.loginWindow = None

    @QtCore.Slot()
    def openTransactionWindow(self):
        if self.transactionWindow is None:
            self.transactionWindow = MoneyTransactionForm(self.account, self.balance)
            self.transactionWindow.show()
        else:
            self.transactionWindow = None

    def setIcon(self):
        appIcon = QIcon("icon.png")
        self.setWindowIcon(appIcon)

class Account:
    def __init__(account, name, surname, age, gender, id, pin, balance):
        account.name = name
        account.surname = surname
        account.age = age
        account.gender = gender
        account.balance = balance
        account.id = id
        account.pin = pin

    def addMoney(account, money):
        money = int(money)
        account.balance += money
    
    def removeMoney(account, money):
        money = int(money)
        if account.balance <= 0:
            print("Insufficient funds! The account doesn't have enough money")
            return False
        if money > account.balance:
            print("Insufficient funds! The account doesn't have enough money")
            return False
        else:
            account.balance -= money
            print("Removed {0} {1} from account: {2}".format(str(money), currency, account.name))
            return True
    
    def checkBalance(account):
        print(account.name)
        print(account.balance)

if __name__ == "__main__":
    app = QtWidgets.QApplication([])
    mainwindow = LoginForm()
    mainwindow.resize(400, 100)
    mainwindow.show()
    sys.exit(app.exec())