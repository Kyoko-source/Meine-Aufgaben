import streamlit as st
import math

# ================== SEITENEINSTELLUNGEN ==================
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

# ================== SOP TEXTDATEN (NUR ANZEIGE) ==================
if "sop_text" not in st.session_state:
    st.session_state.sop_text = {
        "Anaphylaxie": {
            "Adrenalin": "0,15 mg (<6 J) | 0,3 mg (6–12 J) | 0,5 mg ≥12 J"
        },
        "Asthma/COPD": {
            "Salbutamol": "altersabhängig vernebeln",
            "Ipratropiumbromid": "500 µg vernebelt (>12 J)",
            "Prednisolon": "100 mg i.v. / rektal"
        },
        "Hypoglykämie": {
            "Glukose": "bis 16 g i.v. langsam / oral bei Wachheit"
        },
        "Krampfanfall": {
            "Midazolam": "0,05 mg/kg i.v. oder alters-/gewichtsabhängig"
        },
        "Schlaganfall": {
            "Jonosteril": "RR <120 mmHg",
            "Urapidil": "5–15 mg langsam i.v. bei RR >220"
        },
        "Kardiales Lungenödem": {
            "Nitro": "0,4–0,8 mg sublingual",
            "Furosemid": "20 mg i.v."
        },
        "Hypertensiver Notfall": {
            "Urapidil": "5–15 mg langsam i.v., max. 20% RR-Senkung"
        },
        "Starke Schmerzen bei Trauma": {
            "Paracetamol": "15 mg/kg oder 1 g",
            "Esketamin": "0,125 mg/kg",
            "Fentanyl": "0,05 mg alle 4 min, max. 2 µg/kg"
        },
        "Brustschmerz ACS": {
            "ASS": "250 mg i.v.",
            "Heparin": "5000 I.E. i.v.",
            "Morphin": "3 mg i.v. bei AF <10"
        },
        "Abdominelle Schmerzen / Koliken": {
            "Paracetamol": "Schmerzskala 3–5",
            "Butylscopolamin": "0,3 mg/kg max. 40 mg",
            "Fentanyl": "bei anhaltenden Schmerzen"
        },
        "Übelkeit / Erbrechen": {
            "Ondansetron": "4 mg i.v. (>60 J)",
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

schulungsmodus = st.toggle("🎓 Schulungsmodus (Erklärungen anzeigen)", value=True)

# ================== ADMIN MODUS ==================
with st.expander("🛠 SOP Anpassung (Admin-Modus)"):
    st.markdown("<div class='admin'>", unsafe_allow_html=True)
    pw = st.text_input("🔐 Passwort", type="password")

    if pw == ADMIN_PASSWORT:
        st.success("Admin-Zugriff aktiv")

        for erk, meds in st.session_state.sop_text.items():
            st.subheader(erk)
            for med, dosis in meds.items():
                new_val = st.text_input(
                    f"{med} – Dosierung",
                    value=dosis,
                    key=f"{erk}_{med}"
                )
                st.session_state.sop_text[erk][med] = new_val
            st.divider()

    elif pw != "":
        st.error("Falsches Passwort")

    st.markdown("</div>", unsafe_allow_html=True)

# ================== SOP ANZEIGE (SCHULUNG) ==================
st.subheader("📘 Aktueller SOP-Stand (Anzeige)")
for erk, meds in st.session_state.sop_text.items():
    with st.expander(erk):
        for med, dosis in meds.items():
            st.markdown(f"**{med}:** {dosis}")

st.caption("Rettungsdienst – Schulungssimulation | Rechner unverändert | SOP-Editor separat")
