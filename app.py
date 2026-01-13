import streamlit as st
import math

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
    alter = st.number_input(
        "Alter des Patienten (Jahre)",
        min_value=0,
        max_value=120,
        step=1
    )
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
            "Hypertensiver Notfall",
            "Starke Schmerzen bei Trauma"
        ]
    )

# --- Zusätzliche Eingaben ---
bewusstseinslage = None
zugang = None
blutdruck = None
trauma_medikament = None

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

if erkrankung == "Starke Schmerzen bei Trauma":
    trauma_medikament = st.radio(
        "Analgetika nach Paracetamol auswählen",
        ["Esketamin", "Fentanyl"]
    )

# ---------- Berechnungslogik ----------
def berechnung(alter, gewicht, erkrankung, bewusstseinslage=None, zugang=None, blutdruck=None, trauma_medikament=None):
    med_list = []

    # --- Anaphylaxie ---
    if erkrankung == "Anaphylaxie":
        if alter < 6:
            dosis = 0.15
        elif 6 <= alter < 12:
            dosis = 0.3
        else:
            dosis = 0.5
        med_list.append(("Adrenalin", f"{dosis:.2f} mg i.m.", "Altersbasierte Dosierung (<6 J:0,15 mg | 6–12 J:0,3 mg | ≥12 J:0,5 mg)"))

    # --- Asthma/COPD ---
    elif erkrankung == "Asthma/COPD":
        if alter >= 12:
            med_list.extend([
                ("Salbutamol", "2,5 mg vernebelt", "Erwachsene Dosis"),
                ("Prednisolon", "100 mg i.v.", "Erwachsene Dosis"),
                ("Ipratropiumbromid", "500 µg vernebelt", "Erwachsene Dosis")
            ])
        elif 4 <= alter < 12:
            med_list.extend([
                ("Salbutamol", "1,25 mg vernebelt", "Kinderdosis"),
                ("Prednisolon", "100 mg rektal", "Kinderdosis")
            ])
        else:
            med_list.extend([
                ("Adrenalin", "2 mg + 2 ml NaCl vernebelt", "Säuglingsdosis"),
                ("Prednisolon", "100 mg rektal", "Säuglingsdosis")
            ])

    # --- Hypoglykämie ---
    elif erkrankung == "Hypoglykämie":
        if bewusstseinslage.startswith("Ansprechbar"):
            med_list.append(("Glucose", "bis 16 g p.o. oder i.v.", "Patient ansprechbar → orale Gabe möglich, sonst langsam i.v."))
        else:
            med_list.append(("Glucose", "bis 16 g i.v.", "Bewusstseinsgestört → nur i.v., langsam applizieren"))

    # --- Krampfanfall ---
    elif erkrankung == "Krampfanfall":
        if zugang.startswith("Ja"):
            dosis_mg = 0.05 * gewicht
            med_list.append(("Midazolam", f"{dosis_mg:.2f} mg i.v. langsam", "0,05 mg/kg KG, langsam i.v. bei Zugang möglich"))
        else:
            if gewicht <= 10:
                med_list.append(("Midazolam", "2,5 mg = 0,5 ml", "Zugang nicht möglich, 0-10 kg"))
            elif gewicht <= 20:
                med_list.append(("Midazolam", "5 mg = 1 ml", "Zugang nicht möglich, 10-20 kg"))
            else:
                med_list.append(("Midazolam", "10 mg = 2 ml", "Zugang nicht möglich, >20 kg"))

    # --- Schlaganfall ---
    elif erkrankung == "Schlaganfall":
        if blutdruck < 120:
            med_list.append(("Jonosteril", "Volumengabe nach Bedarf", "Blutdruck <120 mmHg → Volumengabe"))
        elif blutdruck > 220:
            med_list.append(("Urapidil", "5–15 mg i.v. langsam", "Blutdruck >220 mmHg → Urapidil langsam i.v."))
        else:
            med_list.append(("Keine akute medikamentöse Therapie", "–", "Blutdruck im Normbereich"))

    # --- Kardiales Lungenödem ---
    elif erkrankung == "Kardiales Lungenödem":
        if blutdruck > 120:
            med_list.extend([
                ("Nitro", "0,4–0,8 mg sublingual", "Blutdruck >120 mmHg → Nitro unter die Zunge"),
                ("Furosemid", "20 mg i.v.", "Immer langsam i.v. applizieren")
            ])
        else:
            med_list.append(("Furosemid", "20 mg i.v.", "Blutdruck ≤120 mmHg → nur Furosemid i.v., langsam applizieren"))

    # --- Hypertensiver Notfall ---
    elif erkrankung == "Hypertensiver Notfall":
        ziel_blutdruck = blutdruck * 0.8
        med_list.append(("Urapidil", "5–15 mg i.v. langsam", f"Blutdruck darf maximal 20% gesenkt werden → Ziel: {ziel_blutdruck:.1f} mmHg"))

    # --- Starke Schmerzen bei Trauma ---
    elif erkrankung == "Starke Schmerzen bei Trauma":
        if alter >= 12 or gewicht >= 30:
            # Paracetamol
            if gewicht < 50:
                paracetamol_dosis = 15 * gewicht
                med_list.append(("Paracetamol", f"{paracetamol_dosis:.1f} mg", "15 mg/kg KG"))
            else:
                med_list.append(("Paracetamol", "1 g", "Gewicht ≥50 kg"))

            # Midazolam
            midazolam_dosis = 0
            if alter > 60:
                midazolam_dosis = 1
            elif gewicht > 50:
                midazolam_dosis = 2
            elif gewicht > 30:
                midazolam_dosis = 1
            if midazolam_dosis > 0:
                med_list.append(("Midazolam", f"{midazolam_dosis} mg", "Sedierung nach Gewicht/Alter"))

            # Esketamin oder Fentanyl
            if trauma_medikament == "Esketamin" and gewicht > 30:
                esk_dosis = 0.125 * gewicht
                med_list.append(("Esketamin", f"{esk_dosis:.2f} mg", "0,125 mg/kg KG"))
            elif trauma_medikament == "Fentanyl" and gewicht > 30:
                dosis_einmal_mg = 0.05  # 50 µg
                dosis_einmal_ug = dosis_einmal_mg * 1000  # Umrechnung in µg
                max_total_ug = 2 * gewicht  # 2 µg/kg KG
                max_gaben = math.floor(max_total_ug / dosis_einmal_ug)
                med_list.append((
                    "Fentanyl",
                    f"{dosis_einmal_mg:.2f} mg i.v. alle 4 Min",
                    f"Maximaldosis: {max_total_ug:.0f} µg → {max_gaben} Gaben möglich"
                ))

    return med_list

# ---------- Button ----------
if st.button("💉 Dosierung berechnen"):
    ergebnisse = berechnung(alter, gewicht, erkrankung, bewusstseinslage, zugang, blutdruck, trauma_medikament)

    st.markdown("<div class='box'>", unsafe_allow_html=True)
    st.markdown("## 📋 Ergebnis")

    for med, dosis, hinweis in ergebnisse:
        st.write(f"**Medikament:** {med}")
        st.write(f"**Dosierung:** {dosis}")
        if schulungsmodus:
            st.markdown("<div class='calc'>", unsafe_allow_html=True)
            st.write(f"**Hinweis:** {hinweis}")
            st.markdown("</div>", unsafe_allow_html=True)
        st.markdown("---")

    st.markdown("</div>", unsafe_allow_html=True)

# ---------- Footer ----------
st.markdown("---")
st.caption("Schulungsanwendung | Keine medizinische Verantwortung")
