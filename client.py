import socket
import chatlib
import sys

SERVER_IP = "127.0.0.1"
SERVER_PORT = 5678

def build_and_send_message(conn, code, data):
    """
    Builds a new message using chatlib, wanted code and message.
    Prints debug info, then sends it to the given socket.
    Paramaters: conn (socket object), code (str), data (str)
    Returns: None
    """
    full_msg = chatlib.build_message(code, data)
    # conn.send(full_msg.encode())
    print("\n*massage sent*\ncommand:", code, "\ndata:", data, "\nsend:", full_msg)

def recv_message_and_parse(conn):
    """
    Recieves a new message from given socket,
    then parses the message using chatlib.
    Paramaters: conn (socket object)
    Returns: cmd (str) and data (str) of the received message.
    If error occured, will return None, None
    """
    msg = conn.recv(10021).decode()
    cmd, data = chatlib.parse_message(msg)
    return cmd, data

def build_send_recv_parse(conn, code, data=""):
    """
    function use the sending and receiving functions that i implemented in the previous section one after the other. The function will return
    the answer from the server in two strings, msg_code and data.
    Paramaters: conn (socket object),  code: (str), data: (str)
    Returns: msg_code, data
    """
    build_and_send_message(conn, code, data)
    return  recv_message_and_parse(conn)

def connect():
    """
    Connects to the server
    Paramaters: None
    Returns: socket object if connected, None otherwise
    """
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect((SERVER_IP, SERVER_PORT))
    return client_socket

def error_and_exit(error_msg):
    """
    Prints an error message and exits the program
    Paramaters: error_msg: error message to be printed
    Returns: None
    """
    print("Error found: \n", error_msg)
    sys.exit()

def login(conn):
    """
    Connects to the server using a username and password
    Paramaters: conn: socket object
    Returns: None
    """
    username = input("Please enter username: \n")
    password = input("Please enter your password: \n")
    login_msg = username+chatlib.DATA_DELIMITER+password
    build_and_send_message(conn, chatlib.PROTOCOL_CLIENT["login_msg"], login_msg)
    answer = recv_message_and_parse(conn)
    while answer[0] != chatlib.PROTOCOL_SERVER["login_ok_msg"]:
        print("\nERROR! ")
        print(answer[1])
        username = input("Please enter username: \n")
        password = input("Please enter your password: \n")
        login_msg = username + chatlib.DATA_DELIMITER + password
        build_and_send_message(conn, chatlib.PROTOCOL_CLIENT["login_msg"], login_msg)
        answer = recv_message_and_parse(conn)
    print("logged-in")

def logout(conn):
    """
    Sends a logout command to the server
    Paramaters: conn: socket object
    Returns: None
    """
    build_and_send_message(conn, chatlib.PROTOCOL_CLIENT["logout_msg"], "")
    print("goodbye")

def get_score(conn):
    """
    Function which accepts a socket and prints the user's current score.
    Paramaters: conn: socket object
    Returns: None
    """
    ask = chatlib.PROTOCOL_CLIENT["score_msg"]
    cmd, data = build_send_recv_parse(conn, ask, "")
    if cmd != chatlib.PROTOCOL_SERVER["score_msg"]:
        error_and_exit(data)
    else:
        print("Your score is:", data, "points.")

def get_highscore(conn):
    """
    Gets a socket and prints the Highscores table
    Paramaters: conn: socket object
    Returns: None
    """
    ask = chatlib.PROTOCOL_CLIENT["highscore_msg"]
    cmd, data = build_send_recv_parse(conn, ask, "")
    if cmd != chatlib.PROTOCOL_SERVER["highscore_msg"]:
        error_and_exit(data)
    else:
        print("\nThe score of all players:\n" + data)

def connect():
    """
    Connect to a server
    Paramaters: None
    Returns: conn: socket object
    """
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect((SERVER_IP, SERVER_PORT))
    return client_socket

def play_question(conn):
    """
    The function accepts socket and plays a question
    Paramaters: conn: socket object
    Returns: None
    """
    quest = build_send_recv_parse(conn, chatlib.PROTOCOL_CLIENT["get_quest_msg"])
    if quest[0] == chatlib.PROTOCOL_SERVER["no_quest_msg"]:
        print("There is no available questions for you.")
        return None
    if quest[0] == chatlib.PROTOCOL_SERVER["error_msg"]:
        error_and_exit(quest[1])
    elif quest[0] == chatlib.PROTOCOL_SERVER["quest_msg"]:
        quest_data = quest[1].split(chatlib.DATA_DELIMITER)
        num = quest_data[0]
        question = quest_data[1]
        answers = [quest_data[2], quest_data[3], quest_data[4], quest_data[5]]
        print("\nQ: ", question)
        for i in range(1, 5):
            print("\t"+str(i)+":\t"+answers[i-1])
        ans_try = input("Choose an answer [1-4]: ")
        while ans_try not in ["1", "2", "3", "4"]:
            ans_try = input("Enter the number of your choice: ")
        score = build_send_recv_parse(conn, chatlib.PROTOCOL_CLIENT["answer_msg"], num+chatlib.DATA_DELIMITER+ans_try)
        if score[0] == chatlib.PROTOCOL_SERVER["correct_answer_msg"]:
            print("Correct!")
        elif score[0] == chatlib.PROTOCOL_SERVER["wrong_answer_msg"]:
            print("Wrong... the correct answer is: #"+score[1])
        else:
            error_and_exit(score[1])

def get_logged_users(conn):
    """
    Server accepts a socket and prints the list of all users currently connected to the server.
    Paramaters: conn: socket object
    Returns: None
    """
    logged_users = build_send_recv_parse(conn, chatlib.PROTOCOL_CLIENT["logged_users_msg"])
    if logged_users[0] == chatlib.PROTOCOL_SERVER["logged_users_list"]:
        print("Logged_users:\n"+logged_users[1])
    else:
        error_and_exit(logged_users[1])

def main():
    client_sock = connect()
    login(client_sock)
    choice = input("""
           p       Play a trivia question
           s       Get my score
           h       Get highscore
           l       Get logged users
           q       Quit
           -Enter your choice: """)
    while choice != "q":
        if choice == "p":
            play_question(client_sock)
        elif choice == "s":
            get_score(client_sock)
        elif choice == "h":
            get_highscore(client_sock)
        elif choice == "l":
            get_logged_users(client_sock)
        else:
            print("Enter the letter of your choice: ")

    choice = input("""
           p       Play a trivia question
           s       Get my score
           h       Get highscore
           l       Get logged users
           q       Quit
           -Enter your choice: """)
    print("Bye!")

    logout(client_sock)
    client_sock.close()

if __name__ == '__main__':
    main()