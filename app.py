import streamlit as st
import datetime
import pytz
import json
import os

# Streamlit Page Setup - MUST BE FIRST
st.set_page_config(page_title="RTW Aufgabenplan", page_icon="🚑", layout="wide")

# Datei zum Speichern der Checkbox-Zustände
STATUS_DATEI = "status.json"

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

def lade_status():
    """Lädt den gespeicherten Status aus JSON, oder gibt leeres Dict zurück."""
    if os.path.exists(STATUS_DATEI):
        with open(STATUS_DATEI, "r") as f:
            return json.load(f)
    return {}

def speichere_status(status_dict):
    """Speichert den Status in der JSON Datei."""
    with open(STATUS_DATEI, "w") as f:
        json.dump(status_dict, f)

def aufgabe_mit_feedback(aufgabe, wochentag, status_dict):
    """Zeigt Checkbox und speichert/liest den Status."""
    jahr, kalenderwoche, _ = datetime.datetime.now().isocalendar()
    key = f"{wochentag}_{jahr}_{kalenderwoche}_{aufgabe}"

    # Status vorher aus dict lesen
    checked = status_dict.get(key, False)

    # Checkbox anzeigen, mit dem geladenen Status als default
    neu_gesetzt = st.checkbox(f"{aufgabe}", value=checked, key=key)

    # Falls Status sich ändert, aktualisiere dict und speichere
    if neu_gesetzt != checked:
        status_dict[key] = neu_gesetzt
        speichere_status(status_dict)
        if neu_gesetzt:
            st.balloons()

    # Aufgabe als Text mit Style je nach Status
    if neu_gesetzt:
        st.markdown(f"<span style='color:green; text-decoration: line-through;'>{aufgabe} ✅</span>", unsafe_allow_html=True)
    else:
        st.markdown(aufgabe)

# Aktuelles Datum und Wochentag
heute_en = datetime.datetime.now().strftime('%A')
heute_deutsch = tage_uebersetzung.get(heute_en, "Unbekannt")
heute_str = datetime.datetime.now().strftime('%d.%m.%Y')
feiertag_heute = feiertage_2025.get(heute_str)

# Sonneninfos (optional statisch)
sonnenaufgang = "05:17"
sonnenuntergang = "21:43"

# Lade gespeicherten Status
status_dict = lade_status()

# Belohnungssystem: Streak und Level
jahr, kalenderwoche, _ = datetime.datetime.now().isocalendar()
heute_key_ktw_rtw = [f"{heute_deutsch}_{jahr}_{kalenderwoche}_{aufgabe}" for aufgabe in aufgaben_ktw.get(heute_deutsch, []) + aufgaben_rtw.get(heute_deutsch, [])]

# Überprüfen, ob alle Aufgaben für den heutigen Tag erledigt sind (alle Checkboxen sind angehakt)
streak = 0
level = 0
if all(status_dict.get(key, False) for key in heute_key_ktw_rtw):
    streak += 1
else:
    streak = 0

# Wenn 3 Tage in Folge alles erledigt wurden, Level erhöhen
if streak == 3:
    level += 1
    streak = 0  # Reset streak after level up

# Set Level based on streaks
if level <= 5:
    level_title = "Anfänger"
    level_color = "orange"
elif 5 < level <= 10:
    level_title = "Richtig angefangen"
    level_color = "orange"
elif 10 < level <= 15:
    level_title = "Routine"
    level_color = "green"
elif 15 < level <= 20:
    level_title = "Profi"
    level_color = "blue"
elif 20 < level <= 50:
    level_title = "Keine halben Sachen"
    level_color = "purple"
elif 50 < level <= 100:
    level_title = "Senior"
    level_color = "black"
else:
    level_title = "Perfektionist"
    level_color = "pink"

# Anzeigen des Levelbalkens
st.markdown(f"## 🎯 Dein aktueller Level: **{level}** - {level_title}")
st.markdown(f"<div style='height: 20px; background-color: {level_color}; width: {level}%'></div>", unsafe_allow_html=True)

# Streamlit Page Setup
st.title("✔ Rettungswache Südlohn Tagesaufgaben ✔", anchor="center")
st.subheader(f"📅 Heute ist {heute_deutsch} ({heute_str})")

# Aufgabenbereich für den aktuellen Tag
st.markdown("## ✅ Aufgaben für heute")
col_ktw, col_rtw = st.columns(2)

with col_ktw:
    st.write("### 🧾 Aufgaben KTW")
    for aufgabe in aufgaben_ktw.get(heute_deutsch, []):
        aufgabe_mit_feedback(aufgabe, heute_deutsch, status_dict)

with col_rtw:
    st.write("### 🚑 Aufgaben RTW")
    for aufgabe in aufgaben_rtw.get(heute_deutsch, []):
        aufgabe_mit_feedback(aufgabe, heute_deutsch, status_dict)

# Wochentags-Auswahl
st.markdown("---")
tag_auswahl = st.selectbox("📌 Wähle einen anderen Wochentag zur Ansicht:", ["—"] + list(tage_uebersetzung.values()))

# Aufgaben für anderen Tag nur anzeigen, wenn sinnvoll gewählt
if tag_auswahl != "—" and tag_auswahl != heute_deutsch:
    st.markdown(f"## 🔄 Aufgaben für {tag_auswahl}")
    col_ktw_alt, col_rtw_alt = st.columns(2)

    with col_ktw_alt:
        st.write("### 🧾 Aufgaben KTW")
        for aufgabe in aufgaben_ktw.get(tag_auswahl, []):
            aufgabe_mit_feedback(aufgabe, tag_auswahl, status_dict)

