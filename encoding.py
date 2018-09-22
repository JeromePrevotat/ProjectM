def encode_msg(src):
	type_prefix = "<msg>"
	len_prefix = "<" + str(len(src)) + ">"
	encoded_msg = type_prefix + len_prefix + src
	encoded_msg = encoded_msg.encode()
	return encoded_msg

def encode_cmd(cmd):
	type_prefix = "<cmd>"
	len_prefix = "<" + str(len(cmd)) + ">"
	encoded_cmd = type_prefix + len_prefix + cmd
	encoded_cmd = encoded_cmd.encode()
	return encoded_cmd

def parse_type_received(src):
	received = ""
	length = 0
	cmd = -1
	if src[0:5] == "<cmd>":
		cmd = True
	elif src[0:5] == "<msg>":
		cmd = False
	else:
		print(src)
		print("TYPE ERROR")
	cmd, args, received, length = parse_received(cmd, src[5:])
	return cmd, args, received, length + len(str(length)) + 7

def parse_received(cmd, src):
	args = None
	msg = None
	#Get the len
	i = 1
	if src[0] != "<":
		return "CONVERT ERROR"
	while(i < len(src) and src[i] != ">"):
		i += 1
	msg_len = int(src[1:i])
	if msg_len > len(src[i:]):
		return "LEN ERROR"
	#Get command and args
	if cmd:
		#Get command
		j = i + 1
		while (j < len(src) and src[j] != "("):
			j += 1
		cmd = src[i + 1:j]
		#Get args
		k = j + 1
		while (k < len(src) and src[k] != ")"):
			k += 1
		args = src[j + 1:k]
	#Get the message
	if not cmd:
		msg = src[i + 1:i + 1 + msg_len]
	return cmd, args, msg, msg_len

if __name__ == "__main__":
	test = "request(test\n)"
	encoded_cmd = encode_cmd(test)
	i = 0
	while (i < 100000):
		cmd, args, msg, length = parse_type_received(encoded_cmd.decode())
		if cmd != "request":
			print(cmd)
		if args != "test\n":
			print("ARGS")
		if msg != None:
			print("MSG")
		i += 1