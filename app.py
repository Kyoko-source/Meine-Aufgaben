import streamlit as st
import math

# ---------- Seiteneinstellungen ----------
st.set_page_config(
    page_title="💊 Medikamentendosierung – Schulungszwecke",
    page_icon="💊",
    layout="wide"
)

# ---------- Design & CSS ----------
st.markdown("""
<style>
/* Hintergrundfarbe */
body {background-color: #f0f4f8;}

/* Hauptboxen */
.box {
    background-color: #ffffff;
    padding: 25px;
    border-radius: 15px;
    box-shadow: 0px 5px 15px rgba(0,0,0,0.1);
    margin-bottom: 20px;
}

/* Eingabebereiche */
.input-box {
    background-color: #e8f0fe;
    padding: 20px;
    border-radius: 12px;
}

/* Ergebnisbereiche */
.result-box {
    background-color: #fff7e6;
    padding: 20px;
    border-radius: 12px;
    box-shadow: 0px 3px 8px rgba(0,0,0,0.05);
}

/* Schulungsmodus Hinweise */
.calc {
    background-color: #e0ffe0;
    padding: 12px;
    border-radius: 10px;
    margin-top: 5px;
}

/* Überschriftenfarben */
h1, h2, h3 { color: #1f4e79; }

/* Buttons */
.stButton>button {
    background-color: #1f4e79;
    color: white;
    font-weight: bold;
    border-radius: 10px;
    padding: 10px 20px;
}
.stButton>button:hover {
    background-color: #2a6fbf;
}
</style>
""", unsafe_allow_html=True)

# ---------- Header ----------
st.markdown("<h1>💊 Medikamentendosierung – Schulungszwecke</h1>", unsafe_allow_html=True)
st.markdown("**Simulation & Ausbildung – Rettungsdienst**")
st.warning(
    "⚠️ Ausschließlich für Schulungs- und Ausbildungszwecke. "
    "Keine Anwendung im Real- oder Einsatzbetrieb."
)

# ---------- Schulungsmodus ----------
schulungsmodus = st.toggle("🎓 Schulungsmodus aktivieren", value=True)

# ---------- Eingabebereich ----------
with st.container():
    st.markdown("<div class='box'>", unsafe_allow_html=True)
    col1, col2 = st.columns([1, 1])

    with col1:
        st.markdown("<div class='input-box'>", unsafe_allow_html=True)
        st.markdown("### ⚖️ Patientendaten")
        alter = st.number_input("Alter des Patienten (Jahre)", min_value=0, max_value=120, step=1)
        patientengruppe = st.radio("Patientengruppe", ["👶 Kind", "🧑 Erwachsener"], horizontal=True)
        if patientengruppe == "👶 Kind":
            gewicht = st.number_input("Gewicht (kg)", min_value=1.0, max_value=80.0, step=0.5)
        else:
            gewicht = st.number_input("Gewicht (optional, kg)", min_value=20.0, max_value=200.0, step=1.0)
        st.markdown("</div>", unsafe_allow_html=True)

    with col2:
        st.markdown("<div class='input-box'>", unsafe_allow_html=True)
        st.markdown("### 🩺 Erkrankung auswählen")
        erkrankung = st.selectbox("Erkrankung", [
            "Anaphylaxie",
            "Asthma/COPD",
            "Hypoglykämie",
            "Krampfanfall",
            "Schlaganfall",
            "Kardiales Lungenödem",
            "Hypertensiver Notfall",
            "Starke Schmerzen bei Trauma"
        ])
        # Zusätzliche Inputs
        bewusstseinslage = None
        zugang = None
        blutdruck = None
        trauma_medikament = None

        if erkrankung == "Hypoglykämie":
            bewusstseinslage = st.radio("Patientenbewusstsein", ["Ansprechbar (orale Gabe möglich)", "Bewusstseinsgestört (nur i.v.)"])
        if erkrankung == "Krampfanfall":
            zugang = st.radio("Zugang verfügbar?", ["Ja, Zugang vorhanden", "Nein, kein Zugang"])
        if erkrankung in ["Schlaganfall", "Kardiales Lungenödem", "Hypertensiver Notfall"]:
            blutdruck = st.number_input("Systolischer Blutdruck (mmHg)", min_value=50, max_value=300, step=1)
        if erkrankung == "Starke Schmerzen bei Trauma":
            trauma_medikament = st.radio("Analgetika nach Paracetamol auswählen", ["Esketamin", "Fentanyl"])

        st.markdown("</div>", unsafe_allow_html=True)
    st.markdown("</div>", unsafe_allow_html=True)

# ---------- Berechnung & Ergebnis ----------
def berechnung(alter, gewicht, erkrankung, bewusstseinslage=None, zugang=None, blutdruck=None, trauma_medikament=None):
    med_list = []
    # (Hier kommt die gleiche Logik wie vorher für alle Erkrankungen, inkl. Fentanyl Korrektur)
    # ...
    return med_list

if st.button("💉 Dosierung berechnen"):
    ergebnisse = berechnung(alter, gewicht, erkrankung, bewusstseinslage, zugang, blutdruck, trauma_medikament)

    st.markdown("<div class='box'>", unsafe_allow_html=True)
    st.markdown("<h2>📋 Ergebnis</h2>", unsafe_allow_html=True)
    for med, dosis, hinweis in ergebnisse:
        st.markdown(f"**💊 Medikament:** {med}")
        st.markdown(f"**💉 Dosierung:** {dosis}")
        if schulungsmodus:
            st.markdown(f"<div class='calc'>**Hinweis:** {hinweis}</div>", unsafe_allow_html=True)
        st.markdown("---")
    st.markdown("</div>", unsafe_allow_html=True)

st.markdown("---")
st.caption("Schulungsanwendung | Keine medizinische Verantwortung")
