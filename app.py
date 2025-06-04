import streamlit as st
import datetime
import pytz
import json
import os

# Datei zum Speichern der Checkbox-Zustände
STATUS_DATEI = "status.json"
STREAK_DATEI = "streak.json"  # Streak wird auch gespeichert

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

def lade_streak():
    """Lädt den aktuellen Streak aus der Datei."""
    if os.path.exists(STREAK_DATEI):
        with open(STREAK_DATEI, "r") as f:
            return json.load(f)
    return {"current_streak": 0, "last_date": ""}

def speichere_streak(streak_dict):
    """Speichert den Streak in der Datei."""
    with open(STREAK_DATEI, "w") as f:
        json.dump(streak_dict, f)

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

def berechne_streak(status_dict, heute_deutsch):
    """Berechnet den aktuellen Streak basierend auf dem Status und speichert ihn."""
    jahr, kalenderwoche, _ = datetime.datetime.now().isocalendar()

    # Überprüfen, ob alle Aufgaben abgehakt wurden
    alle_abgehakt = all(
        status_dict.get(f"{heute_deutsch}_{jahr}_{kalenderwoche}_{aufgabe}", False)
        for aufgabe in aufgaben_ktw.get(heute_deutsch, []) + aufgaben_rtw.get(heute_deutsch, [])
    )

    streak_dict = lade_streak()
    if alle_abgehakt:
        if streak_dict["last_date"] == heute_deutsch:  # Wenn der Streak am selben Tag wiederholt wird
            streak_dict["current_streak"] += 1
        else:  # Wenn der Streak neu gestartet wird
            streak_dict["current_streak"] = 1
        streak_dict["last_date"] = heute_deutsch
    else:
        streak_dict["current_streak"] = 0
        streak_dict["last_date"] = ""

    speichere_streak(streak_dict)
    return streak_dict["current_streak"]

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

# Streamlit Page Setup - MUST BE FIRST
st.set_page_config(page_title="RTW Aufgabenplan", page_icon="🚑", layout="wide")

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

# Berechne und zeige den Streak
current_streak = berechne_streak(status_dict, heute_deutsch)
st.markdown(f"### 📈 Dein Streak: {current_streak} Tage hintereinander alle Aufgaben abgehakt")

# Zusätzliche Tagesinfos: Uhrzeit, Sonnenaufgang, Sonnenuntergang, Feiertag
st.markdown("---")
col1, col2, col3, col4 = st.columns(4)
col1.metric("🕒 Uhrzeit", get_current_time())
col2.metric("🌅 Sonnenaufgang", sonnenaufgang)
col3.metric("🌇 Sonnenuntergang", sonnenuntergang)
col4.metric("🎉 Feiertag", feiertag_heute if feiertag_heute else "Kein Feiertag heute 😟")

# Wochentags-Auswahl
st.markdown("---")
tag_auswahl = st.selectbox("📌 Wähle einen anderen Wochentag zur Ansicht:", ["—"] + list(tage_uebersetzung.values()))

# Aufgaben für anderen Tag nur anzeigen, wenn sinnvoll gewählt
if tag_auswahl != "—":
    st.write(f"### Aufgaben für
