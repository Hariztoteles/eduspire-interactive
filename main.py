# ==========================================
# EduSpire Interactive - main.py (Full Script)
# Pusat Kendali Utama & Alur Simulasi Aplikasi
# Watermark Kreator: HARIZTOTELES_GamEdu
# ==========================================

import os
import time

# Import modul-modul modular yang sudah kita buat
from license_guard import generate_license_key, verify_license, CREATOR_WATERMARK
from welcome_audio import play_welcome_bumper
from doc_parser import DocParser
from tabs_manager import TabsManager
from question_generator import QuestionGenerator
from exam_engine import ExamEngine
from export_manager import ExportManager
from pdf_exporter import PDFExporter
from question_exporter import QuestionExporter

def main():
    print("==================================================")
    print("      SELAMAT DATANG DI EDUSPIRE INTERACTIVE      ")
    print(f"      Watermark Proteksi: {CREATOR_WATERMARK}     ")
    print("==================================================")

    # ----------------------------------------------------
    # TAHAP 1: VERIFIKASI LISENSI PEMBELI (KEYGEN)
    # ----------------------------------------------------
    print("\n--- [TAHAP 1] VERIFIKASI LISENSI ---")
    buyer_name = "Budi Santoso, S.Pd."
    buyer_email = "budi.teacher@school.edu"
    
    # Sistem otomatis membuatkan key untuk pembeli tersebut
    valid_key = generate_license_key(buyer_name, buyer_email)
    print(f"Informasi Pembeli : {buyer_name} ({buyer_email})")
    print(f"Generated Key    : {valid_key}")

    # Memverifikasi lisensi
    if not verify_license(buyer_name, buyer_email, valid_key):
        print("[GAGAL] Lisensi tidak sah. Aplikasi dihentikan.")
        return

    # ----------------------------------------------------
    # TAHAP 2: AUDIO BUMPER OPENING (Karya Musik Anda)
    # ----------------------------------------------------
    print("\n--- [TAHAP 2] PEMUTARAN AUDIO BUMPER ---")
    play_welcome_bumper()

    # ----------------------------------------------------
    # TAHAP 3: UNGGAH & PEMINDAIAN DOKUMEN / BUKU LOKAL
    # ----------------------------------------------------
    print("\n--- [TAHAP 3] UPLOAD & PARSING DOKUMEN ---")
    dummy_book = "buku_materi_ajar.pdf"
    
    # Buat file dummy sementara untuk simulasi
    with open(dummy_book, "w", encoding="utf-8") as f:
        f.write("Simulasi teks lengkap materi buku ratusan halaman.")

    parser = DocParser(dummy_book)
    if parser.validate_file():
        chapters = parser.scan_chapters_and_content()

    # ----------------------------------------------------
    # TAHAP 4: RANGKUMAN & MIND MAP (Tab 1-3 & Tab 5)
    # ----------------------------------------------------
    print("\n--- [TAHAP 4] TAMPILAN RANGKUMAN & PETA KONSEP ---")
    tabs = TabsManager("Buku Pintar Kurikulum Merdeka")
    tabs.generate_tab_summary(chapter_id=1)
    tabs.generate_tab_mindmap(chapter_id=1)

    # ----------------------------------------------------
    # TAHAP 5: GENERATOR BANK SOAL KUSTOM (Tab 4)
    # ----------------------------------------------------
    print("\n--- [TAHAP 5] KOMPOSISI & GENERATE BANK SOAL ---")
    # Pengguna mengatur komposisi (misal: 12 PG, 8 True/False, 3 Esai, 2 Matching = 25 Soal)
    q_gen = QuestionGenerator(pg_count=12, tf_count=8, essay_count=3, matching_count=2)
    bank_soal = q_gen.generate_question_bank()

    # Opsi Ekspor Soal ke PDF, Word, atau .bnk
    if bank_soal:
        q_exporter = QuestionExporter(bank_soal, "Ujian Evaluasi Bab 1")
        q_exporter.export_to_pdf("Hasil_Bank_Soal.pdf")
        q_exporter.export_to_word("Hasil_Bank_Soal.docx")
        q_exporter.export_to_bnk("Hasil_Bank_Soal.bnk")

    # ----------------------------------------------------
    # TAHAP 6: PELAKSANAAN UJIAN INTERAKTIF (Exam Engine)
    # ----------------------------------------------------
    print("\n--- [TAHAP 6] SESI UJIAN SISWA ---")
    student = ExamEngine("Andi Pratama", "Kelas X-A SMAN 36")
    student.start_exam()
    
    # Simulasi siswa menandai soal ragu-ragu
    student.bookmark_question(4)
    student.bookmark_question(12)
    
    # Simulasi siswa menyelesaikan ujian (Benar 22 dari 25 soal)
    time.sleep(1)
    final_score, badge = student.submit_exam(correct_answers_count=22, total_questions=25)

    # ----------------------------------------------------
    # TAHAP 7: EKSPOR DATA GURU & CETAK LAPORAN PDF
    # ----------------------------------------------------
    print("\n--- [TAHAP 7] REKAPITULASI & LAPORAN AKHIR ---")
    
    # Rekapitulasi Nilai Guru
    exporter_guru = ExportManager("Kelas X-A SMAN 36")
    exporter_guru.add_student_record("Andi Pratama", "NIS-101", final_score, badge)
    exporter_guru.export_to_google_spreadsheet()
    exporter_guru.export_via_email("haris.teacher@sman36.edu")

    # Cetak Sertifikat PDF Peserta
    pdf_rep = PDFExporter("Sertifikat Kelulusan Ujian EduSpire")
    pdf_rep.generate_pdf_report("Andi Pratama", final_score, "Sertifikat_Andi_Pratama.pdf")

    # Bersihkan file sampah simulasi uji coba di folder
    cleanup_files = [dummy_book, "Hasil_Bank_Soal.pdf", "Hasil_Bank_Soal.docx", "Hasil_Bank_Soal.bnk", "Sertifikat_Andi_Pratama.pdf"]
    for file in cleanup_files:
        if os.path.exists(file):
            os.remove(file)

    print("\n==================================================")
    print("   SELURUH ALUR Aplikasi EduSpire Berjalan Sukses! ")
    print("==================================================")

if __name__ == "__main__":
    main()