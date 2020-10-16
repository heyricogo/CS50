from cs50 import get_int

while True:
    height = get_int("Height : ")
    if height < 24 and height >= 0:
        for i in range(height):
            print((height - (i+1)) * " ", end="")
            print("#" * (i + 2), end = "")
            print()
        break



