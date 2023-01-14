
import random
import socket
import chatlib
import select

# GLOBALS
users = {}
questions = {}
logged_users = {}
messages_to_send = []

ERROR_MSG = "Error! "
SERVER_PORT = 5678
SERVER_IP = "127.0.0.1"

def build_and_send_message(conn, code, msg):
    """
    Builds a new message using chatlib, wanted code and message.
    Prints debug info, then sends it to the given socket.
    Parameters: conn (socket object), code (str), data (str)
    Returns: Nothing
    """
    full_msg = chatlib.build_message(code, msg)
    messages_to_send.append((conn, full_msg.encode()))
    conn.send(full_msg.encode())
    print("[SERVER] ", conn.getpeername(), full_msg)  # Debug print

def recv_message_and_parse(conn):
    """
    Receives a new message from given socket,
    then parses the message using chatlib.
    Parameters: conn (socket object)
    Returns: cmd (str) and data (str) of the received message.
    If error occurred, will return None, None
    """
    try:
        full_msg = conn.recv(10021).decode()
    except ConnectionResetError as error:
        print(error)
        return None, None
    cmd, data = chatlib.parse_message(full_msg)
    print("[CLIENT] ", conn.getpeername(), full_msg)  # Debug print
    return cmd, data

def print_client_socket(sockets_list):
    for sock in sockets_list:
        address = sock.getpeername()
        print("IP: " + address[0] + ", Port: " + str(address[1]))

def load_questions():
    """
    Loads questions bank from file to complete
    Receives: -
    Returns: questions dictionary
    """
    global questions
    questions = {
        2313: {"question": "How much is 2+2", "answers": ["3", "4", "2", "1"], "correct": 2},
        4122: {"question": "What is the capital of France?", "answers": ["Lion", "Marseille", "Paris", "Montpelier"],
               "correct": 3}
    }

    return questions

def load_user_database():
    """
    Loads users list from file to complete
    Receives: -
    Returns: user dictionary
    """
    global users
    users = {
        "test": {"password": "test", "score": 0, "questions_asked": []},
        "yossi": {"password": "123", "score": 50, "questions_asked": []},
        "master": {"password": "master", "score": 200, "questions_asked": []}
    }
    return users

def setup_socket():
    """
    Creates new listening socket and returns it
    Receives: -
    Returns: the socket object
    """
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.bind((SERVER_IP, SERVER_PORT))
    sock.listen()
    print("listening....")

    return sock

def send_error(conn, error_msg):
    """
    Send error message with given message
    Receives: socket, message error string from called function
    Returns: None
    """
    build_and_send_message(conn, chatlib.PROTOCOL_SERVER["error_msg"], error_msg)

def handle_getscore_message(conn, username):
    global users
    score = users[username]["score"]
    build_and_send_message(conn, chatlib.PROTOCOL_SERVER["score_msg"], str(score))

def handle_logout_message(conn):
    """
    Closes the given socket (in later chapters, also remove user from logged_users dictionary)
    Receives: socket
    Returns: None
    """
    global logged_users
    user = conn.getpeername()
    if user in logged_users:
        print("the user: {" + logged_users.pop(user) + "} logout and disconnected")
    else:
        print("the user disconnected")
    conn.close()

def is_login(conn):
    return conn.getpeername() in logged_users

def handle_login_message(conn, data):
    """
    Gets socket and message data of login message. Checks  user and pass exists and match.
    If not - sends error and finished. If all ok, sends OK message and adds user and address to logged_users
    Receives: socket, message code and data
    Returns: None (sends answer to client)
    """
    global users  # needed to access the same users dictionary from all functions
    global logged_users  # used later

    [username, password] = chatlib.split_data(data, 2)
    if username in users:
        if users[username]["password"] == password:
            if not is_login(conn):
                build_and_send_message(conn, chatlib.PROTOCOL_SERVER["login_ok_msg"], "")
                logged_users[conn.getpeername()] = username
            else:
                send_error(conn, "this user already login")
        else:
            send_error(conn, "the password didn't match")
    else:
        send_error(conn, "the username doesn't exist")

def handle_highscore_massage(conn):
    global users
    # sort usernames by score from highest to lowest
    highscore = sorted(users, key=lambda u: users[u]["score"], reverse=True)
    # build highscore data in string
    highscore_data = ""
    for user in highscore:
        highscore_data = highscore_data + "\t" + user + ":" + str(users[user]["score"]) + "\n"

    build_and_send_message(conn, chatlib.PROTOCOL_SERVER["highscore_msg"], highscore_data)

def handle_client_message(conn, cmd, data):
    """
    Gets message code and data and calls the right function to handle command
    Receives: socket, message code and data
    Returns: None
    """
    global logged_users
    if cmd == chatlib.PROTOCOL_CLIENT["login_msg"]:
        handle_login_message(conn, data)
    elif not is_login(conn):
        send_error(conn, "command before login")
    #    elif cmd == chatlib.PROTOCOL_CLIENT["logout_msg"]:
    #        handle_logout_message(conn)
    elif cmd == chatlib.PROTOCOL_CLIENT["score_msg"]:
        handle_getscore_message(conn, logged_users[conn.getpeername()])
    elif cmd == chatlib.PROTOCOL_CLIENT["highscore_msg"]:
        handle_highscore_massage(conn)
    elif cmd == chatlib.PROTOCOL_CLIENT["logged_users_msg"]:
        handle_logged_message(conn)
    elif cmd == chatlib.PROTOCOL_CLIENT["get_quest_msg"]:
        handle_question_massage(conn)
    elif cmd == chatlib.PROTOCOL_CLIENT["answer_msg"]:
        handle_answer_massage(conn, logged_users[conn.getpeername()], data)
    else:
        send_error(conn, "command didn't recognized")

def handle_logged_message(conn):
    logged_str = ','.join(logged_users.values())
    build_and_send_message(conn, chatlib.PROTOCOL_SERVER["logged_users_list"], logged_str)

def handle_question_massage(conn):
    build_and_send_message(conn, chatlib.PROTOCOL_SERVER["quest_msg"], create_random_question())

def handle_answer_massage(conn, username, answer_data):
    [quest_num, client_answer] = chatlib.split_data(answer_data, 2)
    correct_answer = str(questions[int(quest_num)]["correct"])
    if correct_answer == client_answer:
        users[username]["score"] += 5
        build_and_send_message(conn, chatlib.PROTOCOL_SERVER["correct_answer_msg"], "")
    else:
        build_and_send_message(conn, chatlib.PROTOCOL_SERVER["wrong_answer_msg"], correct_answer)

def create_random_question():
    quest_num = random.choice(list(questions.keys()))
    question = questions[quest_num]

    full_quest_msg = str(quest_num) + chatlib.DATA_DELIMITER + question["question"] + chatlib.DATA_DELIMITER
    full_quest_msg += chatlib.DATA_DELIMITER.join(question["answers"]) + chatlib.DATA_DELIMITER + str(
        question["correct"])

    return full_quest_msg

def main():

    global users, questions, messages_to_send

    print("Welcome to Trivia Server!")

    load_questions()
    load_user_database()
    server_sock = setup_socket()

    client_sockets_list = []
    while True:
        ready_to_read, ready_to_write, in_error = select.select([server_sock] + client_sockets_list, client_sockets_list, [])
        for current_socket in ready_to_read:
            if current_socket is server_sock:
                (client_socket, client_address) = server_sock.accept()
                print("\nnew client connected", client_address)
                client_sockets_list.append(client_socket)
                print_client_socket(client_sockets_list)
            else:
                try:
                    cmd, data = recv_message_and_parse(current_socket)
                    if cmd is None or cmd == chatlib.PROTOCOL_CLIENT["logout_msg"]:
                        print("client logout" + str(current_socket.getpeername()))
                        client_sockets_list.remove(current_socket)
                        handle_logout_message(current_socket)
                    elif cmd in chatlib.PROTOCOL_CLIENT.values():
                        handle_client_message(current_socket, cmd, data)
                    else:
                        send_error(current_socket, "invalid cmd")
                        print("ERROR: client sent:", cmd, ":", data)
                except ConnectionResetError:
                    client_sockets_list.remove(current_socket)
                    handle_logout_message(current_socket)

        for out_msg in messages_to_send:
            current_socket, data = out_msg
            if current_socket in ready_to_write:
                try:
                    current_socket.send(data)
                except ConnectionResetError:
                    print("user disconnected")
                    handle_logout_message(current_socket)

if __name__ == '__main__':
    main()