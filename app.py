import streamlit as st

# ================== GRUNDEINSTELLUNGEN ==================
st.set_page_config(
    page_title="💊 Medikamentendosierung – Schulungszwecke",
    page_icon="💊",
    layout="wide"
)

ADMIN_PASSWORT = "MediDos"

# ================== DESIGN ==================
st.markdown("""
<style>
body { background-color: #f2f6fa; }
.card {
    background-color: white;
    padding: 25px;
    border-radius: 16px;
    box-shadow: 0 4px 12px rgba(0,0,0,0.08);
    margin-bottom: 20px;
}
.header { color: #1f4e79; }
.calc {
    background-color: #e8fff0;
    padding: 12px;
    border-radius: 10px;
    margin-top: 6px;
}
.admin {
    background-color: #fff4e6;
    padding: 20px;
    border-radius: 12px;
    border: 2px solid #ff9800;
}
</style>
""", unsafe_allow_html=True)

# ================== SOP-DATEN ==================
if "sop" not in st.session_state:
    st.session_state.sop = {
        "Anaphylaxie": {
            "Adrenalin": "0,15 / 0,3 / 0,5 mg je nach Alter"
        },
        "Asthma/COPD": {
            "Salbutamol": "altersabhängig vernebeln",
            "Ipratropiumbromid": "500 µg vernebeln (>12 J)",
            "Prednisolon": "100 mg i.v./rektal"
        },
        "Hypoglykämie": {
            "Glukose": "bis 16 g i.v. langsam / oral möglich"
        },
        "Krampfanfall": {
            "Midazolam": "0,05 mg/kg i.v. oder altersabhängig"
        },
        "Schlaganfall": {
            "Jonosteril": "RR <120 mmHg",
            "Urapidil": "5–15 mg langsam i.v."
        },
        "Kardiales Lungenödem": {
            "Nitro": "0,4–0,8 mg sublingual",
            "Furosemid": "20 mg i.v."
        },
        "Hypertensiver Notfall": {
            "Urapidil": "5–15 mg langsam i.v."
        },
        "Starke Schmerzen bei Trauma": {
            "Paracetamol": "15 mg/kg oder 1 g",
            "Midazolam": "1–2 mg alters-/gewichtsabhängig",
            "Esketamin": "0,125 mg/kg",
            "Fentanyl": "0,05 mg alle 4 min, max. 2 µg/kg"
        },
        "Brustschmerz ACS": {
            "ASS": "250 mg i.v.",
            "Heparin": "5000 I.E. i.v.",
            "Morphin": "3 mg i.v. bei AF <10"
        },
        "Abdominelle Schmerzen / Koliken": {
            "Paracetamol": "15 mg/kg oder 1 g",
            "Butylscopolamin": "0,3 mg/kg max. 40 mg",
            "Fentanyl": "0,05 mg, max. 2 µg/kg"
        },
        "Übelkeit / Erbrechen": {
            "Ondansetron": "4 mg i.v.",
            "Dimenhydrinat": "31 mg i.v. + 31 mg Infusion"
        },
        "Instabile Bradykardie": {
            "Adrenalin": "1 mg in 500 ml Jonosteril",
            "Atropin": "0,5 mg i.v. bis max. 3 mg"
        },
        "Benzodiazepin-Intoxikation": {
            "Flumazenil": "0,5 mg langsam i.v."
        },
        "Opiat-Intoxikation": {
            "Naloxon": "0,4 mg i.v. auf 10 ml verdünnt"
        },
        "Lungenarterienembolie": {
            "Heparin": "5000 I.E. i.v."
        }
    }

# ================== HEADER ==================
st.markdown("<h1 class='header'>💊 Medikamentendosierung – Schulungszwecke</h1>", unsafe_allow_html=True)
st.warning("⚠️ Ausschließlich für Schulungs- und Ausbildungszwecke – keine reale Anwendung!")

# ================== ADMIN MODUS ==================
with st.expander("🛠 SOP Anpassung (Admin-Modus)"):
    st.markdown("<div class='admin'>", unsafe_allow_html=True)
    passwort = st.text_input("🔐 Admin-Passwort", type="password")

    if passwort == ADMIN_PASSWORT:
        st.success("Zugriff gewährt")

        for erkrankung, medikamente in st.session_state.sop.items():
            st.subheader(erkrankung)
            for med, dosis in medikamente.items():
                new_dosis = st.text_input(
                    f"{med} – Dosierung",
                    value=dosis,
                    key=f"{erkrankung}_{med}"
                )
                st.session_state.sop[erkrankung][med] = new_dosis
            st.divider()

    elif passwort != "":
        st.error("Falsches Passwort")

    st.markdown("</div>", unsafe_allow_html=True)

# ================== ANZEIGE SOP (SCHULUNG) ==================
st.subheader("📋 Aktueller SOP-Stand (Schulung)")
for erkrankung, medikamente in st.session_state.sop.items():
    with st.expander(erkrankung):
        for med, dosis in medikamente.items():
            st.markdown(f"**{med}:** {dosis}")

st.caption("Rettungsdienst – Schulungssimulation | Admin-Modus aktivierbar")
