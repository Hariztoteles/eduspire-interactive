# ==========================================
# EduSpire Interactive - doc_parser.py
# Modul Pembaca Dokumen Lokal (PDF/Word) & Deteksi Bab
# Watermark: HARIZTOTELES_GamEdu
# ==========================================

import os

class DocParser:
    def __init__(self, file_path: str):
        self.file_path = file_path
        self.file_name = os.path.basename(file_path)
        self.extension = os.path.splitext(file_path)[1].lower()

    def validate_file(self) -> bool:
        """Memeriksa apakah file ada dan formatnya didukung (PDF atau DOCX)"""
        if not os.path.exists(self.file_path):
            print(f"[ERROR] File tidak ditemukan: {self.file_name}")
            return False
        
        if self.extension in [".pdf", ".docx"]:
            print(f"[SUKSES] Format file valid ({self.extension}): {self.file_name}")
            return True
        else:
            print(f"[WARNING] Format '{self.extension}' tidak didukung. Harap gunakan PDF atau Word (.docx).")
            return False

    def scan_chapters_and_content(self):
        """
        Mensimulasikan pemindaian dokumen untuk mendeteksi daftar isi dan struktur bab.
        Pada implementasi nyata, modul ini mengekstrak teks dan mencari pola kata 'Bab' atau 'Chapter'.
        """
        print(f"\n📂 Memindai struktur dokumen: {self.file_name}...")
        
        # Simulasi hasil deteksi bab otomatis dari buku/dokumen yang diunggah
        detected_chapters = [
            {"id": 1, "title": "Bab 1: Pendahuluan & Konsep Dasar"},
            {"id": 2, "title": "Bab 2: Analisis Teori & Prinsip Utama"},
            {"id": 3, "title": "Bab 3: Studi Kasus & Penerapan Praktis"},
            {"id": 4, "title": "Bab 4: Kesimpulan & Evaluasi Akhir"}
        ]
        
        print("🔍 Hasil Deteksi Bab Otomatis:")
        for ch in detected_chapters:
            print(f"   - [Bab {ch['id']}] {ch['title']}")
            
        return detected_chapters

if __name__ == "__main__":
    # Contoh pengujian modul secara mandiri
    sample_file = "buku_materi_contoh.pdf"
    
    # Membuat file dummy untuk tes jika belum ada
    if not os.path.exists(sample_file):
        with open(sample_file, "w") as f:
            f.write("Dummy PDF content for EduSpire Interactive.")
            
    parser = DocParser(sample_file)
    if parser.validate_file():
        parser.scan_chapters_and_content()
        
    # Membersihkan file dummy pengujian
    if os.path.exists(sample_file):
        os.remove(sample_file)