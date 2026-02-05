import socket
import json
import time
import threading

def receive_question(client_socket):
    question_data, server_address = client_socket.recvfrom(1024)
    question_data = question_data.decode()
    return json.loads(question_data)

def send_answer(client_socket, answer, server_address):
    client_socket.sendto(answer.encode(), server_address)

def receive_feedback(client_socket):
    feedback, _ = client_socket.recvfrom(1024)
    return feedback.decode()

def play_quiz(client_socket, server_address):
    # Add a delay to ensure the client is ready
    time.sleep(1)

    try:
        client_socket.settimeout(30)
        while True:
            # Receive and display the question
            question_data = receive_question(client_socket)
            if not question_data:
                break  # Exit the loop if there is no question data

            print(f"\nQuestion: {question_data['question']}")
            for option in question_data['options']:
                print(option)

            # Record start time for the user to calculate the time taken
            start_time = time.time()

            # Get the user's answer
            user_answer = input("Your answer (Enter A, B, or C): ").upper()

            # Send the answer to the server
            send_answer(client_socket, user_answer, server_address)

            # Receive and display the feedback
            feedback = receive_feedback(client_socket)
            print(f"Feedback: {feedback}")

            # Record end time for the user to calculate the time taken
            end_time = time.time()
            time_taken = end_time - start_time
            print(f"Time taken: {time_taken:.2f} seconds")

    finally:
        client_socket.close()
        print("Client closed.")

def main():
    server_address = ('127.0.0.1', 8888)
    client = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    
    try:
        client.sendto("JOIN".encode(), server_address)

        start_signal, _ = client.recvfrom(1024)
        if start_signal.decode() == "START":
            # Start the quiz in the main thread (no need for threading here)
            play_quiz(client, server_address)

    finally:
        # Close the client socket when the quiz is finished
        client.close()
        print("Client closed.")

if __name__ == "__main__":
    main()
