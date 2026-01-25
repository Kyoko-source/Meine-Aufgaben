import streamlit as st
import math

# ================== CONFIG ==================
st.set_page_config(
    page_title="💊 Medikamentendosierung – Schulung",
    page_icon="💊",
    layout="wide"
)

# ================== STYLE ==================
st.markdown("""
<style>
body { background:#edf2f7; font-family:Segoe UI; }
.card {
    background:white; padding:25px; border-radius:18px;
    box-shadow:0 8px 18px rgba(0,0,0,0.08); margin-bottom:20px;
}
.med {
    padding:16px; border-radius:14px; margin-bottom:12px;
}
.green { background:#e8f5e9; border-left:6px solid #43a047; }
.blue { background:#e3f2fd; border-left:6px solid #1e88e5; }
.red { background:#ffe5e5; border-left:6px solid #e53935; }
.orange { background:#fff3e0; border-left:6px solid #fb8c00; }
.badge {
    display:inline-block; background:#1f4e79; color:white;
    padding:4px 10px; border-radius:999px; font-size:0.8em;
}
</style>
""", unsafe_allow_html=True)

st.title("💊 Medikamentendosierung – Schulungszwecke")
st.warning("⚠️ Ausschließlich für Schulung / Simulation – keine reale Anwendung!")

# ================== SESSION STATE ==================
if "result" not in st.session_state:
    st.session_state.result = None

# ================== FORM ==================
with st.form("med_form"):
    st.markdown("<div class='card'>", unsafe_allow_html=True)
    c1, c2 = st.columns(2)

    with c1:
        alter = st.number_input("Alter (Jahre)", 0, 120, 50)
        gewicht = st.number_input("Gewicht (kg)", 1.0, 200.0, 80.0)

    with c2:
        erkrankung = st.selectbox("Erkrankung", [
            "Anaphylaxie",
            "Asthma/COPD",
            "Hypoglykämie",
            "Krampfanfall",
            "Schlaganfall",
            "Kardiales Lungenödem",
            "Hypertensiver Notfall",
            "Starke Schmerzen bei Trauma",
            "Brustschmerz ACS",
            "Abdominelle Schmerzen / Koliken",
            "Übelkeit / Erbrechen",
            "Instabile Bradykardie",
            "Benzodiazepin-Intoxikation",
            "Opiat-Intoxikation",
            "Lungenarterienembolie"
        ])

        blutdruck = atemfrequenz = schmerz = None
        zugang = asystolie = None
        zusatz_schmerz = None

        if erkrankung in ["Schlaganfall","Kardiales Lungenödem","Hypertensiver Notfall"]:
            blutdruck = st.number_input("Systolischer RR", 50, 300, 140)

        if erkrankung == "Krampfanfall":
            zugang = st.radio("i.v. Zugang?", ["Ja","Nein"])

        if erkrankung == "Brustschmerz ACS":
            atemfrequenz = st.number_input("Atemfrequenz", 0, 60, 16)

        if erkrankung == "Abdominelle Schmerzen / Koliken":
            schmerz = st.slider("Schmerzskala", 1, 10, 5)

        if erkrankung == "Instabile Bradykardie":
            asystolie = st.radio("Asystolie-Gefahr?", ["Ja","Nein"])

        if erkrankung == "Starke Schmerzen bei Trauma" and gewicht >= 30:
            zusatz_schmerz = st.radio(
                "Analgetische Zusatzmedikation",
                ["Midazolam + Esketamin", "Fentanyl"],
                horizontal=True
            )

    submit = st.form_submit_button("💉 Dosierung berechnen")
    st.markdown("</div>", unsafe_allow_html=True)

# ================== BERECHNUNG ==================
if submit:
    meds = []

    # ---------- ANAPHYLAXIE ----------
    if erkrankung == "Anaphylaxie":
        dosis = "0,5 mg i.m." if alter >= 12 else "0,3 mg i.m."
        meds.append(("Adrenalin", dosis, "red", ""))

    # ---------- ASTHMA/COPD ----------
    if erkrankung == "Asthma/COPD":
        meds.append(("Salbutamol", "2,5 mg vernebelt", "green", ""))

    # ---------- HYPOGLYKÄMIE ----------
    if erkrankung == "Hypoglykämie":
        meds.append(("Glukose", "bis 16 g i.v.", "green", ""))

    # ---------- KRAMPFANFALL ----------
    if erkrankung == "Krampfanfall":
        if zugang == "Ja":
            meds.append(("Midazolam", f"{0.05*gewicht:.2f} mg i.v.", "blue", "0,05 mg/kg"))
        else:
            meds.append(("Midazolam", "10 mg bukkal", "blue", ""))

    # ---------- SCHMERZ TRAUMA ----------
    if erkrankung == "Starke Schmerzen bei Trauma":
        meds.append(("Paracetamol", f"{15*gewicht:.0f} mg i.v.", "green", "15 mg/kg"))

        if zusatz_schmerz == "Midazolam + Esketamin":
            meds.append(("Midazolam", "1 mg i.v.", "blue", ""))
            meds.append(("Esketamin", f"{0.125*gewicht:.2f} mg i.v.", "blue", "0,125 mg/kg"))

        if zusatz_schmerz == "Fentanyl":
            max_ug = 2 * gewicht
            gaben = math.floor(max_ug / 50)
            meds.append(("Fentanyl", "0,05 mg i.v. alle 4 min", "red", f"max. {gaben} Gaben"))

    # ---------- ACS ----------
    if erkrankung == "Brustschmerz ACS":
        meds.append(("ASS", "250 mg i.v.", "green", ""))
        meds.append(("Heparin", "5000 I.E.", "green", ""))
        if atemfrequenz and atemfrequenz < 10:
            meds.append(("⚠️ WARNUNG", "Atemdepression", "orange", "AF < 10"))

    st.session_state.result = meds

# ================== OUTPUT ==================
if st.session_state.result:
    st.markdown("<div class='card'>", unsafe_allow_html=True)
    st.subheader("📋 Therapieempfehlung")

    for med, dosis, color, info in st.session_state.result:
        st.markdown(
            f"<div class='med {color}'><b>{med}</b><br>{dosis}"
            f"{f'<div class=badge>{info}</div>' if info else ''}</div>",
            unsafe_allow_html=True
        )

    st.markdown("</div>", unsafe_allow_html=True)

st.caption("Rettungsdienst – Schulungssimulation | Keine Haftung")
