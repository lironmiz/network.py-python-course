# Protocol Constants

CMD_FIELD_LENGTH = 16  # Exact length of cmd field (in bytes)
LENGTH_FIELD_LENGTH = 4   # Exact length of length field (in bytes)
MAX_DATA_LENGTH = 10**LENGTH_FIELD_LENGTH-1  # Max size of data field according to protocol
MSG_HEADER_LENGTH = CMD_FIELD_LENGTH + 1 + LENGTH_FIELD_LENGTH + 1  # Exact size of header (CMD+LENGTH fields)
MAX_MSG_LENGTH = MSG_HEADER_LENGTH + MAX_DATA_LENGTH  # Max size of total message
DELIMITER = "|"  # Delimiter character in protocol
DATA_DELIMITER = "#"  # Delimiter in the data part of the message

# Protocol Messages
# In this dictionary we will have all the client and server command names

PROTOCOL_CLIENT = {
	"login_msg": "LOGIN",
	"logout_msg": "LOGOUT",
	"score_msg": "MY_SCORE",
	"highscore_msg": "HIGHSCORE",
	"logged_users_msg": "LOGGED",
	"get_quest_msg": "GET_QUESTION",
	"answer_msg": "SEND_ANSWER"
}

PROTOCOL_SERVER = {
	"login_ok_msg": "LOGIN_OK",
	"login_failed_msg": "ERROR",
	"score_msg": "YOUR_SCORE",
	"highscore_msg": "ALL_SCORE",
	"logged_users_list": "LOGGED_ANSWER",
	"quest_msg": "YOUR_QUESTION",
	"correct_answer_msg": "CORRECT_ANSWER",
	"wrong_answer_msg": "WRONG_ANSWER",
	"no_quest_msg": "NO_QUESTION",
	"error_msg": "ERROR"
}

ERROR_RETURN = None  # What is returned in case of an error

def build_message(cmd, data):
	"""
	Gets command name (str) and data field (str) and creates a valid protocol message
	Returns: str, or None if error occurred
	:type cmd: str
	:type data: str
	"""
	if len(cmd) > CMD_FIELD_LENGTH or len(data) > MAX_DATA_LENGTH:
		return None
	full_cmd = cmd + " "*(CMD_FIELD_LENGTH-len(cmd))
	data_len = str(len(data))
	full_data_len = "0"*(LENGTH_FIELD_LENGTH-len(data_len))+data_len
	full_msg = DELIMITER.join([full_cmd, full_data_len, data])
	return full_msg

def parse_message(data):
	"""
	Parses protocol message and returns command name and data field
	Returns: cmd (str), data (str). If some error occurred, returns None, None
	:type data: str
	"""
	list_data = data.split("|")
	cmd = list_data[0]
	if len(list_data) != 3 or len(cmd) != CMD_FIELD_LENGTH:
		return None, None
	data_len = list_data[1].replace(" ", "")
	data_len1 = list_data[1]
	if len(data_len1) != LENGTH_FIELD_LENGTH or not data_len.isdigit():
		return None, None
	msg = list_data[2]
	data_len = int(data_len)
	if len(msg) != data_len \
		or not 0 <= data_len <= 9999:
		return None, None
	cmd = cmd.replace(" ", "")
	return cmd, msg

def split_data(msg, expected_fields):
	"""
	Helper method. gets a string and number of expected fields in it. Splits the string
	using protocol's data field delimiter (|#) and validates that there are correct number of fields.
	Returns: list of fields if all ok. If some error occurred, returns None
	:type expected_fields: int
	:type msg: str
	"""
	msg_split = msg.split(DATA_DELIMITER)
	if len(msg_split) == expected_fields:
		return msg_split
	return []

def join_data(msg_fields):
	"""
	Helper method. Gets a list, joins all of it's fields to one string divided by the data delimiter.
	Returns: string that looks like cell1#cell2#cell3
	:type msg_fields: list
	"""
	for i in range(len(msg_fields)):
		msg_fields[i] = str(msg_fields[i])
	return DATA_DELIMITER.join(msg_fields)
