def encode_msg(src):
	prefix = "<" + str(len(src)) + ">"
	encoded_msg = prefix + src
	encoded_msg = encoded_msg.encode()
	return encoded_msg

def decode_msg(src):
	decoded_msg = src.decode()
	msg = parse_decoded_msg(decoded_msg)
	return msg

def parse_decoded_msg(src):
	i = 1
	if src[0] != "<":
		return "CONVERT ERROR"
	else:
		while(src[i] != ">" and i < len(src)):
			i += 1
		msg_len = int(src[1:i])
		if msg_len > len(src[i:]):
			return "LEN ERROR"
		msg = src[i + 1:i + 1 + msg_len]
		return msg
