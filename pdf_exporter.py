# ==========================================
# EduSpire Interactive - pdf_exporter.py
# Modul Cetak Laporan PDF (Sertifikat Nilai & Rangkuman Buku)
# Watermark: HARIZTOTELES_GamEdu
# ==========================================

import os

class PDFExporter:
    def __init__(self, title: str):
        self.title = title
        self.watermark = "HARIZTOTELES_GamEdu"

    def generate_pdf_report(self, student_name: str, score: float, output_filename: str):
        """Mensimulasikan pembuatan file PDF sertifikat nilai peserta"""
        print(f"\n📄 [PDF GENERATOR] Merancang dokumen PDF untuk: {student_name}...")
        print(f"   • Judul Dokumen : {self.title}")
        print(f"   • Skor Akhir    : {score} / 100")
        print(f"   • Watermark     : Tersemat lisensi [{self.watermark}]")
        
        # Simulasi pembuatan file fisik
        with open(output_filename, "w", encoding="utf-8") as f:
            f.write(f"=== SERTIFIKAT HASIL EVALUASI ===\n")
            f.write(f"Aplikasi: EduSpire Interactive\n")
            f.write(f"Kreator: {self.watermark}\n")
            f.write(f"Peserta: {student_name}\n")
            f.write(f"Skor: {score}\n")
            
        print(f"   ✅ File PDF berhasil disimpan sebagai: '{output_filename}'")

if __name__ == "__main__":
    # Contoh pengujian cetak PDF
    exporter = PDFExporter("Sertifikat Hasil Ujian EduSpire")
    exporter.generate_pdf_report("Budi Santoso", 92.5, "Sertifikat_Budi_Santoso.pdf")
    
    # Bersihkan file uji coba fisik
    if os.path.exists("Sertifikat_Budi_Santoso.pdf"):
        os.remove("Sertifikat_Budi_Santoso.pdf")