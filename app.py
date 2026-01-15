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
.header { color: #1f4e79; }
.calc {
    background-color: #e8fff0;
    padding: 12px;
    border-radius: 10px;
    margin-top: 6px;
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
.admin {
    background-color: #fff4e6;
    padding: 20px;
    border-radius: 12px;
    border: 2px solid #ff9800;
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

    # ---------- LUNGENARTERIENEMBOLIE ----------
    if erkrankung == "Lungenarterienembolie":
        meds.append((
            "Heparin",
            "5000 I.E. i.v.",
            "Antikoagulation bei Verdacht auf LAE"
        ))

    # ---------- OPIAT-INTOXIKATION ----------
    if erkrankung == "Opiat-Intoxikation":
        meds.append((
            "Naloxon",
            "0,4 mg i.v.",
            "0,4 mg auf 10 ml NaCl aufziehen, langsam titrieren"
        ))

    # ---------- BENZODIAZEPIN-INTOXIKATION ----------
    if erkrankung == "Benzodiazepin-Intoxikation":
        meds.append(("Flumazenil", "0,5 mg i.v.", "Langsam i.v. applizieren"))

    # ---------- INSTABILE BRADYKARDIE ----------
    if erkrankung == "Instabile Bradykardie":
        if asystolie_gefahr == "Ja":
            meds.append((
                "Adrenalin-Infusion",
                "1 mg Adrenalin in 500 ml Jonosteril",
                "1 Tropfen pro Sekunde"
            ))
        else:
            meds.append(("Atropin", "0,5 mg i.v.", "Wiederholbar bis max. 3 mg"))

    # ---------- ÜBELKEIT / ERBRECHEN ----------
    if erkrankung == "Übelkeit / Erbrechen":
        if alter >= 60:
            meds.append(("Ondansetron", "4 mg i.v.", "Einmalig, ggf. 1× wiederholbar"))
        else:
            meds.append(("Dimenhydrinat", "31 mg i.v.", "Zusätzlich 31 mg in die Infusion"))

    # ---------- BRUSTSCHMERZ ACS ----------
    if erkrankung == "Brustschmerz ACS":
        meds.append(("ASS", "250 mg i.v.", ""))
        meds.append(("Heparin", "5000 I.E. i.v.", ""))
        if atemfrequenz is not None and atemfrequenz < 10:
            meds.append(("Morphin", "3 mg i.v.", "AF < 10/min"))

    # ---------- HYPERTENSIVER NOTFALL ----------
    if erkrankung == "Hypertensiver Notfall" and blutdruck:
        ziel = int(blutdruck * 0.8)
        meds.append(("Urapidil", "5–15 mg langsam i.v.", f"Ziel-Sys ≈ {ziel} mmHg"))

    # ---------- KARDIALES LUNGENÖDEM ----------
    if erkrankung == "Kardiales Lungenödem" and blutdruck:
        meds.append(("Furosemid", "20 mg i.v.", ""))
        if blutdruck > 120:
            meds.append(("Nitro", "0,4–0,8 mg sublingual", "RR > 120 mmHg"))

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

    # ---------- HYPOGLYKÄMIE ----------
    if erkrankung == "Hypoglykämie":
        meds.append(("Glukose", "bis 16 g i.v.", "Langsam i.v. / oral bei wachem Patienten"))

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

# ================== ADMIN BUTTON ==================
if st.button("🛠 SOP Anpassung (Admin-Modus)"):
    with st.expander("Admin-Modus"):
        st.markdown("<div class='admin'>", unsafe_allow_html=True)
        pw = st.text_input("🔐 Passwort", type="password")
        if pw == "MediDos":
            st.success("Admin-Zugriff aktiv")
            # SOP-Daten für Admin (editable)
            if "sop_admin" not in st.session_state:
                st.session_state.sop_admin = {
                    "Anaphylaxie": {"Adrenalin": "0,15 mg (<6 J) | 0,3 mg (6–12 J) | 0,5 mg ≥12 J"},
                    "Asthma/COPD": {"Salbutamol": "altersabhängig", "Ipratropiumbromid": "500 µg (>12 J)", "Prednisolon": "100 mg i.v./rektal"},
                    "Hypoglykämie": {"Glukose": "bis 16 g i.v. langsam / oral"},
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
            # SOP bearbeiten
            for erk, meds in st.session_state.sop_admin.items():
                st.subheader(erk)
                for med, dosis in meds.items():
                    new_val = st.text_input(f"{med} – Dosierung", value=dosis, key=f"{erk}_{med}")
                    st.session_state.sop_admin[erk][med] = new_val
                st.divider()
        elif pw != "":
            st.error("Falsches Passwort")
        st.markdown("</div>", unsafe_allow_html=True)

st.caption("Rettungsdienst – Schulungssimulation | Keine Haftung")
