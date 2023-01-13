# exercise 2.3.5 from unit 2
'''
Ido wrote a client and ran it against the echo server. To his surprise, he got the following error.

Traceback (most recent call last):
File "C:/idos_client.py", line 5, in <module>
idos_socket.send("hey there")
TypeError: a bytes-like object is required, not 'str'

'''

# Answer: The encode method is not used
