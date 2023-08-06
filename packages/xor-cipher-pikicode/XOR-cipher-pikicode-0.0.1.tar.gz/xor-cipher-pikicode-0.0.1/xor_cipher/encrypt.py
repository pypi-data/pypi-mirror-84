import sys
import base64

def encrypt(key, input_file, output_file):
    data = ''
    with open(input_file, 'r') as file:
        data = file.read()
    data_len = len(data)
    key_len = len(key)
    key=data_len//key_len*key+key[:data_len%key_len]
    # print(key)
    # print(data)
    encrypted = []
    with open(output_file, 'w') as file:
        for i in range(len(key)):
        	encrypted.append(chr(ord(key[i])^ord(data[i])))
        encrypted = ''.join(encrypted).encode('utf-8')
        encrypted = base64.b64encode(encrypted).decode('utf-8')
        file.write(encrypted)
#----------end of encrypt-----------
def decrypt(key, input_file, output_file):
    with open(input_file, 'r') as file:
        data = file.read()
    data = base64.b64decode(data.encode('utf-8')).decode('utf-8')
    data_len = len(data)
    key_len = len(key)
    key=data_len//key_len*key+key[:data_len%key_len]

    result = []
    for i in range(len(key)):
        result.append(chr(ord(data[i])^ord(key[i])))
    result=''.join(result)
    with open(output_file, 'w') as file:
        file.write(result)
#-------end of decrypt----------
#python encrypt.py 'action' 'input file' 'output file' 'key'
if __name__ == '__main__':
    action = sys.argv[1]
    input_ = sys.argv[2]
    output = sys.argv[3]
    try:
        key = sys.argv[4]
    except:
        import getpass
        key = getpass.getpass(prompt='Input Key: ')
    # print(key)
    if action == 'e':
        encrypt(key,input_,output)
    elif action == 'd':
        decrypt(key, input_, output)
