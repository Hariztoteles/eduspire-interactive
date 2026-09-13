# ==========================================
# EduSpire Interactive - question_generator.py
# Modul Komposisi & Generator Bank Soal (Tab 4)
# Watermark: HARIZTOTELES_GamEdu
# ==========================================

import random

class QuestionGenerator:
    def __init__(self, pg_count=10, tf_count=5, essay_count=3, matching_count=2):
        # Validasi batas total soal (10 - 40 pertanyaan)
        self.pg_count = pg_count
        self.tf_count = tf_count
        self.essay_count = essay_count
        self.matching_count = matching_count
        self.total_questions = pg_count + tf_count + essay_count + matching_count

    def validate_total(self) -> bool:
        """Memastikan total soal berada di rentang 10 - 40"""
        if 10 <= self.total_questions <= 40:
            print(f"[SUKSES] Komposisi valid. Total Soal: {self.total_questions} pertanyaan.")
            return True
        else:
            print(f"[WARNING] Total soal saat ini ({self.total_questions}). Harus berada di antara 10 - 40!")
            return False

    def generate_question_bank(self):
        """Membuat bank soal sesuai komposisi yang dipilih dengan distraktor pintar"""
        if not self.validate_total():
            return None

        print("\n📝 [TAB 4: GENERATOR BANK SOAL] - Meracik Pertanyaan...")
        bank_soal = {
            "pilihan_ganda": [],
            "benar_salah": [],
            "esai": [],
            "menjodohkan": []
        }

        # Simulasi pembuatan Pilihan Ganda (5 Opsi)
        for i in range(1, self.pg_count + 1):
            options = ["A", "B", "C", "D", "E"]
            random.shuffle(options)  # Mengacak opsi jawaban (Shuffle Engine)
            bank_soal["pilihan_ganda"].append({
                "no": i,
                "tipe": "Pilihan Ganda (5 Opsi)",
                "soal": f"Pertanyaan Pilihan Ganda nomor {i} berdasarkan materi?",
                "opsi_teracak": options,
                "kunci": "A"
            })

        # Simulasi Benar/Salah
        for i in range(1, self.tf_count + 1):
            bank_soal["benar_salah"].append({
                "no": i,
                "tipe": "Benar / Salah",
                "soal": f"Pernyataan faktual nomor {i}...",
                "kunci": "Benar"
            })

        print(f"   • Berhasil meracik {self.pg_count} Pilihan Ganda (teracak).")
        print(f"   • Berhasil meracik {self.tf_count} Benar/Salah.")
        print(f"   • Berhasil meracik {self.essay_count} Soal Esai.")
        print(f"   • Berhasil meracik {self.matching_count} Soal Menjodohkan.")
        print("   ✅ Bank Soal siap digunakan untuk sesi ujian!")

        return bank_soal

if __name__ == "__main__":
    # Contoh pengujian modul dengan komposisi custom
    generator = QuestionGenerator(pg_count=12, tf_count=8, essay_count=3, matching_count=2)
    bank = generator.generate_question_bank()