import streamlit as st
import datetime
import pytz
import json
import os
import hashlib

# Passwortabfrage (zentriert & gestylt)
def check_password():
    def password_entered():
        if st.session_state["password"] == "RettSüd15":
            st.session_state["passwort_akzeptiert"] = True
        else:
            st.session_state["passwort_akzeptiert"] = False
            st.error("❌ Falsches Passwort. Bitte versuche es erneut.")

    if "passwort_akzeptiert" not in st.session_state or not st.session_state["passwort_akzeptiert"]:
        col1, col2, col3 = st.columns([1, 2, 1])
        with col2:
            st.markdown(
                """
                <div style="text-align:center; margin-top:100px;">
                    <h2 style="color:#2e7d32;">🔐 Zugriff geschützt</h2>
                    <p style="color:#555;">Bitte Passwort eingeben, um fortzufahren.</p>
                </div>
                """,
                unsafe_allow_html=True
            )
            st.text_input("Passwort", type="password", on_change=password_entered, key="password", 
                          placeholder="Passwort hier eingeben")
        st.stop()

check_password()

STATUS_DATEI = "status.json"

aufgaben_ktw = {
    "Montag": ["Fächerdesi 1-6", "Umkleide Bad SW-Bereich reinigen"],
    "Dienstag": ["BZ Kontrolle", "Fächerdesi 7-8", "BZ Messung"],
    "Mittwoch": ["Innenraumdesi KTW"],
    "Donnerstag": ["Auto waschen (KTW)", "Garage reinigen"],
    "Freitag": ["Betriebsmittelkontrolle", "O2 Schlauch + Fingertipp wechseln"],
    "Samstag": ["Wäsche gemacht?"],
    "Sonntag": ["Küche reinigen alle Fronten"]
}

aufgaben_rtw = {
    "Montag": ["Fächerdesi 1-6", "Umkleide Bad SW-Bereich reinigen"],
    "Dienstag": ["BZ Kontrolle", "Fächerdesi 7-11"],
    "Mittwoch": ["Innenraumdesi RTW"],
    "Donnerstag": ["Auto waschen (RTW)", "Garage reinigen", "Betriebsmittelkontrolle"],
    "Freitag": ["Fach 12-18 desinfizieren", "O2 Schlauch + Fingertipp wechseln", "Betriebsmittel Kontrolle"],
    "Samstag": ["Fach 20-22 desinfizieren"],
    "Sonntag": ["Küche reinigen alle Fronten"]
}

tage_uebersetzung = {
    "Monday": "Montag",
    "Tuesday": "Dienstag",
    "Wednesday": "Mittwoch",
    "Thursday": "Donnerstag",
    "Friday": "Freitag",
    "Saturday": "Samstag",
    "Sunday": "Sonntag"
}

def lade_status():
    if os.path.exists(STATUS_DATEI):
        with open(STATUS_DATEI, "r") as f:
            return json.load(f)
    return {}

def speichere_status(status_dict):
    with open(STATUS_DATEI, "w") as f:
        json.dump(status_dict, f)

def aufgabe_mit_feedback(aufgabe, wochentag, status_dict, fahrzeug, readonly=False):
    jahr, kalenderwoche, _ = datetime.datetime.now().isocalendar()
    raw_key = f"{fahrzeug}_{wochentag}_{jahr}_{kalenderwoche}_{aufgabe}"
    key_hash = hashlib.md5(raw_key.encode()).hexdigest()
    checked = status_dict.get(key_hash, False)

    if readonly:
        if checked:
            st.markdown(f"<span style='color:green; text-decoration: line-through;'>✅ {aufgabe}</span>", unsafe_allow_html=True)
        else:
            st.markdown(f"<span style='color:red;'>⏳ {aufgabe}</span>", unsafe_allow_html=True)
    else:
        neu_gesetzt = st.checkbox("", value=checked, key=key_hash)
        if neu_gesetzt != checked:
            status_dict[key_hash] = neu_gesetzt
            speichere_status(status_dict)
            if neu_gesetzt:
                st.balloons()

        if neu_gesetzt:
            st.markdown(f"<span style='color:green; text-decoration: line-through;'>✅ {aufgabe}</span>", unsafe_allow_html=True)
        else:
            st.markdown(f"<span style='color:red;'>⏳ {aufgabe}</span>", unsafe_allow_html=True)

heute_en = datetime.datetime.now().strftime('%A')
heute_deutsch = tage_uebersetzung.get(heute_en, "Unbekannt")
heute_str = datetime.datetime.now().strftime('%d.%m.%Y')

status_dict = lade_status()

st.set_page_config(page_title="RTW Aufgabenplan", page_icon="🚑", layout="wide")

# Haupt-Titel in schönem dunkelgrün mit Schatten
st.markdown(
    """
    <h1 style="
        text-align:center; 
        color:#2e7d32; 
        text-shadow: 1px 1px 2px #a5d6a7;
        margin-bottom: 10px;
    ">✔ Rettungswache Südlohn Tagesaufgaben ✔</h1>
    """,
    unsafe_allow_html=True
)

# Untertitel zentriert und dezent dunkelgrau
st.markdown(
    f"""
    <h4 style="
        text-align:center; 
        color:#555; 
        margin-top: -15px; 
        margin-bottom: 40px;
        font-weight: normal;
    ">📅 Heute ist {heute_deutsch} ({heute_str})</h4>
    """,
    unsafe_allow_html=True
)

col_ktw, col_rtw = st.columns(2)

with col_ktw:
    st.markdown("""
    <div style="
        border: 2px solid #2e7d32; 
        border-radius: 12px; 
        padding: 20px; 
        background: #e8f5e9;
        box-shadow: 2px 2px 8px rgba(46, 125, 50, 0.25);
    ">
    <h3 style="color:#2e7d32; margin-bottom: 15px;">🧾 Aufgaben KTW</h3>
    """, unsafe_allow_html=True)
    for aufgabe in aufgaben_ktw.get(heute_deutsch, []):
        aufgabe_mit_feedback(aufgabe, heute_deutsch, status_dict, fahrzeug="KTW", readonly=False)
    st.markdown("</div>", unsafe_allow_html=True)

with col_rtw:
    st.markdown("""
    <div style="
        border: 2px solid #1976d2; 
        border-radius: 12px; 
        padding: 20px; 
        background: #e3f2fd;
        box-shadow: 2px 2px 8px rgba(25, 118, 210, 0.25);
    ">
    <h3 style="color:#1976d2; margin-bottom: 15px;">🚑 Aufgaben RTW</h3>
    """, unsafe_allow_html=True)
    for aufgabe in aufgaben_rtw.get(heute_deutsch, []):
        aufgabe_mit_feedback(aufgabe, heute_deutsch, status_dict, fahrzeug="RTW", readonly=False)
    st.markdown("</div>", unsafe_allow_html=True)

# Separator als schöner feiner Balken mit etwas Farbe
st.markdown(
    """
    <hr style="
        border:none;
        height:1.5px;
        background: linear-gradient(to right, #2e7d32, #1976d2);
        margin: 40px 0;
    ">
    """, unsafe_allow_html=True
)

tag_auswahl = st.selectbox(
    label="📌 Wähle einen anderen Wochentag zur Ansicht:",
    options=["—"] + list(tage_uebersetzung.values()),
    help="Wähle einen Tag, um vergangene oder zukünftige Aufgaben zu sehen."
)

if tag_auswahl != "—":
    st.markdown(f"<h3 style='color:#444; margin-bottom:15px;'>🔎 Aufgaben für {tag_auswahl}</h3>", unsafe_allow_html=True)
    col_ktw, col_rtw = st.columns(2)

    with col_ktw:
        st.markdown("""
        <div style="
            border: 2px solid #2e7d32; 
            border-radius: 12px; 
            padding: 20px; 
            background: #e8f5e9;
            box-shadow: 2px 2px 8px rgba(46, 125, 50, 0.25);
        ">
        <h4 style="color:#2e7d32; margin-bottom: 15px;">🧾 Aufgaben KTW</h4>
        """, unsafe_allow_html=True)
        for aufgabe in aufgaben_ktw.get(tag_auswahl, []):
            aufgabe_mit_feedback(aufgabe, tag_auswahl, status_dict, fahrzeug="KTW", readonly=True)
        st.markdown("</div>", unsafe_allow_html=True)

    with col_rtw:
        st.markdown("""
        <div style="
            border: 2px solid #1976d2; 
            border-radius: 12px; 
            padding: 20px; 
            background: #e3f2fd;
            box-shadow: 2px 2px 8px rgba(25, 118, 210, 0.25);
        ">
        <h4 style="color:#1976d2; margin-bottom: 15px;">🚑 Aufgaben RTW</h4>
        """, unsafe_allow_html=True)
        for aufgabe in aufgaben_rtw.get(tag_auswahl, []):
            aufgabe_mit_feedback(aufgabe, tag_auswahl, status_dict, fahrzeug="RTW", readonly=True)
        st.markdown("</div>", unsafe_allow_html=True)

# Tagesinfos im Footer-Bereich, ebenfalls hübsch gestaltet
st.markdown("---")

def get_current_time():
    timezone = pytz.timezone('Europe/Berlin')
    return datetime.datetime.now(timezone).strftime('%H:%M:%S')

feiertage_2025 = {
    "01.01.2025": "Neujahrstag",
    "06.01.2025": "Heilige Drei Könige",
    "08.03.2025": "Internationaler Frauentag",
    "18.04.2025": "Karfreitag",
    "21.04.2025": "Ostermontag",
    "01.05.2025": "Tag der Arbeit",
    "29.05.2025": "Christi Himmelfahrt",
    "09.06.2025": "Pfingstmontag",
    "19.06.2025": "Fronleichnam",
    "03.10.2025": "Tag der Deutschen Einheit",
    "31.10.2025": "Reformationstag",
    "01.11.2025": "Allerheiligen",
    "19.11.2025": "Buß- und Bettag",
    "25.12.2025": "1. Weihnachtstag",
    "26.12.2025": "2. Weihnachtstag"
}

feiertag_heute = feiertage_2025.get(heute_str)

col1, col2, col3, col4 = st.columns(4)

# Einheitliche kleine Boxen für Tagesinfos mit Farbakzenten passend zum Thema
col1.markdown(f"""
    <div style="
        background:#e8f5e9; 
        border:1.5px solid #2e7d32; 
        border-radius:8px; 
        padding:12px; 
        text-align:center;
        font-weight:bold;
        color:#2e7d32;
        box-shadow: 1px 1px 4px rgba(46, 125, 50, 0.15);
    ">
        🕒 Uhrzeit<br><span style='font-size:24px;'>{get_current_time()}</span>
    </div>
""", unsafe_allow_html=True)

col2.markdown(f"""
    <div style="
        background:#e3f2fd; 
        border:1.5px solid #1976d2; 
        border-radius:8px; 
        padding:12px; 
        text-align:center;
        font-weight:bold;
        color:#1976d2;
        box-shadow: 1px 1px 4px rgba(25, 118, 210, 0.15);
    ">
        🎉 Feiertag<br><span style='font-size:20px;'>{feiertag_heute if feiertag_heute else "Kein Feiertag heute 😟"}</span>
    </div>
""", unsafe_allow_html=True)

col3.markdown("""
    <div style="
        background:#f5f5f5; 
        border:1.5px solid #ccc; 
        border-radius:8px; 
        padding:12px; 
        text-align:center;
        font-weight:bold;
        color:#555;
        box-shadow: 1px 1px 4
