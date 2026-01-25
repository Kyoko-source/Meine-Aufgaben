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
/* BODY & FONTS */
body {
    background: #f4f7fa;
    font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
    color: #1f2937;
}

/* CARD */
.card {
    background: white;
    padding: 30px;
    border-radius: 20px;
    box-shadow: 0 12px 24px rgba(0,0,0,0.08);
    margin-bottom: 25px;
    transition: transform 0.2s;
}
.card:hover {
    transform: translateY(-3px);
}

/* MEDICATION ENTRY */
.med {
    padding: 18px 20px;
    border-radius: 16px;
    margin-bottom: 16px;
    font-size: 0.95em;
    transition: transform 0.2s, box-shadow 0.2s;
}
.med:hover {
    transform: scale(1.02);
    box-shadow: 0 8px 16px rgba(0,0,0,0.1);
}

/* COLORS */
.green { background:#e8f5e9; border-left:6px solid #43a047; }
.blue { background:#e3f2fd; border-left:6px solid #1e88e5; }
.red { background:#ffe5e5; border-left:6px solid #e53935; }
.orange { background:#fff3e0; border-left:6px solid #fb8c00; }

/* BADGES */
.badge {
    display:inline-block;
    background: #1f4e79;
    color: white;
    padding: 6px 12px;
    border-radius: 999px;
    font-size: 0.8em;
    margin-top: 6px;
}

/* BUTTON */
.stButton>button {
    background: linear-gradient(135deg,#4cafef,#1f4e79);
    color:white;
    font-weight:bold;
    padding:14px 28px;
    border-radius:18px;
    font-size:1em;
    box-shadow: 0 6px 12px rgba(0,0,0,0.1);
    transition: transform 0.2s, box-shadow 0.2s;
}
.stButton>button:hover {
    transform: scale(1.05);
    box-shadow: 0 8px 16px rgba(0,0,0,0.15);
}
</style>
""", unsafe_allow_html=True)

# ================== TITLE & WARNING ==================
st.title("💊 Medikamentendosierung – Schulungszwecke")
st.warning("⚠️ Ausschließlich für Schulung / Simulation – keine reale Anwendung!")

# ================== SESSION STATE ==================
if "result" not in st.session_state:
    st.session_state.result = None

# ================== PATIENT & ERKRANKUNG ==================
st.markdown("<div class='card'>", unsafe_allow_html=True)
col1, col2 = st.columns(2)

with col1:
    alter = st.number_input("Alter (Jahre)", 0, 120, 50)
    gewicht = st.number_input("Gewicht (kg)", 1.0, 200.0, 80.0, step=0.1)

with col2:
    erkrankung = st.selectbox("Erkrankung", [
        "Anaphylaxie","Asthma/COPD","Hypoglykämie","Krampfanfall",
        "Schlaganfall","Kardiales Lungenödem","Hypertensiver Notfall",
        "Starke Schmerzen bei Trauma","Brustschmerz ACS",
        "Abdominelle Schmerzen / Koliken","Übelkeit / Erbrechen",
        "Instabile Bradykardie","Benzodiazepin-Intoxikation",
        "Opiat-Intoxikation","Lungenarterienembolie"
    ])

# ================== DYNAMISCHE ZUSATZFELDER ==================
blutdruck = atemfrequenz = schmerzskala = None
zugang = asystolie = None
zusatz_schmerz = None

if erkrankung in ["Schlaganfall","Kardiales Lungenödem","Hypertensiver Notfall"]:
    blutdruck = st.number_input("Systolischer Blutdruck (mmHg)", 50, 300, 140)

if erkrankung == "Krampfanfall":
    zugang = st.radio("i.v. Zugang vorhanden?", ["Ja","Nein"])

if erkrankung == "Brustschmerz ACS":
    atemfrequenz = st.number_input("Atemfrequenz (/min)", 0, 60, 16)

if erkrankung == "Abdominelle Schmerzen / Koliken":
    schmerzskala = st.slider("Schmerzskala (1–10)", 1, 10, 5)

if erkrankung == "Instabile Bradykardie":
    asystolie = st.radio("Gefahr einer Asystolie?", ["Ja","Nein"])

if erkrankung == "Starke Schmerzen bei Trauma" and gewicht >= 30:
    zusatz_schmerz = st.radio(
        "Zusatzmedikation wählen",
        ["Midazolam + Esketamin", "Fentanyl"],
        horizontal=True
    )

st.markdown("</div>", unsafe_allow_html=True)

# ================== BERECHNUNG ==================
def berechne_med(gewicht, alter, erkrankung, blutdruck=None, zugang=None,
                  atemfrequenz=None, schmerzskala=None, asystolie=None, zusatz_schmerz=None):
    meds = []

    # ---------------------- ANAPHYLAXIE ----------------------
    if erkrankung == "Anaphylaxie":
        if alter < 6:
            meds.append(("Adrenalin", "0,15 mg i.m.", "red", "Kinder <6 Jahre"))
        elif alter < 12:
            meds.append(("Adrenalin", "0,3 mg i.m.", "red", "Kinder 6–12 Jahre"))
        else:
            meds.append(("Adrenalin", "0,5 mg i.m.", "red", "Patient ≥12 Jahre"))

    # ---------------------- ASTHMA/COPD ----------------------
    if erkrankung == "Asthma/COPD":
        if alter > 12:
            meds.append(("Salbutamol", "2,5 mg vernebelt", "green", "Patient >12 J"))
            meds.append(("Ipratropiumbromid", "500 µg vernebelt", "green", "Patient >12 J"))
            meds.append(("Prednisolon", "100 mg i.v.", "green", ""))
        elif 4 <= alter <= 12:
            meds.append(("Salbutamol", "1,25 mg vernebelt", "green", "Kinder 4–12 J"))
            meds.append(("Prednisolon", "100 mg rektal", "green", "Kinder 4–12 J"))
        else:
            meds.append(("Adrenalin", "2 mg + 2 ml NaCl vernebelt", "red", "Kinder <4 J"))
            meds.append(("Prednisolon", "100 mg rektal", "green", "Kinder <4 J"))

    # ---------------------- HYPOGLYKÄMIE ----------------------
    if erkrankung == "Hypoglykämie":
        meds.append(("Glukose", "bis 16 g i.v.", "green", "Langsam i.v./oral bei wachem Patienten"))

    # ---------------------- KRAMPFANFALL ----------------------
    if erkrankung == "Krampfanfall":
        if zugang == "Ja":
            meds.append(("Midazolam", f"{0.05*gewicht:.2f} mg i.v.", "blue", "0,05 mg/kg"))
        else:
            if gewicht <= 10:
                meds.append(("Midazolam", "2,5 mg (0,5 ml)", "blue", ""))
            elif gewicht <= 20:
                meds.append(("Midazolam", "5 mg (1 ml)", "blue", ""))
            else:
                meds.append(("Midazolam", "10 mg (2 ml)", "blue", ""))

    # ---------------------- SCHMERZEN / TRAUMA ----------------------
    if erkrankung == "Starke Schmerzen bei Trauma":
        meds.append(("Paracetamol", f"{15*gewicht:.0f} mg i.v.", "green", "15 mg/kg"))
        if zusatz_schmerz == "Midazolam + Esketamin":
            meds.append(("Midazolam", "1 mg i.v.", "blue", ""))
            meds.append(("Esketamin", f"{0.125*gewicht:.2f} mg i.v.", "blue", "0,125 mg/kg"))
        elif zusatz_schmerz == "Fentanyl":
            dosis_einmal_mg = 0.05
            dosis_einmal_ug = dosis_einmal_mg*1000
            max_total_ug = 2*gewicht
            max_gaben = math.floor(max_total_ug/dosis_einmal_ug)
            meds.append(("Fentanyl", "0,05 mg i.v. alle 4 min", "red", f"Maximal {max_gaben} Gaben"))

    # ---------------------- BRUSTSCHMERZ ACS ----------------------
    if erkrankung == "Brustschmerz ACS":
        meds.append(("ASS", "250 mg i.v.", "green", ""))
        meds.append(("Heparin", "5000 I.E. i.v.", "green", ""))
        if atemfrequenz and atemfrequenz < 10:
            meds.append(("Morphin", "3 mg i.v.", "orange", "AF < 10/min"))

    # ---------------------- Weitere Erkrankungen ----------------------
    if erkrankung == "Schlaganfall":
        if blutdruck and blutdruck < 120:
            meds.append(("Jonosteril", "", "green", "RR <120 mmHg"))
        elif blutdruck and blutdruck > 220:
            meds.append(("Urapidil", "5–15 mg i.v.", "red", "RR >220 mmHg"))

    if erkrankung == "Kardiales Lungenödem":
        meds.append(("Furosemid", "20 mg i.v.", "green", ""))
        if blutdruck and blutdruck > 120:
            meds.append(("Nitro", "0,4–0,8 mg sublingual", "green", "RR >120 mmHg"))

    if erkrankung == "Hypertensiver Notfall" and blutdruck:
        ziel = int(blutdruck*0.8)
        meds.append(("Urapidil", "5–15 mg langsam i.v.", "red", f"Ziel-Sys ≈ {ziel} mmHg"))

    if erkrankung == "Abdominelle Schmerzen / Koliken":
        if 3 <= schmerzskala <=5 and gewicht >= 30:
            dosis = 15*gewicht if gewicht<=50 else 1000
            meds.append(("Paracetamol", f"{dosis:.0f} mg i.v.", "green", ""))
        if 6 <= schmerzskala <=10:
            dosis = min(0.3*gewicht, 40)
            meds.append(("Butylscopolamin", f"{dosis:.2f} mg i.v.", "green", "max. 40 mg"))
            if gewicht >= 30:
                dosis_einmal_mg = 0.05
                dosis_einmal_ug = dosis_einmal_mg*1000
                max_total_ug = 2*gewicht
                max_gaben = math.floor(max_total_ug/dosis_einmal_ug)
                meds.append(("Fentanyl", f"0,05 mg i.v.", "red", f"Maximal {max_gaben} Gaben"))

    if erkrankung == "Übelkeit / Erbrechen":
        if alter >= 60:
            meds.append(("Ondansetron", "4 mg i.v.", "green", "Einmalig"))
        else:
            meds.append(("Dimenhydrinat", "31 mg i.v.", "green", "Zusätzlich 31 mg Infusion"))

    if erkrankung == "Instabile Bradykardie":
        if asystolie == "Ja":
            meds.append(("Adrenalin-Infusion", "1 mg in 500 ml Jonosteril", "red", "1 Tropfen/Sekunde"))
        else:
            meds.append(("Atropin", "0,5 mg i.v.", "green", "Bis max. 3 mg"))

    if erkrankung == "Benzodiazepin-Intoxikation":
        meds.append(("Flumazenil", "0,5 mg i.v.", "green", "Langsam i.v."))

    if erkrankung == "Opiat-Intoxikation":
        meds.append(("Naloxon", "0,4 mg i.v.", "red", "Langsam titrieren"))

    if erkrankung == "Lungenarterienembolie":
        meds.append(("Heparin", "5000 I.E. i.v.", "green", ""))

    return meds

# ================== BERECHNUNG BUTTON ==================
if st.button("💉 Dosierung berechnen"):
    st.session_state.result = berechne_med(
        gewicht, alter, erkrankung, blutdruck, zugang, atemfrequenz,
        schmerzskala, asystolie, zusatz_schmerz
    )

# ================== DYNAMISCHE MEDIKAMENTE REA ==================

# Session State
if "rea_meds_given" not in st.session_state:
    st.session_state.rea_meds_given = []

# Medikamentenlogik abhängig vom Fortschritt Helfer 2
def get_rea_meds(step_h2):
    meds = []

    if step_h2 >= 1:
        meds.append(("Adrenalin", "1 mg i.v./i.o.", "alle 3–5 Min"))

    if step_h2 >= 3:
        meds.append(("Amiodaron", "300 mg i.v.", "nach 3. Schock"))

    if step_h2 >= 4:
        meds.append(("Adrenalin", "1 mg i.v./i.o.", "wiederholen"))

    return meds


# ================== MEDIKAMENTE IM REA-MODUS ==================
if st.session_state.get("rea_mode", False):

    meds = get_rea_meds(st.session_state.rea_step_h2)

    if meds:
        st.markdown("### 💉 Medikamente – Helfer 1")

        for med, dosis, info in meds:
            med_key = f"{med}_{dosis}"

            col_m1, col_m2 = st.columns([3, 1])

            with col_m1:
                st.markdown(
                    f"""
                    <div class='med red'>
                        <b>{med}</b><br>
                        {dosis}
                        <div class='badge'>{info}</div>
                    </div>
                    """,
                    unsafe_allow_html=True
                )

            with col_m2:
                if med_key not in st.session_state.rea_meds_given:
                    if st.button("Geben", key=med_key):
                        st.session_state.rea_meds_given.append(med_key)
                else:
                    st.success("✔ gegeben")

# ================== AUSGABE ==================
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

