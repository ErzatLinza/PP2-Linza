class BankAccount:
    def __init__ (self,balance):
        self.balance = balance
        

    def withdraw(self, amount):
        self.amount = amount

        if self.amount > self.balance:
            print("You donot have that much money")
        else:

            print("your bank account has: ", self.balance - self.amount)
        
p1 = BankAccount(3000)
p1.withdraw(4000)

p1.withdraw(2000)
