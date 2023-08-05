import socket
# Socket API is used to send messages across network via TCP.

global s, hostIP, port
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# Creates socket object with arguments specifying address family & socket type.
# AF_INET is the Internet address family for IPv4.
# SOCK_STREAM is the socket type for TCP.
hostIP, port = '10.0.0.15', '1234'
# Default HostIP and port for sending messages from client to server.


def client(message):
    """
    Allows a message to be sent from client to server via TCP,
    provided that the server is expecting a message,
    and that the bitlength of the message is less than or equal
    to that of which the server is expecting.

    Parameters:
    message(str): Message to be sent
    """
    s.connect((hostIP, port))
    # Establish connection to server and initiate three-way handshake.
    print(message)
    # Prints message to be sent to console
    s.send(message.encode())
    # Encodes message and sends it to the server.
    s.close
    # Socket closed to establish the completion of the message being sent.


def server_setup(listenDuration):
    """
    Establishes the server by setting up a listening socket
    on the same TCP port as that which the client uses to send messages.

    Parameters:
    listenDuration(int): Number of allowed unaccepted connections.
    """
    s.bind(('', port))
    # Associates the socket with a specific network interface and port.
    s.listen(listenDuration)
    # Enables the server to accept connections.


def server_recieve(bitLength):
    """
    Allows server to recieve message from client via TCP.

    Parameters:
    bitLength(int): Bit length of expected message to be received

    Returns:
    data(str): Recieved message
    """
    c, addr = s.accept()
    # Establish connection with client
    data = c.recv(bitLength).decode()
    # Accepts portion message, in accordance to the bitLength, and decodes it.
    c.close()
    # Socket closed to establish the completion of the message being recieved.
    return data


def setHostIP(IP):
    """
    Sets the Server IP address to desired value IP.

    Parameters:
    IP(str): An IP adress
    """
    global hostIP
    hostIP = IP
    # Replaces old IP address value with new IP argument.


def setPort(P):
    """
    Sets the TCP port to desired value P.
    Superuser privileges may be required for ports < 1024.
    If you are unsure, preferably use ports > 1023

    Parameters:
    P(str): A port number
    """
    global port
    port = P
    # Replaces old port value with new P argument.


def getHostIP():
    """
    Retreives the current Server IP address.

    Returns:
    hostIP(str): Current host IP
    """
    return hostIP


def getPort():
    """
    Retreives the current TCP port.

    Returns:
    hostIP(str): Current TCP port
    """
    return port
