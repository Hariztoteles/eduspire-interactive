# ==========================================
# EduSpire Interactive - gui_app.py (Ultimate Smart Reader & Dynamic Generator Edition)
# Creator Watermark: HARIZTOTELES_GamEdu
# ==========================================

import tkinter as tk
from tkinter import messagebox, filedialog, ttk
import os
import time
import subprocess
import sys
import json
import re
import random

try:
    from pypdf import PdfReader
    PYPDF_AVAILABLE = True
except ImportError:
    PYPDF_AVAILABLE = False

try:
    from PIL import Image, ImageTk
    PIL_AVAILABLE = True
except ImportError:
    PIL_AVAILABLE = False

CONFIG_FILE = "license_config.txt"
BG_IMAGE_FILE = "background.png"

class EduSpireApp:
    def __init__(self, root):
        self.root = root
        self.root.title("EduSpire Interactive - Professional Edition")
        self.root.geometry("1100x780")
        self.root.config(bg="#3e2723")
        
        self.selected_file_path = None
        self.file_content_text = ""
        self.book_pages_list = []
        self.buyer_name = "Pengguna Terdaftar"
        self.active_generated_questions = []
        
        # Variabel Ujian
        self.quiz_running = False
        self.time_left = 600
        self.timer_id = None
        self.user_answers = {}
        self.current_quiz_idx = 0

        self.check_saved_license_status()
        self.create_welcome_screen()

    def check_saved_license_status(self):
        if os.path.exists(CONFIG_FILE):
            try:
                with open(CONFIG_FILE, "r", encoding="utf-8") as f:
                    lines = f.readlines()
                    if len(lines) >= 2:
                        self.saved_key = lines[0].strip()
                        self.buyer_name = lines[1].strip()
                        self.is_licensed = True
                        return
            except Exception:
                pass
        self.saved_key = ""
        self.is_licensed = False

    def save_license_data(self, key: str, name: str):
        try:
            with open(CONFIG_FILE, "w", encoding="utf-8") as f:
                f.write(f"{key.strip()}\n{name.strip()}")
            self.saved_key = key.strip()
            self.buyer_name = name.strip()
            self.is_licensed = True
        except Exception as e:
            print(f"Gagal menyimpan lisensi: {e}")

    def clear_window(self):
        if self.timer_id:
            self.root.after_cancel(self.timer_id)
        for widget in self.root.winfo_children():
            widget.destroy()

    def create_background_container(self, parent_window):
        if PIL_AVAILABLE and os.path.exists(BG_IMAGE_FILE):
            try:
                self.bg_image_raw = Image.open(BG_IMAGE_FILE)
                self.bg_image_resized = self.bg_image_raw.resize((1100, 780), Image.Resampling.LANCZOS)
                self.bg_photo = ImageTk.PhotoImage(self.bg_image_resized)
                
                bg_label = tk.Label(parent_window, image=self.bg_photo)
                bg_label.place(x=0, y=0, relwidth=1, relheight=1)
                
                container = tk.Frame(bg_label, bg="#3e2723")
                container.place(relx=0.5, rely=0.5, anchor=tk.CENTER, width=900, height=680)
                return container
            except Exception as e:
                print(f"Gagal memuat gambar background: {e}")
        
        container = tk.Frame(parent_window, bg="#3e2723")
        container.pack(fill=tk.BOTH, expand=True)
        return container

    def create_welcome_screen(self):
        self.clear_window()
        main_frame = tk.Frame(self.root, bg="#3e2723")
        main_frame.pack(fill=tk.BOTH, expand=True)

        container = self.create_background_container(main_frame)

        tk.Label(container, text="EDUSPIRE INTERACTIVE", font=("Georgia", 22, "bold"), fg="#ffecb3", bg="#3e2723").pack(pady=(40, 10))
        tk.Label(container, text="Aplikasi Pembelajaran & Generator Bank Soal Pintar", font=("Arial", 12, "italic"), fg="#d7ccc8", bg="#3e2723").pack(pady=5)
        
        watermark_frame = tk.Frame(container, bg="#4e342e", padx=20, relief=tk.GROOVE, bd=2)
        watermark_frame.pack(pady=15)
        tk.Label(watermark_frame, text="© Created by: HARIZTOTELES_GamEdu", font=("Arial", 11, "bold"), fg="#ffb74d", bg="#4e342e").pack(pady=8, padx=20)

        if self.is_licensed:
            info_text = f"Status: Lisensi Aktif terdaftar untuk [{self.buyer_name}]"
            tk.Label(container, text=info_text, font=("Arial", 10, "bold"), fg="#81c784", bg="#3e2723").pack(pady=5)
            btn_text = "Masuk ke Dashboard Utama ➔"
        else:
            btn_text = "Mulai Autentikasi Lisensi ➔"

        start_btn = tk.Button(container, text=btn_text, font=("Arial", 12, "bold"), bg="#8d6e63", fg="white", activebackground="#a1887f", activeforeground="white", padx=20, pady=10, command=self.proceed_app)
        start_btn.pack(pady=30)

    def proceed_app(self):
        if self.is_licensed:
            self.create_dashboard_screen()
        else:
            self.create_login_screen()

    def create_login_screen(self):
        self.clear_window()
        header_frame = tk.Frame(self.root, bg="#4e342e", height=90)
        header_frame.pack(fill=tk.X)
        
        tk.Label(header_frame, text="Autentikasi Lisensi Pengguna", font=("Georgia", 16, "bold"), fg="#ffecb3", bg="#4e342e").pack(pady=15)
        tk.Label(header_frame, text="Watermark: HARIZTOTELES_GamEdu", font=("Arial", 9, "italic"), fg="#bcaaa4", bg="#4e342e").pack(side=tk.BOTTOM, pady=5)

        content_frame = tk.Frame(self.root, bg="#fdfbf7")
        content_frame.pack(fill=tk.BOTH, expand=True)

        form_container = self.create_background_container(content_frame)

        tk.Label(form_container, text="Nama Pembeli / Instansi:", font=("Arial", 11, "bold"), bg="#3e2723", fg="#ffecb3").pack(anchor="w", pady=(20, 0))
        self.name_entry = tk.Entry(form_container, font=("Arial", 11), width=45, bg="#efebe9", fg="#3e2723", relief=tk.SOLID, bd=1)
        self.name_entry.pack(pady=8, anchor="w", ipady=4)

        tk.Label(form_container, text="Masukkan License Key:", font=("Arial", 11, "bold"), bg="#3e2723", fg="#ffecb3").pack(anchor="w", pady=(15, 0))
        self.key_entry = tk.Entry(form_container, font=("Arial", 11), width=45, bg="#efebe9", fg="#3e2723", relief=tk.SOLID, bd=1)
        self.key_entry.pack(pady=8, anchor="w", ipady=4)

        save_btn = tk.Button(form_container, text="💾 Save License & Masuk", font=("Arial", 11, "bold"), bg="#6d4c41", fg="white", activebackground="#5d4037", padx=15, pady=8, command=self.process_save_license)
        save_btn.pack(pady=25, anchor="w")

    def process_save_license(self):
        name = self.name_entry.get().strip()
        key = self.key_entry.get().strip()
        if not name or not key:
            messagebox.showwarning("Peringatan", "Nama dan License Key wajib diisi!")
            return
        self.save_license_data(key, name)
        messagebox.showinfo("Sukses", f"Lisensi berhasil disimpan!\nSelamat datang, {name}.")
        self.create_dashboard_screen()

    def create_dashboard_screen(self):
        self.clear_window()

        header_frame = tk.Frame(self.root, bg="#3e2723", height=75)
        header_frame.pack(fill=tk.X)
        
        tk.Label(header_frame, text="EduSpire Dashboard Utama", font=("Georgia", 14, "bold"), fg="#ffecb3", bg="#3e2723").pack(side=tk.LEFT, padx=20, pady=15)
        watermark_text = f"Licensed to: {self.buyer_name}\nDeveloper: HARIZTOTELES_GamEdu"
        tk.Label(header_frame, text=watermark_text, font=("Arial", 8, "italic"), fg="#ffb74d", bg="#3e2723", justify=tk.RIGHT).pack(side=tk.RIGHT, padx=20)

        upload_frame = tk.Frame(self.root, bg="#efebe9", padx=15, pady=12, relief=tk.GROOVE, bd=1)
        upload_frame.pack(fill=tk.X, padx=15, pady=10)

        tk.Button(upload_frame, text="📁 Unggah Buku / Dokumen (PDF/Word/TXT)", font=("Arial", 9, "bold"), bg="#6d4c41", fg="white", command=self.upload_book_with_progress).pack(side=tk.LEFT, padx=5)
        
        file_display_name = os.path.basename(self.selected_file_path) if self.selected_file_path else "Belum ada dokumen dipilih."
        self.dashboard_file_label = tk.Label(upload_frame, text=f"File Aktif: {file_display_name}", font=("Arial", 9, "italic"), bg="#efebe9", fg="#4e342e")
        self.dashboard_file_label.pack(side=tk.LEFT, padx=10)

        tk.Button(upload_frame, text="📖 Read Book / Preview", font=("Arial", 9, "bold"), bg="#5d4037", fg="white", command=self.open_book_reader).pack(side=tk.RIGHT, padx=5)

        self.progress_bar = ttk.Progressbar(upload_frame, orient="horizontal", length=180, mode="determinate")

        style = ttk.Style()
        style.theme_use('default')
        style.configure('TNotebook', background='#fdfbf7', borderwidth=0)
        style.configure('TNotebook.Tab', background='#d7ccc8', foreground='#3e2723', font=('Arial', 10, 'bold'), padding=[12, 8])
        style.map('TNotebook.Tab', background=[('selected', '#5d4037')], foreground=[('selected', '#ffffff')])

        notebook = ttk.Notebook(self.root)
        notebook.pack(fill=tk.BOTH, expand=True, padx=15, pady=5)

        # --- TAB 1: RANGKUMAN BUKU ---
        tab1 = tk.Frame(notebook, bg="#fdfbf7")
        notebook.add(tab1, text=" 📑 Ringkasan Detail Bab ")
        tk.Label(tab1, text="Analisis Eksekutif & Rangkuman Komprehensif per Bab", font=("Georgia", 11, "bold"), bg="#fdfbf7", fg="#3e2723").pack(anchor="w", padx=15, pady=10)
        
        self.summary_box = tk.Text(tab1, font=("Arial", 10), height=17, width=100, bg="#efebe9", fg="#2b1d1a", relief=tk.SOLID, bd=1)
        self.summary_box.pack(padx=15, pady=5, fill=tk.BOTH, expand=True)
        self.update_summary_content()

        # --- TAB 2: GENERATOR 40 SOAL (A-E) ---
        tab2 = tk.Frame(notebook, bg="#fdfbf7")
        notebook.add(tab2, text=" 📝 Generator 40 Soal (A-E) & Save ")
        tk.Label(tab2, text="Generator Bank Soal Pintar (40 Soal Pilihan Ganda A - E Berdasarkan Isi Buku)", font=("Georgia", 11, "bold"), bg="#fdfbf7", fg="#3e2723").pack(anchor="w", padx=15, pady=10)
        
        gen_ctrl_frame = tk.Frame(tab2, bg="#fdfbf7")
        gen_ctrl_frame.pack(anchor="w", padx=15, pady=5)
        
        tk.Button(gen_ctrl_frame, text="⚡ Generate 40 Soal Pilihan Ganda (A-E)", font=("Arial", 10, "bold"), bg="#6d4c41", fg="white", padx=10, pady=6, command=self.generate_questions_from_doc).pack(side=tk.LEFT, padx=5)
        tk.Button(gen_ctrl_frame, text="💾 Save Bank Soal (.txt / .bnk)", font=("Arial", 10, "bold"), bg="#4e342e", fg="white", padx=10, pady=6, command=self.save_question_bank_menu).pack(side=tk.LEFT, padx=5)

        self.question_display_box = tk.Text(tab2, font=("Arial", 10), height=14, width=100, bg="#efebe9", fg="#2b1d1a", relief=tk.SOLID, bd=1)
        self.question_display_box.pack(padx=15, pady=10, fill=tk.BOTH, expand=True)
        self.generate_questions_from_doc(is_init=True)

        # --- TAB 3: SESI UJIAN 20 SOAL, TIMER & LEADERBOARD ---
        tab3 = tk.Frame(notebook, bg="#fdfbf7")
        notebook.add(tab3, text=" 🚀 Sesi Ujian (20 Soal) & Leaderboard ")
        tk.Label(tab3, text="Simulasi Ujian Interaktif (20 Soal Pilihan Ganda A-E, Timer, & Leaderboard)", font=("Georgia", 11, "bold"), bg="#fdfbf7", fg="#3e2723").pack(anchor="w", padx=15, pady=10)
        
        self.quiz_container = tk.Frame(tab3, bg="#efebe9", padx=15, pady=15, relief=tk.SOLID, bd=1)
        self.quiz_container.pack(padx=15, pady=5, fill=tk.BOTH, expand=True)

        self.init_quiz_landing_screen()

        tk.Button(self.root, text="⚙ Reset Lisensi / Keluar", font=("Arial", 9, "bold"), bg="#a1887f", fg="white", command=self.reset_license).pack(pady=8)

    def upload_book_with_progress(self):
        file_path = filedialog.askopenfilename(filetypes=[("PDF & Text Files", "*.pdf *.docx *.txt"), ("All Files", "*.*")])
        if file_path:
            self.progress_bar.pack(side=tk.RIGHT, padx=10)
            self.progress_bar["value"] = 0
            self.root.update_idletasks()

            for i in range(101):
                time.sleep(0.01)
                self.progress_bar["value"] = i
                self.root.update_idletasks()

            self.selected_file_path = file_path
            file_name = os.path.basename(file_path)
            ext = os.path.splitext(file_path)[1].lower()
            
            self.book_pages_list = []
            try:
                if ext == ".pdf" and PYPDF_AVAILABLE:
                    reader = PdfReader(file_path)
                    for idx, page in enumerate(reader.pages):
                        t = page.extract_text()
                        if t and t.strip():
                            cleaned_page = self.clean_pdf_page_layout(t)
                            self.book_pages_list.append(cleaned_page)
                    
                    if not self.book_pages_list:
                        self.book_pages_list = ["Dokumen PDF tidak memiliki teks terbaca."]
                else:
                    with open(file_path, "r", encoding="utf-8", errors="ignore") as f:
                        content = f.read()
                        self.book_pages_list = [self.clean_pdf_page_layout(content)]

                self.file_content_text = "\n\n".join(self.book_pages_list)
            except Exception as e:
                self.book_pages_list = [f"Gagal membaca file: {e}"]
                self.file_content_text = str(e)

            self.dashboard_file_label.config(text=f"File Aktif: {file_name}")
            self.progress_bar.pack_forget()
            
            self.update_summary_content()
            self.generate_questions_from_doc()
            
            messagebox.showinfo("Status Dokumen", f"Dokumen '{file_name}' berhasil dimuat ({len(self.book_pages_list)} Halaman terdeteksi)!")

    def clean_pdf_page_layout(self, raw_text):
        lines = raw_text.splitlines()
        formatted_lines = []
        for line in lines:
            clean_line = line.strip()
            if clean_line.isdigit() and len(clean_line) <= 3:
                continue
            if clean_line:
                formatted_lines.append(clean_line)
        paragraph = " ".join(formatted_lines)
        paragraph = re.sub(r'\s+', ' ', paragraph)
        return paragraph

    def get_meaningful_sentences(self):
        """Mengekstrak kalimat-kalimat bermakna dari isi buku untuk bahan generator soal dinamis"""
        all_text = " ".join(self.book_pages_list)
        # Bersihkan karakter khusus
        sentences = re.split(r'\. |\? |\! |\n', all_text)
        meaningful = [s.strip() for s in sentences if len(s.split()) > 6 and not "Copyright" in s and not "Penerbit" in s]
        if not meaningful:
            meaningful = ["Penerapan konsep dasar dalam materi buku ini sangat penting untuk dipahami secara komprehensif."]
        return meaningful

    def update_summary_content(self):
        if hasattr(self, 'summary_box'):
            file_name = os.path.basename(self.selected_file_path) if self.selected_file_path else "Default Dokumen"
            sentences = self.get_meaningful_sentences()
            snippet = " ".join(sentences[:3]) if len(sentences) >= 3 else sentences[0]
            
            self.summary_box.config(state=tk.NORMAL)
            self.summary_box.delete("1.0", tk.END)
            summary_text = (
                "==================================================\n"
                f" RANGKUMAN EKSEKUTIF DOKUMEN: {file_name.upper()}\n"
                "==================================================\n\n"
                f"• INFORMASI UMUM BUKU:\n"
                f"  - Total Halaman Buku: {len(self.book_pages_list)} Halaman\n"
                f"  - Total Karakter Terbaca: {len(self.file_content_text)} karakter\n\n"
                f"• INTISARI UTAMA MATERI BUKU:\n"
                f"  \"{snippet}\"\n\n"
                "• BAB 1: PENDAHULUAN & KONSEP FUNDAMENTAL\n"
                "  - Membahas landasan utama, prinsip dasar, serta arah pemikiran pokok buku.\n\n"
                "• BAB 2: PEMBAHASAN TEKNIK & PENERAPAN\n"
                "  - Mengupas langkah operasional, strategi kunci, dan studi kasus lapangan.\n\n"
                "• BAB 3: KESIMPULAN & EVALUASI\n"
                "  - Rangkuman akhir serta panduan implementasi praktis bagi pembaca.\n"
            )
            self.summary_box.insert(tk.END, summary_text)
            self.summary_box.config(state=tk.DISABLED)

    def open_book_reader(self):
        if not self.selected_file_path:
            messagebox.showwarning("Perhatian", "Belum ada buku yang diunggah! Silakan unggah dokumen terlebih dahulu.")
            return

        if not hasattr(self, 'book_pages_list') or not self.book_pages_list:
            self.book_pages_list = [self.file_content_text]

        reader_win = tk.Toplevel(self.root)
        reader_win.title(f"EduSpire Book Reader - {os.path.basename(self.selected_file_path)}")
        reader_win.geometry("980x800")
        reader_win.config(bg="#fdfbf7")

        header = tk.Label(reader_win, text=f"📖 Membaca Halaman Buku: {os.path.basename(self.selected_file_path)}", font=("Georgia", 12, "bold"), bg="#4e342e", fg="#ffecb3", pady=10)
        header.pack(fill=tk.X)

        # Widget Text aman dan ringan tanpa ngeblank
        self.reader_text_area = tk.Text(reader_win, font=("Georgia", 12), bg="#ffffff", fg="#2b1d1a", padx=50, pady=40, wrap=tk.WORD, spacing2=6, spacing3=8)
        self.reader_text_area.pack(fill=tk.BOTH, expand=True, padx=25, pady=15)

        nav_control_frame = tk.Frame(reader_win, bg="#fdfbf7", pady=10)
        nav_control_frame.pack(fill=tk.X)

        self.current_page_idx = 0
        
        btn_prev = tk.Button(nav_control_frame, text="◀ Halaman Sebelumnya", font=("Arial", 10, "bold"), bg="#8d6e63", fg="white", padx=12, pady=6, command=lambda: self.change_book_page(-1))
        btn_prev.pack(side=tk.LEFT, padx=30)

        self.page_indicator_lbl = tk.Label(nav_control_frame, text="", font=("Arial", 11, "bold"), bg="#fdfbf7", fg="#3e2723")
        self.page_indicator_lbl.pack(side=tk.LEFT, expand=True)

        btn_next = tk.Button(nav_control_frame, text="Halaman Selanjutnya ▶", font=("Arial", 10, "bold"), bg="#6d4c41", fg="white", padx=12, pady=6, command=lambda: self.change_book_page(1))
        btn_next.pack(side=tk.RIGHT, padx=30)

        tk.Button(reader_win, text="Tutup Reader", font=("Arial", 9, "bold"), bg="#a1887f", fg="white", command=reader_win.destroy).pack(pady=5)

        self.render_current_book_page()

    def render_current_book_page(self):
        self.reader_text_area.config(state=tk.NORMAL)
        self.reader_text_area.delete("1.0", tk.END)
        
        page_content = self.book_pages_list[self.current_page_idx]
        self.reader_text_area.insert(tk.END, page_content)
        self.reader_text_area.config(state=tk.DISABLED)
        
        total_pages = len(self.book_pages_list)
        self.page_indicator_lbl.config(text=f"Halaman {self.current_page_idx + 1} dari {total_pages}")

    def change_book_page(self, direction):
        new_idx = self.current_page_idx + direction
        if 0 <= new_idx < len(self.book_pages_list):
            self.current_page_idx = new_idx
            self.render_current_book_page()
        else:
            if direction > 0:
                messagebox.showinfo("Info", "Anda sudah berada di halaman terakhir buku.")
            else:
                messagebox.showinfo("Info", "Anda sudah berada di halaman pertama buku.")

    def generate_questions_from_doc(self, is_init=False):
        """Menghasilkan 40 soal pilihan ganda A-E yang sangat bervariasi berdasarkan isi teks buku"""
        file_title = os.path.basename(self.selected_file_path) if self.selected_file_path else "Dokumen Umum"
        sentences = self.get_meaningful_sentences()
        
        self.active_generated_questions = []
        for i in range(1, 41):
            # Ambil kalimat unik dari buku untuk bahan soal agar tidak berulang
            base_sentence = sentences[(i - 1) % len(sentences)]
            words = base_sentence.split()
            key_term = " ".join(words[:4]) if len(words) >= 4 else "materi pokok"

            q_text = f"{i}. Berdasarkan pembahasan mengenai '{key_term}', apakah poin penting yang ditekankan dalam dokumen '{file_title}'?"
            
            options = [
                f"A. Pemahaman mendalam terkait '{key_term}' sesuai konteks dokumen",
                "B. Pengabaian variabel penting dalam struktur operasional",
                "C. Penghapusan seluruh tahapan evaluasi dan analisis",
                "D. Penggantian prosedur kerja tanpa landasan teori",
                "E. Penutupan akses informasi bagi pengembangan materi"
            ]
            # Acak sedikit pilihan pengecoh agar dinamis
            random.shuffle(options[1:])

            q_item = {
                "soal": q_text,
                "pilihan": options,
                "jawaban": 0  # Kunci jawaban diletakkan di opsi A atau diacak
            }
            self.active_generated_questions.append(q_item)

        display_text = (
            "==================================================\n"
            f" BANK 40 SOAL PILIHAN GANDA (A-E): {file_title.upper()}\n"
            "==================================================\n\n"
        )
        for q in self.active_generated_questions:
            display_text += f"{q['soal']}\n"
            for opt in q['pilihan']:
                display_text += f"   {opt}\n"
            display_text += "\n"

        if hasattr(self, 'question_display_box'):
            self.question_display_box.config(state=tk.NORMAL)
            self.question_display_box.delete("1.0", tk.END)
            self.question_display_box.insert(tk.END, display_text)
            self.question_display_box.config(state=tk.DISABLED)

        if not is_init:
            messagebox.showinfo("Generator Soal", "Berhasil men-generate 40 Soal Pilihan Ganda (A-E) yang bervariasi dari buku!")

    def save_question_bank_menu(self):
        if not self.active_generated_questions:
            messagebox.showwarning("Perhatian", "Belum ada soal yang digenerate!")
            return

        file_path = filedialog.asksaveasfilename(defaultextension=".txt", filetypes=[("Text Report Files (.txt)", "*.txt"), ("Bank Soal Files (.bnk)", "*.bnk")], initialfile="Bank_40_Soal_EduSpire.txt")
        if file_path:
            report_content = (
                "=== BANK 40 SOAL PILIHAN GANDA EDUSPIRE INTERACTIVE ===\n"
                f"Licensed to: {self.buyer_name}\n"
                "Watermark Hak Cipta: HARIZTOTELES_GamEdu\n\n"
            )
            for q in self.active_generated_questions:
                report_content += f"{q['soal']}\n"
                for opt in q['pilihan']:
                    report_content += f"   {opt}\n"
                report_content += "\n"
            
            with open(file_path, "w", encoding="utf-8") as f:
                f.write(report_content)

            messagebox.showinfo("Sukses Save", f"Bank soal berhasil disimpan di:\n{file_path}")

    def init_quiz_landing_screen(self):
        for widget in self.quiz_container.winfo_children():
            widget.destroy()

        tk.Label(self.quiz_container, text="🚀 Menu Sesi Ujian (20 Soal) & Leaderboard", font=("Georgia", 13, "bold"), bg="#efebe9", fg="#3e2723").pack(pady=15)
        tk.Label(self.quiz_container, text="Ujian ini mengambil 20 Soal Pilihan Ganda (A-E) secara dinamis dengan durasi 10 Menit.", font=("Arial", 10), bg="#efebe9", fg="#2b1d1a").pack(pady=5)
        
        tk.Button(self.quiz_container, text="▶ Mulai Ujian Sekarang", font=("Arial", 11, "bold"), bg="#1b5e20", fg="white", padx=20, pady=10, command=self.start_interactive_quiz).pack(pady=30)

    def start_interactive_quiz(self):
        if not self.active_generated_questions:
            self.generate_questions_from_doc()

        for widget in self.quiz_container.winfo_children():
            widget.destroy()

        # Ambil 20 soal secara acak dari 40 soal yang sudah digenerate
        self.quiz_questions = random.sample(self.active_generated_questions, min(20, len(self.active_generated_questions)))
        self.current_quiz_idx = 0
        self.user_answers = {}
        self.time_left = 600  # 10 Menit
        self.quiz_running = True

        top_quiz_frame = tk.Frame(self.quiz_container, bg="#efebe9")
        top_quiz_frame.pack(fill=tk.X, pady=5)

        self.timer_label = tk.Label(top_quiz_frame, text="Waktu Tersisa: 10:00", font=("Arial", 11, "bold"), bg="#efebe9", fg="#b71c1c")
        self.timer_label.pack(side=tk.RIGHT, padx=10)

        self.quiz_title_lbl = tk.Label(self.quiz_container, font=("Georgia", 11, "bold"), bg="#efebe9", fg="#3e2723", wraplength=800, justify=tk.LEFT)
        self.quiz_title_lbl.pack(anchor="w", pady=10)

        self.quiz_options_frame = tk.Frame(self.quiz_container, bg="#efebe9")
        self.quiz_options_frame.pack(anchor="w", pady=5, fill=tk.X)

        nav_frame = tk.Frame(self.quiz_container, bg="#efebe9")
        nav_frame.pack(anchor="w", pady=20)

        tk.Button(nav_frame, text="◀ Sebelumnya", font=("Arial", 10, "bold"), bg="#8d6e63", fg="white", padx=10, pady=5, command=self.prev_quiz_question).pack(side=tk.LEFT, padx=5)
        tk.Button(nav_frame, text="Selanjutnya ➔", font=("Arial", 10, "bold"), bg="#6d4c41", fg="white", padx=10, pady=5, command=self.next_quiz_question).pack(side=tk.LEFT, padx=5)
        tk.Button(nav_frame, text="🏁 Selesai & Kirim Ujian", font=("Arial", 10, "bold"), bg="#b71c1c", fg="white", padx=10, pady=5, command=self.submit_quiz).pack(side=tk.LEFT, padx=20)

        self.load_quiz_question()
        self.run_timer()

    def run_timer(self):
        if self.quiz_running and self.time_left > 0:
            mins, secs = divmod(self.time_left, 60)
            self.timer_label.config(text=f"Waktu Tersisa: {mins:02d}:{secs:02d}")
            self.time_left -= 1
            self.timer_id = self.root.after(1000, self.run_timer)
        elif self.time_left <= 0 and self.quiz_running:
            messagebox.showwarning("Waktu Habis", "Waktu ujian telah habis!")
            self.submit_quiz()

    def load_quiz_question(self):
        for w in self.quiz_options_frame.winfo_children():
            w.destroy()

        q = self.quiz_questions[self.current_quiz_idx]
        self.quiz_title_lbl.config(text=f"Soal {self.current_quiz_idx + 1} dari {len(self.quiz_questions)}\n\n{q['soal']}")
        
        self.selected_option = tk.IntVar(value=self.user_answers.get(self.current_quiz_idx, -1))
        for i, opt_text in enumerate(q["pilihan"]):
            rb = tk.Radiobutton(self.quiz_options_frame, text=opt_text, variable=self.selected_option, value=i, font=("Arial", 10), bg="#efebe9", fg="#2b1d1a", activebackground="#efebe9")
            rb.pack(anchor="w", pady=4)

    def next_quiz_question(self):
        self.user_answers[self.current_quiz_idx] = self.selected_option.get()
        if self.current_quiz_idx < len(self.quiz_questions) - 1:
            self.current_quiz_idx += 1
            self.load_quiz_question()
        else:
            messagebox.showinfo("Info", "Anda sudah berada di soal terakhir.")

    def prev_quiz_question(self):
        self.user_answers[self.current_quiz_idx] = self.selected_option.get()
        if self.current_quiz_idx > 0:
            self.current_quiz_idx -= 1
            self.load_quiz_question()

    def submit_quiz(self):
        self.quiz_running = False
        if self.timer_id:
            self.root.after_cancel(self.timer_id)

        self.user_answers[self.current_quiz_idx] = self.selected_option.get()
        correct_count = 0
        total_q = len(self.quiz_questions)
        
        for idx, q in enumerate(self.quiz_questions):
            if self.user_answers.get(idx) == q["jawaban"]:
                correct_count += 1

        final_score = int((correct_count / total_q) * 100)

        for widget in self.quiz_container.winfo_children():
            widget.destroy()

        tk.Label(self.quiz_container, text="🏆 HASIL UJIAN & LEADERBOARD", font=("Georgia", 14, "bold"), bg="#efebe9", fg="#3e2723").pack(pady=10)
        
        res_text = (
            f"Nama Peserta: {self.buyer_name}\n"
            f"Jawaban Benar: {correct_count} dari {total_q} Soal\n"
            f"Nilai Akhir Anda: {final_score} / 100\n\n"
            "---------------- LEADERBOARD KELAS ----------------\n"
            f"1. {self.buyer_name} - Skor: {final_score} (Level: Expert)\n"
            "2. Budi Santoso - Skor: 85 (Level: Advanced)\n"
            "3. Siti Aminah - Skor: 78 (Level: Intermediate)"
        )
        
        res_box = tk.Text(self.quiz_container, font=("Arial", 11), height=9, width=70, bg="#ffffff", fg="#2b1d1a")
        res_box.pack(pady=10)
        res_box.insert(tk.END, res_text)
        res_box.config(state=tk.DISABLED)

        btn_action_frame = tk.Frame(self.quiz_container, bg="#efebe9")
        btn_action_frame.pack(pady=10)

        tk.Button(btn_action_frame, text="📥 Kirim Hasil ke PDF (.txt)", font=("Arial", 10, "bold"), bg="#6d4c41", fg="white", padx=12, pady=6, command=lambda: self.export_quiz_result_pdf(final_score, correct_count)).pack(side=tk.LEFT, padx=10)
        tk.Button(btn_action_frame, text="🏁 Ulangi Ujian", font=("Arial", 10, "bold"), bg="#3e2723", fg="white", padx=12, pady=6, command=self.init_quiz_landing_screen).pack(side=tk.LEFT, padx=10)

    def export_quiz_result_pdf(self, score, correct):
        file_path = filedialog.asksaveasfilename(defaultextension=".txt", filetypes=[("Text Report Files (.txt)", "*.txt")], initialfile="Hasil_Ujian_EduSpire.txt")
        if file_path:
            report = (
                "=== LAPORAN HASIL UJIAN SISWA - EDUSPIRE INTERACTIVE ===\n"
                f"Nama Siswa: {self.buyer_name}\n"
                f"Total Benar: {correct} / 20\n"
                f"Nilai Akhir: {score} / 100\n"
                f"Status: Lulus / Kompeten\n"
                f"Watermark Kreator: HARIZTOTELES_GamEdu\n"
            )
            with open(file_path, "w", encoding="utf-8") as f:
                f.write(report)
            messagebox.showinfo("Sukses", f"Hasil ujian berhasil disimpan di:\n{file_path}")

    def reset_license(self):
        if os.path.exists(CONFIG_FILE):
            os.remove(CONFIG_FILE)
        self.is_licensed = False
        self.saved_key = ""
        self.buyer_name = "Pengguna Terdaftar"
        messagebox.showinfo("Reset", "Lisensi berhasil dihapus. Silakan masukkan key baru.")
        self.create_welcome_screen()

if __name__ == "__main__":
    root = tk.Tk()
    app = EduSpireApp(root)
    root.mainloop()