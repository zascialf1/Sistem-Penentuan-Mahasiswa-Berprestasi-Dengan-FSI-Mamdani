import tkinter as tk
from tkinter import messagebox


# fungsi keanggotaan

def mf_linear_down(x, a, b):
    if x <= a: return 1.0
    if x >= b: return 0.0
    return (b - x) / (b - a)

def mf_linear_up(x, a, b):
    if x <= a: return 0.0
    if x >= b: return 1.0
    return (x - a) / (b - a)

def mf_triangle(x, a, b, c):
    if x <= a or x >= c: return 0.0
    if x <= b: return (x - a) / (b - a)
    return (c - x) / (c - b)

def fuzzify_ipk(x):
    return {
        'Rendah': mf_linear_down(x, 1.5, 2.5),
        'Sedang': mf_triangle(x, 2.0, 2.75, 3.5),
        'Tinggi': mf_linear_up(x, 3.0, 4.0)
    }

def fuzzify_prestasi(x):
    return {
        'Rendah': mf_linear_down(x, 20, 40),
        'Sedang': mf_triangle(x, 20, 45, 70),
        'Tinggi': mf_linear_up(x, 50, 100)
    }

def fuzzify_organisasi(x):
    return {
        'Rendah': mf_linear_down(x, 2, 4),
        'Sedang': mf_triangle(x, 2, 5, 8),
        'Tinggi': mf_linear_up(x, 6, 10)
    }

def fuzzify_kehadiran(x):
    return {
        'Rendah': mf_linear_down(x, 50, 65),
        'Sedang': mf_triangle(x, 55, 75, 90),
        'Tinggi': mf_linear_up(x, 75, 100)
    }

def mf_output(label, z):
    if label == 'Cukup':       return mf_linear_down(z, 20, 50)
    if label == 'Baik':        return mf_triangle(z, 30, 55, 80)
    if label == 'Sangat Baik': return mf_linear_up(z, 60, 100)
    return 0.0

RULES = [
    {'cond': [('ipk','Tinggi'),('prs','Tinggi'),('org','Tinggi'),('had','Tinggi')], 'out': 'Sangat Baik'},
    {'cond': [('ipk','Tinggi'),('prs','Tinggi'),('org','Sedang'),('had','Tinggi')], 'out': 'Sangat Baik'},
    {'cond': [('ipk','Tinggi'),('prs','Sedang'),('org','Tinggi'),('had','Tinggi')], 'out': 'Baik'},
    {'cond': [('ipk','Sedang'),('prs','Tinggi'),('org','Tinggi'),('had','Tinggi')], 'out': 'Baik'},
    {'cond': [('ipk','Tinggi'),('prs','Rendah'),('org','Rendah'),('had','Tinggi')], 'out': 'Cukup'},
    {'cond': [('ipk','Sedang'),('prs','Sedang'),('org','Sedang'),('had','Sedang')], 'out': 'Baik'},
    {'cond': [('ipk','Rendah'),('prs','Rendah'),('org','Rendah'),('had','Rendah')], 'out': 'Cukup'},
    {'cond': [('ipk','Rendah'),('prs','Sedang'),('org','Sedang'),('had','Sedang')], 'out': 'Cukup'},
    {'cond': [('ipk','Tinggi'),('prs','Tinggi'),('org','Rendah'),('had','Sedang')], 'out': 'Baik'},
    {'cond': [('ipk','Sedang'),('prs','Rendah'),('org','Tinggi'),('had','Tinggi')], 'out': 'Cukup'},
    {'cond': [('ipk','Tinggi'),('prs','Sedang'),('org','Sedang'),('had','Sedang')], 'out': 'Baik'},
]

def hitung_fuzzy(ipk, prestasi, organisasi, kehadiran):
    mf_i = fuzzify_ipk(ipk)
    mf_p = fuzzify_prestasi(prestasi)
    mf_o = fuzzify_organisasi(organisasi)
    mf_h = fuzzify_kehadiran(kehadiran)
    var_map = {'ipk': mf_i, 'prs': mf_p, 'org': mf_o, 'had': mf_h}

    alpha_map = {'Cukup': 0.0, 'Baik': 0.0, 'Sangat Baik': 0.0}
    for rule in RULES:
        alpha = min(var_map[v][k] for v, k in rule['cond'])
        if alpha > alpha_map[rule['out']]:
            alpha_map[rule['out']] = alpha

    N = 1000
    num = 0.0
    den = 0.0
    for i in range(N + 1):
        z = i / N * 100
        mu = 0.0
        for label, alpha in alpha_map.items():
            if alpha > 0:
                mu = max(mu, min(alpha, mf_output(label, z)))
        num += z * mu
        den += mu

    z_star = num / den if den > 0 else 0.0

    if z_star < 40:
        kategori = 'Cukup'
        warna = '#e74c3c'
    elif z_star < 65:
        kategori = 'Baik'
        warna = '#e67e22'
    else:
        kategori = 'Sangat Baik'
        warna = '#27ae60'

    return z_star, kategori, warna

# GUI

class FuzzyApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Sistem Penentuan Mahasiswa Berprestasi (Fuzzy Mamdani)")
        self.geometry("500x530")
        self.resizable(False, False)
        self.configure(bg='#f5f6fa')
        self._build_ui()

    def _build_ui(self):
        # header
        header = tk.Frame(self, bg='#2c3e50', pady=14)
        header.pack(fill='x')
        tk.Label(header, text="Sistem Penentuan Mahasiswa Berprestasi",
                 font=('Segoe UI', 13, 'bold'), fg='white', bg='#2c3e50').pack()
        tk.Label(header, text="Fuzzy Inference System — Metode Mamdani",
                 font=('Segoe UI', 9), fg='#bdc3c7', bg='#2c3e50').pack()

        # form input
        form = tk.Frame(self, bg='#f5f6fa', padx=40, pady=18)
        form.pack(fill='x')

        fields = [
            ("IPK (0 – 4.00)",           'ipk', '3.5'),
            ("Prestasi Lomba (0 – 100)", 'prs', '75'),
            ("Organisasi (0 – 10)",      'org', '7'),
            ("Kehadiran (0 – 100%)",     'had', '85'),
        ]

        self.entries = {}
        for label, key, default in fields:
            row = tk.Frame(form, bg='#f5f6fa')
            row.pack(fill='x', pady=6)
            tk.Label(row, text=label, font=('Segoe UI', 10),
                     bg='#f5f6fa', width=24, anchor='w').pack(side='left')
            entry = tk.Entry(row, font=('Segoe UI', 11), width=10,
                             justify='center', relief='solid', bd=1)
            entry.insert(0, default)
            entry.pack(side='left', padx=(8, 0))
            entry.bind('<Return>', lambda e: self.hitung())
            self.entries[key] = entry

        # tombol hitung
        tk.Button(self, text="HITUNG",
                  font=('Segoe UI', 11, 'bold'),
                  bg='#2980b9', fg='white',
                  activebackground='#1f618d',
                  relief='flat', padx=30, pady=8,
                  cursor='hand2',
                  command=self.hitung).pack(pady=(0, 18))

        # output area 
        out = tk.Frame(self, bg='#ecf0f1',
                       highlightbackground='#bdc3c7',
                       highlightthickness=1,
                       padx=24, pady=18)
        out.pack(fill='x', padx=40)

        tk.Label(out, text="Hasil Penilaian",
                 font=('Segoe UI', 9), fg='#7f8c8d', bg='#ecf0f1').pack()

        # skor angka
        self.lbl_skor = tk.Label(out, text="–",
                                  font=('Segoe UI', 34, 'bold'),
                                  fg='#2c3e50', bg='#ecf0f1')
        self.lbl_skor.pack()

        # skala kategori (cukup/baik/sangat baik) 
        skala_frame = tk.Frame(out, bg='#ecf0f1')
        skala_frame.pack(fill='x', pady=(10, 4))

        # 3 kotak kategori
        self.kotak = {}
        kategori_list = [
            ('Cukup',       '#fadbd8', '#e74c3c'),
            ('Baik',        '#fdebd0', '#e67e22'),
            ('Sangat Baik', '#d5f5e3', '#27ae60'),
        ]
        for kat, bg_off, bg_on in kategori_list:
            col = tk.Frame(skala_frame, bg='#ecf0f1')
            col.pack(side='left', expand=True, fill='x', padx=4)

            box = tk.Frame(col, bg='#dfe6e9',
                           highlightbackground='#bdc3c7',
                           highlightthickness=1,
                           pady=10)
            box.pack(fill='x')

            lbl = tk.Label(box, text=kat,
                           font=('Segoe UI', 10, 'bold'),
                           fg='#7f8c8d', bg='#dfe6e9')
            lbl.pack()

            self.kotak[kat] = (box, lbl, bg_off, bg_on)

        # keterangan kategori aktif
        self.lbl_kategori = tk.Label(out,
                                      text="Masukkan nilai lalu klik HITUNG",
                                      font=('Segoe UI', 10),
                                      fg='#7f8c8d', bg='#ecf0f1')
        self.lbl_kategori.pack(pady=(10, 0))

    def _reset_kotak(self):
        for kat, (box, lbl, bg_off, bg_on) in self.kotak.items():
            box.config(bg='#dfe6e9', highlightbackground='#bdc3c7')
            lbl.config(fg='#7f8c8d', bg='#dfe6e9')

    def _aktifkan_kotak(self, kategori, warna):
        box, lbl, bg_off, bg_on = self.kotak[kategori]
        box.config(bg=bg_on, highlightbackground=bg_on)
        lbl.config(fg='white', bg=bg_on)

    def hitung(self):
        try:
            ipk = float(self.entries['ipk'].get())
            prs = float(self.entries['prs'].get())
            org = float(self.entries['org'].get())
            had = float(self.entries['had'].get())
        except ValueError:
            messagebox.showerror("Input Error", "Semua nilai harus berupa angka.")
            return

        if not (0 <= ipk <= 4):
            messagebox.showerror("Input Error", "IPK harus antara 0 – 4"); return
        if not (0 <= prs <= 100):
            messagebox.showerror("Input Error", "Prestasi Lomba harus antara 0 – 100"); return
        if not (0 <= org <= 10):
            messagebox.showerror("Input Error", "Organisasi harus antara 0 – 10"); return
        if not (0 <= had <= 100):
            messagebox.showerror("Input Error", "Kehadiran harus antara 0 – 100"); return

        z_star, kategori, warna = hitung_fuzzy(ipk, prs, org, had)

        self.lbl_skor.config(text=f"{z_star:.2f}", fg=warna)
        self.lbl_kategori.config(
            text=f"Mahasiswa termasuk kategori: {kategori}", fg=warna)

        self._reset_kotak()
        self._aktifkan_kotak(kategori, warna)

if __name__ == '__main__':
    app = FuzzyApp()
    app.mainloop()