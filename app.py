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

    if patientengruppe == "👶 Kind":
        gewicht = st.number_input(
            "Gewicht (kg)",
            min_value=1.0,
            max_value=80.0,
            step=0.5
        )
    else:
        gewicht = st.number_input(
            "Gewicht (optional)",
            min_value=40.0,
            max_value=200.0,
            step=1.0
        )

with col2:
    st.markdown("### 🩺 Erkrankung")
    erkrankung = st.selectbox(
        "Erkrankung auswählen",
        [
            "Anaphylaxie",
            "Krampfanfall",
            "Starke Schmerzen",
            "Fieber"
        ]
    )

# ---------- Berechnungslogik ----------
def berechnung(gewicht, gruppe, erkrankung):

    if erkrankung == "Anaphylaxie":
        dosis = min(0.01 * gewicht, 0.5)
        return "Adrenalin", f"{dosis:.2f} mg i.m.", "0,01 mg/kg, max. 0,5 mg"

    if erkrankung == "Krampfanfall":
        dosis = min(0.2 * gewicht, 10)
        return "Midazolam", f"{dosis:.1f} mg", "0,2 mg/kg, max. 10 mg"

    if erkrankung == "Starke Schmerzen":
        dosis = min(0.1 * gewicht, 10)
        return "Morphin", f"{dosis:.1f} mg i.v.", "0,1 mg/kg, max. 10 mg"

    if erkrankung == "Fieber":
        dosis = min(15 * gewicht, 1000)
        return "Paracetamol", f"{dosis:.0f} mg", "15 mg/kg, max. 1.000 mg"

    return None

# ---------- Button ----------
if st.button("💉 Dosierung berechnen"):
    med, dosis, regel = berechnung(gewicht, patientengruppe, erkrankung)

    st.markdown("<div class='box'>", unsafe_allow_html=True)
    st.markdown("## 📋 Ergebnis")

    st.write(f"**Medikament:** {med}")
    st.write(f"**Dosierung:** {dosis}")

    if schulungsmodus:
        st.markdown("<div class='calc'>", unsafe_allow_html=True)
        st.markdown("### 🎓 Schulungshinweise")
        st.write(f"**Berechnungsregel:** {regel}")
        st.write(f"**Rechenweg:** Gewicht × Dosierungsfaktor")
        st.write("⚠️ Maximaldosis immer beachten")
        st.markdown("</div>", unsafe_allow_html=True)

    st.markdown("</div>", unsafe_allow_html=True)

# ---------- Footer ----------
st.markdown("---")
st.caption("Schulungsanwendung | Keine medizinische Verantwortung")
