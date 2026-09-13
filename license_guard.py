# ==========================================
# EduSpire Interactive - license_guard.py
# Modul Validasi Lisensi & Keygen Pembeli
# Watermark: HARIZTOTELES_GamEdu
# ==========================================

import hashlib

CREATOR_WATERMARK = "HARIZTOTELES_GamEdu"

def generate_license_key(name: str, email: str) -> str:
    """
    Fungsi generator keygen sederhana berdasarkan nama dan email pembeli.
    Menghasilkan string unik yang berfungsi sebagai kunci lisensi.
    """
    raw_data = f"{name.strip().lower()}-{email.strip().lower()}-EDUSPIRE-2026"
    # Membuat hash MD5 lalu mengambil 12 karakter pertama dipisah strip agar rapi
    hash_object = hashlib.md5(raw_data.encode())
    hex_dig = hash_object.hexdigest().upper()
    
    # Format Key: EDU-XXXX-XXXX-XXXX
    key = f"EDU-{hex_dig[0:4]}-{hex_dig[4:8]}-{hex_dig[8:12]}"
    return key

def verify_license(name: str, email: str, input_key: str) -> bool:
    """
    Memverifikasi apakah key yang dimasukkan pembeli cocok dengan data nama & email mereka.
    """
    expected_key = generate_license_key(name, email)
    if input_key.strip().upper() == expected_key:
        print(f"[SUCCESS] Lisensi valid untuk: {name} ({email})")
        print(f"[BRANDS] Sistem dilindungi oleh watermark: {CREATOR_WATERMARK}")
        return True
    else:
        print("[WARNING] Lisensi tidak valid!")
        return False

if __name__ == "__main__":
    # Contoh pengujian lokal sistem keygen
    test_name = "Budi Santoso"
    test_email = "budi@example.com"
    sample_key = generate_license_key(test_name, test_email)
    
    print(f"Contoh Nama : {test_name}")
    print(f"Contoh Email: {test_email}")
    print(f"Generated Key: {sample_key}")
    
    # Uji verifikasi
    verify_license(test_name, test_email, sample_key)