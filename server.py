import socket
import json
import time
import threading

quiz_data = {
    "question1": {"question": "What is the capital of France?", "options": ["A. Berlin", "B. Madrid", "C. Paris"], "correct_answer": "C"},
    "question2": {"question": "Which planet is known as the Red Planet?", "options": ["A. Mars", "B. Venus", "C. Jupiter"], "correct_answer": "A"},
    "question3": {"question": "What is the largest mammal in the world?", "options": ["A. Elephant", "B. Blue Whale", "C. Giraffe"], "correct_answer": "B"},
    "question4": {"question": "What is the capital of Japan?", "options": ["A. Tokyo", "B. Beijing", "C. Seoul"], "correct_answer": "A"},
    "question5": {"question": "Which element has the chemical symbol 'O'?", "options": ["A. Oxygen", "B. Gold", "C. Silver"], "correct_answer": "A"},
    "question6": {"question": "Who painted the Mona Lisa?", "options": ["A. Leonardo da Vinci", "B. Vincent van Gogh", "C. Pablo Picasso"], "correct_answer": "A"},
    "question7": {"question": "What is the currency of Japan?", "options": ["A. Yen", "B. Won", "C. Ringgit"], "correct_answer": "A"},
    "question8": {"question": "Which country is known as the Land of the Rising Sun?", "options": ["A. Japan", "B. China", "C. South Korea"], "correct_answer": "A"},
    "question9": {"question": "What is the smallest prime number?", "options": ["A. 0", "B. 1", "C. 2"], "correct_answer": "C"},
    "question10": {"question": "Who developed the theory of relativity?", "options": ["A. Albert Einstein", "B. Isaac Newton", "C. Galileo Galilei"], "correct_answer": "A"},
    "question11": {"question": "Which planet is known as the Blue Planet?", "options": ["A. Earth", "B. Neptune", "C. Uranus"], "correct_answer": "A"},
    "question12": {"question": "In which year did World War II end?", "options": ["A. 1945", "B. 1939", "C. 1941"], "correct_answer": "A"},
    "question13": {"question": "What is the largest desert in the world?", "options": ["A. Sahara Desert", "B. Antarctica", "C. Gobi Desert"], "correct_answer": "B"},
    "question14": {"question": "Who wrote 'To Kill a Mockingbird'?", "options": ["A. Harper Lee", "B. J.K. Rowling", "C. Ernest Hemingway"], "correct_answer": "A"},
    "question15": {"question": "Which element has the chemical symbol 'H'?", "options": ["A. Hydrogen", "B. Helium", "C. Carbon"], "correct_answer": "A"},
    "question16": {"question": "What is the largest planet in our solar system?", "options": ["A. Jupiter", "B. Saturn", "C. Neptune"], "correct_answer": "A"},
    "question17": {"question": "Who is known as the 'Father of Computer Science'?", "options": ["A. Alan Turing", "B. Bill Gates", "C. Steve Jobs"], "correct_answer": "A"},
    "question18": {"question": "What is the capital of Australia?", "options": ["A. Sydney", "B. Melbourne", "C. Canberra"], "correct_answer": "C"},
    "question19": {"question": "In which year did the first manned moon landing occur?", "options": ["A. 1969", "B. 1971", "C. 1965"], "correct_answer": "A"},
    "question20": {"question": "Who wrote 'Pride and Prejudice'?", "options": ["A. Jane Austen", "B. Charlotte Brontë", "C. Emily Dickinson"], "correct_answer": "A"},
    "question21": {"question": "What is the capital of Brazil?", "options": ["A. Rio de Janeiro", "B. Brasília", "C. São Paulo"], "correct_answer": "B"},
    "question22": {"question": "Which mammal can fly?", "options": ["A. Bat", "B. Kangaroo", "C. Dolphin"], "correct_answer": "A"},
    "question23": {"question": "What is the main ingredient in guacamole?", "options": ["A. Avocado", "B. Tomato", "C. Onion"], "correct_answer": "A"},
    "question24": {"question": "Who painted 'Starry Night'?", "options": ["A. Vincent van Gogh", "B. Pablo Picasso", "C. Claude Monet"], "correct_answer": "A"},
    "question25": {"question": "What is the currency of South Africa?", "options": ["A. Rand", "B. Dollar", "C. Euro"], "correct_answer": "A"},
}


def send_question(server_socket, client_address, question_data):
    message = json.dumps(question_data)
    server_socket.sendto(message.encode(), client_address)

def handle_client(server_socket, client_address):
    total_points = 0
    for question_key, question_data in quiz_data.items():
        send_question(server_socket, client_address, question_data)

        # Record start time for the client to calculate the time taken
        start_time = time.time()

        # Receive the client's answer
        client_answer, _ = server_socket.recvfrom(1024)
        client_answer = client_answer.decode().upper()

        # Calculate the time taken
        end_time = time.time()
        time_taken = end_time - start_time

        # Check the answer
        correct_answer = question_data["correct_answer"]
        if client_answer == correct_answer:
            # Calculate points based on the time taken
            points = int(1000 / time_taken)  # Adjust the scoring mechanism as needed
            total_points += points
            feedback = f"\nCorrect! You earned {points} points. Total points: {total_points}"
        else:
            feedback = f"\nWrong! The correct answer is {correct_answer}. You earned 0 points. Total points: {total_points}"

        # Send feedback to the client
        server_socket.sendto(feedback.encode(), client_address)

def main():
    server = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    server.bind(('127.0.0.1', 8888))

    # Set a 30-second timeout for the server socket
    server.settimeout(30)

    print("Server waiting for players to join...")

    clients = set()

    try:
        while len(clients) < 1:
            client_request, client_address = server.recvfrom(1024)
            client_request = client_request.decode().upper()

            if client_request == "JOIN":
                clients.add(client_address)
                print(f"Player at {client_address} joined the game.")

        # Signal all clients to start the game
        for client in clients:
            server.sendto("START".encode(), client)

        # Handle each client in a separate thread
        threads = []
        for client in clients:
            thread = threading.Thread(target=handle_client, args=(server, client))
            threads.append(thread)
            thread.start()

        # Wait for all threads to finish
        for thread in threads:
            thread.join()

    finally:
        # Close the server socket only after all threads have finished
        server.close()
        print("Server closed.")

if __name__ == "__main__":
    main()
