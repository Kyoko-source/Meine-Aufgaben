import streamlit as st
import math

# ================== PAGE CONFIG ==================
st.set_page_config(
    page_title="💊 Medikamentendosierung – Schulung",
    page_icon="💊",
    layout="wide"
)

# ================== STYLES ==================
st.markdown("""
<style>
body {
    background-color: #edf2f7;
    font-family: 'Segoe UI', sans-serif;
    color: #1f4e79;
}

.header {
    font-size: 2.6em;
    font-weight: 700;
    margin-bottom: 15px;
}

.card {
    background: white;
    padding: 25px;
    border-radius: 20px;
    box-shadow: 0 8px 20px rgba(0,0,0,0.08);
    margin-bottom: 20px;
}

.calc {
    background: #e3fcec;
    border-left: 5px solid #4caf50;
    padding: 12px 16px;
    border-radius: 10px;
    font-size: 0.95em;
}

.med {
    padding: 16px;
    border-radius: 14px;
    margin-bottom: 12px;
    box-shadow: 0 6px 14px rgba(0,0,0,0.06);
    transition: transform 0.2s ease;
}
.med:hover { transform: translateX(4px); }

.red { background: #ffe5e5; border-left: 6px solid #e53935; }
.blue { background: #e3f2fd; border-left: 6px solid #1e88e5; }
.green { background: #e8f5e9; border-left: 6px solid #43a047; }
.orange { background: #fff3e0; border-left: 6px solid #fb8c00; }

.badge {
    display: inline-block;
    background: #1f4e79;
    color: white;
    padding: 4px 10px;
    border-radius: 999px;
    font-size: 0.8em;
    margin-top: 6px;
}

.stButton>button {
    background: linear-gradient(90deg, #4cafef, #1f4e79);
    color: white;
    font-weight: bold;
    padding: 12px 26px;
    border-radius: 14px;
}
.stButton>button:hover {
    transform: scale(1.05);
}
</style>
""", unsafe_allow_html=True)

# ================== HEADER ==================
st.markdown("<div class='header'>💊 Medikamentendosierung – Schulungszwecke</div>", unsafe_allow_html=True)
st.warning("⚠️ Ausschließlich für Schulung / Simulation – keine reale Anwendung!")

schulungsmodus = st.toggle("🎓 Schulungsmodus", value=True)

# ================== INPUT ==================
with st.container():
    st.markdown("<div class='card'>", unsafe_allow_html=True)
    c1, c2 = st.columns(2)

    with c1:
        st.subheader("👤 Patient")
        alter = st.number_input("Alter (Jahre)", 0, 120, 50)
        gewicht = st.number_input("Gewicht (kg)", 1.0, 200.0, 80.0)

    with c2:
        st.subheader("🩺 Erkrankung")
        erkrankung = st.selectbox("Auswahl", [
            "Anaphylaxie","Asthma/COPD","Hypoglykämie","Krampfanfall",
            "Schlaganfall","Kardiales Lungenödem","Hypertensiver Notfall",
            "Starke Schmerzen bei Trauma","Brustschmerz ACS",
            "Abdominelle Schmerzen / Koliken","Übelkeit / Erbrechen",
            "Instabile Bradykardie","Benzodiazepin-Intoxikation",
            "Opiat-Intoxikation","Lungenarterienembolie"
        ])

        blutdruck = zugang = atemfrequenz = schmerzskala = asystolie = None

        if erkrankung in ["Schlaganfall","Kardiales Lungenödem","Hypertensiver Notfall"]:
            blutdruck = st.number_input("Systolischer RR", 50, 300, 140)

        if erkrankung == "Krampfanfall":
            zugang = st.radio("i.v. Zugang?", ["Ja","Nein"])

        if erkrankung == "Brustschmerz ACS":
            atemfrequenz = st.number_input("Atemfrequenz", 0, 60, 16)

        if erkrankung == "Abdominelle Schmerzen / Koliken":
            schmerzskala = st.slider("Schmerzskala", 1, 10, 5)

        if erkrankung == "Instabile Bradykardie":
            asystolie = st.radio("Asystolie-Gefahr?", ["Ja","Nein"])

    st.markdown("</div>", unsafe_allow_html=True)

# ================== EXTRA UI: TRAUMA ==================
zusatz_schmerz = None
if erkrankung == "Starke Schmerzen bei Trauma" and gewicht >= 30:
    st.markdown("<div class='card'>", unsafe_allow_html=True)
    st.subheader("💉 Analgetische Zusatzmedikation")
    zusatz_schmerz = st.radio(
        "Auswahl:",
        ["Midazolam + Esketamin","Fentanyl"],
        horizontal=True
    )
    st.markdown("</div>", unsafe_allow_html=True)

# ================== CALC ==================
def berechne(zusatz):
    meds = []

    if erkrankung == "Starke Schmerzen bei Trauma":
        meds.append(("Paracetamol", f"{15*gewicht:.0f} mg i.v.", "green", "15 mg/kg"))

        if zusatz == "Midazolam + Esketamin":
            meds.append(("Midazolam", "1 mg i.v.", "blue", "Sedierung"))
            meds.append(("Esketamin", f"{0.125*gewicht:.2f} mg i.v.", "blue", "0,125 mg/kg"))

        elif zusatz == "Fentanyl":
            max_ug = 2 * gewicht
            gaben = math.floor(max_ug / 50)
            meds.append(("Fentanyl", "0,05 mg i.v. alle 4 min", "red", f"max. {gaben} Gaben"))

    if erkrankung == "Brustschmerz ACS":
        meds.append(("ASS","250 mg i.v.","green",""))
        meds.append(("Heparin","5000 I.E.","green",""))
        if atemfrequenz and atemfrequenz < 10:
            meds.append(("⚠️ WARNUNG","Atemdepression möglich","orange","AF < 10/min"))

    return meds

# ================== OUTPUT ==================
if st.button("💉 Dosierung berechnen"):
    result = berechne(zusatz_schmerz)
    st.markdown("<div class='card'>", unsafe_allow_html=True)
    st.subheader("📋 Therapieempfehlung")

    for med, dosis, color, info in result:
        st.markdown(
            f"<div class='med {color}'><b>{med}</b><br>{dosis}"
            f"{f'<div class=badge>{info}</div>' if info else ''}</div>",
            unsafe_allow_html=True
        )

    st.markdown("</div>", unsafe_allow_html=True)

st.caption("Rettungsdienst – Schulungssimulation | Keine Haftung")
