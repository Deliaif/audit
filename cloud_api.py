import streamlit as st
import requests
import os

# --- 1. Konfigurasi API ---
# API_KEY diambil dari environment variable Streamlit (aman, tidak muncul di UI)
API_KEY = st.secrets.get("API_KEY")

PAGESPEED_API = "https://www.googleapis.com/pagespeedonline/v5/runPagespeed"

# --- 2. Fungsi Audit ---
def run_audit(url):
    """Menjalankan audit menggunakan Google PageSpeed API."""
    params = {
        "url": url,
        "key": API_KEY,
        "strategy": "desktop"
    }

    try:
        response = requests.get(PAGESPEED_API, params=params)
        if response.status_code == 200:
            results = response.json()
            performance_score = results["lighthouseResult"]["categories"]["performance"]["score"] * 100
            fetch_date = results["lighthouseResult"]["fetchTime"].split("T")[0]

            st.success(f"✅ Audit berhasil untuk: {url}")
            st.metric("Skor Kinerja (Desktop)", f"{int(performance_score)}/100")
            st.write(f"📅 Audit terakhir pada: {fetch_date}")

            # Core Web Vitals
            def get_metric(audit_key):
                audit = results["lighthouseResult"]["audits"].get(audit_key)
                return audit.get("displayValue", "N/A") if audit else "N/A"

            st.subheader("📊 Core Web Vitals")
            st.write(f"- **Largest Contentful Paint (LCP)**: {get_metric('largest-contentful-paint')}")
            st.write(f"- **Cumulative Layout Shift (CLS)**: {get_metric('cumulative-layout-shift')}")
            st.write(f"- **First Contentful Paint (FCP)**: {get_metric('first-contentful-paint')}")
        else:
            error_msg = response.json().get("error", {}).get("message", "Tidak ada pesan error.")
            st.error(f"❌ Error {response.status_code}: {error_msg}")
    except requests.exceptions.RequestException as e:
        st.error(f"❌ Terjadi kesalahan koneksi: {e}")

# --- 3. UI Streamlit ---
st.title("🌐 Website Performance Checker")
st.write("Cek skor kinerja situs menggunakan **Google PageSpeed Insights API** secara aman.")

url_input = st.text_input("Masukkan URL situs web", placeholder="https://contoh.com")

if st.button("🔍 Jalankan Audit"):
    if not API_KEY:
        st.error("❌ API Key tidak ditemukan. Tambahkan ke Streamlit secrets.")
    elif not url_input.strip():
        st.warning("Masukkan URL terlebih dahulu.")
    else:
        if not (url_input.startswith("http://") or url_input.startswith("https://")):
            url_input = "https://" + url_input
        run_audit(url_input)
