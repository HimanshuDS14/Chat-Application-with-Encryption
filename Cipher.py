def encrypt(text , key):
    result = ""
    for i in range(len(text)):
        char = text[i]
        
        if char.isupper():
            result = result + chr(( (ord(char) + key-65) %26 +65))
        elif char == " ":
            result = result + " "

        elif char.islower():
            result+=chr( (ord(char)+key-97)%26 +97)
        elif char.isnumeric():
            result+=chr((ord(char)+key-48)%10+48)
        else:
            result = result+char

    return result


def decrypt(text, key):
    result = ""
    for i in range(len(text)):
        char = text[i]

        if char.isupper():
            result = result + chr(((ord(char) - key - 65) % 26 + 65))
        elif char == " ":
            result = result +" "
        elif char.islower():
            result += chr((ord(char) - key - 97) % 26 + 97)
        elif char.isnumeric():
            result += chr((ord(char)-key-48)%10+48)
        else:
            result = result + char
    return result

