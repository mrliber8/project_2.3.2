'''
value = 'xyz'

value_altered = ''.join(chr(ord(letter)+1) for letter in value)

print(value_altered)


username_list = ["000000"]

for username in username_list:
    for letter in range(0, len(username)):
        print(username[letter])
        value_altered = ''.join(chr(ord(letter)+1) for letter in username)

        print(value_altered)

passwd = "0000000"
#
passwd = "1234567"


i = 0
list = list(passwd)

for _ in range(len(list)):
    i += -1
    print(list[i])
    list[i] = chr(ord(passwd[i]) + 1)

print(list)


passwd = "1234567"
list = list(passwd)
test = 0
i = -1
while test < 10:
    new_uni = ord(list[i]) + 1

    # NB. Het wachtwoord bestaat uit alleen kleine letters en cijfers.
    # Hoofdletters en speciale symbolen kunnen we dus overslaan
    if new_uni == 58:
        new_uni = 97

    list[i] = chr(new_uni)
    print(list)
    test += 1
'''
'''
def increment_string_recursive(s, index=None):
    # If the index is not specified, start with the last character
    if index is None:
        index = len(s) - 1
    
    if s == "zzzzzzz":
        return s
    
    s_list = list(s)
    
    def increment_char(c):
        if '0' <= c <= '8':
            return chr(ord(c) + 1), False
        elif c == '9':
            return 'a', False
        elif 'a' <= c <= 'y':
            return chr(ord(c) + 1), False
        else:  # c == 'z'
            return '0', True
    
    # Increment the character at the current index
    s_list[index], carry = increment_char(s_list[index])
    
    # If there's a carry and the current index is not the first character, recursively increment the next character to the left
    if carry and index > 0:
        result =  increment_string_recursive(''.join(s_list), index - 1)
    else:
        result =  ''.join(s_list)
    
    print(result)
    return result
    


current_string = "0000000"
final_string = "zzzzzzz"

while current_string != final_string:
    # Call the function with the current string
    current_string = increment_string_recursive(current_string)
    # The function itself prints each increment, so no need for additional printing here

'''



def increment_char(c):
    if '0' <= c <= '8':
        return chr(ord(c) + 1), False
    elif c == '9':
        return 'a', False
    elif 'a' <= c <= 'y':
        return chr(ord(c) + 1), False
    else:  # c == 'z'
        return '0', True


def find_password(dict):
    #{'000000': 7, '000001': 8}

    for stu_number, passwd_length in dict.items():

        # To start, create a list filled with 0's equal to the discovered length
        zero_list = [0] * passwd_length
        # {'000000': 7}
        # get unicode representation of the char

        for _ in range(25):
            start_time = time.perf_counter()
            call_server(student_number, password)
            end_time = time.perf_counter()
            duration = end_time - start_time
        pass

    return "hoi"


find_password({'000000': 7, '000001': 8})


#print(guess_list[0])
#print(len(guess_list))


'''
for x in range(len(guess_list)):
    print(guess_list[x])

    # Send x number of times
    for _ in range(20):
        start_time = time.perf_counter()
        call_server(student_number, password)
        end_time = time.perf_counter()
        duration = end_time - start_time

    # Timen

    # Gemiddelde berekenen
'''

