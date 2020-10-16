import sys
import cs50


def main():
    while True:
        # handles lack of argv[1]
        if sys.argv[1]:
            # Get the key
            key = int(sys.argv[1])
            if key >= 0:
                # Get the plaintext
                plaintext = cs50.get_string("plaintext: ")
                print("ciphertext: ", end="")
                # Encipher
                for char in plaintext:
                    if char.isalpha():
                        if char.islower():
                            p = ((ord(char) - 97 + key) % 26) + 97
                            print(chr(p), end="")
                        if char.isupper():
                            p = ((ord(char) - 65 + key) % 26) + 65
                            print(chr(p), end="")
                    else:
                        print(char, end="")
                print()
                break
            break
        else:
            print("Please enter a key number")
            return 1
        return 0


if __name__ == "__main__":
    main()