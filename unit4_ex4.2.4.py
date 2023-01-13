# exercise 4.2.4 from unit 4
'''
Look at the line of code in front of you

ready_to_read, ready_to_write, in_error = select.select([server_socket] + client_sockets, [], [])

Why transfer the server's socket object (server_socket) to the select function?

'''

# Answer: To know which sockets new customers want to connect

