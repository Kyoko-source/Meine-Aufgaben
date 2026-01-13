import streamlit as st

# ---------- Seiteneinstellungen ----------
st.set_page_config(
    page_title="Medikamentendosierung – Schulungszwecke",
    page_icon="💊",
    layout="wide"
)

# ---------- Design ----------
st.markdown("""
<style>
.main { background-color: #f4f6f8; }
.box {
    background-color: #ffffff;
    padding: 25px;
    border-radius: 12px;
    box-shadow: 0px 0px 10px rgba(0,0,0,0.08);
}
.calc {
    background-color: #eef5ff;
    padding: 15px;
    border-radius: 10px;
}
</style>
""", unsafe_allow_html=True)

# ---------- Header ----------
st.title("💊 Medikamentendosierung – Schulungszwecke")
st.subheader("Simulation & Ausbildung – Rettungsdienst")

st.warning(
    "⚠️ Ausschließlich für Schulungs- und Ausbildungszwecke. "
    "Keine Anwendung im Real- oder Einsatzbetrieb."
)

# ---------- Schulungsmodus ----------
schulungsmodus = st.toggle("🎓 Schulungsmodus aktivieren", value=True)

# ---------- Auswahl Patientengruppe ----------
patientengruppe = st.radio(
    "Patientengruppe auswählen",
    ["👶 Kind", "🧑 Erwachsener"],
    horizontal=True
)

# ---------- Eingaben ----------
col1, col2 = st.columns(2)

with col1:
    st.markdown("### ⚖️ Patientendaten")

    # Alter immer erfassen
    alter = st.number_input(
        "Alter des Patienten (Jahre)",
        min_value=0,
        max_value=120,
        step=1
    )

    # Gewicht nach Gruppe
    if patientengruppe == "👶 Kind":
        gewicht = st.number_input(
            "Gewicht (kg)",
            min_value=1.0,
            max_value=80.0,
            step=0.5
        )
    else:
        gewicht = st.number_input(
            "Gewicht (optional, kg)",
            min_value=20.0,
            max_value=200.0,
            step=1.0
        )

with col2:
    st.markdown("### 🩺 Erkrankung")
    erkrankung = st.selectbox(
        "Erkrankung auswählen",
        [
            "Anaphylaxie",
            "Asthma/COPD",
            "Hypoglykämie",
            "Krampfanfall",
            "Schlaganfall",
            "Kardiales Lungenödem",
            "Hypertensiver Notfall"
        ]
    )

# --- Zusätzliche Eingaben für bestimmte Erkrankungen ---
bewusstseinslage = None
zugang = None
blutdruck = None

if erkrankung == "Hypoglykämie":
    bewusstseinslage = st.radio(
        "Patientenbewusstsein",
        ["Ansprechbar (orale Gabe möglich)", "Bewusstseinsgestört (nur i.v.)"]
    )

if erkrankung == "Krampfanfall":
    zugang = st.radio(
        "Zugang verfügbar?",
        ["Ja, Zugang vorhanden", "Nein, kein Zugang"]
    )

if erkrankung in ["Schlaganfall", "Kardiales Lungenödem", "Hypertensiver Notfall"]:
    blutdruck = st.number_input(
        "Systolischer Blutdruck (mmHg)",
        min_value=50,
        max_value=300,
        step=1
    )

# ---------- Berechnungslogik ----------
def berechnung(alter, gewicht, erkrankung, bewusstseinslage=None, zugang=None, blutdruck=None):

    # --- Anaphylaxie ---
    if erkrankung == "Anaphylaxie":
        if alter < 6:
            dosis = 0.15
        elif 6 <= alter < 12:
            dosis = 0.3
        else:
            dosis = 0.5
        return [("Adrenalin", f"{dosis:.2f} mg i.m.", "Altersbasierte Dosierung (<6 J:0,15 mg | 6–12 J:0,3 mg | ≥12 J:0,5 mg)")]

    # --- Asthma/COPD ---
    if erkrankung == "Asthma/COPD":
        if alter >= 12:
            meds = [
                ("Salbutamol", "2,5 mg vernebelt", "Erwachsene Dosis"),
                ("Prednisolon", "100 mg i.v.", "Erwachsene Dosis"),
                ("Ipratropiumbromid", "500 µg vernebelt", "Erwachsene Dosis")
            ]
        elif 4 <= alter < 12:
            meds = [
                ("Salbutamol", "1,25 mg vernebelt", "Kinderdosis"),
                ("Prednisolon", "100 mg rektal", "Kinderdosis")
            ]
        else:  # unter 4 Jahre
            meds = [
                ("Adrenalin", "2 mg + 2 ml NaCl vernebelt", "Säuglingsdosis"),
                ("Prednisolon", "100 mg rektal", "Säuglingsdosis")
            ]
        return meds

    # --- Hypoglykämie ---
    if erkrankung == "Hypoglykämie":
        if bewusstseinslage is None:
            return [("Glucose", "bis 16 g i.v. langsam", "Langsame Applikation")]
        if bewusstseinslage.startswith("Ansprechbar"):
            return [("Glucose", "bis 16 g p.o. oder i.v.", "Patient ansprechbar → orale Gabe möglich, sonst langsam i.v.")]
        else:
            return [("Glucose", "bis 16 g i.v.", "Bewusstseinsgestört → nur i.v., langsam applizieren")]

    # --- Krampfanfall ---
    if erkrankung == "Krampfanfall":
        if zugang is None:
            return []
        if zugang.startswith("Ja"):
            dosis_mg = 0.05 * gewicht
            return [("Midazolam", f"{dosis_mg:.2f} mg i.v. langsam", "0,05 mg/kg KG, langsam i.v. bei Zugang möglich")]
        else:
            if gewicht <= 10:
                return [("Midazolam", "2,5 mg = 0,5 ml", "Zugang nicht möglich, 0-10 kg")]
            elif gewicht <= 20:
                return [("Midazolam", "5 mg = 1 ml", "Zugang nicht möglich, 10-20 kg")]
            else:
                return [("Midazolam", "10 mg = 2 ml", "Zugang nicht möglich, >20 kg")]

    # --- Schlaganfall ---
    if erkrankung == "Schlaganfall":
        if blutdruck is None:
            return []
        if blutdruck < 120:
            return [("Jonosteril", "Volumengabe nach Bedarf", "Blutdruck <120 mmHg → Volumengabe")]
        elif blutdruck > 220:
            return [("Urapidil", "5–15 mg i.v. langsam", "Blutdruck >220 mmHg → Urapidil langsam i.v.")]
        else:
            return [("Keine akute medikamentöse Therapie", "–", "Blutdruck im Normbereich")]

    # --- Kardiales Lungenödem ---
    if erkrankung == "Kardiales Lungenödem":
        if blutdruck is None:
            return []
        if blutdruck > 120:
            return [
                ("Nitro", "0,4–0,8 mg sublingual", "Blutdruck >120 mmHg → Nitro unter die Zunge"),
                ("Furosemid", "20 mg i.v.", "Immer langsam i.v. applizieren")
            ]
        else:
            return [
                ("Furosemid", "20 mg i.v.", "Blutdruck ≤120 mmHg → nur Furosemid i.v., langsam applizieren")
            ]

    # --- Hypertensiver Notfall ---
    if erkrankung == "Hypertensiver Notfall":
        if blutdruck is None:
            return []
        ziel_blutdruck = blutdruck * 0.8
        return [
            ("Urapidil", "5–15 mg i.v. langsam", f"Blutdruck darf maximal 20% gesenkt werden → Ziel: {ziel_blutdruck:.1f} mmHg")
        ]

    return []

# ---------- Button ----------
if st.button("💉 Dosierung berechnen"):
    ergebnisse = berechnung(alter, gewicht, erkrankung, bewusstseinslage, zugang, blutdruck)

    st.markdown("<div class='box'>", unsafe_allow_html=True)
    st.markdown("## 📋 Ergebnis")

    for med, dosis, hinweis in ergebnisse:
        st.write(f"**Medikament:** {med}")
        st.write(f"**Dosierung:** {dosis}")
        if schulungsmodus:
            st.markdown("<div class='calc'>", unsafe_allow_html=True)
            st.write(f"**Hinweis:** {hinweis}")
            if erkrankung == "Anaphylaxie":
                st.info("ℹ️ Dosierung erfolgt altersbasiert, nicht nach Gewicht.")
            elif erkrankung == "Hypoglykämie":
                st.info("ℹ️ Beachte Bewusstseinslage: oral möglich nur wenn ansprechbar.")
            elif erkrankung == "Krampfanfall":
                st.info("ℹ️ Dosierung nach Gewicht und Zugangsverfügbarkeit.")
            elif erkrankung == "Schlaganfall":
                st.info("ℹ️ Blutdruckabhängige Therapie beachten.")
            elif erkrankung == "Kardiales Lungenödem":
                st.info("ℹ️ Blutdruckabhängige Therapie beachten: Nitro + Furosemid oder nur Furosemid.")
            elif erkrankung == "Hypertensiver Notfall":
                st.info("ℹ️ Blutdruck darf maximal 20% gesenkt werden → Zielwert beachten.")
            else:
                st.write("⚠️ Gewicht für Berechnung beachten, falls relevant.")
            st.markdown("</div>", unsafe_allow_html=True)
        st.markdown("---")

    st.markdown("</div>", unsafe_allow_html=True)

# ---------- Footer ----------
st.markdown("---")
st.caption("Schulungsanwendung | Keine medizinische Verantwortung")
