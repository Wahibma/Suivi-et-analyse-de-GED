import pandas as pd
import streamlit as st
import plotly.express as px

# crée les 

# Charger le fichier CSV combiné
fichier_sortie = 'GOODLIFE_régroupe1.csv'
df_combine = pd.read_csv(fichier_sortie, encoding='iso-8859-1', sep=';')

# Créer une application Streamlit avec un menu latéral
st.sidebar.title("Menu")

# Choix de l'application à afficher
app_mode = st.sidebar.selectbox(
    "Choisissez l'application :",
    ["Nombre d'indices par type de document", "Durée entre versions de documents par type de document"]
)

# Choix de l'option de représentation
option = st.sidebar.selectbox(
    "Choisissez le type de représentation :",
    ["Tableau", "Boxplot"]
)

if app_mode == "Nombre d'indices par type de document":
    st.title("Nombre d'indices par type de document")
    
    if option == "Tableau":
        # Calculer le nombre moyen d'indices par type de document
        moyenne_indices_par_type = df_combine.groupby('TYPE DE DOCUMENT')['Nombre d\'indices'].median().reset_index()
        moyenne_indices_par_type.columns = ['TYPE DE DOCUMENT', 'Nombre max d\'indices']
        
        # Afficher le tableau
        st.dataframe(round(moyenne_indices_par_type, 0))

    elif option == "Boxplot":
        # Créer le boxplot avec plotly.express
        fig = px.box(df_combine, x='desc_lot', y='Nombre d\'indices', 
                     title='Nombres d\'indices par Type de Document',
                     labels={'desc_lot': 'Type de Document', 'Nombre d\'indices': 'Nombre d\'indices'})
        st.plotly_chart(fig)

elif app_mode == "Durée entre versions de documents par type de document":
    st.title("Durée entre versions de documents par type de document")
    
    if option == "Tableau":
        # Calculer la durée moyenne entre les versions de documents par type
        duree_moyenne_versions_par_type = df_combine.groupby('TYPE DE DOCUMENT')['Différence en jours'].max().reset_index()
        duree_moyenne_versions_par_type.columns = ['TYPE DE DOCUMENT', 'Durée moyenne entre versions (jours)']
        
        # Afficher le tableau
        st.dataframe(round(duree_moyenne_versions_par_type, 2))

    elif option == "Boxplot":
        # Créer le boxplot avec plotly.express
        fig = px.box(df_combine, x='TYPE DE DOCUMENT', y='Différence en jours', 
                     title='Durée entre Versions par Type de Document',
                     labels={'Différence en jours': 'Durée entre Versions (jours)', 'TYPE DE DOCUMENT': 'Type de Document'})
        st.plotly_chart(fig)
