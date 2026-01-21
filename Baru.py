import random
import os
from datetime import datetime

class RunnerTrainingGame:
    def __init__(self):
        # Statistik pemain
        self.speed = 50
        self.power = 50
        self.stamina = 50
        self.current_stamina = 100  # Bar stamina saat ini
        self.max_stamina = 100
        
        # Countdown dan kompetisi (RANDOM)
        self.days_left = random.randint(10, 15)
        self.competition_day = self.days_left
        
        # Minimum poin untuk menang (RANDOM)
        self.min_points_to_win = random.randint(170, 200)
        
        # Kondisi pemain
        self.is_injured = False
        self.injury_type = None
        self.fatigue_level = 0  # 0 normal, 1-3 fatigue ringan sampai berat
        
        # Riwayat event
        self.daily_event = None
        self.last_action = None
        
        # Leadboard (pesaing AI)
        self.competitors = self.generate_competitors()
    
    def generate_competitors(self):
        """Generate pesaing AI untuk leadboard"""
        names = ["Bambang Pelari", "Siti Kecepatan", "Rudi Kuat", "Maya Sprint", "Budi Marathoner", "Rina Petir", "Hendra Terukir", "Novi Kilat"]
        competitors = []
        for i, name in enumerate(names):
            score = random.randint(180, 280)
            competitors.append({"rank": i + 1, "name": name, "score": score})
        competitors.sort(key=lambda x: x["score"], reverse=True)
        for i, comp in enumerate(competitors):
            comp["rank"] = i + 1
        return competitors
        
    def clear_screen(self):
        """Bersihkan layar terminal"""
        os.system('clear' if os.name == 'posix' else 'cls')
    
    def display_header(self):
        """Tampilkan header game"""
        self.clear_screen()
        print("=" * 70)
        print("🏃 RUNNER TRAINING CHAMPIONSHIP 🏃".center(70))
        print("=" * 70)
        print()
    
    def get_effective_stats(self):
        """Hitung stat efektif dengan mempertimbangkan cedera/kelelahan"""
        speed_eff = self.speed
        power_eff = self.power
        stamina_eff = self.stamina
        
        # Kurangi stat jika cedera
        if self.is_injured:
            speed_eff = int(self.speed * 0.7)
            power_eff = int(self.power * 0.7)
            stamina_eff = int(self.stamina * 0.7)
        
        # Kurangi stat jika lelah
        if self.fatigue_level > 0:
            reduction = 1 - (self.fatigue_level * 0.15)
            speed_eff = int(speed_eff * reduction)
            power_eff = int(power_eff * reduction)
            stamina_eff = int(stamina_eff * reduction)
        
        return speed_eff, power_eff, stamina_eff
    
    def display_status(self):
        """Tampilkan status pemain"""
        self.display_header()
        
        # Countdown
        print(f"⏰ COUNTDOWN KOMPETISI: {self.days_left} hari tersisa")
        if self.days_left <= 3:
            print("   ⚠️  WAKTUNYA HAMPIR HABIS!")
        print()
        
        # Statistik dengan efek cedera
        print("📊 STATISTIK PEMAIN:")
        speed_eff, power_eff, stamina_eff = self.get_effective_stats()
        
        speed_display = f"{speed_eff}/100 (dari {self.speed})" if self.is_injured or self.fatigue_level > 0 else f"{self.speed}/100"
        power_display = f"{power_eff}/100 (dari {self.power})" if self.is_injured or self.fatigue_level > 0 else f"{self.power}/100"
        stamina_display = f"{stamina_eff}/100 (dari {self.stamina})" if self.is_injured or self.fatigue_level > 0 else f"{self.stamina}/100"
        
        print(f"   Speed:    {self.create_bar(speed_eff, 100)} {speed_display}")
        print(f"   Power:    {self.create_bar(power_eff, 100)} {power_display}")
        print(f"   Stamina:  {self.create_bar(stamina_eff, 100)} {stamina_display}")
        print()
        
        # Energy bar (stamina bar saat ini)
        print("⚡ ENERGY BAR (Energi Latihan):")
        print(f"   {self.create_bar(self.current_stamina, self.max_stamina)} {self.current_stamina}/{self.max_stamina}")
        print()
        
        # Kondisi kesehatan
        print("💪 KONDISI KESEHATAN:")
        if self.is_injured:
            print(f"   ❌ TERLUKA: {self.injury_type}")
            print("      (Pergi ke rumah sakit untuk penyembuhan)")
        elif self.fatigue_level > 0:
            fatigue_text = ["Sedikit lelah", "Cukup lelah", "Sangat lelah"][self.fatigue_level - 1]
            print(f"   ⚠️  KELELAHAN: {fatigue_text}")
            print("      (Efektivitas latihan berkurang)")
        else:
            print("   ✅ Sehat dan segar!")
        print()
    
    def create_bar(self, current, maximum, length=20):
        """Buat visual bar"""
        percentage = (current / maximum) * 100
        filled = int((percentage / 100) * length)
        bar = "█" * filled + "░" * (length - filled)
        return bar
    
    def main_menu(self):
        """Menu utama game"""
        self.display_status()
        
        # Tampilkan info kompetisi
        print("📍 INFO KOMPETISI:")
        print(f"   Target Poin Minimum: {self.min_points_to_win}/300 untuk menang")
        print()
        
        print("📋 MENU UTAMA:")
        print("1. 🏋️  Latihan SPEED (Meningkatkan kecepatan)")
        print("2. 💪 Latihan POWER (Meningkatkan kekuatan)")
        print("3. 🫀 Latihan STAMINA (Meningkatkan stamina)")
        print("4. 😴 ISTIRAHAT (Isi energi, kurangi 1 hari)")
        print("5. 🏥 RUMAH SAKIT (Sembuhkan cedera, kurangi 1 hari)")
        print("6. 📖 Lihat Statistik Lengkap")
        print("7. 🏆 Lihat Leadboard")
        print("8. 🏁 Mulai Kompetisi")
        print("9. ❌ Keluar Game")
        print()
        print("=" * 70)
        
        return input("Pilih menu (1-9): ").strip()
    
    def trigger_daily_event(self):
        """Trigger random event pada setiap hari"""
        if self.is_injured or self.daily_event:
            return
        
        events = [
            {
                "name": "Sarapan Bergizi",
                "desc": "Kamu makan sarapan yang bergizi tinggi!",
                "effect": "speed",
                "value": 5
            },
            {
                "name": "Bersemangat",
                "desc": "Hari ini kamu merasa sangat bersemangat!",
                "effect": "power",
                "value": 5
            },
            {
                "name": "Istirahat Cukup",
                "desc": "Tidur malam yang nyenyak membuat stamina meningkat!",
                "effect": "stamina",
                "value": 5
            },
            {
                "name": "Cedera Ringan",
                "desc": "Kamu terkilir saat latihan!",
                "effect": "injury",
                "injury": "Terkilir"
            },
            {
                "name": "Kelelahan Ekstrem",
                "desc": "Terlalu sering latihan tanpa istirahat yang cukup!",
                "effect": "fatigue",
                "level": 3
            },
            {
                "name": "Cuaca Bagus",
                "desc": "Cuaca cerah membuat semangat latihan meningkat!",
                "effect": "none"
            }
        ]
        
        event = random.choice(events)
        
        if event["effect"] == "speed":
            self.speed = min(100, self.speed + event["value"])
            print(f"✨ EVENT: {event['name']}")
            print(f"   {event['desc']}")
            print(f"   +{event['value']} Speed!")
        elif event["effect"] == "power":
            self.power = min(100, self.power + event["value"])
            print(f"✨ EVENT: {event['name']}")
            print(f"   {event['desc']}")
            print(f"   +{event['value']} Power!")
        elif event["effect"] == "stamina":
            self.stamina = min(100, self.stamina + event["value"])
            print(f"✨ EVENT: {event['name']}")
            print(f"   {event['desc']}")
            print(f"   +{event['value']} Stamina!")
        elif event["effect"] == "injury":
            self.is_injured = True
            self.injury_type = event["injury"]
            print(f"⚠️  EVENT: {event['name']}")
            print(f"   {event['desc']}")
            print(f"   Efektivitas latihan berkurang 50%!")
        elif event["effect"] == "fatigue":
            self.fatigue_level = event["level"]
            print(f"⚠️  EVENT: {event['name']}")
            print(f"   {event['desc']}")
            print(f"   Efektivitas latihan berkurang {event['level']*20}%!")
        else:
            print(f"✨ EVENT: {event['name']}")
            print(f"   {event['desc']}")
        
        print()
        input("Tekan ENTER untuk melanjutkan...")
        self.daily_event = event["name"]
    
    def training_speed(self):
        """Latihan Speed"""
        self.display_header()
        print("🏃 LATIHAN SPEED")
        print("=" * 70)
        
        # Cek energy
        if self.current_stamina < 15:
            print("❌ Energi terlalu rendah untuk latihan!")
            print(f"   (Energi saat ini: {self.current_stamina}/100)")
            print("   Gunakan ISTIRAHAT untuk mengisi energi.")
            input("Tekan ENTER untuk kembali...")
            return
        
        # Cek kondisi kesehatan
        if self.is_injured:
            print(f"❌ Kamu terluka ({self.injury_type})!")
            print("   Tidak bisa latihan. Pergi ke rumah sakit terlebih dahulu.")
            input("Tekan ENTER untuk kembali...")
            return
        
        # Random chance
        risk_of_failure = max(0, (100 - self.current_stamina) // 10)  # 0-10% risk
        
        self.current_stamina -= 15
        self.days_left -= 1
        
        # Cek apakah latihan berhasil
        if random.randint(0, 100) < risk_of_failure:
            print("❌ Latihan GAGAL!")
            print(f"   Energi terlalu rendah, latihan tidak efektif!")
            print(f"   Energi sekarang: {self.current_stamina}/100")
            print(f"   Hari tersisa: {self.days_left}")
        else:
            # Hitung peningkatan
            base_gain = random.randint(3, 8)
            
            # Kurangi efektivitas jika ada kondisi negatif
            if self.fatigue_level > 0:
                effectiveness = 1 - (self.fatigue_level * 0.2)
                base_gain = int(base_gain * effectiveness)
                print(f"⚠️  Efektivitas latihan berkurang karena kelelahan!")
            
            self.speed = min(100, self.speed + base_gain)
            
            print(f"✅ Latihan SPEED BERHASIL!")
            print(f"   +{base_gain} Speed ({self.speed}/100)")
            print(f"   -15 Energy ({self.current_stamina}/100)")
            print(f"   Hari tersisa: {self.days_left}")
        
        self.trigger_daily_event()
        input("Tekan ENTER untuk kembali...")
    
    def training_power(self):
        """Latihan Power"""
        self.display_header()
        print("💪 LATIHAN POWER")
        print("=" * 70)
        
        # Cek energy
        if self.current_stamina < 20:
            print("❌ Energi terlalu rendah untuk latihan!")
            print(f"   (Energi saat ini: {self.current_stamina}/100)")
            print("   Gunakan ISTIRAHAT untuk mengisi energi.")
            input("Tekan ENTER untuk kembali...")
            return
        
        # Cek kondisi kesehatan
        if self.is_injured:
            print(f"❌ Kamu terluka ({self.injury_type})!")
            print("   Tidak bisa latihan. Pergi ke rumah sakit terlebih dahulu.")
            input("Tekan ENTER untuk kembali...")
            return
        
        # Random chance
        risk_of_failure = max(0, (100 - self.current_stamina) // 10)  # 0-10% risk
        
        self.current_stamina -= 20
        self.days_left -= 1
        
        # Cek apakah latihan berhasil
        if random.randint(0, 100) < risk_of_failure:
            print("❌ Latihan GAGAL!")
            print(f"   Energi terlalu rendah, latihan tidak efektif!")
            print(f"   Energi sekarang: {self.current_stamina}/100")
            print(f"   Hari tersisa: {self.days_left}")
        else:
            # Hitung peningkatan
            base_gain = random.randint(3, 8)
            
            # Kurangi efektivitas jika ada kondisi negatif
            if self.fatigue_level > 0:
                effectiveness = 1 - (self.fatigue_level * 0.2)
                base_gain = int(base_gain * effectiveness)
                print(f"⚠️  Efektivitas latihan berkurang karena kelelahan!")
            
            self.power = min(100, self.power + base_gain)
            
            print(f"✅ Latihan POWER BERHASIL!")
            print(f"   +{base_gain} Power ({self.power}/100)")
            print(f"   -20 Energy ({self.current_stamina}/100)")
            print(f"   Hari tersisa: {self.days_left}")
        
        self.trigger_daily_event()
        input("Tekan ENTER untuk kembali...")
    
    def training_stamina(self):
        """Latihan Stamina"""
        self.display_header()
        print("🫀 LATIHAN STAMINA")
        print("=" * 70)
        
        # Cek energy
        if self.current_stamina < 25:
            print("❌ Energi terlalu rendah untuk latihan!")
            print(f"   (Energi saat ini: {self.current_stamina}/100)")
            print("   Gunakan ISTIRAHAT untuk mengisi energi.")
            input("Tekan ENTER untuk kembali...")
            return
        
        # Cek kondisi kesehatan
        if self.is_injured:
            print(f"❌ Kamu terluka ({self.injury_type})!")
            print("   Tidak bisa latihan. Pergi ke rumah sakit terlebih dahulu.")
            input("Tekan ENTER untuk kembali...")
            return
        
        # Random chance
        risk_of_failure = max(0, (100 - self.current_stamina) // 10)  # 0-10% risk
        
        self.current_stamina -= 25
        self.days_left -= 1
        
        # Cek apakah latihan berhasil
        if random.randint(0, 100) < risk_of_failure:
            print("❌ Latihan GAGAL!")
            print(f"   Energi terlalu rendah, latihan tidak efektif!")
            print(f"   Energi sekarang: {self.current_stamina}/100")
            print(f"   Hari tersisa: {self.days_left}")
        else:
            # Hitung peningkatan
            base_gain = random.randint(3, 8)
            
            # Kurangi efektivitas jika ada kondisi negatif
            if self.fatigue_level > 0:
                effectiveness = 1 - (self.fatigue_level * 0.2)
                base_gain = int(base_gain * effectiveness)
                print(f"⚠️  Efektivitas latihan berkurang karena kelelahan!")
            
            self.stamina = min(100, self.stamina + base_gain)
            
            print(f"✅ Latihan STAMINA BERHASIL!")
            print(f"   +{base_gain} Stamina ({self.stamina}/100)")
            print(f"   -25 Energy ({self.current_stamina}/100)")
            print(f"   Hari tersisa: {self.days_left}")
        
        self.trigger_daily_event()
        input("Tekan ENTER untuk kembali...")
    
    def rest(self):
        """Istirahat untuk isi energy"""
        self.display_header()
        print("😴 ISTIRAHAT")
        print("=" * 70)
        
        self.current_stamina = self.max_stamina
        self.days_left -= 1
        
        # Mengurangi fatigue
        if self.fatigue_level > 0:
            self.fatigue_level -= 1
            print("✅ Istirahat yang nyenyak mengurangi kelelahan!")
        
        print(f"✅ Istirahat selesai!")
        print(f"   Energy terisi penuh: {self.current_stamina}/{self.max_stamina}")
        print(f"   Hari tersisa: {self.days_left}")
        
        self.trigger_daily_event()
        input("Tekan ENTER untuk kembali...")
    
    def hospital(self):
        """Pergi ke rumah sakit"""
        self.display_header()
        print("🏥 RUMAH SAKIT")
        print("=" * 70)
        
        self.days_left -= 1
        
        if self.is_injured:
            self.is_injured = False
            self.injury_type = None
            print("✅ Cedera berhasil disembuhkan!")
            print(f"   Hari tersisa: {self.days_left}")
        elif self.fatigue_level > 0:
            self.fatigue_level = 0
            print("✅ Kelelahan berhasil dikurangi!")
            print(f"   Hari tersisa: {self.days_left}")
        else:
            print("✅ Pemeriksaan kesehatan selesai!")
            print("   Kondisi kesehatan baik-baik saja!")
            print(f"   Hari tersisa: {self.days_left}")
        
        self.trigger_daily_event()
        input("Tekan ENTER untuk kembali...")
    
    def show_stats(self):
        """Tampilkan statistik lengkap"""
        self.display_header()
        print("📊 STATISTIK LENGKAP")
        print("=" * 70)
        print()
        print(f"Speed:        {self.create_bar(self.speed, 100)} {self.speed}/100")
        print(f"Power:        {self.create_bar(self.power, 100)} {self.power}/100")
        print(f"Stamina:      {self.create_bar(self.stamina, 100)} {self.stamina}/100")
        print()
        print(f"Energy Bar:   {self.create_bar(self.current_stamina, self.max_stamina)} {self.current_stamina}/{self.max_stamina}")
        print()
        print(f"Hari Tersisa: {self.days_left} hari")
        print()
        
        # Analisis performa
        total_stats = self.speed + self.power + self.stamina
        avg_stats = total_stats // 3
        
        print("📈 ANALISIS PERFORMA:")
        if avg_stats >= 80:
            print("   ⭐ Performa LUAR BIASA! Kamu siap untuk kompetisi!")
        elif avg_stats >= 60:
            print("   👍 Performa BAIK! Masih ada ruang untuk improvement.")
        elif avg_stats >= 40:
            print("   😐 Performa CUKUP! Butuh lebih banyak latihan.")
        else:
            print("   ⚠️  Performa RENDAH! Tingkatkan latihan sekarang!")
        
        print()
        input("Tekan ENTER untuk kembali...")
    
    def show_leadboard(self):
        """Tampilkan leadboard kompetisi"""
        self.display_header()
        print("🏆 LEADBOARD KOMPETISI 🏆")
        print("=" * 70)
        print()
        
        # Hitung skor pemain saat ini
        player_score = self.speed + self.power + self.stamina
        
        # Buat list untuk sorting
        all_competitors = self.competitors.copy()
        all_competitors.append({"rank": 0, "name": "ANDA", "score": player_score, "is_player": True})
        all_competitors.sort(key=lambda x: x["score"], reverse=True)
        
        # Cari posisi pemain
        player_rank = 0
        for i, comp in enumerate(all_competitors):
            if comp.get("is_player", False):
                player_rank = i + 1
                break
        
        # Tampilkan top 10
        print(f"\n{'RANK':<6} {'NAMA':<20} {'SKOR':<10}")
        print("-" * 70)
        
        for i, comp in enumerate(all_competitors[:10]):
            if comp.get("is_player", False):
                print(f"#{i+1:<5} {comp['name']:<20} {comp['score']:<10} ← ANDA")
            else:
                print(f"#{i+1:<5} {comp['name']:<20} {comp['score']:<10}")
        
        print()
        print(f"Posisi Anda: {player_rank}/{len(all_competitors)}")
        print(f"Skor Anda: {player_score}/300")
        print(f"Minimum untuk menang: {self.min_points_to_win}/300")
        
        if player_rank == 1:
            print("\n🥇 ANDA ADALAH JUARA! 🥇")
        elif player_rank <= 3:
            print(f"\n🏅 Anda sedang di posisi ke-{player_rank}!")
        
        print()
        input("Tekan ENTER untuk kembali...")
    
    def competition(self):
        """Mulai kompetisi"""
        self.display_header()
        print("🏁 KOMPETISI DIMULAI!")
        print("=" * 70)
        print()
        
        # Total score
        total_score = self.speed + self.power + self.stamina
        
        print(f"Final Speed:   {self.speed}/100")
        print(f"Final Power:   {self.power}/100")
        print(f"Final Stamina: {self.stamina}/100")
        print(f"Total Score:   {total_score}/300")
        print()
        
        # Buat final leadboard
        all_competitors = self.competitors.copy()
        all_competitors.append({"rank": 0, "name": "ANDA", "score": total_score, "is_player": True})
        all_competitors.sort(key=lambda x: x["score"], reverse=True)
        
        player_rank = 0
        for i, comp in enumerate(all_competitors):
            if comp.get("is_player", False):
                player_rank = i + 1
                break
        
        print(f"Anda berada di posisi: #{player_rank}/{len(all_competitors)-1}")
        print()
        
        # Cek apakah menang
        if total_score >= self.min_points_to_win:
            print("=" * 70)
            print(f"🏆 SELAMAT! KAMU MENANG KOMPETISI! JUARA {player_rank}/{len(all_competitors)-1} 🏆".center(70))
            print("=" * 70)
            print()
            
            if player_rank == 1:
                print("⭐ JUARA PERTAMA! ⭐")
                print("Kamu adalah pelari terbaik di championship ini!")
            elif player_rank <= 3:
                print(f"🥇 JUARA NOMOR {player_rank}! 🥇")
                print(f"Kamu berhasil naik ke podium!")
            else:
                print("🏅 PEMENANG! 🏅")
                print("Kamu berhasil memenangkan kompetisi ini!")
        else:
            print("=" * 70)
            print("❌ SAYANG! KAMU KALAH DALAM KOMPETISI ❌".center(70))
            print("=" * 70)
            print()
            print(f"Skormu: {total_score}/300")
            print(f"Posisi Akhir: #{player_rank}/{len(all_competitors)-1}")
            print(f"Minimum untuk menang: {self.min_points_to_win} poin")
            print(f"Kurang: {self.min_points_to_win - total_score} poin")
            print()
            print("Jangan menyerah! Coba lagi dengan strategi yang lebih baik!")
        
        print()
        input("Tekan ENTER untuk keluar...")
        return True
    
    def game_over_check(self):
        """Cek apakah game over (hari habis sebelum kompetisi)"""
        if self.days_left <= 0:
            self.display_header()
            print("⏰ WAKTU HABIS! KOMPETISI DIMULAI!")
            print("=" * 70)
            print()
            return self.competition()
        return False
    
    def run(self):
        """Main game loop"""
        print("\n" * 2)
        print("=" * 70)
        print("🏃 SELAMAT DATANG DI RUNNER TRAINING CHAMPIONSHIP 🏃".center(70))
        print("=" * 70)
        print()
        print(f"⏰ Misi Anda: Melatih diri selama {self.competition_day} hari")
        print(f"🎯 Target Poin Minimum: {self.min_points_to_win}/300 untuk menang")
        print(f"🏆 Kalahkan 8 pesaing lainnya untuk menjadi juara!")
        print()
        print("Tips:")
        print("- Latih Speed, Power, dan Stamina secara seimbang")
        print("- Jaga energi dengan istirahat yang cukup")
        print("- Hindari cedera dengan menjaga kesehatan")
        print("- Cedera akan mengurangi efektivitas stat hingga 30%")
        print("- Lihat leadboard untuk melihat posisi Anda")
        print()
        input("Tekan ENTER untuk memulai...")
        
        # Game loop
        while True:
            if self.game_over_check():
                break
            
            pilihan = self.main_menu()
            
            if pilihan == "1":
                self.training_speed()
            elif pilihan == "2":
                self.training_power()
            elif pilihan == "3":
                self.training_stamina()
            elif pilihan == "4":
                self.rest()
            elif pilihan == "5":
                self.hospital()
            elif pilihan == "6":
                self.show_stats()
            elif pilihan == "7":
                self.show_leadboard()
            elif pilihan == "8":
                self.competition()
                break
            elif pilihan == "9":
                self.display_header()
                print("Terima kasih sudah bermain!")
                print("Sampai jumpa lagi!")
                break
            else:
                print("❌ Pilihan tidak valid!")
                input("Tekan ENTER untuk melanjutkan...")

# Main
if __name__ == "__main__":
    game = RunnerTrainingGame()
    game.run()

