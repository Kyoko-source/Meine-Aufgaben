import streamlit as st
import datetime
import pytz
import json
import os
import hashlib

# 🔒 Verbesserte Passwortabfrage – zentriert & gestylt
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
            st.markdown("## 🔐 Zugriff geschützt")
            st.markdown("Bitte Passwort eingeben, um fortzufahren.")
            st.text_input("Passwort", type="password", on_change=password_entered, key="password")
        st.stop()

# Passwortprüfung zuerst ausführen
check_password()

# ===========================
# ✅ RTW/KTW Aufgaben-App mit Dark Mode + Export/Import
# ===========================

st.set_page_config(page_title="RTW Aufgabenplan", page_icon="🚑", layout="wide")

STATUS_DATEI = "status.json"

# Dark Mode Toggle in Sidebar
if "dark_mode" not in st.session_state:
    st.session_state.dark_mode = False

dark_mode = st.sidebar.checkbox("🌙 Dark Mode aktivieren", value=st.session_state.dark_mode)
st.session_state.dark_mode = dark_mode

# Dynamisches Styling je nach Mode
if dark_mode:
    bg_color_ktw = "#1b361b"
    border_color_ktw = "#4caf50"
    text_color_ktw = "#a5d6a7"
    bg_color_rtw = "#3e1f1f"
    border_color_rtw = "#ef5350"
    text_color_rtw = "#ef9a9a"
    bg_info_1 = "#2e7d32"
    bg_info_2 = "#c62828"
    bg_info_3 = "#f57c00"
    bg_info_4 = "#5e35b1"
    page_bg = "#121212"
    page_text = "#fafafa"

    st.markdown(f"""
    <style>
    .reportview-container {{
        background-color: {page_bg};
        color: {page_text};
    }}
    .css-1d391kg {{
        background-color: {page_bg};
    }}
    .css-ffhzg2 {{
        background-color: {page_bg};
    }}
    </style>
    """, unsafe_allow_html=True)

else:
    bg_color_ktw = "#e8f5e9"
    border_color_ktw = "#2e7d32"
    text_color_ktw = "#2e7d32"
    bg_color_rtw = "#ffebee"
    border_color_rtw = "#c62828"
    text_color_rtw = "#c62828"
    bg_info_1 = "#e8f5e9"
    bg_info_2 = "#ffebee"
    bg_info_3 = "#fff3e0"
    bg_info_4 = "#ede7f6"
    page_bg = "#ffffff"
    page_text = "#000000"

# Daten / Aufgaben
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

def get_current_time():
    timezone = pytz.timezone('Europe/Berlin')
    return datetime.datetime.now(timezone).strftime('%H:%M:%S')

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

# Aktuelles Datum und Wochentag
heute_en = datetime.datetime.now(pytz.timezone('Europe/Berlin')).strftime('%A')
heute_deutsch = tage_uebersetzung.get(heute_en, "Unbekannt")
heute_str = datetime.datetime.now(pytz.timezone('Europe/Berlin')).strftime('%d.%m.%Y')
feiertag_heute = feiertage_2025.get(heute_str)

# Lade gespeicherten Status
status_dict = lade_status()

# Seitentitel & Header
st.title("✔ Rettungswache Südlohn Tagesaufgaben ✔")
st.subheader(f"📅 Heute ist {heute_deutsch} ({heute_str})")

# Export / Import Funktionen für offline Nutzung
st.sidebar.markdown("---")
st.sidebar.markdown("### 💾 Status speichern / laden")

if st.sidebar.button("Status exportieren (JSON herunterladen)"):
    st.sidebar.download_button(
        label="Download Status JSON",
        data=json.dumps(status_dict, indent=2),
        file_name=f"status_{heute_str}.json",
        mime="application/json"
    )

uploaded_file = st.sidebar.file_uploader("Status JSON importieren", type=["json"])
if uploaded_file is not None:
    try:
        imported_status = json.load(uploaded_file)
        if isinstance(imported_status, dict):
            status_dict.update(imported_status)
            speichere_status(status_dict)
            st.sidebar.success("✅ Status erfolgreich importiert!")
        else:
            st.sidebar.error("❌ Ungültiges Format!")
    except Exception as e:
        st.sidebar.error(f"❌ Fehler beim Import: {e}")

# Aufgabenbereiche in Boxen mit Farben & Überschrift und Liste
col_ktw, col_rtw = st.columns(2)

with col_ktw:
    st.markdown(f"""
    <div style="
        background-color:{bg_color_ktw}; 
        border:2px solid {border_color_ktw}; 
        border-radius:12px; 
        padding:20px; 
        box-shadow: 2px 3px 8px rgba(46, 125, 50, 0.15);
        color: {text_color_ktw};
    ">
        <h3 style='color:{border_color_ktw}; margin-bottom:12px;'>🧾 Aufgaben KTW</h3>
    """, unsafe_allow_html=True)
    for aufgabe in aufgaben_ktw.get(heute_deutsch, []):
        aufgabe_mit_feedback(aufgabe, heute_deutsch, status_dict, fahrzeug="KTW", readonly=False)
    st.markdown("</div>", unsafe_allow_html=True)

with col_rtw:
    st.markdown(f"""
    <div style="
        background-color:{bg_color_rtw}; 
        border:2px solid {border_color_rtw}; 
        border-radius:12px; 
        padding:20px; 
        box-shadow: 2px 3px 8px rgba(198, 40, 40, 0.15);
        color: {text_color_rtw};
    ">
        <h3 style='color:{border_color_rtw}; margin-bottom:12px;'>🚑 Aufgaben RTW</h3>
    """, unsafe_allow_html=True)
    for aufgabe in aufgaben_rtw.get(heute_deutsch, []):
        aufgabe_mit_feedback(aufgabe, heute_deutsch, status_dict, fahrzeug="RTW", readonly=False)
    st.markdown("</div>", unsafe_allow_html=True)

# Dropdown für andere Tage
st.markdown("---")
tag_auswahl = st.selectbox("📌 Wähle einen anderen Wochentag zur Ansicht:", ["—"] + list(tage_uebersetzung.values()))

if tag_auswahl != "—":
    st.write(f"### 🔎 Aufgaben für {tag_auswahl}")
    col_ktw, col_rtw = st.columns(
