import streamlit as st
import datetime
import pytz
import json
import os

# Datei zum Speichern der Checkbox-Zustände und Notizen
STATUS_DATEI = "status.json"
NOTIZEN_DATEI = "notizen.json"

# Aufgabenlisten KTW und RTW
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

def lade_json_datei(datei_name):
    if os.path.exists(datei_name):
        with open(datei_name, "r") as f:
            return json.load(f)
    return {}

def speichere_json_datei(datei_name, data):
    with open(datei_name, "w") as f:
        json.dump(data, f)

def aufgabe_mit_feedback_und_notiz(aufgabe, wochentag, status_dict, notizen_dict):
    """Checkbox, Textfarbe, Linie & kleine Notiz speichern/anzeigen."""
    jahr, kalenderwoche, _ = datetime.datetime.now().isocalendar()
    key = f"{wochentag}_{jahr}_{kalenderwoche}_{aufgabe}"

    checked = status_dict.get(key, False)
    notiz = notizen_dict.get(key, "")

    col1, col2 = st.columns([0.1, 0.9])
    with col1:
        neu_gesetzt = st.checkbox("", value=checked, key=key)
    with col2:
        # Text mit Stil
        if neu_gesetzt:
            st.markdown(f"<span style='color:green; text-decoration: line-through;'>{aufgabe} ✅</span>", unsafe_allow_html=True)
        else:
            st.markdown(aufgabe)
        # Notizfeld
        neue_notiz = st.text_area("Notiz:", value=notiz, key=f"notiz_{key}", height=50)

    # Änderungen speichern
    if neu_gesetzt != checked:
        status_dict[key] = neu_gesetzt
        speichere_json_datei(STATUS_DATEI, status_dict)
        if neu_gesetzt:
            st.balloons()
    if neue_notiz != notiz:
        notizen_dict[key] = neue_notiz
        speichere_json_datei(NOTIZEN_DATEI, notizen_dict)

# -------------------- CHAT --------------------

# Chat-Nachrichten im Session State halten
if "chat_nachrichten" not in st.session_state:
    st.session_state.chat_nachrichten = []

if "chat_nickname" not in st.session_state:
    st.session_state.chat_nickname = None

if "chat_visible" not in st.session_state:
    st.session_state.chat_visible = False

def zeige_chat():
    st.markdown("## 💬 Team Chat")

    # Nickname setzen, wenn noch keiner
    if st.session_state.chat_nickname is None:
        nick = st.text_input("Gib deinen Nickname ein (frei erfunden):", key="nickname_input")
        if nick.strip() != "":
            st.session_state.chat_nickname = nick.strip()
            st.experimental_rerun()

    else:
        # Chat anzeigen
        for msg in st.session_state.chat_nachrichten:
            zeit = msg["zeit"]
            nick = msg["nick"]
            text = msg["text"]
            st.markdown(f"**[{zeit}] {nick}:** {text}")

        # Neue Nachricht
        neue_msg = st.text_input("Nachricht schreiben:", key="chat_input")

        if st.button("Senden"):
            if neue_msg.strip() != "":
                jetzt = datetime.datetime.now().strftime("%H:%M:%S")
                st.session_state.chat_nachrichten.append({
                    "zeit": jetzt,
                    "nick": st.session_state.chat_nickname,
                    "text": neue_msg.strip()
                })
                st.experimental_rerun()

# ----------------- Hauptseite -----------------

# Aktuelles Datum und Wochentag
heute_en = datetime.datetime.now().strftime('%A')
heute_deutsch = tage_uebersetzung.get(heute_en, "Unbekannt")
heute_str = datetime.datetime.now().strftime('%d.%m.%Y')
feiertag_heute = feiertage_2025.get(heute_str)

# Sonneninfos (optional statisch)
sonnenaufgang = "05:17"
sonnenuntergang = "21:43"

# Lade gespeicherten Status und Notizen
status_dict = lade_json_datei(STATUS_DATEI)
notizen_dict = lade_json_datei(NOTIZEN_DATEI)

st.set_page_config(page_title="RTW Aufgabenplan", page_icon="🚑", layout="wide")
st.title("✔ Rettungswache Südlohn Tagesaufgaben ✔")
st.subheader(f"📅 Heute ist {heute_deutsch} ({heute_str})")

st.markdown("## ✅ Aufgaben für heute")
col_ktw, col_rtw = st.columns(2)

with col_ktw:
    st.write("### 🚑 Aufgaben KTW")
    for aufgabe in aufgaben_ktw.get(heute_deutsch, []):
        aufgabe_mit_feedback_und_notiz(aufgabe, heute_deutsch, status_dict, notizen_dict)

with col_rtw:
    st.write("### 🚑 Aufgaben RTW")
    for aufgabe in aufgaben_rtw.get(heute_deutsch, []):
        aufgabe_mit_feedback_und_notiz(aufgabe, heute_deutsch, status_dict, notizen_dict)

st.markdown("---")
tag_auswahl = st.selectbox("📌 Wähle einen anderen Wochentag zur Ansicht:", ["—"] + list(tage_uebersetzung.values()))

if tag_auswahl != "—" and tag_auswahl != heute_deutsch:
    st.markdown(f"## 🔄 Aufgaben für {tag_auswahl}")
    col_ktw_alt, col_rtw_alt = st.columns(2)
    with col_ktw_alt:
        st.write("### 🚑 Aufgaben KTW")
        for aufgabe in aufgaben_ktw.get(tag_auswahl, []):
            aufgabe_mit_feedback_und_notiz(aufgabe, tag_auswahl, status_dict, notizen_dict)
    with col_rtw_alt:
        st.write("### 🚑 Aufgaben RTW")
        for aufgabe in aufgaben_rtw.get(tag_auswahl, []):
            aufgabe_mit_feedback_und_notiz(aufgabe, tag_auswahl, status_dict, notizen_dict)

# Chat Icon zum Ein-/Ausklappen
chat_col1, chat_col2, chat_col3, chat_col4, chat_col5 = st.columns([0.8,0.05,0.05,0.05,0.05])
with chat_col5:
    if st.button("💬"):
        st.session_state.chat_visible = not st.session_state.chat_visible

if st.session_state.chat_visible:
    zeige_chat()

# Zusatzinfos
st.markdown("---")
st.markdown("### 🌤️ Zusätzliche Tagesinfos")
col1, col2, col3, col4 = st.columns(4)
col1.metric("🕒 Uhrzeit", get_current_time())
col2.metric("🌅 Sonnenaufgang", sonnenaufgang)
col3.metric("🌇 Sonnenuntergang", sonnenuntergang)
col4.metric("🎉 Feiertag", feiertag_heute if feiertag_heute else "Kein Feiertag heute 😟")
