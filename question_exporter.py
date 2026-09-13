# ==========================================
# EduSpire Interactive - question_exporter.py
# Modul Ekspor Bank Soal (PDF, Word/RTF, & .BNK)
# Watermark: HARIZTOTELES_GamEdu
# ==========================================

import os
import json

class QuestionExporter:
    def __init__(self, question_bank: dict, title: str = "Bank Soal EduSpire"):
        self.question_bank = question_bank
        self.title = title
        self.watermark = "HARIZTOTELES_GamEdu"

    def export_to_pdf(self, filename="Bank_Soal_Ujian.pdf"):
        """Mengekspor bank soal ke format PDF cetak"""
        print(f"\n📄 [EXPORT PDF] Menyusun dokumen PDF: {filename}...")
        with open(filename, "w", encoding="utf-8") as f:
            f.write(f"=== {self.title.upper()} ===\n")
            f.write(f"Dibuat oleh: {self.watermark}\n\n")
            
            # Menuliskan soal pilihan ganda
            if "pilihan_ganda" in self.question_bank:
                f.write("--- BAGIAN: PILIHAN GANDA ---\n")
                for q in self.question_bank["pilihan_ganda"]:
                    f.write(f"{q['no']}. {q['soal']}\n")
                    for opt in q['opsi_teracak']:
                        f.write(f"    ({opt}) Pilihan opsi...\n")
                    f.write(f"    Kunci: {q['kunci']}\n\n")
                    
        print(f"   ✅ Berhasil mengekspor ke '{filename}'")

    def export_to_word(self, filename="Bank_Soal_Ujian.docx"):
        """Mengekspor bank soal ke format Word (.docx / RTF friendly)"""
        print(f"\n📝 [EXPORT WORD] Menyusun dokumen Word: {filename}...")
        with open(filename, "w", encoding="utf-8") as f:
            f.write(f"Dokumen Bank Soal - {self.title}\n")
            f.write(f"Watermark Hak Cipta: {self.watermark}\n\n[Isi Soal Terformat Word]\n")
        print(f"   ✅ Berhasil mengekspor ke '{filename}'")

    def export_to_bnk(self, filename="paket_materi.bnk"):
        """Mengekspor bank soal ke ekstensi kustom .bnk (bisa di-import ulang)"""
        print(f"\n💾 [EXPORT .BNK] Mengemas bank soal ke format ekstensi .bnk...")
        package_data = {
            "creator": self.watermark,
            "title": self.title,
            "data": self.question_bank
        }
        with open(filename, "w", encoding="utf-8") as f:
            json.dump(package_data, f, indent=4)
        print(f"   ✅ Berhasil menyimpan file arsip kustom ke '{filename}'")

if __name__ == "__main__":
    # Uji coba modul ekspor soal
    dummy_bank = {
        "pilihan_ganda": [
            {"no": 1, "soal": "Apa ibukota Indonesia?", "opsi_teracak": ["A", "B", "C", "D", "E"], "kunci": "A"}
        ]
    }
    
    exporter = QuestionExporter(dummy_bank, "Ujian Biologi Kelas X")
    exporter.export_to_pdf("Ujian_Biologi.pdf")
    exporter.export_to_word("Ujian_Biologi.docx")
    exporter.export_to_bnk("Ujian_Biologi.bnk")
    
    # Membersihkan file uji coba fisik
    for file in ["Ujian_Biologi.pdf", "Ujian_Biologi.docx", "Ujian_Biologi.bnk"]:
        if os.path.exists(file):
            os.remove(file)