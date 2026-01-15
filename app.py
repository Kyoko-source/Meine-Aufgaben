import streamlit as st
import math

# ================== SEITENEINSTELLUNGEN ==================
st.set_page_config(
    page_title="💊 Medikamentendosierung – Schulungszwecke",
    page_icon="💊",
    layout="wide"
)

# ================== DESIGN ==================
st.markdown("""
<style>
body { background-color: #f2f6fa; }

/* Karten für Eingaben und Ergebnisse */
.card {
    background-color: #ffffff;
    padding: 25px;
    border-radius: 16px;
    box-shadow: 0 4px 12px rgba(0,0,0,0.05);
    margin-bottom: 20px;
}

/* Header der Seite */
.header { 
    color: white; 
    padding: 12px; 
    border-radius: 10px; 
}

/* Infobox für Hinweise */
.calc {
    background-color: #dff6ff; /* hellblau */
    padding: 12px;
    border-radius: 10px;
    margin-top: 6px;
}

/* Buttons */
.stButton>button {
    background-color: #1f4e79;
    color: white;
    font-weight: bold;
    border-radius: 12px;
    padding: 10px 22px;
}
.stButton>button:hover {
    background-color: #2a6fbf;
}

/* Admin-Box */
.admin {
    background-color: #fff4e6;
    padding: 20px;
    border-radius: 12px;
    border: 2px solid #ff9800;
}
</style>
""", unsafe_allow_html=True)

# ================== HEADER ==================
st.markdown("<h1 class='header' style='background-color:#4da6ff'>💊 Medikamentendosierung – Schulungszwecke</h1>", unsafe_allow_html=True)
st.warning("⚠️ Ausschließlich für Schulungs- und Ausbildungszwecke – keine reale Anwendung!")

schulungsmodus = st.toggle("🎓 Schulungsmodus (Erklärungen anzeigen)", value=True)

# ================== FARBKATEGORIEN ==================
farbkategorien = {
    "🔴 Herzkreislauf": ["Kardiales Lungenödem", "Hypertensiver Notfall", "Brustschmerz ACS", "Instabile Bradykardie"],
    "🔵 Atemweg": ["Asthma/COPD", "Anaphylaxie"],
    "🟣 Trauma/Schmerz": ["Starke Schmerzen bei Trauma", "Abdominelle Schmerzen / Koliken"],
    "🟢 Neurologie/Intoxikation": ["Schlaganfall", "Krampfanfall", "Hypoglykämie", "Benzodiazepin-Intoxikation",
                                     "Opiat-Intoxikation", "Lungenarterienembolie", "Übelkeit / Erbrechen"]
}

select_options = []
for cat, liste in farbkategorien.items():
    for e in liste:
        select_options.append(f"{cat} {e}")

# ================== EINGABEN ==================
with st.container():
    st.markdown("<div class='card'>", unsafe_allow_html=True)
    col1, col2 = st.columns(2)

    with col1:
        st.subheader("👤 Patient")
        alter = st.number_input("Alter (Jahre)", 0, 120, 50)
        gewicht = st.number_input("Gewicht (kg)", 1.0, 200.0, 80.0)

    with col2:
        st.subheader("🩺 Erkrankung")
        erkrankung_auswahl = st.selectbox("Auswahl", select_options)
        emoji = erkrankung_auswahl[:2]
        farbe = "#1f4e79"
        if emoji == "🔴": farbe = "#e74c3c"
        elif emoji == "🔵": farbe = "#3498db"
        elif emoji == "🟣": farbe = "#9b59b6"
        elif emoji == "🟢": farbe = "#2ecc71"
        st.markdown(f"<h3 class='header' style='background-color:{farbe}'>{erkrankung_auswahl[2:]}</h3>", unsafe_allow_html=True)
        erkrankung = erkrankung_auswahl[2:]

        blutdruck = None
        zugang = None
        atemfrequenz = None
        schmerzskala = None
        asystolie_gefahr = None

        if erkrankung in ["Schlaganfall", "Kardiales Lungenödem", "Hypertensiver Notfall"]:
            blutdruck = st.number_input("Systolischer Blutdruck (mmHg)", 50, 300, 140)

        if erkrankung == "Krampfanfall":
            zugang = st.radio("Zugang vorhanden?", ["Ja", "Nein"])

        if erkrankung == "Brustschmerz ACS":
            atemfrequenz = st.number_input("Atemfrequenz (/min)", 0, 60, 16)

        if erkrankung == "Abdominelle Schmerzen / Koliken":
            schmerzskala = st.slider("Schmerzskala (1–10)", 1, 10, 5)

        if erkrankung == "Instabile Bradykardie":
            asystolie_gefahr = st.radio("Gefahr einer Asystolie?", ["Ja", "Nein"])

    st.markdown("</div>", unsafe_allow_html=True)

# ================== BERECHNUNG ==================
def berechne():
    meds = []

    # ---------- ANAPHYLAXIE ----------
    if erkrankung == "Anaphylaxie":
        if alter < 6:
            meds.append(("Adrenalin", "0,15 mg i.m.", "Kinder <6 Jahre"))
        elif 6 <= alter < 12:
            meds.append(("Adrenalin", "0,3 mg i.m.", "Kinder 6–12 Jahre"))
        else:
            meds.append(("Adrenalin", "0,5 mg i.m.", "Patient ≥12 Jahre"))

    # ---------- ASTHMA/COPD ----------
    if erkrankung == "Asthma/COPD":
        if alter > 12:
            meds.append(("Salbutamol", "2,5 mg vernebelt", "Patient >12 J"))
            meds.append(("Ipratropiumbromid", "500 µg vernebelt", "Patient >12 J"))
            meds.append(("Prednisolon", "100 mg i.v.", ""))
        elif 4 <= alter <= 12:
            meds.append(("Salbutamol", "1,25 mg vernebelt", "Kinder 4–12 J"))
            meds.append(("Prednisolon", "100 mg rektal", "Kinder 4–12 J"))
        else:
            meds.append(("Adrenalin", "2 mg + 2 ml NaCl vernebelt", "Kinder <4 J"))
            meds.append(("Prednisolon", "100 mg rektal", "Kinder <4 J"))

    # Weitere Erkrankungen hier einfügen wie zuvor (Krampfanfall, Hypoglykämie, Trauma etc.)
    return meds

# ================== AUSGABE ==================
if st.button("💉 Dosierung berechnen"):
    ergebnis = berechne()
    st.markdown("<div class='card'>", unsafe_allow_html=True)
    st.subheader("📋 Therapieempfehlung")
    for med, dosis, hinweis in ergebnis:
        st.markdown(f"**💊 {med}**")
        st.markdown(f"➡️ **Dosierung:** {dosis}")
        if schulungsmodus and hinweis:
            st.markdown(f"<div class='calc'>ℹ️ {hinweis}</div>", unsafe_allow_html=True)
        st.markdown("---")
    st.markdown("</div>", unsafe_allow_html=True)

# ================== ADMIN-MODUS IN SIDEBAR ==================
st.sidebar.markdown("### 🛠 Admin-Modus – SOP Anpassung")
if "admin_access" not in st.session_state:
    st.session_state.admin_access = False

if not st.session_state.admin_access:
    pw = st.sidebar.text_input("🔐 Passwort eingeben", type="password")
    if pw == "MediDos":
        st.session_state.admin_access = True
        st.sidebar.success("Admin-Zugriff aktiviert")
    elif pw != "":
        st.sidebar.error("Falsches Passwort")

if st.session_state.admin_access:
    st.sidebar.markdown("---")
    st.sidebar.markdown("#### SOP bearbeiten")
    if "sop_admin" not in st.session_state:
        st.session_state.sop_admin = {}  # Kann mit bisherigen SOP-Daten initialisiert werden
    for erk, meds in st.session_state.sop_admin.items():
        st.sidebar.subheader(erk)
        for med, dosis in meds.items():
            new_val = st.sidebar.text_input(f"{med} – Dosierung", value=dosis, key=f"{erk}_{med}")
            st.session_state.sop_admin[erk][med] = new_val

st.caption("Rettungsdienst – Schulungssimulation | Keine Haftung")
