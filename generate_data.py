import json
import random
import os

# Konfiguration
output_folder = 'output'
anzahl_dateien = 56

# Sicherstellen, dass der Ordner existiert
if not os.path.exists(output_folder):
    os.makedirs(output_folder)

# Die Optionen basierend auf Ihren Originaldateien
hospitality_options = [
    "Mercedes-Benz Business Center - Business Seat",
    "Mercedes-Benz Business Center - Loge",
    "Porsche Tunnel Club",
    "MECHATRONIK Württemberg Lounge - Business Seat",
    "MECHATRONIK Württemberg Lounge - Loge",
    "CLUB 1893"
]

ticket_options = [
    "Ich bin selbst VIP-Dauerkarteninhaber bzw. Unternehmens-Verantwortlicher",
    "Ich bin Mitarbeiter des Unternehmens",
    "Ich bin ein direkter Angehöriger (Familie/Freunde/Bekannte)",
    "Ich wurde als Geschäftspartner oder Kunde eingeladen",
    "Ich habe bei einem Gewinnspiel, Verlosung o.ä. teilgenommen",
    "Ich nutze Tageskarten (ohne Dauerkarten-Arrangement) als Ticketkäufer",
    "Ich nutze Tageskarten (ohne Dauerkarten-Arrangement) und wurde eingeladen",
    ""
]

rating_keys = [
    "... die An- und Abreise bzw. Parkmöglichkeiten?",
    "... den Einlassprozess (Abwicklung / Dauer)?",
    "... den Hostessen-Service?",
    "... das Catering (Qualität & Auswahl)?",
    "... das Servicepersonal des Caterers?",
    "... die Atmosphäre & das Entertainment?",
    "... die Aktionsbereiche (Partner-Promotions / Getränke-Bars / Candy-Bar / Piano Bar)?",
    "... das Ambiente des Lounge- und Tischbereichs?",
    "... die Möglichkeit des Knüpfens bzw. Pflegens geschäftlicher Kontakte?",
    "... insgesamt Ihr Spieltagserlebnis?"
]

recommendation_options = ["Ja", "Eher ja", "Eher nein", "Nein"]
specification_options = ["Lounge", "Flügel", "Rondell", "Loge", ""]

# Generator-Funktion
print(f"Erstelle {anzahl_dateien} simulierte Umfragen im Ordner '{output_folder}'...")

for i in range(1, anzahl_dateien + 1):
    # Zufällige Bewertungen generieren (Tendenz eher positiv 3-5, damit es realistisch wirkt)
    ratings = {}
    for key in rating_keys:
        # Gewichtet: Höhere Wahrscheinlichkeit für 3, 4, 5
        ratings[key] = float(random.choices([1, 2, 3, 4, 5], weights=[5, 10, 20, 40, 25])[0])

    # Datenstruktur zusammenbauen
    survey_data = {
        "kickoff": "2023-10-01T15:00:00Z",
        "eventName": "Test Event",
        "answers": {
            "In welchem Hospitality-Bereich waren Sie zu Gast?": {
                "options": hospitality_options,
                "selected": random.choice(hospitality_options)
            },
            "Wenn Sie mögen, können Sie hier Ihren Bereich genauer spezifizieren (Lounge / Flügel / Rondell / Loge):": random.choice(specification_options),
            "Wie sind Sie an Ihr VIP-Ticket gekommen?": {
                "options": ticket_options,
                "selected": random.choice(ticket_options)
            },
            "Wie bewerten Sie...": ratings,
            "Würden Sie den VIP-Hospitality-Bereich des VfB Stuttgart weiterempfehlen?": random.choices(recommendation_options, weights=[40, 30, 20, 10])[0],
            "Was hat Ihnen besonders gut gefallen oder wo sehen Sie Verbesserungsbedarf?": f"Simulierter Kommentar {i}",
            "Möchten Sie zukünftig Informationen zu Hospitality-Angeboten des VfB Stuttgart erhalten?": random.choice(["Ja, ich bin interessiert", "Nein"]),
            "Bitte tragen Sie für eine Kontaktaufnahme Ihre Daten ein [Name / Ggf. Unternehmen / E-Mail / Telefon]": f"User {i} / 555-01{i:02d}"
        }
    }

    # Dateiname definieren (z.B. Simulated_Umfrage_1.json)
    filename = os.path.join(output_folder, f'Simulated_Umfrage_{i}.json')
    
    # JSON schreiben
    with open(filename, 'w', encoding='utf-8') as f:
        json.dump(survey_data, f, ensure_ascii=False, indent=4)

print("Fertig! Die Daten wurden generiert.")