def read_fees():
    with open("fees.txt", "r") as file:
        return file.read()


print(read_fees())