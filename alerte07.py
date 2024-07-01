import streamlit as st
import pandas as pd
import plotly.graph_objs as go
from PIL import Image
import os

# Les noms des projets
projets = {
    'LIGTHWELL': 'LIGTHWELL.csv',
    '40_LAFFITE': '40_LAFFITE.csv',
    'MDLF': 'MDLF.csv',
    'AXA_MAT': 'AXA_MAT.csv',
    'LEDGER': 'LEDGER.csv',
    'GOODLIFE': 'GOODLIFE.csv',
    'PECM': 'PECM.csv'
}

# Fonction pour afficher le logo
def afficher_logo():
    chemin_logo = os.path.join('logo1.jpeg')  # Remplacez par le chemin relatif vers votre logo
    try:
        logo = Image.open(chemin_logo)
        st.image(logo, width=250)
    except FileNotFoundError:
        st.error(f"Le fichier logo n'a pas été trouvé à l'emplacement : {chemin_logo}")

# Styles CSS personnalisés
styles = """
    <style>
        .header {
            background-color: #007BFF;
            color: white;
            font-weight: bold;
            text-align: center;
            padding: 10px;
            font-size: 24px;
            border-radius: 10px;
        }
        .subheader {
            font-size: 20px;
            font-weight: bold;
            margin-top: 20px;
        }
        .section {
            margin-top: 20px;
            margin-bottom: 20px;
        }
        .table-header {
            background-color: #f8f9fa;
            color: black;
            font-weight: bold;
            text-align: center;
            padding: 10px;
        }
        .lightgreen {
            background-color: lightgreen;
            color: black;
        }
        .yellow {
            background-color: yellow;
            color: black;
        }
        .red {
            background-color: red;
            color: white;
        }
        .orange {
            background-color: orange;
            color: black.
        }
    </style>
"""
st.markdown(styles, unsafe_allow_html=True)

# Fonction pour déterminer le niveau d'alerte en fonction du nombre d'indices
def determiner_niveau_alerte(compte):
    if compte < 3:
        return "Tout va bien"
    elif 3 <= compte <= 6:
        return "Attention ! Des indices à surveiller"
    else:
        return "Alerte !!! Trop d’indice à haut risque !!!"

# Fonction pour créer un graphique circulaire à partir des données
def create_pie_chart(data, column, title):
    labels = data[column].value_counts().index.tolist()
    values = data[column].value_counts().values.tolist()

    color_map = {
        "Tout va bien": "lightgreen",
        "Attention ! Des indices à surveiller": "yellow",
        "Alerte !!! Trop d’indice à haut risque !!!": "red",
        "Tout va bien !": "lightgreen",
        "Attention ! Des indices à surveiller !": "orange"
    }

    colors = [color_map[label] for label in labels]

    trace = go.Pie(labels=labels, values=values, hole=0.3,
                   marker=dict(colors=colors),
                   textinfo='percent',
                   insidetextorientation='horizontal')
    layout = go.Layout(
        title=title,
        margin=dict(l=20, r=20, t=30, b=20),
        legend=dict(orientation='h', xanchor='center', x=0.5, y=-0.1),
        annotations=[dict(text=title, x=0.5, y=0.5, font_size=20, showarrow=False)]
    )
    return go.Figure(data=[trace], layout=layout)

# Afficher le logo et l'entête
afficher_logo()
st.markdown("<div class='header'>Indicateur de Récapitulatif d'Alerte</div>", unsafe_allow_html=True)
st.markdown("""
    <div class='subheader'>Conception d’indicateurs préventifs</div>
    <p>Les indicateurs d’alerte sont basés sur deux critères principaux :</p>
    <h4>Alerte 1 : Nombre d’indices</h4>
    <ul>
        <li><span class='lightgreen'>Tout va bien (vert)</span> : Moins de 3 indices, indiquant que les documents sont sous contrôle avec peu de révisions nécessaires.</li>
        <li><span class='yellow'>Attention (jaune)</span> : Entre 3 et 6 indices, signalant que certains documents nécessitent une surveillance.</li>
        <li><span class='red'>Alerte (rouge)</span> : Plus de 6 indices, avertissant que trop de documents sont soumis à un nombre élevé de révisions, nécessitant une intervention immédiate.</li>
    </ul>
    <p>Un nombre élevé de révisions peut indiquer des modifications fréquentes, nécessitant une attention particulière.</p>
    <h4>Alerte 2 : Proportion des deux principaux indices</h4>
    <ul>
        <li><span class='lightgreen'>Tout va bien ! (vert)</span> : Les deux premiers indices les plus fréquents représentent 80% ou plus du total des indices, indiquant une bonne maîtrise des révisions.</li>
        <li><span class='orange'>Attention (orange)</span> : Signalant une dispersion des révisions et nécessitant une surveillance.</li>
    </ul>
    <p>Établir des indicateurs pour surveiller et prévenir les risques liés aux indices.</p>
    """, unsafe_allow_html=True)

# Disposition des filtres en ligne
st.markdown("<div class='subheader section'>Sélections</div>", unsafe_allow_html=True)
col1, col2 = st.columns([1, 1])
with col1:
    onglet = st.selectbox("Catégorie", ["Par LOT", "Par TYPE DE DOCUMENT"])
with col2:
    selected_file_path = st.selectbox("Projet", list(projets.keys()))

# Fonction pour charger les données depuis un fichier
def charger_donnees(chemin_fichier):
    spec_types = {
        'Date dépôt GED': str,
        'TYPE DE DOCUMENT': str,
        'PROJET': str,
        'EMET': str,
        'LOT': str,
        'INDICE': str,
        'Libellé du document': str
    }
    donnees = pd.read_csv(chemin_fichier, encoding='iso-8859-1', sep=';', dtype=spec_types, low_memory=False)
    donnees['Date dépôt GED'] = pd.to_datetime(donnees['Date dépôt GED'], format='%d/%m/%Y', errors='coerce')
    return donnees

# Charger les données du fichier sélectionné
df = charger_donnees(projets[selected_file_path])

# Calcul des indices et alertes
group_column = 'LOT' if onglet == "Par LOT" else 'TYPE DE DOCUMENT'
total_indices = df.groupby(group_column).size().rename(f"Total Indices par {group_column}")
indices_groupes = df.groupby([group_column, 'INDICE']).size().reset_index(name="Nombre de documents")
indices_groupes = indices_groupes.merge(total_indices, on=group_column)
indices_groupes['Proportion'] = (indices_groupes['Nombre de documents'] / indices_groupes[f"Total Indices par {group_column}"] * 100).round(2)

top_deux_indices = indices_groupes.sort_values(by=[group_column, 'Proportion'], ascending=[True, False]).groupby(group_column).head(2)
somme_proportions_top_deux = top_deux_indices.groupby(group_column)['Proportion'].sum().reset_index(name='Somme des deux principales proportions')
somme_proportions_top_deux['Somme des deux principales proportions'] = somme_proportions_top_deux['Somme des deux principales proportions'].round(0).astype(int).astype(str) + '%'

indices_uniques = df.groupby(group_column)['INDICE'].nunique().reset_index(name='Compteur Indice')
dernier_indice = df.sort_values(by=[group_column, 'INDICE'], ascending=[True, False]).drop_duplicates(subset=group_column, keep='first')[[group_column, 'INDICE']].rename(columns={'INDICE': 'Dernier Indice'})

donnees_finales = somme_proportions_top_deux.merge(indices_uniques, on=group_column)
donnees_finales = donnees_finales.merge(dernier_indice, on=group_column)
donnees_finales['Alerte 1 : nbre d\'indices'] = donnees_finales['Compteur Indice'].apply(determiner_niveau_alerte)
donnees_finales['Alerte 2: Frequence d\'indices'] = donnees_finales['Somme des deux principales proportions'].apply(lambda x: "Tout va bien !" if x[:-1].isdigit() and int(x[:-1]) >= 80 else "Attention ! Des indices à surveiller")

# Abréger ou faire un saut de ligne pour les longues chaînes
donnees_finales['Somme des deux principales proportions'] = donnees_finales['Somme des deux principales proportions'].apply(lambda x: x.replace(' ', '\n'))

colonnes_ordonnees = [group_column, 'Compteur Indice', 'Dernier Indice', 'Alerte 1 : nbre d\'indices', 'Somme des deux principales proportions', 'Alerte 2: Frequence d\'indices']
donnees_finales = donnees_finales[colonnes_ordonnees]

# Fonctions pour colorer les cellules en fonction des alertes
def color_alerte(val):
    if val == "Tout va bien":
        color = 'lightgreen'
    elif val == "Attention ! Des indices à surveiller":
        color = 'yellow'
    else:
        color = 'red'
    return f'background-color: {color}'

def color_alerte2(val):
    if val == "Tout va bien !":
        color = 'lightgreen'
    else:
        color = 'orange'
    return f'background-color: {color}'

# Recherche par lots et alertes
st.markdown("<div class='subheader section'>Recherche</div>", unsafe_allow_html=True)
col3, col4, col5 = st.columns([1, 1, 1])
with col3:
    search_value = st.selectbox(f"Rechercher par {group_column}...", ["Tous"] + list(donnees_finales[group_column].unique()))
with col4:
    search_value_alert = st.selectbox("Rechercher par Alerte 1...", ["Tous"] + list(donnees_finales['Alerte 1 : nbre d\'indices'].unique()))
with col5:
    search_value_alert2 = st.selectbox("Rechercher par Alerte 2...", ["Tous"] + list(donnees_finales['Alerte 2: Frequence d\'indices'].unique()))

# Filtrer les données en fonction de la recherche
df_filtered = donnees_finales.copy()
if search_value != "Tous":
    df_filtered = df_filtered[df_filtered[group_column] == search_value]
if search_value_alert != "Tous":
    df_filtered = df_filtered[df_filtered['Alerte 1 : nbre d\'indices'] == search_value_alert]
if search_value_alert2 != "Tous":
    df_filtered = df_filtered[df_filtered['Alerte 2: Frequence d\'indices'] == search_value_alert2]

# Afficher le tableau des données filtrées
def display_table(dataframe):
    styled_dataframe = dataframe.style.applymap(color_alerte, subset=['Alerte 1 : nbre d\'indices']).applymap(color_alerte2, subset=['Alerte 2: Frequence d\'indices'])
    st.dataframe(styled_dataframe, height=600)

    col6, col7 = st.columns(2)
    with col6:
        st.plotly_chart(create_pie_chart(dataframe, 'Alerte 1 : nbre d\'indices', 'Alerte 1'), use_container_width=True)
    with col7:
        st.plotly_chart(create_pie_chart(dataframe, 'Alerte 2: Frequence d\'indices', 'Alerte 2'), use_container_width=True)

display_table(df_filtered)
