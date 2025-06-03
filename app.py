import streamlit as st
import datetime

wochentag_saetze = {
    "Montag": "Heute ist die Faecherdesi dran!",
    "Dienstag": "Heute ist die BZ Kontrolle dran ✅",
    "Mittwoch": "Heute ist die Innen Desi dran",
    "Donnerstag": "Heute wird das Auto gewaschen",
    "Freitag": "Heute wird O2 Schlauch und Fingertipp gewechselt",
    "Samstag": "Heute findest du bestimmt noch was zu tun",
    "Sonntag": "Grillen, Chillen, Kasten Killen"
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
