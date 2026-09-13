# ==========================================
# EduSpire Interactive - welcome_audio.py
# Modul Audio Bumper Opening (7-10 Detik)
# Watermark: HARIZTOTELES_GamEdu
# ==========================================

import time
import sys
import os

def play_welcome_bumper():
    """
    Memutar potongan audio opening (7-10 detik) menggunakan karya musik Anda sendiri.
    Pastikan file 'welcome_sound.wav' sudah diletakkan di folder yang sama.
    """
    print("==========================================")
    print("🎵 [AUDIO BUMPER] Memutar Opening EduSpire Interactive...")
    print("   Watermark Aktif: HARIZTOTELES_GamEdu")
    print("==========================================")
    
    audio_file = "welcome_sound.wav"
    
    if os.path.exists(audio_file):
        print(f"✅ File lagu ditemukan: '{audio_file}'")
        if sys.platform == "win32":
            try:
                import winsound
                # Memutar file audio .wav di background
                winsound.PlaySound(audio_file, winsound.SND_ASYNC)
            except Exception as e:
                print(f"[INFO] Gagal memutar audio: {e}")
    else:
        print(f"⚠️ Perhatian: File '{audio_file}' belum dimasukkan.")
        print("   Aplikasi berjalan menggunakan simulasi teks (silent mode).")
        print("   Tips: Masukkan potongan lagu 7-10 detik berformat .wav ke folder ini.")

    # Durasi bumper opening (8 detik sesuai rentang 7-10 detik)
    for i in range(8, 0, -1):
        print(f"   Memuat musik pembuka... sisa {i} detik", end="\r")
        time.sleep(1)
        
    print("\n🎵 [AUDIO BUMPER] Selesai. Selamat datang di aplikasi!\n")

if __name__ == "__main__":
    play_welcome_bumper()