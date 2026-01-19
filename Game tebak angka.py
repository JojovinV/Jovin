#Game tebak angka

secret_number = 67
guess = 0
while guess != secret_number:
    guess = int(input("Tebak angka antara 1-100: "))
    if guess < secret_number:
        print("Terlalu kecil!")
    elif guess > secret_number:
        print("Terlalu besar!")
print("Selamat! Anda menebak angka dengan benar.")