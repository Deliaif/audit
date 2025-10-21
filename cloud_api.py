import requests
import json
import sys

# --- 1. Konfigurasi API ---
# GANTI DENGAN KUNCI API ASLI ANDA
API_KEY = "AIzaSyD01GQOed0EG5ot0lEE0ElU5HhWzbjZQVc" 

# GANTI DENGAN ENDPOINT API YANG SESUAI JIKA ANDA MENGGUNAKAN LAYANAN LAIN
PAGESPEED_API = "https://www.googleapis.com/pagespeedonline/v5/runPagespeed"

# --- 2. Input dari Pengguna ---
def get_user_input():
    """Meminta URL dari pengguna dan melakukan validasi sederhana."""
    
    print("--- Alat Cek Situs Web Sederhana (Menggunakan PageSpeed API) ---")
    
    # Cek apakah API Key sudah diganti dari placeholder
    if API_KEY == "AIzaSyD01GQOed0EG5ot0lEE0ElU5HhWzbjZQVc":
        print("\n[PERINGATAN] Harap ganti variabel 'API_KEY' di kode dengan kunci Anda yang sebenarnya.")
        # Lanjutkan untuk demonstrasi, tetapi API akan gagal
    
    target_url = input("Masukkan URL situs web yang ingin diaudit (contoh: https://google.com): ").strip()

    if not target_url:
        print("Error: URL tidak boleh kosong.")
        sys.exit(1)
        
    # Validasi sederhana agar URL diawali http/https
    if not (target_url.startswith('http://') or target_url.startswith('https://')):
        target_url = 'https://' + target_url # Asumsi HTTPS jika tidak ada skema

    return target_url

# --- 3. Fungsi Utama Audit ---
def run_audit(url):
    """Mengirim permintaan ke API dan memproses hasilnya."""
    
    # Parameter permintaan ke API Google PageSpeed
    params = {
        'url': url, 
        'key': API_KEY,
        'strategy': 'desktop'  # Anda bisa ganti ke 'mobile'
    }

    print("\n" + "=" * 50)
    print(f"Menganalisis URL: {url}")
    print("=" * 50)
    
    try:
        # Mengirim permintaan GET
        response = requests.get(PAGESPEED_API, params=params)
        
        # Cek status kode respons
        if response.status_code == 200:
            results = response.json()
            
            print("✅ AUDIT BERHASIL")
            
            # Mendapatkan skor kinerja utama (dikalikan 100 karena API memberikan nilai 0.x)
            performance_score = results['lighthouseResult']['categories']['performance']['score'] * 100
            
            print(f"Skor Kinerja Desktop: **{int(performance_score)}/100**")
            print(f"Audit Terakhir pada: {results['lighthouseResult']['fetchTime'].split('T')[0]}")
            
            # Menampilkan metrik Core Web Vitals
            print("\nMetrik Core Web Vitals:")
            
            def get_metric_value(audit_key):
                """Fungsi helper untuk mendapatkan nilai metrik."""
                audit = results['lighthouseResult']['audits'].get(audit_key)
                return audit.get('displayValue', 'N/A') if audit else 'N/A'

            print(f"- Largest Contentful Paint (LCP): {get_metric_value('largest-contentful-paint')}")
            print(f"- Cumulative Layout Shift (CLS): {get_metric_value('cumulative-layout-shift')}")
            print(f"- First Contentful Paint (FCP): {get_metric_value('first-contentful-paint')}")
            
            print("\n" + "=" * 50)

        elif response.status_code == 400:
            print(f"❌ Error: Kesalahan di sisi permintaan (Status {response.status_code}).")
            # Kemungkinan API Key tidak valid atau URL tidak dapat diakses
            print(f"Pesan: {response.json().get('error', {}).get('message', 'Tidak ada pesan error.')}")

        else:
            print(f"❌ Gagal memanggil API. Kode Status: {response.status_code}")
            print(f"Detail Error: {response.text}")


    except requests.exceptions.RequestException as e:
        print(f"❌ Terjadi kesalahan koneksi atau jaringan: {e}")

# --- 4. Main Program ---
if __name__ == "__main__":
    target_url = get_user_input()
    run_audit(target_url)