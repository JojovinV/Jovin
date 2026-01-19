import pygame
import random
import sys

# Data kuda Uma Musume
uma_musume = {
    "Special Week": {
        "sejarah": "Special Week adalah salah satu kuda legendaris di Uma Musume. Dia dikenal sebagai 'Empress' dan memiliki kemampuan luar biasa dalam balapan.",
        "rekor": "Memenangkan Triple Crown (Satsuki Sho, Tokyo Yushun, Kikuka Sho) dan berbagai kompetisi internasional lainnya."
    },
    "Silence Suzuka": {
        "sejarah": "Silence Suzuka adalah rival utama Special Week. Dia dikenal dengan kecepatannya yang luar biasa dan semangat juang yang tinggi.",
        "rekor": "Pemenang Japanese Derby, Tenno Sho, dan berbagai acara balapan elit."
    },
    "Gold Ship": {
        "sejarah": "Gold Ship adalah kuda jantan yang kuat dan tegas. Dia sering membantu teman-temannya dan dikenal dengan kekuatannya yang luar biasa.",
        "rekor": "Memenangkan Arima Kinen, Takarazuka Kinen, dan kompetisi lainnya dengan dominasi."
    },
    "Seiun Sky": {
        "sejarah": "Seiun Sky adalah kuda yang elegan dan misterius. Dia memiliki kemampuan untuk melihat masa depan dan sering memberikan nasihat.",
        "rekor": "Pemenang Hopeful Stakes dan berbagai balapan dengan catatan waktu yang impresif."
    },
    "King Halo": {
        "sejarah": "King Halo adalah kuda jantan yang bijak dan pemimpin. Dia dikenal dengan kepemimpinannya di tim.",
        "rekor": "Memenangkan Satsuki Sho dan balapan lainnya dengan strategi yang brilian."
    }
}

print("List Kuda Uma Musume:")
for name in uma_musume.keys():
    print(f"- {name}")

nama = input("Masukkan nama kuda: ").strip()

if nama in uma_musume:
    print(f"\nSejarah {nama}: {uma_musume[nama]['sejarah']}")
    print(f"Rekor Kemenangan: {uma_musume[nama]['rekor']}")
else:
    print("Nama kuda tidak ditemukan.")
