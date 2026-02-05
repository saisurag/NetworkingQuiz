import tkinter as tk
from tkinter import messagebox
from threading import Thread
import socket
import json

class QuizClient:
    def __init__(self, root, server_address):
        self.root = root
        self.server_address = server_address
        self.root.title("Quiz Game")
        self.root.geometry("600x400")

        self.question_label = tk.Label(root, text="", font=("Helvetica", 14))
        self.question_label.pack(pady=10)

        self.option_buttons = []
        for i in range(3):
            button = tk.Button(root, text="", font=("Helvetica", 12), command=lambda i=i: self.send_answer(chr(65 + i)))
            button.pack(pady=5)
            self.option_buttons.append(button)

        self.feedback_label = tk.Label(root, text="", font=("Helvetica", 12))
        self.feedback_label.pack(pady=10)

        self.socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.socket.settimeout(30)
        self.socket.sendto("JOIN".encode(), self.server_address)
        self.receive_thread = Thread(target=self.receive_data)
        self.receive_thread.start()

    def send_answer(self, answer):
        self.socket.sendto(answer.encode(), self.server_address)

    def receive_data(self):
        try:
            while True:
                data, _ = self.socket.recvfrom(1024)
                data = data.decode()
                
                if data == "START":
                    self.ask_question()
                elif data.startswith("{"):
                    question_data = json.loads(data)
                    self.display_question(question_data)
                else:
                    self.display_feedback(data)

        except socket.timeout:
            messagebox.showinfo("Game Over", "The quiz has ended.")
            self.root.destroy()

    def ask_question(self):
        self.feedback_label.config(text="")
        self.socket.settimeout(30)  # Set a timeout for answering each question

    def display_question(self, question_data):
        question = question_data["question"]
        options = question_data["options"]
        self.question_label.config(text=question)

        for i in range(3):
            self.option_buttons[i].config(text=options[i])

    def display_feedback(self, feedback):
        self.feedback_label.config(text=feedback)


def main():
    root = tk.Tk()
    server_address = ('127.0.0.1', 8888)  # Replace with the server's IP and port
    client = QuizClient(root, server_address)
    root.mainloop()


if __name__ == "__main__":
    main()
