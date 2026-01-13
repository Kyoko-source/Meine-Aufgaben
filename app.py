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
            "Asthma/COPD"
        ]
    )

# ---------- Berechnungslogik ----------
def berechnung(alter, gewicht, erkrankung):

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
                ("Prednisolon", "100 mg i.v.", "Erwachsene Dosis")
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

    return []

# ---------- Button ----------
if st.button("💉 Dosierung berechnen"):
    ergebnisse = berechnung(alter, gewicht, erkrankung)

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
            else:
                st.write("⚠️ Gewicht für Berechnung beachten, falls relevant.")
            st.markdown("</div>", unsafe_allow_html=True)
        st.markdown("---")

    st.markdown("</div>", unsafe_allow_html=True)

# ---------- Footer ----------
st.markdown("---")
st.caption("Schulungsanwendung | Keine medizinische Verantwortung")
