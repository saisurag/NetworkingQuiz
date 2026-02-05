# Networking Quiz Game

A simple networking-based quiz game using User Datagram Protocol (UDP) for communication. This project was done as part of the CPEG 460 Computer Networks course at Hamad Bin Khalifa University.

Client communicates with the central server using UDP, and is prompted with hard-coded multiple-choice questions.

# Technologies involved

- Client-server architecture
- Use of UDP Protocol for real-time communication
- Ports and sockets
- Unicast communication for direct communication
- JavaScript Object Notation (JSON) for packet format

# Reasons for Implementation

- Competitor to Kahoot but on a local machine using networking – playing on the same machine
- UDP allows for focus on faster communication and real-time updates – beneficial for engaging users
- Intrigue and interest in implementing concepts learnt in CPEG-460 but not covered practically (intentional deviation from TCP)

# Limitations

- Requires HTTPS, Web Browser, Web Socket
- Large delay mplementation period
- Question bank is limited and manually hard-coded
- Limited scalability due to thread reliance
- Lack of security and reliability due to UDP

# Future Works
-  Connect to 'https://the-trivia-api.com/' API to have larger question bank
-  Improve scalability via implementation of thread lock
