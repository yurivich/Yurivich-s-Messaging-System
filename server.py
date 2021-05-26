import socket
import time
import requests
import socketserver
import sys
import threading
from datetime import date


class Service(socketserver.BaseRequestHandler):
    def ask_creds(self):

        self.send(b"Welcome To Yurivich's Messaging System... This program is still in development, but if you want to contribute, here is my page : https://github.com/yurivich/Yurivich-s-Messaging-System / Thank You :D")
        first = self.receive(b"First Name : ").decode("utf-8").strip()
        if first == "":
            self.send(b"First Name is required!")
            exit()
        last = self.receive(b"Last Name : ").decode("utf-8").strip()
        if last == "":
            self.send(b"Last Name is required!")
            exit()
        year = self.receive(
            b"In what year were you born? : ").decode("utf-8").strip()
        if year == "":
            self.send(b"Gotta specify a year good sir!")
            exit()
        self.send(b"Calculating your age...")
        time.sleep(2.5)
        todays_date = date.today()
        calc = eval("%s - %s" % (todays_date.year, year))
        self.send(b"Calculations Finished...")
        time.sleep(1)

        email = self.receive(b"Your email : ").decode("utf-8").strip()
        if email == "":
            self.send(b"Email is Required!")
            exit()
        if "@" not in email:
            self.send(b"The @ sign is required!")
            exit()
        password_input = self.receive(b"Password : ").decode("utf-8").strip()
        if password_input == "":
            self.send(b"Passsword Cannot Be Empty!")
            exit()
        confirm_input = self.receive(
            b"Confirm Password : ").decode("utf-8").strip()
        if password_input != confirm_input:
            self.send(b"Passwords do not match")
            exit()
        test = self.receive(
            b"Are you sure you want to register? Y/N : ").decode("utf-8").strip()
        if test == "Y" or "y":
            time.sleep(2)
            self.send(
                b"Thank you for registering... Your account will be active shortly...")
            # Saving User's Account Details | We'll create the accounts later
            file = open("requests.txt", "w")
            input = ["First Name : "+first+" Last Name : "+last +
                     " Email : "+email+" Password : "+password_input+" Age ", calc]
            file.writelines(str(input))
            file.close()
        else:
            cancel = self.receive(
                b"Canceling your request...").decode("utf-8").strip()

    def handle(self):
        signup = self.ask_creds()

    def send(self, string, newline=True):
        if newline:
            string = string + b"\n"
        self.request.sendall(string)

    def receive(self, prompt=b"> "):
        self.send(prompt, newline=False)
        return self.request.recv(4096).strip()


class ThreadedService(
    socketserver.ThreadingMixIn,
    socketserver.TCPServer,
    socketserver.DatagramRequestHandler,
):
    pass


def main():
    print("Starting server...")
    port = 7018
    host = "127.0.0.1"

    service = Service
    server = ThreadedService((host, port), service)
    server.allow_reuse_address = True

    server_thread = threading.Thread(target=server.serve_forever)

    server_thread.daemon = True
    server_thread.start()

    print("Server started on" + str(server.server_address) + "!")

    while True:
        time.sleep(10)


if __name__ == "__main__":
    main()
