import json
import os
from datetime import datetime
from typing import List, Dict

class TodoApp:
    def __init__(self):
        self.file_path = "todolist_data.json"
        self.tasks = []
        self.load_data()
    
    def load_data(self):
        """Memuat data dari file JSON"""
        if os.path.exists(self.file_path):
            try:
                with open(self.file_path, 'r', encoding='utf-8') as f:
                    self.tasks = json.load(f)
            except:
                self.tasks = []
        else:
            self.tasks = []
    
    def save_data(self):
        """Menyimpan data ke file JSON"""
        with open(self.file_path, 'w', encoding='utf-8') as f:
            json.dump(self.tasks, f, ensure_ascii=False, indent=2)
    
    def add_task(self, title: str, task_type: str, due_date: str, description: str = ""):
        """Menambah tugas atau ulangan baru"""
        try:
            # Validasi format tanggal
            datetime.strptime(due_date, "%Y-%m-%d")
        except ValueError:
            print("❌ Format tanggal salah! Gunakan format: YYYY-MM-DD (contoh: 2025-02-15)")
            return False
        
        task = {
            "id": len(self.tasks) + 1,
            "title": title,
            "type": task_type,  # "tugas" atau "ulangan"
            "due_date": due_date,
            "description": description,
            "completed": False,
            "created_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }
        
        self.tasks.append(task)
        self.save_data()
        print(f"✅ {task_type.capitalize()} '{title}' berhasil ditambahkan!")
        return True
    
    def view_all_tasks(self):
        """Menampilkan semua tugas dan ulangan"""
        if not self.tasks:
            print("\n📋 Belum ada tugas atau ulangan. Mulai tambahkan sekarang!")
            input("\nTekan Enter untuk lanjut...")
            return
        
        # Sort berdasarkan tanggal
        sorted_tasks = sorted(self.tasks, key=lambda x: x["due_date"])
        
        print("\n" + "="*70)
        print("📋 DAFTAR TUGAS DAN ULANGAN")
        print("="*70)
        
        for task in sorted_tasks:
            status = "✓" if task["completed"] else "○"
            task_type_display = "📝 Tugas" if task["type"] == "tugas" else "📚 Ulangan"
            
            # Hitung hari tersisa
            today = datetime.now().date()
            due_date = datetime.strptime(task["due_date"], "%Y-%m-%d").date()
            days_left = (due_date - today).days
            
            if days_left < 0:
                days_info = "⏰ SUDAH TERLEWAT"
            elif days_left == 0:
                days_info = "⚠️  HARI INI"
            else:
                days_info = f"📅 {days_left} hari lagi"
            
            print(f"\n[{status}] ID: {task['id']} | {task_type_display}")
            print(f"    Judul: {task['title']}")
            print(f"    Tanggal: {task['due_date']} {days_info}")
            if task['description']:
                print(f"    Keterangan: {task['description']}")
            print(f"    Status: {'Selesai ✓' if task['completed'] else 'Belum Selesai'}")
        
        print("\n" + "="*70)
    
    def view_upcoming_tasks(self):
        """Menampilkan tugas dan ulangan yang akan datang"""
        today = datetime.now().date()
        upcoming = [task for task in self.tasks 
                   if not task["completed"] and 
                   datetime.strptime(task["due_date"], "%Y-%m-%d").date() >= today]
        
        if not upcoming:
            print("\n✅ Tidak ada tugas atau ulangan yang akan datang!")
            input("\nTekan Enter untuk lanjut...")
            return
        
        upcoming = sorted(upcoming, key=lambda x: x["due_date"])
        
        print("\n" + "="*70)
        print("⏰ TUGAS DAN ULANGAN YANG AKAN DATANG")
        print("="*70)
        
        for task in upcoming:
            task_type_display = "📝 Tugas" if task["type"] == "tugas" else "📚 Ulangan"
            due_date = datetime.strptime(task["due_date"], "%Y-%m-%d").date()
            days_left = (due_date - today).days
            
            print(f"\n[ID: {task['id']}] {task_type_display}")
            print(f"    Judul: {task['title']}")
            print(f"    Tanggal: {task['due_date']} ({days_left} hari)")
            if task['description']:
                print(f"    Keterangan: {task['description']}")
        
        print("\n" + "="*70)
        input("\nTekan Enter untuk lanjut...")
    
    def view_overdue_tasks(self):
        """Menampilkan tugas dan ulangan yang sudah terlewat"""
        today = datetime.now().date()
        overdue = [task for task in self.tasks 
                  if not task["completed"] and 
                  datetime.strptime(task["due_date"], "%Y-%m-%d").date() < today]
        
        if not overdue:
            print("\n✅ Tidak ada tugas atau ulangan yang terlewat!")
            input("\nTekan Enter untuk lanjut...")
            return
        
        overdue = sorted(overdue, key=lambda x: x["due_date"])
        
        print("\n" + "="*70)
        print("⚠️  TUGAS DAN ULANGAN YANG SUDAH TERLEWAT")
        print("="*70)
        
        for task in overdue:
            task_type_display = "📝 Tugas" if task["type"] == "tugas" else "📚 Ulangan"
            due_date = datetime.strptime(task["due_date"], "%Y-%m-%d").date()
            days_overdue = (today - due_date).days
            
            print(f"\n[ID: {task['id']}] {task_type_display}")
            print(f"    Judul: {task['title']}")
            print(f"    Tanggal: {task['due_date']} ({days_overdue} hari yang lalu)")
            if task['description']:
                print(f"    Keterangan: {task['description']}")
        
        print("\n" + "="*70)
        input("\nTekan Enter untuk lanjut...")
    
    def mark_completed(self, task_id: int):
        """Menandai tugas sebagai selesai"""
        for task in self.tasks:
            if task["id"] == task_id:
                task["completed"] = True
                self.save_data()
                print(f"✅ '{task['title']}' ditandai sebagai selesai!")
                return True
        
        print("❌ Tugas tidak ditemukan!")
        return False
    
    def delete_task(self, task_id: int):
        """Menghapus tugas"""
        for i, task in enumerate(self.tasks):
            if task["id"] == task_id:
                title = task["title"]
                self.tasks.pop(i)
                self.save_data()
                print(f"🗑️  '{title}' berhasil dihapus!")
                return True
        
        print("❌ Tugas tidak ditemukan!")
        return False
    
    def edit_task(self, task_id: int):
        """Mengubah tugas"""
        for task in self.tasks:
            if task["id"] == task_id:
                print(f"\n📝 Edit: {task['title']}")
                print("Kolom mana yang ingin diubah?")
                print("1. Judul")
                print("2. Tipe (tugas/ulangan)")
                print("3. Tanggal")
                print("4. Keterangan")
                
                choice = input("\nPilihan (1-4): ").strip()
                
                if choice == "1":
                    new_title = input("Judul baru: ").strip()
                    if new_title:
                        task["title"] = new_title
                        print("✅ Judul diperbarui!")
                elif choice == "2":
                    new_type = input("Tipe (tugas/ulangan): ").strip().lower()
                    if new_type in ["tugas", "ulangan"]:
                        task["type"] = new_type
                        print("✅ Tipe diperbarui!")
                    else:
                        print("❌ Tipe tidak valid!")
                        return False
                elif choice == "3":
                    new_date = input("Tanggal baru (YYYY-MM-DD): ").strip()
                    try:
                        datetime.strptime(new_date, "%Y-%m-%d")
                        task["due_date"] = new_date
                        print("✅ Tanggal diperbarui!")
                    except ValueError:
                        print("❌ Format tanggal salah!")
                        return False
                elif choice == "4":
                    new_desc = input("Keterangan baru: ").strip()
                    task["description"] = new_desc
                    print("✅ Keterangan diperbarui!")
                else:
                    print("❌ Pilihan tidak valid!")
                    return False
                
                self.save_data()
                return True
        
        print("❌ Tugas tidak ditemukan!")
        return False
    
    def show_statistics(self):
        """Menampilkan statistik tugas"""
        total = len(self.tasks)
        completed = len([t for t in self.tasks if t["completed"]])
        pending = total - completed
        
        tugas_count = len([t for t in self.tasks if t["type"] == "tugas"])
        ulangan_count = len([t for t in self.tasks if t["type"] == "ulangan"])
        
        print("\n" + "="*70)
        print("📊 STATISTIK")
        print("="*70)
        print(f"Total Tugas/Ulangan: {total}")
        print(f"  📝 Tugas: {tugas_count}")
        print(f"  📚 Ulangan: {ulangan_count}")
        print(f"\nStatus:")
        print(f"  ✅ Selesai: {completed}")
        print(f"  ⏳ Belum Selesai: {pending}")
        
        if total > 0:
            percentage = (completed / total) * 100
            print(f"  📈 Persentase Selesai: {percentage:.1f}%")
        
        print("="*70)
        input("\nTekan Enter untuk lanjut...")

def main():
    app = TodoApp()
    
    while True:
        print("\n" + "="*70)
        print("📚 APLIKASI TODO LIST UNTUK SISWA 📚")
        print("="*70)
        print("\n1. Tambah Tugas")
        print("2. Tambah Ulangan")
        print("3. Lihat Semua Tugas/Ulangan")
        print("4. Lihat Tugas yang Akan Datang")
        print("5. Lihat Tugas yang Terlewat")
        print("6. Tandai Selesai")
        print("7. Edit Tugas")
        print("8. Hapus Tugas")
        print("9. Lihat Statistik")
        print("10. Keluar")
        print("="*70)
        
        choice = input("\nPilihan (1-10): ").strip()
        
        if choice == "1":
            print("\n➕ TAMBAH TUGAS")
            title = input("Judul tugas: ").strip()
            if not title:
                print("❌ Judul tidak boleh kosong!")
                continue
            
            due_date = input("Tanggal deadline (YYYY-MM-DD): ").strip()
            description = input("Keterangan (opsional): ").strip()
            app.add_task(title, "tugas", due_date, description)
        
        elif choice == "2":
            print("\n➕ TAMBAH ULANGAN")
            title = input("Judul ulangan: ").strip()
            if not title:
                print("❌ Judul tidak boleh kosong!")
                continue
            
            due_date = input("Tanggal ulangan (YYYY-MM-DD): ").strip()
            description = input("Keterangan (opsional): ").strip()
            app.add_task(title, "ulangan", due_date, description)
        
        elif choice == "3":
            app.view_all_tasks()
        
        elif choice == "4":
            app.view_upcoming_tasks()
        
        elif choice == "5":
            app.view_overdue_tasks()
        
        elif choice == "6":
            app.view_all_tasks()
            try:
                task_id = int(input("\nMasukkan ID tugas yang selesai: "))
                app.mark_completed(task_id)
            except ValueError:
                print("❌ ID harus berupa angka!")
        
        elif choice == "7":
            app.view_all_tasks()
            try:
                task_id = int(input("\nMasukkan ID tugas untuk diedit: "))
                app.edit_task(task_id)
            except ValueError:
                print("❌ ID harus berupa angka!")
        
        elif choice == "8":
            app.view_all_tasks()
            try:
                task_id = int(input("\nMasukkan ID tugas untuk dihapus: "))
                confirm = input("Yakin hapus? (y/n): ").strip().lower()
                if confirm == 'y':
                    app.delete_task(task_id)
            except ValueError:
                print("❌ ID harus berupa angka!")
        
        elif choice == "9":
            app.show_statistics()
        
        elif choice == "10":
            print("\n👋 Terima kasih telah menggunakan TODO LIST! Semangat belajar! 🎓")
            break
        
        else:
            print("❌ Pilihan tidak valid! Silakan pilih 1-10")

if __name__ == "__main__":
    main()
