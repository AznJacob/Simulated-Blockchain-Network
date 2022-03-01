from socket import *

serverPort = 10001
serverSocket = socket(AF_INET, SOCK_DGRAM)
serverSocket.bind(("localhost", serverPort))
bufferSize = 2048

print("Client A is ready to receive.")
while True:
    clientAddress = serverSocket.recvfrom(2048)
    received_confirmation = clientAddress[0].decode()
    if received_confirmation[0] == 'A':
        with open("Unconfirmed_T_A.txt", 'r') as rf:
            unconfirmed_tx = rf.read()

        if unconfirmed_tx == received_confirmation:
            with open("Confirmed_balance_A1.txt", "w") as wf, open("Unconfirmed_balance_A1.txt", "r") as rf:
                balance_a1 = rf.read()
                wf.write(balance_a1)
            with open("Confirmed_balance_A2.txt", "w") as wf, open("Unconfirmed_balance_A2.txt", "r") as rf:
                balance_a2 = rf.read()
                wf.write(balance_a2)
            with open("Confirmed_T_A.txt", "a") as af, open("Unconfirmed_T_A.txt", "w") as wf:
                wf.write("")
                af.write(received_confirmation)


    else:
        with open("Confirmed_T_A.txt", "a") as af:
            af.write(received_confirmation)
        tx_amount1 = int(received_confirmation[16:24], 16)
        tx_amount2 = int(received_confirmation[40:48], 16)
        tx_amount3 = int(received_confirmation[64:72], 16)
        tx_amount4 = int(received_confirmation[88:96], 16)

        with open("Unconfirmed_balance_A1.txt", 'r') as rf1, open("Unconfirmed_balance_A2.txt") as rf2:
            balance_a1 = int(rf1.read(), 16)
            balance_a2 = int(rf2.read(), 16)

        if received_confirmation[15] == '1':
            balance_a1 += tx_amount1
        else:
            balance_a2 += tx_amount1

        if received_confirmation[39] == '1':
            balance_a1 += tx_amount2
        else:
            balance_a2 += tx_amount2

        if received_confirmation[63] == '1':
            balance_a1 += tx_amount3
        else:
            balance_a2 += tx_amount3

        if received_confirmation[87] == '1':
            balance_a1 += tx_amount4
        else:
            balance_a2 += tx_amount4

        new_balance_a1 = hex(balance_a1)[2:]

        new_balance_a2 = hex(balance_a2)[2:]

        hex_balance_a1 = ('0' * (8 - len(new_balance_a1)) + new_balance_a1).upper()
        hex_balance_a2 = ('0' * (8 - len(new_balance_a2)) + new_balance_a2).upper()

        with open("Confirmed_balance_A1.txt", "w") as wfc, open("Unconfirmed_balance_A1.txt", "w") as wfu:
            wfc.write(hex_balance_a1)
            wfu.write(hex_balance_a1)

        with open("Confirmed_balance_A2.txt", "w") as wfc, open("Unconfirmed_balance_A2.txt", "w") as wfu:
            wfc.write(hex_balance_a2)
            wfu.write(hex_balance_a2)