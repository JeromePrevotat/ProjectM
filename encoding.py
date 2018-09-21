if __name__ == "__main__":
	msg = "yolo"
	print(len(msg))
	print(len(msg.encode('utf-8')))
	print(len(msg.encode()))
	encoded_msg = msg.encode()
	print(type(encoded_msg))
	print(len(encoded_msg))
def encode_msg(src):
	msg_length = len(src)
	prefix = "<" + str(msg_length) + ">"
	encoded_msg = prefix + src
	return encoded_msg

def decode_msg(src):
	print(type(src))