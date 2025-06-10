import streamlit as st
import datetime
import pytz
import json
import os
import hashlib

# ====== Passwortabfrage ======
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

check_password()

# ====== Seite konfigurieren ======
st.set_page_config(page_title="RTW Aufgabenplan", page_icon="🚑", layout="wide", initial_sidebar_state="auto")

# ====== Dark Mode Toggle ======
if "dark_mode" not in st.session_state:
    st.session_state.dark_mode = False

def toggle_dark_mode():
    st.session_state.dark_mode = not st.session_state.dark_mode

st.sidebar.button("🌙 Dark Mode umschalten", on_click=toggle_dark_mode)

# Farben abhängig vom Dark Mode
if st.session_state.dark_mode:
    bg_color_ktw = "#2e7d32"
    border_color_ktw = "#a5d6a7"
    text_color_ktw = "white"

    bg_color_rtw = "#c62828"
    border_color_rtw = "#ef9a9a"
    text_color_rtw = "white"

    background_color_page = "#121212"
    text_color_page = "white"
else:
    bg_color_ktw = "#e8f5e9"
    border_color_ktw = "#2e7d32"
    text_color_ktw = "#2e7d32"

    bg_color_rtw = "#ffebee"
    border_color_rtw = "#c62828"
    text_color_rtw = "#c62828"

    background_color_page = "white"
    text_color_page = "black"

st.markdown(
    f"""
    <style>
    body {{
        background-color: {background_color_page};
        color: {text_color_page};
    }}
    </style>
    """,
    unsafe_allow_html=True,
)

# ====== Daten ======
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

# ====== Funktionen ======

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
            st.markdown(f"<span style='color:#4caf50; text-decoration: line-through;'>✅ {aufgabe}</span>", unsafe_allow_html=True)
        else:
            st.markdown(f"<span style='color:#f44336;'>⏳ {aufgabe}</span>", unsafe_allow_html=True)
    else:
        neu_gesetzt = st.checkbox("", value=checked, key=key_hash)
        if neu_gesetzt != checked:
            status_dict[key_hash] = neu_gesetzt
            speichere_status(status_dict)
            if neu_gesetzt:
                st.balloons()

        if neu_gesetzt:
            st.markdown(f"<span style='color:#4caf50; text-decoration: line-through;'>✅ {aufgabe}</span>", unsafe_allow_html=True)
        else:
            st.markdown(f"<span style='color:#f44336;'>⏳ {aufgabe}</span>", unsafe_allow_html=True)

# ====== Aktuelles Datum & Status laden ======
heute_en = datetime.datetime.now().strftime('%A')
heute_deutsch = tage_uebersetzung.get(heute_en, "Unbekannt")
heute_str = datetime.datetime.now().strftime('%d.%m.%Y')
feiertag_heute = feiertage_2025.get(heute_str)

status_dict = lade_status()

# ====== UI ======
st.title("✔ Rettungswache Südlohn Tagesaufgaben ✔")
st.subheader(f"📅 Heute ist {heute_deutsch} ({heute_str})")

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
        for aufgabe in aufgaben_ktw.get(tag_auswahl, []):
            aufgabe_mit_feedback(aufgabe, tag_auswahl, status_dict, fahrzeug="KTW", readonly=True)
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
        for aufgabe in aufgaben_rtw.get(tag_auswahl, []):
            aufgabe_mit_feedback(aufgabe, tag_auswahl, status_dict, fahrzeug="RTW", readonly=True)
        st.markdown("</div>", unsafe_allow_html=True)

# Tagesinfos mit 4 farbigen Boxen
st.markdown("---")
st.markdown("### 🌤️ Zusätzliche Tagesinfos")

col1, col2, col3, col4 = st.columns(4)

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
        background:#ffebee; 
        border:1.5px solid #c62828; 
        border-radius:8px; 
        padding:12px; 
        text-align:center;
        font-weight:bold;
        color:#c62828;
        box-shadow: 1px 1px 4px rgba(198, 40, 40, 0.15);
    ">
        🎉 Feiertag<br><span style='font-size:20px;'>{feiertag_heute if feiertag_heute else "Kein Feiertag heute 😟"}</span>
    </div>
""", unsafe_allow_html=True)

col3.markdown(f"""
    <div style="
        background:#fff3e0; 
        border:1.5px solid #f57c00; 
        border-radius:8px; 
        padding:12px; 
        text-align:center;
        font-weight:bold;
        color:#f57c00;
        box-shadow: 1px 1px 4px rgba(245, 124, 0, 0.15);
    ">
        ⚠️ Sicherheits-Check<br>
        <span style='font-size:18px; font-weight:normal;'>
            Vor Fahrtbeginn: Fahrzeug-Check durchführen!
        </span>
    </div>
""", unsafe_allow_html=True)

col4.markdown(f"""
    <div style="
        background:#ede7f6; 
        border:1.5px solid #5e35b1; 
        border-radius:8px; 
        padding:12px; 
        text-align:center;
        font-weight:bold;
        color:#5e35b1;
        box-shadow: 1px 1px 4px rgba(94, 53, 177, 0.15);
    ">
        📌 Tipp<br><span style='font-size:18px;'>Regelmäßig Aufgaben prüfen!</span>
    </div>
""", unsafe_allow_html=True)
