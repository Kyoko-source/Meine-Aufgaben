import streamlit as st
import math

# ================== SEITENEINSTELLUNGEN ==================
st.set_page_config(
    page_title="💊 Medikamentendosierung – Schulungszwecke",
    page_icon="💊",
    layout="wide"
)

# ================== STYLES ==================
st.markdown("""
<style>
/* === Body & Fonts === */
body {
    background-color: #edf2f7;
    font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
    color: #1f4e79;
}

/* === Karten === */
.card, .calc, .admin {
    background-color: #ffffff;
    padding: 25px;
    border-radius: 20px;
    box-shadow: 0 8px 20px rgba(0,0,0,0.1);
    margin-bottom: 20px;
    transition: transform 0.2s ease, box-shadow 0.2s ease;
}
.card:hover, .calc:hover, .admin:hover {
    transform: translateY(-3px);
    box-shadow: 0 12px 24px rgba(0,0,0,0.15);
}

/* === Header === */
.header {
    color: #1f4e79;
    font-weight: 700;
    font-size: 2.5em;
    margin-bottom: 20px;
}

/* === Buttons === */
.stButton>button {
    background: linear-gradient(90deg, #4cafef 0%, #1f4e79 100%);
    color: white;
    font-weight: bold;
    border-radius: 12px;
    padding: 12px 25px;
    transition: all 0.3s ease;
}
.stButton>button:hover {
    background: linear-gradient(90deg, #1f4e79 0%, #4cafef 100%);
    transform: scale(1.05);
}

/* === Input Widgets === */
.stNumberInput>div>input, .stSelectbox>div>div>div {
    border-radius: 10px;
    border: 1px solid #cfd8dc;
    padding: 8px;
}

/* === Schulungs-Hinweise === */
.calc {
    background-color: #e3fcec;
    border-left: 4px solid #4caf50;
    font-size: 0.95em;
    padding: 12px 18px;
}

/* === Admin Bereich === */
.admin {
    background-color: #fff8e1;
    border-left: 4px solid #ff9800;
}

/* === Medikamentenliste === */
.med-list {
    background: #f5f7fa;
    padding: 15px;
    border-radius: 15px;
    margin-bottom: 12px;
    transition: transform 0.2s ease;
}
.med-list:hover {
    transform: translateX(3px);
    box-shadow: 0 6px 12px rgba(0,0,0,0.08);
}

/* === Warnungen === */
.stWarning {
    background-color: #fff3cd !important;
    color: #856404 !important;
    border-radius: 12px;
    padding: 15px;
    font-weight: 500;
}
</style>
""", unsafe_allow_html=True)

# ================== HEADER ==================
st.markdown("<h1 class='header'>💊 Medikamentendosierung – Schulungszwecke</h1>", unsafe_allow_html=True)
st.warning("⚠️ Ausschließlich für Schulungs- und Ausbildungszwecke – keine reale Anwendung!")

schulungsmodus = st.toggle("🎓 Schulungsmodus (Erklärungen anzeigen)", value=True)

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
                "Übelkeit / Erbrechen",
                "Instabile Bradykardie",
                "Benzodiazepin-Intoxikation",
                "Opiat-Intoxikation",
                "Lungenarterienembolie"
            ]
        )

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

    # ---------- HYPOGLYKÄMIE ----------
    if erkrankung == "Hypoglykämie":
        meds.append(("Glukose", "bis 16 g i.v.", "Langsam i.v. / oral bei wachem Patienten"))

    # ---------- KRAMPFANFALL ----------
    if erkrankung == "Krampfanfall":
        if zugang == "Ja":
            meds.append(("Midazolam", f"{0.05 * gewicht:.2f} mg i.v.", "0,05 mg/kg KG"))
        else:
            if gewicht <= 10:
                meds.append(("Midazolam", "2,5 mg (0,5 ml)", ""))
            elif gewicht <= 20:
                meds.append(("Midazolam", "5 mg (1 ml)", ""))
            else:
                meds.append(("Midazolam", "10 mg (2 ml)", ""))

    # ---------- SCHLAGANFALL ----------
    if erkrankung == "Schlaganfall":
        if blutdruck and blutdruck < 120:
            meds.append(("Jonosteril", "", "RR <120 mmHg"))
        elif blutdruck and blutdruck > 220:
            meds.append(("Urapidil", "5–15 mg i.v.", "RR >220 mmHg"))

    # ---------- KARDIALES LUNGENÖDEM ----------
    if erkrankung == "Kardiales Lungenödem":
        meds.append(("Furosemid", "20 mg i.v.", ""))
        if blutdruck and blutdruck > 120:
            meds.append(("Nitro", "0,4–0,8 mg sublingual", "RR >120 mmHg"))

    # ---------- HYPERTENSIVER NOTFALL ----------
    if erkrankung == "Hypertensiver Notfall" and blutdruck:
        ziel = int(blutdruck * 0.8)
        meds.append(("Urapidil", "5–15 mg langsam i.v.", f"Ziel-Sys ≈ {ziel} mmHg"))

    # ---------- STARKER SCHMERZ / TRAUMA ----------
    if erkrankung == "Starke Schmerzen bei Trauma":
        if gewicht >= 30:
            meds.append(("Paracetamol", f"{15*gewicht:.0f} mg i.v.", "15 mg/kg"))
            mid_esket_fent = st.radio("Zusatzmedikation wählen:", ["Midazolam + Esketamin", "Fentanyl"])
            if mid_esket_fent == "Midazolam + Esketamin":
                if gewicht >= 30:
                    meds.append(("Midazolam", "1 mg i.v.", "Gewicht >30 kg"))
                    meds.append(("Esketamin", f"{0.125*gewicht:.2f} mg i.v.", "0,125 mg/kg"))
            else:
                dosis_einmal_mg = 0.05  # Fentanyl
                dosis_einmal_ug = dosis_einmal_mg * 1000
                max_total_ug = 2 * gewicht
                max_gaben = math.floor(max_total_ug / dosis_einmal_ug)
                meds.append(("Fentanyl", f"0,05 mg i.v. alle 4 min", f"Maximal {max_gaben} Gaben"))

    # ---------- BRUSTSCHMERZ ACS ----------
    if erkrankung == "Brustschmerz ACS":
        meds.append(("ASS", "250 mg i.v.", ""))
        meds.append(("Heparin", "5000 I.E. i.v.", ""))
        if atemfrequenz is not None and atemfrequenz < 10:
            meds.append(("Morphin", "3 mg i.v.", "AF < 10/min"))

    # ---------- ABDOMINALE SCHMERZEN / KOLIKEN ----------
    if erkrankung == "Abdominelle Schmerzen / Koliken":
        if 3 <= schmerzskala <=5 and gewicht >= 30:
            if gewicht > 50:
                meds.append(("Paracetamol", "1 g i.v.", "Gewicht >50 kg"))
            else:
                meds.append(("Paracetamol", f"{15*gewicht:.0f} mg i.v.", "15 mg/kg"))
        if 6 <= schmerzskala <=10:
            dosis = 0.3*gewicht
            if dosis > 40: dosis = 40
            meds.append(("Butylscopolamin", f"{dosis:.2f} mg i.v.", "max. 40 mg"))
            if gewicht >= 30:
                dosis_einmal_mg = 0.05
                dosis_einmal_ug = dosis_einmal_mg*1000
                max_total_ug = 2*gewicht
                max_gaben = math.floor(max_total_ug / dosis_einmal_ug)
                meds.append(("Fentanyl", f"0,05 mg i.v.", f"Maximal {max_gaben} Gaben"))

    # ---------- ÜBELKEIT / ERBRECHEN ----------
    if erkrankung == "Übelkeit / Erbrechen":
        if alter >= 60:
            meds.append(("Ondansetron", "4 mg i.v.", "Einmalig"))
        else:
            meds.append(("Dimenhydrinat", "31 mg i.v.", "Zusätzlich 31 mg Infusion"))

    # ---------- INSTABILE BRADYKARDIE ----------
    if erkrankung == "Instabile Bradykardie":
        if asystolie_gefahr == "Ja":
            meds.append(("Adrenalin-Infusion", "1 mg in 500 ml Jonosteril", "1 Tropfen/Sekunde"))
        else:
            meds.append(("Atropin", "0,5 mg i.v.", "Bis max. 3 mg"))

    # ---------- BENZODIAZEPIN-INTOXIKATION ----------
    if erkrankung == "Benzodiazepin-Intoxikation":
        meds.append(("Flumazenil", "0,5 mg i.v.", "Langsam i.v."))

    # ---------- OPIAT-INTOXIKATION ----------
    if erkrankung == "Opiat-Intoxikation":
        meds.append(("Naloxon", "0,4 mg i.v.", "Auf 10 ml aufziehen, langsam titrieren"))

    # ---------- LUNGENARTERIENEMBOLIE ----------
    if erkrankung == "Lungenarterienembolie":
        meds.append(("Heparin", "5000 I.E. i.v.", ""))

    return meds

# ================== AUSGABE ==================
if st.button("💉 Dosierung berechnen"):
    ergebnis = berechne()
    st.markdown("<div class='card'>", unsafe_allow_html=True)
    st.subheader("📋 Therapieempfehlung")
    for i, (med, dosis, hinweis) in enumerate(ergebnis):
        st.markdown(f"<div class='med-list'><b>💊 {med}</b><br>➡️ Dosierung: {dosis}</div>", unsafe_allow_html=True)
        if schulungsmodus and hinweis:
            st.markdown(f"<div class='calc'>ℹ️ {hinweis}</div>", unsafe_allow_html=True)
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
        st.session_state.sop_admin = {
            "Anaphylaxie": {"Adrenalin": "0,15 mg (<6 J) | 0,3 mg (6–12 J) | 0,5 mg ≥12 J"},
            "Asthma/COPD": {"Salbutamol": "altersabhängig", "Ipratropiumbromid": "500 µg (>12 J)", "Prednisolon": "100 mg i.v./rektal"},
            "Hypoglykämie": {"Glukose": "bis 16 g i.v. / oral"},
            "Krampfanfall": {"Midazolam": "0,05 mg/kg"},
            "Schlaganfall": {"Jonosteril": "RR <120 mmHg", "Urapidil": "5–15 mg i.v."},
            "Kardiales Lungenödem": {"Nitro": "0,4–0,8 mg sublingual", "Furosemid": "20 mg i.v."},
            "Hypertensiver Notfall": {"Urapidil": "5–15 mg i.v."},
            "Starke Schmerzen bei Trauma": {"Paracetamol": "15 mg/kg oder 1 g", "Esketamin": "0,125 mg/kg", "Fentanyl": "0,05 mg alle 4 min, max. 2 µg/kg"},
            "Brustschmerz ACS": {"ASS": "250 mg i.v.", "Heparin": "5000 I.E. i.v.", "Morphin": "3 mg i.v."},
            "Abdominelle Schmerzen / Koliken": {"Paracetamol": "15 mg/kg oder 1 g", "Butylscopolamin": "0,3 mg/kg max.40 mg", "Fentanyl": "0,05 mg, max. 2 µg/kg"},
            "Übelkeit / Erbrechen": {"Ondansetron": "4 mg i.v.", "Dimenhydrinat": "31 mg i.v. + 31 mg Infusion"},
            "Instabile Bradykardie": {"Adrenalin": "1 mg in 500 ml Jonosteril", "Atropin": "0,5 mg i.v. bis max. 3 mg"},
            "Benzodiazepin-Intoxikation": {"Flumazenil": "0,5 mg i.v."},
            "Opiat-Intoxikation": {"Naloxon": "0,4 mg i.v. auf 10 ml"},
            "Lungenarterienembolie": {"Heparin": "5000 I.E. i.v."}
        }
    for erk, meds in st.session_state.sop_admin.items():
        st.sidebar.subheader(erk)
        for med, dosis in meds.items():
            new_val = st.sidebar.text_input(f"{med} – Dosierung", value=dosis, key=f"{erk}_{med}")
            st.session_state.sop_admin[erk][med] = new_val

st.caption("Rettungsdienst – Schulungssimulation | Keine Haftung")
