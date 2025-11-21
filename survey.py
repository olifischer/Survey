import json
import glob
import os
import pandas as pd
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import textwrap

def wrap_labels(labels, width=30):
    """Fügt <br> ein, um Text umzubrechen."""
    wrapped_labels = []
    for label in labels:
        wrapped = "<br>".join(textwrap.wrap(label, width=width))
        wrapped_labels.append(wrapped)
    return wrapped_labels

def create_fixed_dashboard():
    # --- 1. DATEN LADEN ---
    folder_path = 'output'
    if not os.path.exists(folder_path):
        print(f"Fehler: Ordner '{folder_path}' fehlt.")
        return

    files = glob.glob(os.path.join(folder_path, '*.json'))
    data_list = []

    for file_path in files:
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = json.load(f)
                answers = content.get('answers', {})
                row = {
                    'Event': content.get('eventName', 'Unbekannt'),
                    'Bereich': answers.get('In welchem Hospitality-Bereich waren Sie zu Gast?', {}).get('selected', 'N/A'),
                    'Ticket_Source': answers.get('Wie sind Sie an Ihr VIP-Ticket gekommen?', {}).get('selected', 'N/A'),
                    'Empfehlung': answers.get('Würden Sie den VIP-Hospitality-Bereich des VfB Stuttgart weiterempfehlen?', 'N/A')
                }
                ratings = answers.get('Wie bewerten Sie...', {})
                for key, value in ratings.items():
                    clean_key = key.replace("... ", "")
                    row[clean_key] = value
                data_list.append(row)
        except Exception:
            continue

    if not data_list:
        print("Keine Daten gefunden.")
        return

    df = pd.DataFrame(data_list)

    # --- 2. LAYOUT ANPASSUNG (HIER IST DER FIX) ---
    
    # WICHTIG: horizontal_spacing drastisch erhöht (von 0.15 auf 0.45)
    # Das gibt dem Text in der Mitte viel mehr Platz.
    fig = make_subplots(
        rows=2, cols=2,
        subplot_titles=(
            "Durchschnittliche Bewertung", 
            "Ticket-Herkunft", 
            "Qualitäts-Matrix (Heatmap)", 
            "Weiterempfehlungsrate"
        ),
        specs=[[{"type": "bar"}, {"type": "bar"}],
               [{"type": "heatmap"}, {"type": "bar"}]],
        vertical_spacing=0.25,   # Platz zwischen oben und unten
        horizontal_spacing=0.45  # <--- HIER: Viel mehr Platz zwischen links und rechts
    )

    # A. Durchschnittsbewertungen (Oben Links)
    rating_cols = [col for col in df.columns if col not in ['Event', 'Bereich', 'Ticket_Source', 'Empfehlung']]
    if rating_cols:
        mean_scores = df[rating_cols].mean().sort_values(ascending=True)
        colors = ['#d62728' if x < 3.0 else '#2ca02c' for x in mean_scores.values]
        
        wrapped_y_labels = wrap_labels(mean_scores.index, width=35)

        fig.add_trace(
            go.Bar(
                y=wrapped_y_labels,
                x=mean_scores.values, 
                orientation='h',
                marker_color=colors,
                text=[f"{val:.2f}" for val in mean_scores.values],
                textposition='auto',
                hovertext=mean_scores.index,
                name="Bewertung"
            ),
            row=1, col=1
        )

    # B. Ticket Herkunft (Oben Rechts) - DER PROBLEM-BEREICH
    source_counts = df['Ticket_Source'].value_counts().head(10)
    
    # Wir brechen den Text etwas früher um (width=25), damit er nicht so breit wird
    formatted_labels = wrap_labels(source_counts.index, width=25)

    fig.add_trace(
        go.Bar(
            x=source_counts.values,
            y=formatted_labels,
            orientation='h',
            marker_color='#1f77b4',
            text=source_counts.values,
            textposition='auto',
            hovertext=source_counts.index, 
            name="Anzahl"
        ),
        row=1, col=2
    )

    # C. Heatmap (Unten Links)
    if rating_cols:
        heatmap_data = df.groupby('Bereich')[rating_cols].mean().T
        y_heatmap_labels = wrap_labels(heatmap_data.index, width=30)
        x_heatmap_labels = wrap_labels(heatmap_data.columns, width=15)

        fig.add_trace(
            go.Heatmap(
                z=heatmap_data.values,
                x=x_heatmap_labels,
                y=y_heatmap_labels,
                colorscale='RdYlGn', 
                zmin=1, zmax=5,
                text=[[f"{val:.1f}" for val in row] for row in heatmap_data.values],
                texttemplate="%{text}",
                name="Matrix"
            ),
            row=2, col=1
        )

    # D. Weiterempfehlung (Unten Rechts)
    rec_counts = df['Empfehlung'].value_counts()
    order = ['Ja', 'Eher ja', 'Eher nein', 'Nein']
    rec_counts = rec_counts.reindex([x for x in order if x in rec_counts.index]).fillna(0)

    fig.add_trace(
        go.Bar(
            x=rec_counts.index,
            y=rec_counts.values,
            marker_color=['#2ca02c', '#98df8a', '#ff9896', '#d62728'],
            text=rec_counts.values,
            textposition='auto',
            name="Empfehlung"
        ),
        row=2, col=2
    )

    # --- 3. GLOBALE EINSTELLUNGEN ---
    fig.update_layout(
        title_text=f"<b>Hospitality Dashboard</b> | Teilnehmer: {len(df)}",
        height=1100, # Etwas höher, damit vertikal mehr Luft ist
        autosize=True,
        showlegend=False,
        template="plotly_white",
        margin=dict(l=10, r=10, t=100, b=50), 
    )

    # WICHTIG: Schriftgröße der Achsen verkleinern (tickfont size)
    # Damit wirken die langen Texte nicht so wuchtig
    fig.update_yaxes(automargin=True, tickfont=dict(size=10))
    fig.update_xaxes(automargin=True, tickfont=dict(size=10))

    output_filename = "Hospitality_Dashboard_Fixed.html"
    fig.write_html(output_filename, config={'responsive': True})
    
    print(f"Erfolg! Optimiertes Dashboard erstellt: {output_filename}")

if __name__ == "__main__":
    create_fixed_dashboard()