import tkinter as tk
from tkinter import scrolledtext, END
from threading import Thread
import socket

class ChatGUI:
    def __init__(self):
        self.window = tk.Tk()
        self.window.title("Lan Chat(project)")
        
        # Text area to display messages
        self.message_area = scrolledtext.ScrolledText(self.window)
        self.message_area.pack(fill=tk.BOTH, expand=True)
        
        # Input field to type messages
        self.input_field = tk.Entry(self.window)
        self.input_field.pack(side=tk.LEFT, fill=tk.X, expand=True)
        
        # Send button
        self.send_button = tk.Button(self.window, text="Send", command=self.send_message)
        self.send_button.pack(side=tk.RIGHT)
        
        # self.input_field.bind('<Return>',self.send_message)
        
        self.client_socket = None
        self.receive_thread = None
        
    def run(self):
        self.window.mainloop()
        
    def send_message(self):
        message = self.input_field.get()
        self.input_field.delete(0, tk.END)
        
        if self.client_socket is not None:
            # Send the message to the server
            self.client_socket.send(message.encode('utf-8'))
            self.display_message(message, "You")
        
    def display_message(self, message, sender):
        formatted_message = f"{sender}: {message}\n"
        self.message_area.insert(tk.END, formatted_message)
        self.message_area.see(tk.END)

    def start_client_program(self):
        # Create a socket object
        self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        
        # Connect to the server
        self.client_socket.connect(('127.0.0.1', 5555))  # Replace with the server IP and port
        
        # Start a new thread to receive messages from the server
        self.receive_thread = Thread(target=self.receive_messages)
        self.receive_thread.daemon = True
        self.receive_thread.start()
        
    def receive_messages(self):
        while True:
            try:
                # Receive messages from the server
                message = self.client_socket.recv(1024).decode('utf-8')
                sender_ip = self.client_socket.getpeername()[0]
                self.display_message(message, sender_ip)
            except:
                # Handle server disconnection
                print('Disconnected from the server')
                self.client_socket.close()
                break

# Example usage
if __name__ == "__main__":
    gui = ChatGUI()
    gui.start_client_program()  # Start the client program and socket connection
    gui.run()
