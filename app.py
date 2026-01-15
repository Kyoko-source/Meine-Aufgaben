# ================== BERECHNUNG – MODULAR ==================
def berechne():
    meds = []

    # Hilfsfunktion für Dosisberechnung
    def dosis_info(name, dosis, hinweis="", erklaerung=""):
        meds.append({
            "med": name,
            "dosis": dosis,
            "hinweis": hinweis,
            "erklaerung": erklaerung
        })

    # ---------- ANAPHYLAXIE ----------
    def anaphylaxie(alter):
        if alter < 6:
            dosis_info(
                "Adrenalin",
                "0,15 mg i.m.",
                "Kinder <6 Jahre",
                "0,15 mg für Kinder unter 6 Jahren nach Leitlinie"
            )
        elif 6 <= alter < 12:
            dosis_info(
                "Adrenalin",
                "0,3 mg i.m.",
                "Kinder 6–12 Jahre",
                "0,3 mg für Kinder zwischen 6 und 12 Jahren"
            )
        else:
            dosis_info(
                "Adrenalin",
                "0,5 mg i.m.",
                "Patient ≥12 Jahre",
                "Standarddosis 0,5 mg für Erwachsene und Kinder ≥12 Jahre"
            )

    # ---------- ASTHMA/COPD ----------
    def asthma_copd(alter):
        if alter > 12:
            dosis_info("Salbutamol", "2,5 mg vernebelt", "Patient >12 J", "Standarddosis Salbutamol für Erwachsene")
            dosis_info("Ipratropiumbromid", "500 µg vernebelt", "Patient >12 J", "Standarddosis Ipratropiumbromid")
            dosis_info("Prednisolon", "100 mg i.v.", "", "Kortikosteroid zur Entzündungshemmung")
        elif 4 <= alter <= 12:
            dosis_info("Salbutamol", "1,25 mg vernebelt", "Kinder 4–12 J", "Halbdosis für Kinder 4–12 Jahre")
            dosis_info("Prednisolon", "100 mg rektal", "Kinder 4–12 J", "Prednisolon in rektaler Form für Kinder")
        else:
            dosis_info("Adrenalin", "2 mg + 2 ml NaCl vernebelt", "Kinder <4 J", "Notfall-Lösung für kleine Kinder")
            dosis_info("Prednisolon", "100 mg rektal", "Kinder <4 J", "Prednisolon rektal")

    # ---------- HYPOGLYKÄMIE ----------
    def hypoglykaemie():
        dosis_info(
            "Glukose",
            "bis 16 g i.v.",
            "Langsam i.v. / oral bei wachem Patienten",
            "Glukose zur schnellen Beseitigung der Hypoglykämie"
        )

    # ---------- KRAMPFANFALL ----------
    def krampfanfall(zugang, gewicht):
        if zugang == "Ja":
            mg = round(0.05 * gewicht, 2)
            dosis_info("Midazolam", f"{mg} mg i.v.", "0,05 mg/kg KG", f"{gewicht} kg * 0,05 mg/kg = {mg} mg")
        else:
            if gewicht <= 10:
                dosis_info("Midazolam", "2,5 mg (0,5 ml)", "", "Gewicht <=10 kg → feste Notfall-Dosis")
            elif gewicht <= 20:
                dosis_info("Midazolam", "5 mg (1 ml)", "", "Gewicht 11–20 kg → feste Notfall-Dosis")
            else:
                dosis_info("Midazolam", "10 mg (2 ml)", "", "Gewicht >20 kg → feste Notfall-Dosis")

    # ---------- SCHLAGANFALL ----------
    def schlaganfall(blutdruck):
        if blutdruck is not None:
            if blutdruck < 120:
                dosis_info("Jonosteril", "", "RR <120 mmHg", "Volumenersatz bei zu niedrigem Blutdruck")
            elif blutdruck > 220:
                dosis_info("Urapidil", "5–15 mg i.v.", "RR >220 mmHg", f"Ziel: RR unter 220 mmHg")

    # ---------- KARDIALES LUNGENÖDEM ----------
    def kardiales_lungenoedem(blutdruck):
        dosis_info("Furosemid", "20 mg i.v.", "", "Schleifendiuretikum zur Entlastung")
        if blutdruck and blutdruck > 120:
            dosis_info("Nitro", "0,4–0,8 mg sublingual", "RR >120 mmHg", "Sublinguale Nitro-Dosis bei hohem Blutdruck")

    # ---------- HYPERTENSIVER NOTFALL ----------
    def hypertensiver_notfall(blutdruck):
        if blutdruck:
            ziel = int(blutdruck * 0.8)
            dosis_info("Urapidil", "5–15 mg langsam i.v.", f"Ziel-Sys ≈ {ziel} mmHg", "Blutdruck langsam senken")

    # ---------- STARKER SCHMERZ / TRAUMA ----------
    def schmerz_trauma(gewicht, zusatz):
        if gewicht >= 30:
            dosis_paracetamol = 15*gewicht
            dosis_info("Paracetamol", f"{dosis_paracetamol:.0f} mg i.v.", "15 mg/kg", f"{gewicht} kg * 15 mg/kg = {dosis_paracetamol:.0f} mg")
            if zusatz == "Midazolam + Esketamin":
                dosis_info("Midazolam", "1 mg i.v.", "Gewicht >30 kg", "Sedierung")
                dosis_esket = 0.125*gewicht
                dosis_info("Esketamin", f"{dosis_esket:.2f} mg i.v.", "0,125 mg/kg", f"{gewicht} kg * 0,125 mg/kg = {dosis_esket:.2f} mg")
            else:
                dosis_einmal_mg = 0.05
                dosis_einmal_ug = dosis_einmal_mg*1000
                max_total_ug = 2*gewicht
                max_gaben = math.floor(max_total_ug/dosis_einmal_ug)
                dosis_info("Fentanyl", f"0,05 mg i.v. alle 4 min", f"Maximal {max_gaben} Gaben", "Schmerztherapie mit Fentanyl")

    # ---------- BRUSTSCHMERZ ACS ----------
    def brustschmerz_acs(atemfrequenz):
        dosis_info("ASS", "250 mg i.v.", "", "Akuttherapie ACS")
        dosis_info("Heparin", "5000 I.E. i.v.", "", "Gerinnungshemmung")
        if atemfrequenz is not None and atemfrequenz < 10:
            dosis_info("Morphin", "3 mg i.v.", "AF < 10/min", "Schmerztherapie bei niedriger AF")

    # ---------- ABDOMINALE SCHMERZEN / KOLIKEN ----------
    def abd_schmerz(gewicht, schmerzskala):
        if 3 <= schmerzskala <=5 and gewicht >= 30:
            dosis_paracetamol = 15*gewicht if gewicht <=50 else 1000
            dosis_info("Paracetamol", f"{dosis_paracetamol:.0f} mg i.v.", f"{'15 mg/kg' if gewicht<=50 else '1 g'}", "Leichte Schmerzen")
        if 6 <= schmerzskala <=10:
            dosis_butyl = 0.3*gewicht
            if dosis_butyl > 40: dosis_butyl = 40
            dosis_info("Butylscopolamin", f"{dosis_butyl:.2f} mg i.v.", "max. 40 mg", "Starke Kolik")
            if gewicht >= 30:
                dosis_einmal_mg = 0.05
                dosis_einmal_ug = dosis_einmal_mg*1000
                max_total_ug = 2*gewicht
                max_gaben = math.floor(max_total_ug/dosis_einmal_ug)
                dosis_info("Fentanyl", f"0,05 mg i.v.", f"Maximal {max_gaben} Gaben", "Starke Schmerzen")

    # ---------- ÜBELKEIT / ERBRECHEN ----------
    def uebelkeit_erbrechen(alter):
        if alter >= 60:
            dosis_info("Ondansetron", "4 mg i.v.", "Einmalig", "Antiemetikum bei älteren Patienten")
        else:
            dosis_info("Dimenhydrinat", "31 mg i.v.", "Zusätzlich 31 mg Infusion", "Antiemetikum bei jüngeren Patienten")

    # ---------- INSTABILE BRADYKARDIE ----------
    def instabile_brady(asystolie):
        if asystolie == "Ja":
            dosis_info("Adrenalin-Infusion", "1 mg in 500 ml Jonosteril", "1 Tropfen/Sekunde", "Gefahr einer Asystolie")
        else:
            dosis_info("Atropin", "0,5 mg i.v.", "Bis max. 3 mg", "Bradykardie ohne Asystolie")

    # ---------- BENZODIAZEPIN-INTOXIKATION ----------
    def benzo_intox():
        dosis_info("Flumazenil", "0,5 mg i.v.", "Langsam i.v.", "Antidot für Benzodiazepine")

    # ---------- OPIAT-INTOXIKATION ----------
    def opiat_intox():
        dosis_info("Naloxon", "0,4 mg i.v.", "Auf 10 ml aufziehen, langsam titrieren", "Antidot für Opiate")

    # ---------- LUNGENARTERIENEMBOLIE ----------
    def lungenembolie():
        dosis_info("Heparin", "5000 I.E. i.v.", "", "Antikoagulation bei Lungenembolie")

    # ================== AUFRUF DER FUNKTIONEN ==================
    if erkrankung == "Anaphylaxie": anaphylaxie(alter)
    elif erkrankung == "Asthma/COPD": asthma_copd(alter)
    elif erkrankung == "Hypoglykämie": hypoglykaemie()
    elif erkrankung == "Krampfanfall": krampfanfall(zugang, gewicht)
    elif erkrankung == "Schlaganfall": schlaganfall(blutdruck)
    elif erkrankung == "Kardiales Lungenödem": kardiales_lungenoedem(blutdruck)
    elif erkrankung == "Hypertensiver Notfall": hypertensiver_notfall(blutdruck)
    elif erkrankung == "Starke Schmerzen bei Trauma": schmerz_trauma(gewicht, st.session_state.get("mid_esket_fent", "Fentanyl"))
    elif erkrankung == "Brustschmerz ACS": brustschmerz_acs(atemfrequenz)
    elif erkrankung == "Abdominelle Schmerzen / Koliken": abd_schmerz(gewicht, schmerzskala)
    elif erkrankung == "Übelkeit / Erbrechen": uebelkeit_erbrechen(alter)
    elif erkrankung == "Instabile Bradykardie": instabile_brady(asystolie_gefahr)
    elif erkrankung == "Benzodiazepin-Intoxikation": benzo_intox()
    elif erkrankung == "Opiat-Intoxikation": opiat_intox()
    elif erkrankung == "Lungenarterienembolie": lungenembolie()

    return meds
