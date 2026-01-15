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
.card {
    background-color: white;
    padding: 25px;
    border-radius: 16px;
    box-shadow: 0 4px 12px rgba(0,0,0,0.08);
    margin-bottom: 20px;
}
.header {
    color: #1f4e79;
}
.calc {
    background-color: #e8fff0;
    padding: 12px;
    border-radius: 10px;
    margin-top: 6px;
}
.warn {
    background-color: #fff3cd;
    padding: 12px;
    border-radius: 10px;
}
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
</style>
""", unsafe_allow_html=True)

# ================== HEADER ==================
st.markdown("<h1 class='header'>💊 Medikamentendosierung – Schulungszwecke</h1>", unsafe_allow_html=True)
st.warning("⚠️ Ausschließlich für Schulungs- und Ausbildungszwecke – keine reale Anwendung.")

schulungsmodus = st.toggle("🎓 Schulungsmodus (Rechenwege anzeigen)", value=True)

# ================== EINGABEN ==================
with st.container():
    st.markdown("<div class='card'>", unsafe_allow_html=True)
    col1, col2 = st.columns(2)

    with col1:
        st.subheader("👤 Patient")
        alter = st.number_input("Alter (Jahre)", 0, 120, 30)
        gewicht = st.number_input("Gewicht (kg)", 1.0, 200.0, 70.0)

    with col2:
        st.subheader("🩺 Erkrankung")
        erkrankung = st.selectbox(
            "Auswahl",
            [
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
                "Übelkeit / Erbrechen"
            ]
        )

        blutdruck = None
        zugang = None
        trauma_wahl = None
        atemfrequenz = None
        schmerzskala = None

        if erkrankung in ["Schlaganfall", "Kardiales Lungenödem", "Hypertensiver Notfall"]:
            blutdruck = st.number_input("Systolischer Blutdruck (mmHg)", 50, 300, 140)

        if erkrankung == "Krampfanfall":
            zugang = st.radio("Zugang vorhanden?", ["Ja", "Nein"])

        if erkrankung == "Starke Schmerzen bei Trauma":
            trauma_wahl = st.radio(
                "Therapie nach Paracetamol",
                ["Paracetamol + Esketamin + Midazolam", "Paracetamol + Fentanyl"]
            )

        if erkrankung == "Brustschmerz ACS":
            atemfrequenz = st.number_input("Atemfrequenz (/min)", 0, 60, 16)

        if erkrankung == "Abdominelle Schmerzen / Koliken":
            schmerzskala = st.slider("Schmerzskala (1–10)", 1, 10, 5)

    st.markdown("</div>", unsafe_allow_html=True)

# ================== BERECHNUNG ==================
def berechne():
    meds = []

    # ---------- ÜBELKEIT / ERBRECHEN ----------
    if erkrankung == "Übelkeit / Erbrechen":
        if alter >= 60:
            meds.append((
                "Ondansetron",
                "4 mg i.v.",
                "Einmalig, ggf. 1× wiederholbar"
            ))
        else:
            meds.append((
                "Dimenhydrinat",
                "31 mg i.v.",
                "Zusätzlich 31 mg in die Infusion geben"
            ))

    # ---------- BRUSTSCHMERZ ACS ----------
    if erkrankung == "Brustschmerz ACS":
        meds.append(("ASS", "250 mg i.v.", "Standardtherapie ACS"))
        meds.append(("Heparin", "5000 I.E. i.v.", "Unfraktioniertes Heparin"))
        if atemfrequenz is not None and atemfrequenz < 10:
            meds.append(("Morphin", "3 mg i.v.", "Nur bei AF < 10/min"))

    # ---------- HYPERTENSIVER NOTFALL ----------
    if erkrankung == "Hypertensiver Notfall" and blutdruck:
        ziel = int(blutdruck * 0.8)
        meds.append(("Urapidil", "5–15 mg langsam i.v.", f"Ziel-Sys ca. {ziel} mmHg (−20 %)"))

    # ---------- KARDIALES LUNGENÖDEM ----------
    if erkrankung == "Kardiales Lungenödem" and blutdruck:
        meds.append(("Furosemid", "20 mg i.v.", "Langsam i.v."))
        if blutdruck > 120:
            meds.append(("Nitro", "0,4–0,8 mg sublingual", "Nur bei RR > 120 mmHg"))

    # ---------- KRAMPFANFALL ----------
    if erkrankung == "Krampfanfall":
        if zugang == "Ja":
            dosis = 0.05 * gewicht
            meds.append(("Midazolam", f"{dosis:.2f} mg i.v.", "0,05 mg/kg KG langsam"))
        else:
            if gewicht <= 10:
                meds.append(("Midazolam", "2,5 mg (0,5 ml)", "Kein Zugang"))
            elif gewicht <= 20:
                meds.append(("Midazolam", "5 mg (1 ml)", "Kein Zugang"))
            else:
                meds.append(("Midazolam", "10 mg (2 ml)", "Kein Zugang"))

    # ---------- HYPOGLYKÄMIE ----------
    if erkrankung == "Hypoglykämie":
        meds.append(("Glukose", "bis 16 g i.v.", "Langsam i.v., alternativ oral bei Wachheit"))

    # ---------- ASTHMA / COPD ----------
    if erkrankung == "Asthma/COPD":
        if alter >= 12:
            meds.extend([
                ("Salbutamol", "2,5 mg vernebelt", "Bronchodilatator"),
                ("Ipratropiumbromid", "500 µg vernebelt", "Zusatz"),
                ("Prednisolon", "100 mg i.v.", "Entzündungshemmung")
            ])
        elif alter >= 4:
            meds.append(("Salbutamol", "1,25 mg vernebelt", "Kinderdosis"))
            meds.append(("Prednisolon", "100 mg rektal", ""))
        else:
            meds.append(("Adrenalin", "2 mg + 2 ml NaCl vernebelt", "Kleinkind"))
            meds.append(("Prednisolon", "100 mg rektal", ""))

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

st.caption("Rettungsdienst – Schulungssimulation | Keine Haftung")
