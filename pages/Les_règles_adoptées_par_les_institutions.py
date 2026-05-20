import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.figure_factory as ff
import numpy as np
from query import *

st.set_page_config(page_title="Dashboasrd",page_icon="🌍",layout="wide",initial_sidebar_state='collapsed')
subheader_style = """
    <style>
        h3 {
            color: darkblue;
            font-size: 45px;
            text-align: center;
            margin: 0;
        }
    </style>
"""

st.markdown(subheader_style, unsafe_allow_html=True)
st.subheader("Les règles adoptées par les institutions régionales africaines")
st.markdown("""
    <style>
    /* Hide the link  */
    h3 a:first-child {
        display: none;
    }
    
    </style>
    """, unsafe_allow_html=True)
st.markdown(
    """
    <style>
        #MainMenu {visibility: hidden;}
        footer {visibility: hidden;}
    </style>
    """,
    unsafe_allow_html=True
)
st.markdown("##")

theme_plotly = None # None or streamlit

# Style
with open('style.css')as f:
    st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html = True)

doc_dom,nbr_total_doc = document_by_domaine()
large_column, small_column = st.columns([2, 1])

with small_column:
    st.info('Nombre de documents ',icon="📌")
    st.metric(label="Documents identifiés avec Droit Dérivé", value= f'{nbr_total_doc[0][0]}')
with large_column:

    def bordered_section(content):
        st.markdown(
            """
            <style>
                .bordered {
                    padding: 5px;
                    margin-bottom: 15px;
                    margin-top: -15px;
                    border: 2px solid #363FFF;
                    border-radius: 10px;
                    box-shadow: 4px 4px 8px 4px rgba(111, 111, 121, 1);
                }
            </style>
            """,
            unsafe_allow_html=True
        )
        st.markdown(f'<div class="bordered">{content}</div>', unsafe_allow_html=True)
        
    
    st.info('Textes des institutions ', icon="📌")
    with st.expander("📁 Titres des documents adoptés par les institutions"):
        showData =st.selectbox('Choisissez une institution à afficher son titre de document: ',options=pd.DataFrame(select_institution_docDerive(),dtype=str),index=None)
        if bool(showData) == True:
            inst_doc= pd.DataFrame(texte_institution(showData),columns=['Nom institution','Titres des documrents derives'])
            titre = '<strong><span style="color: red;font-size:15px"><br></span></strong>'.join(inst_doc['Titres des documrents derives'].astype(str))
            # content = '''
            #             <strong>Titre du document: </strong><span style="color:#3F4243;font-size:16px">''' + titre + '''</span>
            #     '''
            newColumnName = "Titres des documents adoptés par: "+ inst_doc.iloc[0,0]
            nbr_doc = len(inst_doc)
            index_doc = []
            doc = 0
            for i in range(nbr_doc):
                doc = "Doc n`{}".format(i+1)
                index_doc.append(doc)
            inst_doc.insert(0,'',index_doc)
            inst_doc.drop(columns=["Nom institution"],inplace=True)
            inst_doc.rename(columns={"Titres des documrents derives": newColumnName},inplace=True)
            st.dataframe(inst_doc,hide_index=True,use_container_width=True)

left,right = st.columns((1,1))
############################ Bar chart #########################################

doc_year = pd.DataFrame(document_by_year(), columns=['Annee', 'Nombre de documents'])
title="<b>Evolution du nombre de documents adoptés  par Année</b>"
fig_doc_year = px.bar(
    doc_year,
    x='Annee',
    y="Nombre de documents",
    template="plotly_white",
    )
fig_doc_year.update_traces(marker_color = 'darkblue')
fig_doc_year.update_layout(plot_bgcolor="rgba(0,0,0,0)")
fig_doc_year.update_layout({
        'title': {
            'text': title,
            'x': 0.5,
            'xanchor': 'center',
            'yanchor': 'top',
            'font': {'size': 18},
        }
    })
right.plotly_chart(fig_doc_year,use_container_width=True)

########################Left (Distribution of documents by domaines) ##########################
df_doc_dom = pd.DataFrame(doc_dom, columns=['Nom du domaine','Nombre de documents'])
title = '<b>Répartition des Documents par Domaine</b>'
fig = px.pie(df_doc_dom,
            values='Nombre de documents',
            names= 'Nom du domaine' ,
            color='Nom du domaine',
            color_discrete_map={'Economie': '#683c46', 'Environnement (Observation/science)': '#1F6D66',
                                'Environnement (Protection)': '#1F6D66', 'Pêche': '#7cc9d0',
                                'Transport et sécurité maritime': '#254d86',
                                'Mines': '#fad185', 'Energie': '#992b81', 'Communications': '#c87451',
                                'Agri-phytosanitaire et sécurité alimentaire': '#958a55',
                                'Justice': '#7f7f7f', 'Diplomatie': '#C592D5'},
            )

fig.update_layout(margin=dict(l=5, r=5),showlegend=False)
fig.update_layout({
        'title': {
            'text': title,
            'x': 0.5,
            'xanchor': 'center',
            'yanchor': 'top',
            'font': {'size': 18},
        }
    })
fig.update_traces(textinfo='percent', textposition='inside')
left.plotly_chart(fig, use_container_width=True, theme=theme_plotly)


############################ Left Pie chart (Distribution of documents by type_doc) #########################################



piechart,listeTextes=st.columns(2,gap='large')
art_texte_type = pd.DataFrame(count_type_par_doc(), columns=['Type_doc' , 'Nombre d\'article ayant ce type'])
title = '<b>Répartition des Documents par Types</b>'
with piechart:
    fig_art_type = px.pie(
        art_texte_type,
        values='Nombre d\'article ayant ce type',
        names= 'Type_doc' ,
        color='Type_doc',
        custom_data='Type_doc',
        color_discrete_map={'Contraignant':'#870709','Non Contraignant':'#071287'}
    )
    
    fig_art_type.update_traces(hovertemplate='Types des documents:%{customdata[0]}'+'<br> Nombre de documents :%{value}',textinfo='percent', textposition='inside')
    fig_art_type.update_layout(
        margin=dict(l=5, r=5),
        plot_bgcolor="rgba(0,0,0,0)"
        )
    fig_art_type.update_layout({
        'title': {
            'text': title,
            'x': 0.5,
            'xanchor': 'center',
            'yanchor': 'top',
            'font': {'size': 18},
        }
    })
    st.plotly_chart(fig_art_type,use_container_width=True, theme=theme_plotly)
    
    
############################ Right Expander  #########################################

with listeTextes:
    st.info('Type des documents',icon="📌")
    with st.expander("📁 Titres des documents par types de leurs textes < Contraignants / Non Contraignants >"):
        choix=st.selectbox(
        "Choisissez un type ",
        options=["Contraignant","Non Contraignant"],
        index=None
        )
        if bool(choix) == True:
            to_display= pd.DataFrame(type_texte(choix),columns=['Titre des documents'])
            newColumnName = 'Textes des documents ayant type :'+ str(showData)
            to_display.rename(columns={'Texte': newColumnName}, inplace=True)
            st.dataframe(to_display, use_container_width=True,hide_index=True)
