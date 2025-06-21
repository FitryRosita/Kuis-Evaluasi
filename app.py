import streamlit as st
import joblib

# === Konfigurasi halaman ===
st.set_page_config(page_title="🎯 Kuis Evaluasi - Cublak-Cublak Suweng", page_icon="🎯")

# === Load soal dari model .pkl ===
soal_pilgan = joblib.load("kuis_evaluasi.pkl")

# === Tampilan awal dan input nama ===
st.title("🎮 Kuis Evaluasi")
st.caption("Topik: Evaluasi Peluang - Cublak-Cublak Suweng")

if "nama_dikunci" not in st.session_state:
    st.session_state.nama_dikunci = False

if not st.session_state.nama_dikunci:
    nama = st.text_input("Masukkan nama kamu:")
    if nama:
        if st.button("Mulai Kuis"):
            st.session_state.nama = nama
            st.session_state.nama_dikunci = True

else:
    st.success(f"Halo, {st.session_state.nama}! Silakan menjawab soal berikut.")

    # === Menampilkan soal-soal ===
    jawaban_pengguna = []
    for i, soal in enumerate(soal_pilgan):
        st.markdown(f"**{i+1}. {soal['soal']}**")
        jawaban = st.radio("Pilih jawaban kamu:", soal["opsi"], key=f"soal_{i}")
        jawaban_pengguna.append(jawaban.strip()[:1])  # Ambil A/B/C/D

    # === Tombol untuk submit jawaban ===
    if st.button("📨 Kirim Jawaban"):
        skor = 0
        benar = 0
        salah = 0
        st.subheader("📊 Hasil Jawaban")
        for i, jawaban in enumerate(jawaban_pengguna):
            kunci = soal_pilgan[i]["jawaban"]
            if jawaban == kunci:
                st.success(f"Soal {i+1}: ✅ Benar (Jawaban: {kunci})")
                skor += 1
                benar += 1
            else:
                st.error(f"Soal {i+1}: ❌ Salah (Jawaban: {kunci})")
                salah += 1

        nilai = int((skor / len(soal_pilgan)) * 100)

        # === Ringkasan skor akhir ===
        st.markdown("---")
        st.subheader("🎓 Ringkasan Nilai Akhir")
        st.markdown(f"""
            <div style='background-color:#fef9e7; padding: 16px; border-radius: 10px; text-align: center;'>
                <h4> Nama: <b>{st.session_state.nama}</b></h4>
                <h5>✅ Jawaban Benar: <b>{benar}</b></h5>
                <h5>❌ Jawaban Salah: <b>{salah}</b></h5>
                <h3>🎯 Nilai: <b>{nilai}/100</b></h3>
            </div>
        """, unsafe_allow_html=True)
