import streamlit as st
import datetime

wochentag_saetze = {
    "Montag": "Heute ist die Fächerdesi dran! 1-6",
    "Dienstag": "Heute ist die BZ Kontrolle + Fächerdesi 7-11 dran",
    "Mittwoch": "Heute ist die Innenraumdesi dran",
    "Donnerstag": "Heute wird das Auto gewaschen und die Garage gereinigt",
    "Freitag": "Heute wird Fach 12-18 desinfiziert, Zusätzlich Betriebsmittelkontrolle und O2 Schlauch + Fingertipp gewechselt",
    "Samstag": "Heute wird Fach 20-22 desinfiziert",
    "Sonntag": "Heute wird die Küche gereinigt"
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

# Heute bestimmen
heute_en = datetime.datetime.now().strftime('%A')
heute_deutsch = tage_uebersetzung.get(heute_en, "Unbekannt")

st.title("Tagesaufgaben")

# Heutigen Satz anzeigen
st.subheader(f"Heute ist {heute_deutsch}:")
st.success(wochentag_saetze.get(heute_deutsch, "Kein Satz für heute definiert."))

# Anderen Tag auswählen
tag_auswahl = st.selectbox("Wähle einen anderen Wochentag:", list(wochentag_saetze.keys()))
st.write(f"📝 Aufgabe für {tag_auswahl}:")
st.info(wochentag_saetze[tag_auswahl])
