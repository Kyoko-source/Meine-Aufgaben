import streamlit as st
import datetime
import pytz
import json
import os
import hashlib
import time
from PIL import Image

# === Passwortschutz für Haupt- und Admin-Bereich ===
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

# === Adminbereich Passwort ===
def check_admin():
    return st.text_input("🔒 Admin Passwort", type="password") == "RWSüd15"

# Passwortprüfung zuerst ausführen
check_password()

st.set_page_config(page_title="RTW Aufgabenplan", page_icon="🚑", layout="wide")

STATUS_DATEI = "status.json"
SCOREBOARD_DATEI = "scoreboard.json"
SPIELBILD_ORDNER = "spielbilder"
SPIELBILD_NAME = "wochenbild.jpg"

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
    "Monday": "Montag", "Tuesday": "Dienstag", "Wednesday": "Mittwoch", "Thursday": "Donnerstag",
    "Friday": "Freitag", "Saturday": "Samstag", "Sunday": "Sonntag"
}

feiertage_2025 = {
    "01.01.2025": "Neujahrstag", "06.01.2025": "Heilige Drei Könige", "08.03.2025": "Internationaler Frauentag",
    "18.04.2025": "Karfreitag", "21.04.2025": "Ostermontag", "01.05.2025": "Tag der Arbeit",
    "29.05.2025": "Christi Himmelfahrt", "09.06.2025": "Pfingstmontag", "19.06.2025": "Fronleichnam",
    "03.10.2025": "Tag der Deutschen Einheit", "31.10.2025": "Reformationstag", "01.11.2025": "Allerheiligen",
    "19.11.2025": "Buß- und Bettag", "25.12.2025": "1. Weihnachtstag", "26.12.2025": "2. Weihnachtstag"
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
        st.markdown(f"<span style='color:{'green' if checked else 'red'};'>{'✅' if checked else '⏳'} {aufgabe}</span>", unsafe_allow_html=True)
    else:
        neu_gesetzt = st.checkbox("", value=checked, key=key_hash)
        if neu_gesetzt != checked:
            status_dict[key_hash] = neu_gesetzt
            speichere_status(status_dict)
            if neu_gesetzt:
                st.balloons()
        st.markdown(f"<span style='color:{'green' if neu_gesetzt else 'red'};'>{'✅' if neu_gesetzt else '⏳'} {aufgabe}</span>", unsafe_allow_html=True)

# === Hauptinhalt ===
heute_en = datetime.datetime.now().strftime('%A')
heute_deutsch = tage_uebersetzung.get(heute_en, "Unbekannt")
heute_str = datetime.datetime.now().strftime('%d.%m.%Y')
feiertag_heute = feiertage_2025.get(heute_str)

status_dict = lade_status()

st.title("✔ Rettungswache Südlohn Tagesaufgaben ✔")
st.subheader(f"📅 Heute ist {heute_deutsch} ({heute_str})")

col_ktw, col_rtw = st.columns(2)

with col_ktw:
    st.markdown("#### 🧾 Aufgaben KTW")
    for aufgabe in aufgaben_ktw.get(heute_deutsch, []):
        aufgabe_mit_feedback(aufgabe, heute_deutsch, status_dict, fahrzeug="KTW")

with col_rtw:
    st.markdown("#### 🚑 Aufgaben RTW")
    for aufgabe in aufgaben_rtw.get(heute_deutsch, []):
        aufgabe_mit_feedback(aufgabe, heute_deutsch, status_dict, fahrzeug="RTW")

# === Tagesinfo Boxen ===
st.markdown("---")
col1, col2, col3, col4 = st.columns(4)
col1.metric("🕒 Uhrzeit", get_current_time())
col2.metric("🎉 Feiertag", feiertag_heute if feiertag_heute else "Kein Feiertag")
col3.markdown("**⚠️ Sicherheits-Check**\n\nVor Fahrtbeginn durchführen!")
col4.markdown("**📌 Tipp**\n\nRegelmäßig Aufgaben prüfen!")

# === Spielbereich (nur wenn Banner geklickt) ===
st.markdown("---")
spiel_anzeigen = st.button("🧩 Zum Fehlerbild-Spiel der Woche")

if spiel_anzeigen:
    st.header("🎯 Fehlerbild-Spiel der Woche")

    if not os.path.exists(SPIELBILD_ORDNER):
        os.makedirs(SPIELBILD_ORDNER)

    bildpfad = os.path.join(SPIELBILD_ORDNER, SPIELBILD_NAME)

    if os.path.exists(bildpfad):
        st.image(bildpfad, caption="🔍 Finde den Fehler im Bild", use_column_width=True)

        if 'startzeit' not in st.session_state:
            if st.button("▶️ Starte Zeitmessung"):
                st.session_state['startzeit'] = time.time()
        else:
            if st.button("🏁 Fehler gefunden!"):
                dauer = time.time() - st.session_state['startzeit']
                name = st.text_input("Dein Name fürs Scoreboard:")
                if st.button("✅ Eintragen") and name:
                    eintrag = {"name": name, "zeit": round(dauer, 2)}
                    if os.path.exists(SCOREBOARD_DATEI):
                        with open(SCOREBOARD_DATEI, "r") as f:
                            daten = json.load(f)
                    else:
                        daten = []
                    daten.append(eintrag)
                    daten.sort(key=lambda x: x['zeit'])
                    with open(SCOREBOARD_DATEI, "w") as f:
                        json.dump(daten, f)
                    del st.session_state['startzeit']

        if os.path.exists(SCOREBOARD_DATEI):
            with open(SCOREBOARD_DATEI, "r") as f:
                daten = json.load(f)
                st.markdown("### 🏆 Scoreboard")
                for i, eintrag in enumerate(daten[:10], 1):
                    st.write(f"{i}. {eintrag['name']} – {eintrag['zeit']} Sekunden")
    else:
        st.info("Kein Bild für diese Woche hochgeladen.")

    if st.checkbox("🔒 Adminbereich anzeigen"):
        if check_admin():
            st.success("Zugang gewährt.")
            hochgeladen = st.file_uploader("🖼️ Neues Fehlerbild hochladen", type=["png", "jpg", "jpeg"])
            if hochgeladen:
                with open(bildpfad, "wb") as f:
                    f.write(hochgeladen.read())
                st.success("Neues Bild gespeichert!")
        else:
            st.error("Falsches Admin-Passwort.")
