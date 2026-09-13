# ==========================================
# EduSpire Interactive - exam_engine.py
# Modul Ujian Interaktif, Timer, & Lockout System
# Watermark: HARIZTOTELES_GamEdu
# ==========================================

import time
import random

class ExamEngine:
    def __init__(self, student_name: str, student_class: str, total_time_minutes: int = 15):
        self.student_name = student_name
        self.student_class = student_class
        self.total_time_seconds = total_time_minutes * 60
        self.is_exam_running = False
        self.bookmarked_questions = []

    def start_exam(self):
        """Memulai ujian: Memicu audio mulai dan mengunci materi (lockout system)"""
        self.is_exam_running = True
        print("\n==========================================")
        print("🚀 [UJIAN DIMULAI] Selamat Mengerjakan!")
        print(f"   Peserta: {self.student_name} ({self.student_class})")
        print("   🎵 [AUDIO MULAI] *Bunyi peluit/gong tes dimulai*")
        print("   🔒 [LOCKOUT SYSTEM] Tab Rangkuman & Mind Map TERKUNCI!")
        print("==========================================")
        
        # Simulasi status materi terkunci
        self.enforce_lockout_check()

    def enforce_lockout_check(self):
        """Memastikan materi tidak bisa dibuka selama ujian berlangsung"""
        if self.is_exam_running:
            print("   [INFO KEAMANAN] Akses materi diblokir. Fokus pada soal ujian!")

    def bookmark_question(self, question_no: int):
        """Fitur penanda soal ragu-ragu (warna kuning)"""
        if question_no not in self.bookmarked_questions:
            self.bookmarked_questions.append(question_no)
            print(f"   📌 Soal nomor {question_no} ditandai sebagai ragu-ragu.")

    def submit_exam(self, correct_answers_count: int, total_questions: int):
        """Menyelesaikan ujian: Menghentikan timer, membuka kunci, & menghitung leaderboard"""
        self.is_exam_running = False
        print("\n==========================================")
        print("🏁 [UJIAN SELESAI] Waktu Berakhir / Disubmit.")
        print("   🎵 [AUDIO SELESAI] *Bunyi bel akhir ujian*")
        print("   🔓 [LOCKOUT SYSTEM] Akses materi & pembahasan DIBUKA KEMBALI!")
        print("==========================================")

        # Perhitungan Skor & Gamifikasi Leaderboard
        base_score = (correct_answers_count / total_questions) * 100
        
        # Simulasi bonus kecepatan (Gamifikasi)
        speed_bonus = random.randint(5, 15)
        final_score = min(100, base_score + (speed_bonus if base_score > 70 else 0))

        # Penentuan Gelar / Badge Unik di Leaderboard
        if final_score >= 90:
            badge = "🏆 The Master (Sempurna & Teliti)"
        elif final_score >= 75:
            badge = "⚡ The Speedster (Cepat & Cerdas)"
        else:
            badge = "💡 The Thinker (Butuh Pendalaman Bab)"

        print(f"\n📊 HASIL EVALUASI - {self.student_name}:")
        print(f"   • Skor Akhir : {final_score:.1f} / 100")
        print(f"   • Predikat   : {badge}")
        print("   • Status     : Data berhasil dimasukkan ke Papan Peringkat (Leaderboard).")

        return final_score, badge

if __name__ == "__main__":
    # Contoh pengujian simulasi ujian mandiri
    engine = ExamEngine("Siti Aminah", "Kelas X-A")
    engine.start_exam()
    
    # Simulasi siswa menandai soal ragu-ragu
    engine.bookmark_question(3)
    engine.bookmark_question(7)
    
    # Simulasi selesai ujian (misal benar 18 dari 20 soal)
    time.sleep(2)
    engine.submit_exam(correct_answers_count=18, total_questions=20)