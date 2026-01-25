import streamlit as st
import math

st.set_page_config(
    page_title="💊 Medikamentendosierung – Schulung",
    page_icon="💊",
    layout="wide"
)

# ================== STYLES ==================
st.markdown("""
<style>
body { background:#edf2f7; font-family:Segoe UI; }
.card { background:white; padding:25px; border-radius:18px;
        box-shadow:0 8px 18px rgba(0,0,0,0.08); margin-bottom:20px; }
.med { padding:16px; border-radius:14px; margin-bottom:12px; }
.red { background:#ffe5e5; border-left:6px solid #e53935; }
.blue { background:#e3f2fd; border-left:6px solid #1e88e5; }
.green { background:#e8f5e9; border-left:6px solid #43a047; }
.badge { display:inline-block; background:#1f4e79; color:white;
         padding:4px 10px; border-radius:999px; font-size:0.8em; }
</style>
""", unsafe_allow_html=True)

st.title("💊 Medikamentendosierung – Schulungszwecke")
st.warning("⚠️ Nur Schulung / Simulation – keine reale Anwendung")

# ================== SESSION STATE ==================
if "result" not in st.session_state:
    st.session_state.result = None

# ================== FORM ==================
with st.form("dosierung_form"):
    st.markdown("<div class='card'>", unsafe_allow_html=True)

    col1, col2 = st.columns(2)

    with col1:
        alter = st.number_input("Alter", 0, 120, 50)
        gewicht = st.number_input("Gewicht (kg)", 1.0, 200.0, 80.0)

    with col2:
        erkrankung = st.selectbox(
            "Erkrankung",
            ["Starke Schmerzen bei Trauma", "Brustschmerz ACS"]
        )

    zusatz = None
    if erkrankung == "Starke Schmerzen bei Trauma":
        zusatz = st.radio(
            "Analgetische Zusatzmedikation",
            ["Midazolam + Esketamin", "Fentanyl"],
            horizontal=True
        )

    submit = st.form_submit_button("💉 Dosierung berechnen")

    st.markdown("</div>", unsafe_allow_html=True)

# ================== BERECHNUNG ==================
if submit:
    meds = []

    if erkrankung == "Starke Schmerzen bei Trauma":
        meds.append(("Paracetamol", f"{15*gewicht:.0f} mg i.v.", "green", "15 mg/kg"))

        if zusatz == "Midazolam + Esketamin":
            meds.append(("Midazolam", "1 mg i.v.", "blue", "Sedierung"))
            meds.append(("Esketamin", f"{0.125*gewicht:.2f} mg i.v.", "blue", "0,125 mg/kg"))

        elif zusatz == "Fentanyl":
            max_ug = 2 * gewicht
            gaben = math.floor(max_ug / 50)
            meds.append(("Fentanyl", "0,05 mg i.v. alle 4 min", "red", f"max. {gaben} Gaben"))

    st.session_state.result = meds

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
