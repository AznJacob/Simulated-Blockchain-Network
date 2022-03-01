from socket import *

serverPortF2 = ("localhost", 20000)
bufferSize = 2048

clientSocket = socket(AF_INET, SOCK_DGRAM)


def choice_one():
    print("Select the Payer:")
    print("1. B0000001")
    print("2. B0000002")
    payer = int(input("Choice: "))
    unconfirmed_tx_text = 'Unconfirmed_T_B.txt'
    if payer == 1:
        unconfirmed_balance_text = 'Unconfirmed_balance_B1.txt'
        payer_tx = "B0000001"
    else:
        unconfirmed_balance_text = 'Unconfirmed_balance_B2.txt'
        payer_tx = "B0000002"

    print("Select the Payee:")
    print("1. A0000001")
    print("2. A0000002")
    payee = int(input("Choice: "))
    if payee == 1:
        payee_tx = "A0000001"
    else:
        payee_tx = "A0000002"
    print("Enter the amount of payment in decimal")
    tx_amount = int(input())

    print(f'Tx:{payer_tx} pays {payee_tx} the amount of {tx_amount} BC.')

    tx_amount_with_fee = tx_amount + 2
    hexdigits = 8
    hexnumber = hex(tx_amount)
    hexlength = len(hexnumber) - 2
    hex_tx_amount = ('0' * (hexdigits - hexlength) + hexnumber[2:])
    tx_all = payer_tx + payee_tx + hex_tx_amount.upper()
    encoded_tx = tx_all.encode()

    with open(unconfirmed_balance_text, 'r') as rf:
        unconfirmed_balance = int(rf.read(), 16)

    if tx_amount_with_fee > unconfirmed_balance:
        print("Insufficient funds.")
    else:
        with open(unconfirmed_balance_text, 'w') as wf:
            new_unconfirmed_balance = hex(unconfirmed_balance - tx_amount_with_fee)[2:]
            hex_new_unconfirmed_balance = ('0' * (hexdigits - len(new_unconfirmed_balance)) + new_unconfirmed_balance)
            wf.write(hex_new_unconfirmed_balance.upper())
        with open(unconfirmed_tx_text, 'a') as af:
            af.write(tx_all)

        clientSocket.sendto(encoded_tx, serverPortF2)


def print_balances():
    print("Balances: ")
    with open('balance_B.txt', 'r') as rf:
        name = rf.read(8)
        unconfirmed_balance = int(rf.read(8), 16)
        confirmed_balance = int(rf.read(8), 16)
        print(f"{name}'s unconfirmed balance is {unconfirmed_balance} BC and confirmed balance is {confirmed_balance} BC.")
        name = rf.read(8)
        unconfirmed_balance = int(rf.read(8), 16)
        confirmed_balance = int(rf.read(8), 16)
        print(f"{name}'s unconfirmed balance is {unconfirmed_balance} BC and confirmed balance is {confirmed_balance} BC.")


def print_unconfirmed_transactions():
    with open('Unconfirmed_T_B.txt', 'r') as rf:
        text = rf.read()
        if text != '':
            print(f"Client B's unconfirmed transactions: {text}")
        else:
            print("There are no unconfirmed transactions yet for B")


def print_confirmed_transactions():
    with open('Confirmed_T_B.txt', 'r') as rf:
        text = rf.read()
        if text != '':
            print(f"Client B's confirmed transactions: {text}")
        else:
            print("There are no confirmed transactions yet for B")


def print_blockchain():
    with open('Blockchain.txt', 'r') as rf:
        print(rf.read())


def update_balances():
    with open("Confirmed_balance_B1.txt", "r") as rfc, open("Unconfirmed_balance_B1.txt", "r") as rfu:
        confirmed_balance_b1 = rfc.read()
        unconfirmed_balance_b1 = rfu.read()
        balances_b1 = "B0000001" + unconfirmed_balance_b1 + confirmed_balance_b1
    with open("Confirmed_balance_B2.txt", "r") as rfc, open("Unconfirmed_balance_B2.txt", "r") as rfu:
        confirmed_balance_b2 = rfc.read()
        unconfirmed_balance_b2 = rfu.read()
        balances_b2 = "B0000002" + unconfirmed_balance_b2 + confirmed_balance_b2
    all_balances = balances_b1 + balances_b2
    with open("balance_B.txt", "w") as wf:
        wf.write(all_balances)


def reset_everything():
    print("Resetting everything related to client B...")
    with open("Confirmed_balance_B1.txt", "w") as wfc, open("Unconfirmed_balance_B1.txt", "w") as wfu:
        wfc.write("000003E8")
        wfu.write("000003E8")
    with open("Confirmed_balance_B2.txt", "w") as wfc, open("Unconfirmed_balance_B2.txt", "w") as wfu:
        wfc.write("000003E8")
        wfu.write("000003E8")
    with open("Unconfirmed_T_B.txt", "w") as wfa:
        wfa.write('')
    with open("Confirmed_T_B.txt", "w") as wft:
        wft.write('')
    with open("Temp_T_F2.txt", "w") as wff:
        wff.write('')


def reset_flag():
    with open('flag.txt', 'w') as wf:
        wf.write('')


while True:
    print("Please make a choice from the following selection:")
    print("0: Reset everything (Change balances of accounts to 1000 BC again and empty transaction files)")
    print("1: Enter a new transaction.")
    print("2: The current balance for each account.")
    print("3: Print the unconfirmed transactions.")
    print("4: Print the confirmed transactions.")
    print("5: Print the blockchain.")
    print("6: Exit.")
    choice = int(input("Choice: "))
    update_balances()
    reset_flag()
    if choice == 0:
        reset_everything()
    elif choice == 1:
        choice_one()
    elif choice == 2:
        print_balances()
    elif choice == 3:
        print_unconfirmed_transactions()
    elif choice == 4:
        print_confirmed_transactions()
    elif choice == 5:
        print_blockchain()
    elif choice == 6:
        print("Exiting...")
        break
    else:
        print("Invalid choice.")