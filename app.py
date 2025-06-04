import streamlit as st
import datetime
import pytz
import json
import os

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

# Feiertage
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

# Funktionen zum Laden und Speichern von Status
def lade_status():
    if os.path.exists(STATUS_DATEI):
        with open(STATUS_DATEI, "r") as f:
            return json.load(f)
    return {}

def speichere_status(status_dict):
    with open(STATUS_DATEI, "w") as f:
        json.dump(status_dict, f)

# Aufgabe mit Feedback (Checkbox)
def aufgabe_mit_feedback(aufgabe, wochentag, status_dict):
    jahr, kalenderwoche, _ = datetime.datetime.now().isocalendar()
    key = f"{wochentag}_{jahr}_{kalenderwoche}_{aufgabe}"

    # Status vorher aus dict lesen
    checked = status_dict.get(key, False)

    # Checkbox anzeigen, mit dem geladenen Status als default
    neu_gesetzt = st.checkbox("", value=checked, key=key)

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

# Berechnung des Streaks (Tage hintereinander alle Aufgaben abgehakt)
def berechne_streak(status_dict):
    streak = 0
    # Start: den aktuellen Tag holen
    heute = datetime.datetime.now().strftime('%A')
    jahr, kalenderwoche, _ = datetime.datetime.now().isocalendar()

    # Wir gehen durch die letzten 7 Tage (einschließlich heute)
    for i in range(7):
        tag_vorher = (datetime.datetime.now() - datetime.timedelta(days=i)).strftime('%A')

        # Überprüfen, ob alle Aufgaben für diesen Tag abgehakt sind
        if all(status_dict.get(f"{tage_uebersetzung.get(tag_vorher)}_{jahr}_{kalenderwoche}_{aufgabe}", False) for aufgabe in aufgaben_ktw.get(tag_vorher, []) + aufgaben_rtw.get(tag_vorher, [])):
            streak += 1
        else:
            break  # Streak unterbrechen, wenn an einem Tag nicht alle Aufgaben erledigt wurden
    return streak

# Lade gespeicherten Status
status_dict = lade_status()

# Streamlit Page Setup
st.set_page_config(page_title="RTW Aufgabenplan", page_icon="🚑", layout="wide")
st.title("✔ Rettungswache Südlohn Tagesaufgaben ✔")
st.subheader(f"📅 Heute ist {tage_uebersetzung.get(datetime.datetime.now().strftime('%A'))} ({datetime.datetime.now().strftime('%d.%m.%Y')})")

# Aufgabenbereich für den aktuellen Tag
st.markdown("## ✅ Aufgaben für heute")
col_ktw, col_rtw = st.columns(2)

with col_ktw:
    st.write("### 🧾 Aufgaben KTW")
    for aufgabe in aufgaben_ktw.get(tage_uebersetzung.get(datetime.datetime.now().strftime('%A')), []):
        aufgabe_mit_feedback(aufgabe, tage_uebersetzung.get(datetime.datetime.now().strftime('%A')), status_dict)

with col_rtw:
    st.write("### 🚑 Aufgaben RTW")
    for aufgabe in aufgaben_rtw.get(tage_uebersetzung.get(datetime.datetime.now().strftime('%A')), []):
        aufgabe_mit_feedback(aufgabe, tage_uebersetzung.get(datetime.datetime.now().strftime('%A')), status_dict)

# Berechnung des Streaks
streak = berechne_streak(status_dict)

# Anzeige des Streaks
st.markdown(f"### 📊 Dein Streak: {streak} Tage hintereinander alle Aufgaben abgehakt! 🎉")
