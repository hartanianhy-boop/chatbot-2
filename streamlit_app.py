import streamlit as st
from google import genai
from google.genai import types
import pandas as pd
from datetime import datetime

# --- KONFIGURASI HALAMAN & TEMA WARNA (SESUAI LK-3) ---
st.set_page_config(
    page_title="HistoriBot AI - Sejarah Pergerakan Nasional",
    page_icon="🏛️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS: Palet Merah Marun (#8B1E1E), Krem (#FAF6F0), Biru Tua (#1E293B) & Mobile-First
st.markdown("""
<style>
    .stApp {
        background-color: #FAF6F0;
        color: #1E293B;
        font-size: 16px;
    }
    h1, h2, h3 {
        color: #8B1E1E !important;
        font-family: 'Georgia', serif;
    }
    .stButton>button {
        background-color: #8B1E1E;
        color: #FFFFFF;
        border-radius: 8px;
        border: none;
        padding: 0.5rem 1rem;
        font-weight: 600;
        width: 100%;
    }
    .stButton>button:hover {
        background-color: #6B1515;
        color: #FAF6F0;
    }
    .card-box {
        background-color: #FFFFFF;
        padding: 1.2rem;
        border-radius: 10px;
        border-left: 5px solid #8B1E1E;
        box-shadow: 0 2px 6px rgba(0,0,0,0.06);
        margin-bottom: 1rem;
    }
    @media (max-width: 768px) {
        .stApp { font-size: 15px; }
    }
</style>
""", unsafe_allow_html=True)

# --- INISIALISASI GEMINI API ---
api_key = st.secrets.get("GEMINI_API_KEY", "")
client = genai.Client(api_key=api_key) if api_key else None

# --- KNOWLEDGE BASE RINGKAS (1908–1945) ---
KNOWLEDGE_BASE = """
Materi Sejarah Pergerakan Nasional Indonesia (1908-1945) - Fase F Kelas XI:
1. 1908 - Kebangkitan Nasional (Budi Utomo): Didirikan 20 Mei 1908 oleh Dr. Soetomo dan pelajar STOVIA atas gagasan dr. Wahidin Sudirohusodo. Menandai perjuangan modern berbasis organisasi.
2. 1912 - Sarekat Islam (SI): Awalnya Sarekat Dagang Islam (H. Samanhudi, 1911), diubah menjadi SI oleh H.O.S. Tjokroaminoto agar menjangkau rakyat luas dan melawan dominasi ekonomi kolonial.
3. 1912 - Indische Partij: Didirikan Tiga Serangkai (Douwes Dekker, Tjipto Mangoenkoesoemo, Ki Hajar Dewantara). Organisasi politik pertama yang secara tegas menuntut kemerdekaan Hindia Belanda.
4. 1922 - Perhimpunan Indonesia (PI): Organisasi mahasiswa di Belanda (Moh. Hatta, dkk.) yang memopulerkan istilah 'Indonesia' dan konsep non-kooperasi (kemandirian bangsa).
5. 1927 - Partai Nasional Indonesia (PNI): Didirikan Ir. Soekarno dkk. dengan asas Marhaenisme dan sikap non-kooperatif terhadap pemerintah kolonial Belanda.
6. 1928 - Sumpah Pemuda: Kongres Pemuda II (27-28 Oktober 1928) menghasilkan ikrar Satu Nusa, Satu Bangsa, Satu Bahasa Indonesia, dipelopori PPPI dengan sekretaris M. Yamin dan dikumandangkannya lagu Indonesia Raya karya W.R. Supratman.
7. 1942-1945 - Pendudukan Jepang & Persiapan Kemerdekaan: Pembentukan BPUPKI (1 Maret 1945) untuk merumuskan dasar negara (Pancasila 1 Juni 1945) dan UUD 1945, dilanjutkan PPKI hingga Proklamasi Kemerdekaan 17 Agustus 1945.
"""

def tanya_gemini(prompt_user, system_instruction):
    if not client:
        return "⚠️ **GEMINI_API_KEY belum diatur.** Silakan tambahkan `GEMINI_API_KEY` di menu *Settings > Secrets* pada Streamlit Cloud."
    try:
        response = client.models.generate_content(
            model="gemini-2.5-flash",
            contents=prompt_user,
            config=types.GenerateContentConfig(
                system_instruction=system_instruction,
                temperature=0.6
            )
        )
        return response.text
    except Exception as e:
        return f"Terjadi kendala koneksi AI: {e}"

# --- INISIALISASI SESSION STATE (MANAJEMEN MEMORI) ---
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []
if "roleplay_history" not in st.session_state:
    st.session_state.roleplay_history = []
if "rekap_nilai" not in st.session_state:
    # Data awal contoh agar Dashboard Guru langsung terlihat fungsional
    st.session_state.rekap_nilai = [
        {"Waktu": "2026-11-15 09:15", "Nama Murid": "Andi Pratama", "Kelas": "XI IPS 1", "Skor": 80, "Topik Minat": "Sumpah Pemuda 1928"},
        {"Waktu": "2026-11-15 09:22", "Nama Murid": "Siti Nurhaliza", "Kelas": "XI IPS 1", "Skor": 100, "Topik Minat": "Budi Utomo & Kebangkitan Nasional"}
    ]
if "pemantik_kronologi" not in st.session_state:
    st.session_state.pemantik_kronologi = ""

# --- NAVIGASI SIDEBAR ---
with st.sidebar:
    st.markdown("## 🏛️ HistoriBot AI")
    st.caption("Asisten Interaktif Sejarah Pergerakan Nasional (Fase F)")
    st.markdown("---")
    menu = st.radio(
        "Pilih Menu Belajar:",
        [
            "🏠 1. Beranda",
            "⏳ 2. Peta Kronologi (1908–1945)",
            "💬 3. Tanya-Jawab AI",
            "🎭 4. Simulasi Roleplay Tokoh",
            "📝 5. Kuis HOTS & Dashboard Guru"
        ]
    )
    st.markdown("---")
    st.info("UPT SMAN 10 Luwu Timur\n\nDikembangkan oleh: Hartani, S.Pd")

# =====================================================================
# HALAMAN 1: BERANDA
# =====================================================================
if menu == "🏠 1. Beranda":
    st.title("Selamat Datang di HistoriBot AI 🇮🇩")
    st.subheader("Asisten Belajar Interaktif Sejarah Pergerakan Nasional Indonesia (1908–1945)")
    
    st.markdown("""
    <div class="card-box">
        <b>Tentang Aplikasi:</b><br>
        <b>HistoriBot AI</b> dirancang khusus untuk murid SMA Fase F agar dapat menjelajahi jejak perjuangan kemerdekaan Indonesia secara interaktif, berdialog langsung dengan simulasi tokoh sejarah, serta menguji kemampuan analisis berpikir tingkat tinggi (HOTS).
    </div>
    """, unsafe_allow_html=True)

    col1, col2 = st.columns(2)
    with col1:
        st.markdown("### 🧭 Panduan Penggunaan")
        st.markdown("""
        1. **Peta Kronologi:** Telusuri peristiwa kunci dari 1908 hingga 1945 dan klik tombol analisis AI.
        2. **Tanya-Jawab AI:** Diskusikan hubungan sebab-akibat peristiwa sejarah bersama pemandu AI.
        3. **Simulasi Roleplay:** Wawancarai langsung simulasi tokoh **Ir. Soekarno** atau **Mohammad Yamin**.
        4. **Kuis & Dashboard:** Kerjakan soal analisis HOTS dengan umpan balik otomatis.
        """)
    with col2:
        st.markdown("### 🎯 Capaian Pembelajaran (Fase F)")
        st.markdown("""
        - Menganalisis lahirnya kesadaran nasional dan pergerakan kebangsaan Indonesia (1908–1928).
        - Mengevaluasi strategi perjuangan kooperatif dan non-kooperatif melawan kolonialisme.
        - Menghubungkan dinamika masa pendudukan Jepang dengan peristiwa Proklamasi 17 Agustus 1945.
        """)

# =====================================================================
# HALAMAN 2: PETA KRONOLOGI DIGITAL
# =====================================================================
elif menu == "⏳ 2. Peta Kronologi (1908–1945)":
    st.title("⏳ Peta Kronologi Digital (1908–1945)")
    st.write("Pilih tonggak tahun peristiwa di bawah ini untuk melihat ringkasan sejarah dan memicu diskusi mendalam bersama AI.")

    peristiwa = {
        "1908 — Lahirnya Budi Utomo": "Didirikan pada 20 Mei 1908 oleh Dr. Soetomo dan pelajar STOVIA. Menjadi pelopor organisasi modern pertama di Hindia Belanda yang mengawali era Kebangkitan Nasional.",
        "1912 — Sarekat Islam & Indische Partij": "Sarekat Islam (H.O.S. Tjokroaminoto) menggerakkan ekonomi dan solidaritas rakyat, sementara Indische Partij (Tiga Serangkai) menjadi partai politik pertama yang menuntut kemerdekaan.",
        "1922 — Perhimpunan Indonesia": "Mahasiswa Indonesia di Belanda (Mohammad Hatta dkk.) memopulerkan identitas 'Indonesia' ke kancah internasional dan menegaskan prinsip kemandirian (non-kooperasi).",
        "1927 — Partai Nasional Indonesia (PNI)": "Ir. Soekarno mendirikan PNI dengan ideologi Marhaenisme untuk menyatukan kekuatan rakyat menghadapi kolonialisme Belanda.",
        "1928 — Kongres Pemuda II & Sumpah Pemuda": "28 Oktober 1928: Para pemuda dari berbagai daerah mengikrarkan Satu Nusa, Satu Bangsa, dan Satu Bahasa Indonesia.",
        "1945 — BPUPKI, PPKI & Proklamasi Kemerdekaan": "Perumusan dasar negara Pancasila, penyusunan UUD 1945, hingga puncak perjuangan bangsa melalui Proklamasi 17 Agustus 1945."
    }

    tahun_pilihan = st.selectbox("Pilih Peristiwa Bersejarah:", list(peristiwa.keys()))
    
    st.markdown(f"""
    <div class="card-box">
        <h4>{tahun_pilihan}</h4>
        <p>{peristiwa[tahun_pilihan]}</p>
    </div>
    """, unsafe_allow_html=True)

    if st.button("🔍 Analisis Peristiwa Ini dengan HistoriBot AI"):
        with st.spinner("HistoriBot AI sedang menyusun analisis sejarah..."):
            sys_prompt = f"Kamu adalah guru sejarah SMA yang inspiratif. Gunakan referensi ini: {KNOWLEDGE_BASE}. Jawab dalam bahasa Indonesia yang runtut dan mudah dipahami siswa SMA."
            hasil = tanya_gemini(f"Jelaskan latar belakang, tokoh kunci, dan dampak jangka panjang dari peristiwa: {tahun_pilihan}", sys_prompt)
            st.markdown("### 💡 Hasil Analisis HistoriBot AI")
            st.write(hasil)

# =====================================================================
# HALAMAN 3: TANYA-JAWAB AI (HISTORICAL CHAT)
# =====================================================================
elif menu == "💬 3. Tanya-Jawab AI":
    st.title("💬 Tanya-Jawab Sejarah (Historical Chat)")
    st.write("Tanyakan apa saja seputar Pergerakan Nasional Indonesia (1908–1945). AI hanya akan menjawab dalam konteks sejarah Indonesia.")

    for msg in st.session_state.chat_history:
        with st.chat_message(msg["role"]):
            st.markdown(msg["content"])

    pertanyaan = st.chat_input("Contoh: Mengapa strategi perjuangan setelah tahun 1908 berubah menjadi organisasi modern?")
    if pertanyaan:
        st.session_state.chat_history.append({"role": "user", "content": pertanyaan})
        with st.chat_message("user"):
            st.markdown(pertanyaan)

        with st.chat_message("assistant"):
            with st.spinner("Menelusuri arsip sejarah..."):
                guardrail_prompt = f"""
                Kamu adalah HistoriBot AI, asisten belajar Sejarah Indonesia SMA Fase F.
                Referensi utama: {KNOWLEDGE_BASE}
                ATURAN KETAT (GUARDRAIL):
                1. Hanya jawab pertanyaan yang berkaitan dengan Sejarah Pergerakan Nasional Indonesia (1908-1945) atau sejarah kemerdekaan Indonesia.
                2. Jika pengguna bertanya di luar topik sejarah (misalnya matematika, game, gosip, atau coding), tolak dengan sopan dan arahkan kembali ke topik Sejarah Pergerakan Nasional.
                3. Gunakan bahasa Indonesia yang edukatif, analitis, dan mendorong siswa berpikir kritis.
                """
                jawaban = tanya_gemini(pertanyaan, guardrail_prompt)
                st.markdown(jawaban)
                st.session_state.chat_history.append({"role": "assistant", "content": jawaban})

    if st.session_state.chat_history:
        if st.button("🗑️ Bersihkan Riwayat Obrolan"):
            st.session_state.chat_history = []
            st.rerun()

# =====================================================================
# HALAMAN 4: SIMULASI ROLEPLAY TOKOH
# =====================================================================
elif menu == "🎭 4. Simulasi Roleplay Tokoh":
    st.title("🎭 Simulasi Roleplay Tokoh Pergerakan")
    st.write("Berdialoglah seolah-olah Anda sedang mewawancarai tokoh pergerakan secara langsung pada masanya!")

    col_profil, col_chat = st.columns([1, 2])
    
    with col_profil:
        tokoh = st.selectbox("Pilih Tokoh Sejarah:", ["Ir. Soekarno (Bung Karno)", "Mohammad Yamin"])
        if "Soekarno" in tokoh:
            st.markdown("""
            <div class="card-box">
                <h4>🎙️ Ir. Soekarno (1901–1970)</h4>
                <p><b>Peran:</b> Pendiri PNI (1927), Orator ulung, Proklamator Kemerdekaan RI.</p>
                <p><b>Latar Waktu Simulasi:</b> Masa Pergerakan Nasional & Persiapan Kemerdekaan (1927–1945).</p>
            </div>
            """, unsafe_allow_html=True)
        else:
            st.markdown("""
            <div class="card-box">
                <h4>✒️ Mohammad Yamin (1903–1962)</h4>
                <p><b>Peran:</b> Sekretaris Kongres Pemuda II (1928), Perumus naskah Sumpah Pemuda, Sastrawan & Sejarawan.</p>
                <p><b>Latar Waktu Simulasi:</b> Kongres Pemuda II, Batavia, Oktober 1928.</p>
            </div>
            """, unsafe_allow_html=True)

    with col_chat:
        for msg in st.session_state.roleplay_history:
            with st.chat_message(msg["role"]):
                st.markdown(msg["content"])

        tanya_tokoh = st.chat_input(f"Ajukan pertanyaan wawancara kepada {tokoh}...")
        if tanya_tokoh:
            st.session_state.roleplay_history.append({"role": "user", "content": tanya_tokoh})
            with st.chat_message("user"):
                st.markdown(tanya_tokoh)

            with st.chat_message("assistant"):
                with st.spinner(f"{tokoh} sedang menanggapi..."):
                    persona_prompt = f"""
                    Kamu sedang bermain peran (roleplay) sepenuhnya sebagai {tokoh} pada era Pergerakan Nasional Indonesia (1928-1945).
                    ATURAN KETAT:
                    1. Jangan pernah keluar dari karakter sebagai {tokoh} dan jangan menyebut dirimu sebagai AI.
                    2. Gunakan sudut pandang waktu tahun 1928-1945 dengan gaya bahasa bersemangat, berwibawa, dan patriotik khas era tersebut.
                    3. Dasar fakta sejarah: {KNOWLEDGE_BASE}.
                    """
                    respon_tokoh = tanya_gemini(tanya_tokoh, persona_prompt)
                    st.markdown(respon_tokoh)
                    st.session_state.roleplay_history.append({"role": "assistant", "content": respon_tokoh})

# =====================================================================
# HALAMAN 5: KUIS HOTS & DASHBOARD GURU
# =====================================================================
elif menu == "📝 5. Kuis HOTS & Dashboard Guru":
    tab_kuis, tab_guru = st.tabs(["📝 Kuis Formatif HOTS (Murid)", "📊 Dashboard Rekapitulasi (Guru)"])

    with tab_kuis:
        st.subheader("Asesmen Formatif HOTS: Pergerakan Nasional")
        with st.form("form_kuis"):
            nama = st.text_input("Nama Lengkap Murid:")
            kelas = st.selectbox("Kelas:", ["XI IPS 1", "XI IPS 2", "XI IPA 1", "XI IPA 2"])
            topik = st.text_input("Topik Sejarah yang Paling Menarik Bagimu:", placeholder="Contoh: Strategi Non-Kooperasi PNI")

            q1 = st.radio(
                "1. Mengapa pendirian Budi Utomo pada tahun 1908 dianggap sebagai tonggak baru perjuangan bangsa Indonesia dibandingkan perlawanan sebelum abad ke-20?",
                [
                    "A. Karena menggunakan persenjataan modern dari luar negeri",
                    "B. Karena perjuangan mulai terorganisir secara modern, bersifat nasional, dan dipimpin golongan terpelajar",
                    "C. Karena langsung berhasil mengusir pemerintah kolonial Belanda dari Pulau Jawa"
                ]
            )
            q2 = st.radio(
                "2. Dampak strategis utama dari ikrar Sumpah Pemuda 28 Oktober 1928 bagi kelangsungan pergerakan nasional adalah...",
                [
                    "A. Menghapus seluruh organisasi kedaerahan secara paksa",
                    "B. Menyatukan identitas kebangsaan (satu nusa, bangsa, dan bahasa) yang melampaui sekat kesukuan",
                    "C. Mendapatkan pengakuan kemerdekaan langsung dari Kerajaan Belanda"
                ]
            )
            q3 = st.radio(
                "3. Perbedaan mendasar antara taktik kooperatif dan non-kooperatif pada masa Pergerakan Nasional terletak pada...",
                [
                    "A. Sikap bersedia atau menolak bekerja sama dengan lembaga bentukan pemerintah kolonial (seperti Volksraad)",
                    "B. Penggunaan bahasa Belanda dalam rapat organisasi",
                    "C. Keanggotaan yang hanya dibuka untuk kalangan bangsawan"
                ]
            )

            submitted = st.form_submit_button("Kirim Jawaban & Lihat Hasil")
            if submitted:
                if not nama.strip():
                    st.warning("Silakan isi Nama Lengkap terlebih dahulu.")
                else:
                    skor = 0
                    umpan_balik = []
                    if q1.startswith("B"):
                        skor += 34
                        umpan_balik.append("✅ **Soal 1 Benar:** Golongan terpelajar dan organisasi modern menjadi ciri utama kebangkitan nasional.")
                    else:
                        umpan_balik.append("❌ **Soal 1 Kurang Tepat:** Kunci utamanya adalah perubahan strategi menjadi organisasi modern oleh kaum terpelajar (B).")

                    if q2.startswith("B"):
                        skor += 33
                        umpan_balik.append("✅ **Soal 2 Benar:** Sumpah Pemuda melebur sifat kedaerahan menjadi identitas nasional Indonesia.")
                    else:
                        umpan_balik.append("❌ **Soal 2 Kurang Tepat:** Sumpah Pemuda berfungsi menyatukan identitas kebangsaan melampaui batas kesukuan (B).")

                    if q3.startswith("A"):
                        skor += 33
                        umpan_balik.append("✅ **Soal 3 Benar:** Non-kooperasi berarti berjuang mandiri tanpa duduk di dewan kolonial seperti Volksraad.")
                    else:
                        umpan_balik.append("❌ **Soal 3 Kurang Tepat:** Perbedaannya ada pada sikap terhadap lembaga bentukan kolonial seperti Volksraad (A).")

                    st.success(f"Terima kasih, **{nama}**! Skor Anda: **{skor} / 100**")
                    for ub in umpan_balik:
                        st.write(ub)

                    # Simpan ke rekap sesi
                    st.session_state.rekap_nilai.append({
                        "Waktu": datetime.now().strftime("%Y-%m-%d %H:%M"),
                        "Nama Murid": nama,
                        "Kelas": kelas,
                        "Skor": skor,
                        "Topik Minat": topik if topik else "-"
                    })

    with tab_guru:
        st.subheader("📊 Dashboard Rekapitulasi Nilai & Aktivitas Murid")
        st.write("Data di bawah ini merekam hasil evaluasi formatif murid dan dapat diunduh sebagai laporan CSV.")
        
        df_rekap = pd.DataFrame(st.session_state.rekap_nilai)
        st.dataframe(df_rekap, use_container_width=True)

        col_m1, col_m2 = st.columns(2)
        col_m1.metric("Total Murid Mengerjakan", f"{len(df_rekap)} Murid")
        col_m2.metric("Rata-Rata Skor Kelas", f"{df_rekap['Skor'].mean():.1f}")

        csv_data = df_rekap.to_csv(index=False).encode("utf-8")
        st.download_button(
            label="📥 Unduh Laporan Rekapitulasi (CSV)",
            data=csv_data,
            file_name="rekap_historibot_ai_sman10lutim.csv",
            mime="text/csv"
        )
