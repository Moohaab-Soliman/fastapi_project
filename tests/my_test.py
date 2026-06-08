import pytest
def add(num1 : int, num2 ):
    return num1 + num2


@pytest.fixture()
def zero_bank_account():
    return BankAccount()

@pytest.fixture()
def bank_account():
    return BankAccount(50)


@pytest.mark.parametrize("x,y,result",[
    (3,4,7),
    (5, 5, 10),
    (1, 3, 4),
])
def test_add(x,y,result):
    print("testing add function")
    assert add(x,y) == result


class InsufficientException(Exception):
    pass

class BankAccount:
    def __init__(self, initial_balance = 0):
        self.balance = initial_balance

    def withdraw(self, amount :int):
        if self.balance < amount:
            raise InsufficientException("Insufficient account balance")
        self.balance -= amount

    def deposit(self, amount):
        self.balance += amount

    def interest_rate(self):
        self.balance *= 1.1



def test_set_init_balance(bank_account):
    assert bank_account.balance == 50

def test_init_balance(zero_bank_account):
    assert zero_bank_account.balance == 0

def test_withdraw(bank_account):
    bank_account.withdraw(10)
    assert bank_account.balance == 40

def test_deposit(bank_account):
    bank_account.deposit(10)
    assert bank_account.balance == 60

def test_collect_interest(bank_account):
    bank_account.interest_rate()
    assert round(bank_account.balance,6) == 55

def test_bank_insufficient_balance(bank_account):
    with pytest.raises(InsufficientException):
        bank_account.withdraw(200)
