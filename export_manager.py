# ==========================================
# EduSpire Interactive - export_manager.py
# Modul Rekapitulasi Nilai & Ekspor Guru
# Watermark: HARIZTOTELES_GamEdu
# ==========================================

class ExportManager:
    def __init__(self, class_name: str):
        self.class_name = class_name
        self.exam_records = []

    def add_student_record(self, name: str, identity_id: str, score: float, badge: str):
        """Menambahkan hasil ujian siswa ke dalam daftar rekap"""
        record = {
            "nama": name,
            "identitas": identity_id,
            "skor": score,
            "predikat": badge
        }
        self.exam_records.append(record)

    def export_to_google_spreadsheet(self):
        """Mensimulasikan ekspor rekap nilai otomatis ke Google Spreadsheet guru"""
        print(f"\n📊 [GURU EXPORT] Mengirim rekap kelas {self.class_name} ke Google Spreadsheet...")
        for idx, rec in enumerate(self.exam_records, 1):
            print(f"   Row {idx} | {rec['nama']} ({rec['identitas']}) -> Skor: {rec['skor']} [{rec['predikat']}]")
        print("   ✅ Sukses! Data rekap berhasil disinkronkan ke Google Spreadsheet.")

    def export_via_email(self, teacher_email: str):
        """Mensimulasikan pengiriman laporan rekap via email kepada pengajar"""
        print(f"\n📧 [GURU EXPORT] Mengirim laporan rekap ke email pengajar: {teacher_email}...")
        print(f"   ✅ Email rekapitulasi kelas {self.class_name} berhasil dikirim!")

if __name__ == "__main__":
    # Contoh pengujian modul
    exporter = ExportManager("Kelas X-A SMAN 36")
    exporter.add_student_record("Budi Santoso", "1001", 92.5, "🏆 The Master")
    exporter.add_student_record("Siti Aminah", "1002", 85.0, "⚡ The Speedster")
    
    exporter.export_to_google_spreadsheet()
    exporter.export_via_email("guru.pembimbing@school.edu")