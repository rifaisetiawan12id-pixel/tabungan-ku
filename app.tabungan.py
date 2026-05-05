import tkinter as tk
from tkinter import messagebox, ttk
from datetime import datetime

class AutoSavingApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Saving Goals Monitor")
        self.root.geometry("750x500")
        
        # List untuk menyimpan data selama aplikasi berjalan
        self.goals = []

        self.setup_ui()

    def setup_ui(self):
        # --- Bagian Input ---
        input_frame = tk.LabelFrame(self.root, text="Tambah Target Menabung", padx=15, pady=10)
        input_frame.pack(fill="x", padx=10, pady=10)

        # Baris 1: Nama & Harga
        tk.Label(input_frame, text="Nama Barang:").grid(row=0, column=0, sticky="w")
        self.ent_nama = tk.Entry(input_frame, width=20)
        self.ent_nama.grid(row=0, column=1, padx=5, pady=5)

        tk.Label(input_frame, text="Target Harga:").grid(row=0, column=2, sticky="w")
        self.ent_harga = tk.Entry(input_frame, width=20)
        self.ent_harga.grid(row=0, column=3, padx=5, pady=5)

        # Baris 2: Terkumpul & Deadline
        tk.Label(input_frame, text="Uang Terkumpul:").grid(row=1, column=0, sticky="w")
        self.ent_terkumpul = tk.Entry(input_frame, width=20)
        self.ent_terkumpul.grid(row=1, column=1, padx=5, pady=5)

        tk.Label(input_frame, text="Deadline (YYYY-MM-DD):").grid(row=1, column=2, sticky="w")
        self.ent_deadline = tk.Entry(input_frame, width=20)
        self.ent_deadline.grid(row=1, column=3, padx=5, pady=5)

        # Tombol Proses
        btn_simpan = tk.Button(input_frame, text="Hitung & Tambahkan Otomatis", 
                               command=self.tambah_target, bg="#2ecc71", fg="white", font=('Arial', 9, 'bold'))
        btn_simpan.grid(row=2, column=0, columnspan=4, pady=10, sticky="we")

        # --- Bagian Tabel ---
        columns = ("Nama", "Harga", "Terkumpul", "Progres", "Sisa Hari", "Tabungan/Hari")
        self.tree = ttk.Treeview(self.root, columns=columns, show='headings')
        
        for col in columns:
            self.tree.heading(col, text=col)
            self.tree.column(col, width=110, anchor="center")

        self.tree.pack(fill="both", expand=True, padx=10, pady=5)

        # Tombol Hapus
        tk.Button(self.root, text="Hapus Data", command=self.hapus_target, bg="#e74c3c", fg="white").pack(pady=10)

    def hitung_otomatis(self, harga, terkumpul, deadline_str):
        # 1. Logika Persentase
        persen = (terkumpul / harga) * 100 if harga > 0 else 0
        
        # 2. Logika Sisa Hari
        sisa_uang = harga - terkumpul
        try:
            deadline_dt = datetime.strptime(deadline_str, "%Y-%m-%d")
            hari_ini = datetime.now()
            selisih = (deadline_dt - hari_ini).days + 1 # +1 agar hari ini terhitung
            
            sisa_hari = max(1, selisih)
            # 3. Logika Tabungan Harian
            per_hari = sisa_uang / sisa_hari if sisa_uang > 0 else 0
        except:
            sisa_hari = 0
            per_hari = 0
            
        return round(persen, 1), sisa_hari, round(per_hari)

    def tambah_target(self):
        try:
            nama = self.ent_nama.get()
            harga = float(self.ent_harga.get())
            terkumpul = float(self.ent_terkumpul.get())
            deadline = self.ent_deadline.get()

            if not nama: 
                messagebox.showwarning("Input Kosong", "Nama barang harus diisi!")
                return

            # Jalankan kalkulasi otomatis
            persen, sisa_hari, per_hari = self.hitung_otomatis(harga, terkumpul, deadline)

            # Masukkan ke tabel
            self.tree.insert("", "end", values=(
                nama, 
                f"Rp {harga:,.0f}", 
                f"Rp {terkumpul:,.0f}", 
                f"{persen}%", 
                f"{sisa_hari} hari", 
                f"Rp {per_hari:,.0f}"
            ))
            
            # Reset form input
            self.ent_nama.delete(0, tk.END)
            self.ent_harga.delete(0, tk.END)
            self.ent_terkumpul.delete(0, tk.END)
            self.ent_deadline.delete(0, tk.END)

        except ValueError:
            messagebox.showerror("Error", "Gunakan angka untuk nominal dan format YYYY-MM-DD untuk tanggal!")

    def hapus_target(self):
        selected = self.tree.selection()
        if selected:
            self.tree.delete(selected[0])

if __name__ == "__main__":
    root = tk.Tk()
    app = AutoSavingApp(root)
    root.mainloop()