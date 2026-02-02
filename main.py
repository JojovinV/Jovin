import json

saldo = 0
pemasukan_list = []
pengeluaran_list = []
FILE_SALDO = "todolist_data.json"

def baca_saldo():
    global saldo, pemasukan_list, pengeluaran_list
    try:
        with open(FILE_SALDO, "r") as file:
            data = json.load(file)
            saldo = data.get("saldo", 0)
            pemasukan_list = data.get("pemasukan", [])
            pengeluaran_list = data.get("pengeluaran", [])
    except:
        saldo = 0
        pemasukan_list = []
        pengeluaran_list = []

def simpan_saldo():
    data = {"saldo": saldo, "pemasukan": pemasukan_list, "pengeluaran": pengeluaran_list}
    with open(FILE_SALDO, "w") as file:
        json.dump(data, file)

def tambah_pemasukan():
    global saldo
    jumlah = int(input("Masukkan jumlah pemasukan: "))
    saldo += jumlah
    pemasukan_list.append(jumlah)
    simpan_saldo()
    print(f"Pemasukan sebesar Rp{jumlah} berhasil ditambahkan!")

def tambah_pengeluaran():
    global saldo
    jumlah = int(input("Masukkan jumlah pengeluaran: "))
    if jumlah > saldo:
        print("Peringatan! Saldo tidak cukup.")
    else:
        saldo -= jumlah
        pengeluaran_list.append(jumlah)
        simpan_saldo()
        print(f"Pengeluaran sebesar Rp{jumlah} berhasil dikurangi!")

def lihat_saldo():
    print("=== Saldo Saat Ini ===")
    print(f"Rp{saldo:,}")

def lihat_laporan():
    total_pemasukan = sum(pemasukan_list)
    total_pengeluaran = sum(pengeluaran_list)
    
    print("\n=== Laporan Keuangan ===")
    print(f"Total Pemasukan: Rp{total_pemasukan:,}")
    print(f"Total Pengeluaran: Rp{total_pengeluaran:,}")
    print(f"Saldo Akhir: Rp{saldo:,}")
    print()

def menu():
    print("=== Aplikasi Pengelola Uang Saku ===")
    print("1. Tambah pemasukan")
    print("2. Tambah pengeluaran")
    print("3. Lihat saldo")
    print("4. Lihat laporan")
    print("5. Keluar")

baca_saldo()
while True:
    menu()
    pilihan = input("Pilih menu: ")

    if pilihan == "1":
        tambah_pemasukan()
    elif pilihan == "2":
        tambah_pengeluaran()
    elif pilihan == "3":
        lihat_saldo()
    elif pilihan == "4":
        lihat_laporan()
    elif pilihan == "5":
        print("Terima kasih!")
        break
    else:
        print("Pilihan tidak valid")