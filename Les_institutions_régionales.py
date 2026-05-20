import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.figure_factory as ff
from query import *
import geopandas as gpd
from shapely.geometry import Polygon


st.set_page_config(page_title="Dashboard",page_icon="🌍",layout="wide",initial_sidebar_state='collapsed')
st.write('<div class="section" id="top"></div>', unsafe_allow_html=True)
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
def scroll_to_top():
    st.markdown(
        """
        <style>
            #scrollToTopBtn {
                position: fixed;
                bottom: 10px;
                right: 20px;
                background-color: #455B62;
                border: none;
                border-radius: 25px;
                padding: 12px 15px;
                cursor: pointer;
                color:white;
                z-index:9999;
            }
            #scrollToTopBtn:hover {
                background-color: #6C8D98;
                border: 1px solid #51707B;
                color:white;
                box-shadow: 2px 2px 2px 2px rgba(111, 111, 121, 1);
            }
        </style>
        <a href="#top">
            <div id= scrollToTopBtn>
                <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" fill="currentColor" class="bi bi-caret-up-square-fill" viewBox="0 0 16 16">
                    <path d="M0 2a2 2 0 0 1 2-2h12a2 2 0 0 1 2 2v12a2 2 0 0 1-2 2H2a2 2 0 0 1-2-2zm4 9h8a.5.5 0 0 0 .374-.832l-4-4.5a.5.5 0 0 0-.748 0l-4 4.5A.5.5 0 0 0 4 11"/>
                </svg>
            </div>
        </a>
        
        """,
        unsafe_allow_html=True
    )

st.markdown(subheader_style, unsafe_allow_html=True)
st.subheader("Cartographie des institutions régionales")
st.subheader("Intéressant l'environnement marin en Afrique de l'Ouest et du Centre")
st.markdown("""
    <style>
    /* Hide the link  */
    h3 a:first-child {
        display: none;
    }
    h5 a:first-child {
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

theme_plotly = None # None or streamlit

with open('style.css')as f:
    st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html = True)

domaine_color_map={'Economie': '#683c46', 'Environnement (Observation/science)': '#1F6D66',
                                'Environnement (Protection)': '#1F6D66', 'Pêche': '#7cc9d0',
                                'Transport et sécurité maritime': '#254d86',
                                'Mines': '#fad185', 'Energie': '#992b81', 'Communications': '#c87451',
                                'Agri-phytosanitaire et sécurité alimentaire': '#958a55',
                                'Justice': '#7f7f7f', 'Diplomatie': '#C592D5'}
table_name_mapping = {
    'Nature document': 'Nature_doc',
    'Type de compétence': 'Type_compet',
    'Type document': 'Type_doc',
    'Zone geographique': 'Zone_geo',
    'Domaine': 'Domaine'
}
def bordered_section(content,classdiv,border='2px',color='#363FFF'):
    st.markdown(
        f"""
        <style>
            .{classdiv} {{
                padding: 5px;
                margin-bottom: 15px;
                margin-top: -15px;
                border: {border} solid {color};
                border-radius: 10px;
                box-shadow: 4px 4px 8px 4px rgba(111, 111, 121, 1);
            }}
        </style>
        """,
        unsafe_allow_html=True
    )
    st.markdown(f'<div class="{classdiv}">{content}</div>', unsafe_allow_html=True)

def fiche_inst(instData):
    res = pd.DataFrame(fiche_institution(instData))
    inst_mere = str(res.iloc[:, 4][0])
    pays = str(res.iloc[:, 5][0])
    if inst_mere ==  "None" :
        inst_mere = '<span>---</span>'
    if pays ==  "None" :
        pays = 'Pays non Africain'
        
    content = '''
                <h5><center>Fiche de l'institution: <strong><span style="color: #2596be;">''' + str(res[0][0]) + '''</span></strong></center></h5>
                <strong>Acronyme français: </strong>''' + str(res[1][0]) + '''
                <br><strong>Acronyme anglais: </strong>''' + str(res[2][0]) + '''
                <br><strong>Date de création: </strong>''' + str(res[3][0]) + '''
                <br><strong>Nom de l'institution mère: </strong>''' + inst_mere + '''
                <br><strong>Pays: </strong>''' + pays + '''
                <br><strong>Domaine: </strong>''' + str(res[6][0]) + '''
                <br><strong>Nature juridique: </strong>''' + str(res[7][0]) + '''
            '''

    bordered_section(content,'inst_fiche',border='3px', color=domaine_color_map.get(str(res[7][0])))
# -----------------------------------------------------------------------------------------------------------------------------------------


content_text = '''Ce tableau de bord présente une cartographie des institutions régionales impliquées dans la conservation de l'environnement marin sur les côtes de l'Afrique Atlantique. Il couvre les pays d'Afrique de l'Ouest et du centre, et vise à faciliter l'identification des acteurs clés à contacter pour la planification spatiale marine dans cette région. Il permet d'identifier les institutions compétentes selon différents critères comme leur secteur d'activité, ou leur date de création.<br><br>Il utilise des couleurs identiques pour chaque secteur d'activité, afin de rendre la lecture plus aisée:'''

legend_text = '''<div style="margin-top: 15px;margin-bottom: 15px;border:1px solid darkgrey;padding: 10px; width: fit-content; margin-left: auto; margin-right: auto;border-radius: 8px;box-shadow: 1px 1px 4px 1px rgba(111, 111, 121, 1);">
                    <div style="display: inline-block; margin-right: 20px;">
                        <div style="width: 15px; height: 15px; background-color: #683c46; display: inline-block;margin-left: 5px;"></div>
                        <span style="margin-left: 5px;">Economie</span>
                    </div>
                    <div style="display: inline-block;">
                        <div style="width: 15px; height: 15px; background-color: #1F6D66; display: inline-block;margin-left: 5px;"></div>
                        <span style="margin-left: 5px;">Environnement</span>
                    </div>
                    <div style="display: inline-block; margin-right: 20px;">
                        <div style="width: 15px; height: 15px; background-color: #7cc9d0; display: inline-block;margin-left: 5px;"></div>
                        <span style="margin-left: 5px;">Pêche</span>
                    </div>
                    <div style="display: inline-block; margin-right: 20px;">
                        <div style="width: 15px; height: 15px; background-color: #254d86; display: inline-block;margin-left: 5px;"></div>
                        <span style="margin-left: 5px;">Transport et sécurité maritime</span>
                    </div>
                    <div style="display: inline-block; margin-right: 20px;">
                        <div style="width: 15px; height: 15px; background-color: #fad185; display: inline-block;margin-left: 5px;"></div>
                        <span style="margin-left: 5px;">Mines</span>
                    </div>
                    <div style="display: inline-block; margin-right: 20px;">
                        <div style="width: 15px; height: 15px; background-color: #992b81; display: inline-block;margin-left: 5px;"></div>
                        <span style="margin-left: 5px;">Energie</span>
                    </div>
                    <div style="display: inline-block; margin-right: 20px;">
                        <div style="width: 15px; height: 15px; background-color: #c87451; display: inline-block;margin-left: 5px;"></div>
                        <span style="margin-left: 5px;">Communications</span>
                    </div>
                    <div style="display: inline-block; margin-right: 20px;">
                        <div style="width: 15px; height: 15px; background-color: #958a55; display: inline-block;margin-left: 5px;"></div>
                        <span style="margin-left: 5px;">Agri-phytosanitaire et sécurité alimentaire</span>
                    </div>
                    <div style="display: inline-block; margin-right: 20px;">
                        <div style="width: 15px; height: 15px; background-color: #7f7f7f; display: inline-block;margin-left: 5px;"></div>
                        <span style="margin-left: 5px;">Justice</span>
                    </div>
                    <div style="display: inline-block; margin-right: 20px;">
                        <div style="width: 15px; height: 15px; background-color: #C592D5; display: inline-block;margin-left: 5px;"></div>
                        <span style="margin-left: 5px;">Diplomatie</span>
                    </div>
                </div>'''

content_text_suite = '''Il identifie également les textes de droit dérivé adoptés par les institutions ayant leur siège en Afrique.'''
st.markdown(f'<div class="text_content">{content_text + legend_text+content_text_suite}</div>', unsafe_allow_html=True)

st.markdown(
    """
    <style>
        .text_content {
            font-family: 'Times New Roman';
            font-size: 18px;
            text-align: justify;
            border-bottom: 2px solid #3F6B79;
            border-right: 2px solid #3F6B79;
            border-bottom-right-radius: 8px;
            box-shadow: 5px 5px 10px rgba(111, 111, 121, 1);
            padding: 10px;
            margin-bottom: 15px;
            margin-top: -15px;
        }
        .text_content:hover {
            border-color: #0038D5;
            cursor: pointer;
            user-select: none;
        }
    </style>
    """,
    unsafe_allow_html=True
)
st.markdown("""---""")
st.markdown('<span style="color: #01394C;font-size:25px;font-family:Times New Romans;"><br><b>🔎 Exploration des Données:</b></span>', unsafe_allow_html=True)
st.markdown('<div style="border-top: 1px solid #3F6B79;padding: 20px;margin-top:10px">', unsafe_allow_html=True)
col1, col2 = st.columns(2)
with col1:

    institution = pd.DataFrame(select_institution())
    st.info('Fiches des institutions ', icon="📌")
    with st.expander("Institution"):
        instData=st.selectbox('Choisissez une institution à afficher sa fiche: ',options=pd.DataFrame(select_institution(),dtype=str),index=None)
        if bool(instData) == True:
            fiche_inst(instData)
with col2:
    st.info('Institutions d\'intérêt pour une zone géographique', icon="📌")
    zoneGeo = pd.DataFrame(view_pays())
    with st.expander("Zone géographique"):
        zonGeoData=st.selectbox('Choisissez une zone géographique à afficher: ',options=zoneGeo[2].unique(),index=None)
        if bool(zonGeoData) == True:
            if zonGeoData in zoneGeo[2].unique():
                to_display= pd.DataFrame(zone_institution(zonGeoData), columns= ['Nom des institution'])
                st.markdown('<span style="color: #01394C;font-size:15px;font-family:Times New Romans;">*Veuillez sélectionner une seule institution à la fois !</span>', unsafe_allow_html=True)
            # selected = st.dataframe(to_display,use_container_width=True,hide_index=True)
            # string_Inst_zone = '<strong><span style="color: red;font-size:15px">,</span></strong>'.join(to_display['Nom des institution'].astype(str))
            # content ='''<strong>Nom des institutions : </strong><span style="color: #3F4243;font-size:16px">'''+string_Inst_zone +'''.</span><br><strong>Nombre total des institutions d\'intérêt pour la zone '''+str(zonGeoData) +''':</strong><span style="color: #2596be;font-size:18px">  ''' + str(len(to_display)) +'''</span>.'''
            # bordered_section(content,'zone_fiche')
            def dataframe_with_selections_Zone(df):
                df_with_selections = df.copy()
                df_with_selections.insert(0, "Select", False)
                chBox = st.column_config.CheckboxColumn(required=True,help="**Veuillez sélectionner une seule institution à la fois !**")
                # Get dataframe row-selections from user with st.data_editor
                edited_df = st.data_editor(
                    df_with_selections,
                    hide_index=True,
                    column_config={"Select": chBox},
                    disabled=df.columns,
                    width=900
                )
                if 'indiceZone' not in st.session_state:
                    st.session_state['indiceZone'] = []
                for i in range(len(edited_df)):
                    if str(edited_df.Select.iloc[i]) == "True" and i not in st.session_state['indiceZone']:
                        st.session_state['indiceZone'].append(i)
                    else:
                        if str(edited_df.Select.iloc[i]) == "False" and i in st.session_state['indiceZone']:
                            st.session_state['indiceZone'].remove(i)
                # Filter the dataframe using the temporary column, then drop the column
                for i in range(len(edited_df)):
                    edited_df.Select.iloc[i] = False
                if len(st.session_state['indiceZone']) > 0:
                    edited_df.Select.iloc[st.session_state['indiceZone'][len(st.session_state['indiceZone']) - 1]] = True
                selected_rows = edited_df[edited_df.Select]
                return selected_rows.drop('Select', axis=1)

            selection = dataframe_with_selections_Zone(to_display)

            if selection.shape[0] > 0 and selection.shape[1] > 0:
                st.markdown('<center><b><span style="color:#282158 ;font-size:23px;font-family:Times New Romans;">Fiche de l\'institution selectionnée<br></span></b></center>', unsafe_allow_html=True)
                fiche_inst(selection.iloc[0, 0])

with col1:  
    st.info('Répartition des institutions par domaine', icon="📌")
    domaine = pd.DataFrame(view_domaine())
    with st.expander("Domaine"):
        domData=st.selectbox('Choisissez un domaine à afficher: ',options=domaine[0].unique(),index=None)
        if bool(domData) == True:
            if domData in domaine[0].unique():
                to_display= pd.DataFrame(domaine_institution(domData), columns= ['Nom des institution'])
                st.markdown('<span style="color: #01394C;font-size:15px;font-family:Times New Romans;">*Veuillez sélectionner une seule institution à la fois !</span>', unsafe_allow_html=True)
            def dataframe_with_selections_Domaine(df):
                df_with_selections = df.copy()
                df_with_selections.insert(0, "Select", False)
                chBox = st.column_config.CheckboxColumn(required=True,help="**Veuillez sélectionner une seule institution à la fois !**")
                # Get dataframe row-selections from user with st.data_editor
                edited_df = st.data_editor(
                    df_with_selections,
                    hide_index=True,
                    column_config={"Select": chBox},
                    disabled=df.columns,
                    width=900
                )
                if 'indiceDom' not in st.session_state:
                    st.session_state['indiceDom'] = []
                for i in range(len(edited_df)):
                    if str(edited_df.Select.iloc[i]) == "True" and i not in st.session_state['indiceDom']:
                        st.session_state['indiceDom'].append(i)
                    else:
                        if str(edited_df.Select.iloc[i]) == "False" and i in st.session_state['indiceDom']:
                            st.session_state['indiceDom'].remove(i)
                # Filter the dataframe using the temporary column, then drop the column
                for i in range(len(edited_df)):
                    edited_df.Select.iloc[i] = False
                if len(st.session_state['indiceDom']) > 0:
                    edited_df.Select.iloc[st.session_state['indiceDom'][len(st.session_state['indiceDom']) - 1]] = True
                selected_rows = edited_df[edited_df.Select]
                return selected_rows.drop('Select', axis=1)

            selection = dataframe_with_selections_Domaine(to_display)

            if selection.shape[0] > 0 and selection.shape[1] > 0:
                st.markdown('<center><b><span style="color:#282158 ;font-size:23px;font-family:Times New Romans;">Fiche de l\'institution selectionnée<br></span></b></center>', unsafe_allow_html=True)
                fiche_inst(selection.iloc[0, 0])
            

with col2:
    st.info('Institutions d\'intérêt pour un pays', icon="📌")
    pays = pd.DataFrame(view_pays())
    with st.expander("Pays"):
        paysData=st.selectbox('Choisissez un pays à afficher: ',options=pays[0].unique(),index=None)
        if bool(paysData) == True:
            if paysData in pays[0].unique():
                to_display= pd.DataFrame(pays_institution(paysData), columns= ['Nom des institution'])
                st.markdown('<span style="color: #01394C;font-size:15px;font-family:Times New Romans;">*Veuillez sélectionner une seule institution à la fois !</span>', unsafe_allow_html=True)
            def dataframe_with_selections_Pays(df):
                df_with_selections = df.copy()
                df_with_selections.insert(0, "Select", False)
                chBox = st.column_config.CheckboxColumn(required=True,help="**Veuillez sélectionner une seule institution à la fois !**")
                # Get dataframe row-selections from user with st.data_editor
                edited_df = st.data_editor(
                    df_with_selections,
                    hide_index=True,
                    column_config={"Select": chBox},
                    disabled=df.columns,
                    width=900
                )
                if 'indicePays' not in st.session_state:
                    st.session_state['indicePays'] = []
                for i in range(len(edited_df)):
                    if str(edited_df.Select.iloc[i]) == "True" and i not in st.session_state['indicePays']:
                        st.session_state['indicePays'].append(i)
                    else:
                        if str(edited_df.Select.iloc[i]) == "False" and i in st.session_state['indicePays']:
                            st.session_state['indicePays'].remove(i)
                # Filter the dataframe using the temporary column, then drop the column
                for i in range(len(edited_df)):
                    edited_df.Select.iloc[i] = False
                if len(st.session_state['indicePays']) > 0:
                    edited_df.Select.iloc[st.session_state['indicePays'][len(st.session_state['indicePays']) - 1]] = True
                selected_rows = edited_df[edited_df.Select]
                return selected_rows.drop('Select', axis=1)

            selection = dataframe_with_selections_Pays(to_display)

            if selection.shape[0] > 0 and selection.shape[1] > 0:
                st.markdown('<center><b><span style="color:#282158 ;font-size:23px;font-family:Times New Romans;">Fiche de l\'institution selectionnée<br></span></b></center>', unsafe_allow_html=True)
                fiche_inst(selection.iloc[0, 0])


st.markdown('<div style="border-top: 1px solid #3F6B79;padding: 20px;margin-bottom:30px;margin-top:30px;">', unsafe_allow_html=True)
st.markdown("""---""")
Inst_count, count_art, count_inst_env,count_inst_mer = count_inst()
total1,total2,total3=st.columns(3,gap='large')

with total1:
    st.info('Institutions enregistrées',icon="📌")
    st.metric(label="Toutes les institutions", value= f'{Inst_count[0][0]}')
with total2:
    st.info('Institutions "Mer"',icon="📌")
    st.metric(label="Institutions compétentes pour la Mer", value= f'{count_inst_mer[0][0]}')
with total3:
    st.info('Institutions "Environnement"',icon="📌")
    st.metric(label="Institutions compétentes pour l'environnement", value= f'{count_inst_env[0][0]}')
st.markdown("""---""")


# --- Filtre pays commun pour les 3 graphiques ---
all_pays_global = pd.DataFrame(view_pays())
pays_options_global = ["Tous les pays"] + sorted(all_pays_global[0].unique().tolist())
filtre_pays_global = st.selectbox(
    "🌍 Filtrer par pays :",
    options=pays_options_global,
    index=0,
    key="filtre_pays_global"
)
pays_label = f'<span style="font-size:14px;color:#3F6B79;">({filtre_pays_global})</span>' if filtre_pays_global != "Tous les pays" else ""

left, right = st.columns((1,1))
######################## Left (Distribution by domaines) ##########################
with left:
    if filtre_pays_global == "Tous les pays":
        inst_dom = aggregate_data()
        title_pie = '<b>Répartition des Institutions par Domaine</b>'
    else:
        inst_dom = aggregate_data_by_pays(filtre_pays_global)
        title_pie = f'<b>Répartition des Institutions par Domaine<br>{pays_label}</b>'

    df_inst_dom = pd.DataFrame(inst_dom, columns=['Libel_domaine', 'Compte'])
    fig = px.pie(
        df_inst_dom,
        values='Compte',
        names='Libel_domaine',
        color='Libel_domaine',
        color_discrete_map=domaine_color_map
    )
    fig.update_layout({
        'title': {
            'text': title_pie,
            'x': 0.5,
            'xanchor': 'center',
            'yanchor': 'top',
            'font': {'size': 18},
        }
    })
    fig.update_layout(legend_title="Domaines")
    fig.update_layout(showlegend=False)
    fig.update_layout(margin=dict(l=5, r=5))
    fig.update_traces(textinfo='percent', textposition='inside')
    st.plotly_chart(fig, use_container_width=True, theme=theme_plotly)

######################## Right (Evolution of institutions) ##########################
with right:
    if filtre_pays_global == "Tous les pays":
        inst_year = pd.DataFrame(institution_by_year(), columns=['Annee', 'Compte'])
        title_bar = "<b> Nombre des institutions créées chaque Année </b>"
    else:
        inst_year = pd.DataFrame(institution_by_year_by_pays(filtre_pays_global), columns=['Annee', 'Compte'])
        title_bar = f"<b> Nombre des institutions créées chaque Année<br>{pays_label}</b>"

    fig_inst_annee = px.bar(inst_year, x="Annee", y="Compte", template="plotly_white")
    fig_inst_annee.update_layout({
        'title': {
            'text': title_bar,
            'x': 0.5,
            'xanchor': 'center',
            'yanchor': 'top',
            'font': {'size': 18},
        }
    })
    fig_inst_annee.update_layout(plot_bgcolor="rgba(0,0,0,0)", xaxis=(dict(showgrid=False)))
    st.plotly_chart(fig_inst_annee, use_container_width=True, theme=theme_plotly)

scroll_to_top()
######################## hiérarchie institutions ##########################

if filtre_pays_global == "Tous les pays":
    insti_parent = institutions_parents()
    title_tree = "<b> Hiérarchie entre institutions </b>"
else:
    insti_parent = institutions_parents_by_pays(filtre_pays_global)
    title_tree = f"<b> Hiérarchie entre institutions<br>{pays_label}</b>"

df_insti_parent = pd.DataFrame(insti_parent, columns=['institutions', 'parents', 'libel_domaine', 'Acronyme_FR'])

if df_insti_parent.empty:
    st.info(f"ℹ️ Aucune relation hiérarchique entre institutions trouvée pour **{filtre_pays_global}**.", icon="📭")
else:
    fig_tree = px.treemap(
        df_insti_parent,
        path=[px.Constant("Institutions", label='none'), 'parents', 'Acronyme_FR'],
        custom_data=['parents', 'institutions', 'libel_domaine'],
        color='libel_domaine',
        color_discrete_map=domaine_color_map
    )
    fig_tree.update_layout({
        'title': {
            'text': title_tree,
            'x': 0.5,
            'xanchor': 'center',
            'yanchor': 'top',
            'font': {'size': 18},
        }
    })
    customdata = fig_tree.data[0]['customdata']
    # Replace '(?)' with 'Other informations'
    customdata[:, 2][customdata[:, 2] == '(?)'] = '<span style="color: red;">Ce parent dispose de plusieurs domaines!!</span>'
    customdata[:, 1][customdata[:, 1] == '(?)'] = '<span style="color: red;">Ce parent dispose de plusieurs filles!!</span>'
    customdata[:, 0][customdata[:, 0] == '(?)'] = 'INSTITUTION'
    fig_tree.update_traces(root_color="lightgrey", hovertemplate='Institution mere: %{customdata[0]}<br>Institution fille: %{customdata[1]}<br>Domaine: %{customdata[2]}')
    fig_tree.update_layout(margin=dict(t=50, l=25, r=25, b=25), font=dict(size=16))
    st.plotly_chart(fig_tree, use_container_width=True)


############################ Line chart #########################################

cum_sum = pd.DataFrame(cum_sum_inst(), columns=['Annee', 'Nombre Institutions', 'Cumul'])
title_cumul = "<b>Evolution du nombre d'institutions par Année (CUMUL)</b>"


fig_cumul=px.line(
    cum_sum,
    x='Annee',
    y="Cumul",
    orientation="v",
    template="plotly_white",
)
fig_cumul.update_layout(
    xaxis=dict(tickmode="linear"),
    plot_bgcolor="rgba(0,0,0,0)",
    yaxis=(dict(showgrid=False)),
)
fig_cumul.update_layout({
        'title': {
            'text': title_cumul,
            'x': 0.5,
            'xanchor': 'center',
            'yanchor': 'top',
            'font': {'size': 18},
        }
    })
st.plotly_chart(fig_cumul,use_container_width=True)

left, right = st.columns((1,1))
############################### map siege ############################
# Liste pour ajouter une colonne des pays en français
correspondance_fr = {
    'South Africa': 'Afrique du Sud',
    'Algeria': 'Algérie',
    'Angola': 'Angola',
    'Benin': 'Bénin',
    'Botswana': 'Botswana',
    'Burkina Faso': 'Burkina Faso',
    'Burundi': 'Burundi',
    'Cameroon': 'Cameroun',
    'Cape Verde': 'Cap-Vert',
    'Comoros': 'Comores',
    'Côte d\'Ivoire': 'Côte d\'Ivoire',
    'Djibouti': 'Djibouti',
    'Egypt': 'Egypte',
    'Eritrea': 'Erythrée',
    'Ethiopia': 'Éthiopie',
    'Gabon': 'Gabon',
    'Gambia': 'Gambie',
    'Ghana': 'Ghana',
    'Guinea': 'Guinée',
    'Eq. Guinea': 'Guinée équatoriale',
    'Guinea-Bissau': 'Guinée-Bissau',
    'Kenya': 'Kenya',
    'Lesotho': 'Lesotho',
    'Liberia': 'Liberia',
    'Libya': 'Libye',
    'Madagascar': 'Madagascar',
    'Malawi': 'Malawi',
    'Mali': 'Mali',
    'Morocco': 'Maroc',
    'Mauritius': 'Maurice',
    'Mauritania': 'Mauritanie',
    'Mozambique': 'Mozambique',
    'Namibia': 'Namibie',
    'Niger': 'Niger',
    'Nigeria': 'Nigeria',
    'Uganda': 'Ouganda',
    'Central African Rep.': 'République centrafricaine',
    'Congo': 'République du Congo',
    'Dem. Rep. Congo': 'République démocratique du Congo',
    'Rwanda': 'Rwanda',
    'Sao Tome and Principe': 'Sao Tomé-et-Principe',
    'Senegal': 'Sénégal',
    'Seychelles': 'Seychelles',
    'Sierra Leone': 'Sierra Leone',
    'Somalia': 'Somalie',
    'Sudan': 'Soudan',
    'S. Sudan': 'Soudan du Sud',
    'eSwatini': 'Eswatini (ex-Swaziland)',
    'Tanzania': 'Tanzanie',
    'Chad': 'Tchad',
    'Togo': 'Togo',
    'Tunisia': 'Tunisie',
    'Zambia': 'Zambie',
    'Zimbabwe': 'Zimbabwe'
}

inst_sie = pd.DataFrame(institution_siege(), columns=['acronyme_fr', 'nom_pays', 'capitale'])
# Charger les données de tous les pays
world_data = gpd.read_file("data/ne_110m_admin_0_countries/ne_110m_admin_0_countries.shp")

# Choisir les pays d'afrique
africa_data = world_data[world_data['REGION_UN'] == 'Africa']
# Ajouter la colonne des pays en français
africa_data['pays'] = africa_data["NAME"].map(correspondance_fr)
# Concatener les données d'afrique et la sortie des requette sql
africa_data = pd.merge(africa_data, inst_sie[['nom_pays', 'acronyme_fr']], left_on='pays', right_on='nom_pays')
# Grouper les institutions dans une seule ligne
africa_data = africa_data.groupby(["NAME", 'pays', 'REGION_UN', "ISO_A3"])['acronyme_fr'].agg(lambda x: "".join("<br> &nbsp;&nbsp;&nbsp;&nbsp;" + x)).reset_index()
africa_data.columns = ['pays_en', 'Pays', 'REGION_UN', 'Acronyme du pays', 'Acronyme d\'nstitution']
fig_inst_sie = px.choropleth(
    africa_data,
    locations="Acronyme du pays",
    hover_name="Pays",
    scope="africa",
    height=600,
    hover_data={'Acronyme d\'nstitution': True, 'Acronyme du pays': False, 'Pays': False},
    color='Pays',
    color_discrete_map={
    'Afrique du Sud': '#1DE29D',
    'Algérie': '#d98d42',
    'Angola': '#6b3bb7',
    'Bénin': '#bb536b',
    'Botswana': '#629b42',
    'Burkina Faso': '#4D3B3B',
    'Burundi': '#4289b8',
    'Cameroun': '#c5b842',
    'Cap-Vert': '#9042b8',
    'Comores': '#b8a042',
    'Côte d\'Ivoire': '#D0EE16',
    'Djibouti': '#bb8b42',
    'Egypte': '#458245',
    'Erythrée': '#8e457e',
    'Éthiopie': '#8d8045',
    'Gabon': '#45a28e',
    'Gambie': '#7a458e',
    'Ghana': '#647D75',
    'Guinée': '#600B0B',
    'Guinée équatoriale': '#458e73',
    'Guinée-Bissau': '#9c8e45',
    'Kenya': '#E21D35',
    'Lesotho': '#458ea7',
    'Liberia': '#458eb2',
    'Libye': '#58458e',
    'Madagascar': '#45b68e',
    'Malawi': '#8e5945',
    'Mali': '#9e8e45',
    'Maroc': '#0D4319',
    'Maurice': '#6e458e',
    'Mauritanie': '#6e8e45',
    'Mozambique': '#458e8b',
    'Namibie': '#8e7045',
    'Niger': '#CD1DE2',
    'Nigeria': '#3C1DE2',
    'Ouganda': '#7e458e',
    'République centrafricaine': '#45928e',
    'République du Congo': '#BD898A',
    'République démocratique du Congo': '#457e8e',
    'Rwanda': '#458e59',
    'Sao Tomé-et-Principe': '#458e45',
    'Sénégal': '#8e454f',
    'Seychelles': '#454d8e',
    'Sierra Leone': '#45488e',
    'Somalie': '#6c8e45',
    'Soudan': '#458e85',
    'Soudan du Sud': '#688e45',
    'Eswatini (ex-Swaziland)': '#458e8e',
    'Tanzanie': '#46723C',
    'Tchad': '#C7249F',
    'Togo': '#0B084B',
    'Tunisie': '#45418e',
    'Zambie': '#458e7a',
    'Zimbabwe': '#8e4645'
}
)
title_text='<b>Les sièges des institutions</b>'
fig_inst_sie.update_layout(showlegend=True,)
fig_inst_sie.update_layout({
        'title': {
            'text': title_text,
            'x': 0.5,
            'xanchor': 'center',
            'yanchor': 'top',
            'font': {'size': 18},
        }
    })
left.plotly_chart(fig_inst_sie,use_container_width=True)

##################### institutions regionales #######################
inst_reg = pd.DataFrame(institution_region(), columns=['id_inst', 'nom_pays', 'libel_zone_geo', 'libel_domaine'])
# Charger les données de tous les pays
world_data = gpd.read_file("data/ne_110m_admin_0_countries/ne_110m_admin_0_countries.shp")
# st.write(list(world_data['ADMIN'].unique()))

# Créer les données du pays cap-vert
cape_verde_polygon = Polygon([(-25, 16), (-24, 16), (-24, 17), (-25, 17)])
cape_verde_data = {
    'pop_est': [587925], # 2021
    'REGION_UN': ['Africa'],
    "NAME": ['Cape Verde'],
    "ISO_A3": ['CPV'],
    'geometry': [cape_verde_polygon]
}
cape_verde_df = gpd.GeoDataFrame(cape_verde_data, geometry='geometry', crs=world_data.crs)
cape_verde_df['REGION_UN'] = 'Africa'
cape_verde_df["NAME"] = 'Cape Verde'
world_data = pd.concat([world_data, cape_verde_df], ignore_index=True)

# Créer les données du pays comoros
comoros_polygon = Polygon([(-44, -12), (-43, -12), (-43, -11), (-44, -11)])
comoros_data = {
    'pop_est': [821625], # 2021
    'REGION_UN': ['Africa'],
    "NAME": ['Comoros'],
    "ISO_A3": ['COM'],
    'geometry': [comoros_polygon]
}
comoros_df = gpd.GeoDataFrame(comoros_data, geometry='geometry', crs=world_data.crs)
world_data = pd.concat([world_data, comoros_df], ignore_index=True)

# Créer les données du pays Sao Tome and Principe
sao_tome_polygon = Polygon([(7, 0), (8, 0), (8, 1), (7, 1)])
sao_tome_data = {
    'pop_est': [223107], # 2021
    'REGION_UN': ['Africa'],
    "NAME": ['Sao Tome and Principe'],
    "ISO_A3": ['STP'],
    'geometry': [sao_tome_polygon]
}
sao_tome_df = gpd.GeoDataFrame(sao_tome_data, geometry='geometry', crs=world_data.crs)
world_data = pd.concat([world_data, sao_tome_df], ignore_index=True)

# Choisir les pays d'afrique
africa_data = world_data[world_data['REGION_UN'] == 'Africa']
# Ajouter la colonne des pays en français
africa_data['pays'] = africa_data["NAME"].map(correspondance_fr)
# Concatener les données d'afrique et la sortie des requette sql
africa_data = pd.merge(africa_data, inst_reg[['id_inst', 'nom_pays', 'libel_zone_geo', 'libel_domaine']], left_on='pays', right_on='nom_pays')
africa_data = africa_data[['REGION_UN', "NAME", "ISO_A3", 'id_inst', 'nom_pays', 'libel_zone_geo', 'libel_domaine']]
africa_data.columns = ['REGION_UN', 'pays_en', 'Acronyme du pays', 'id_inst', 'Pays', 'Zone géographique', 'Domaine']
# Calculer nombre d'institution par région
region_data = africa_data.groupby(['Zone géographique'])['id_inst'].count()
region_df = region_data.reset_index(name='Nombre d\'institutions')
# Trier le nombre d'institution et les stocker dans une liste
nbr_inst = region_df['Nombre d\'institutions'].to_list()
nbr_inst.sort()
# Créer une couleur pour chaque région suivant le nombre d'institution
color_scale = [
    (0, "#9FB5F4"), (nbr_inst[0]/nbr_inst[4], "#9FB5F4"),
    (nbr_inst[0]/nbr_inst[4], "#4940FA"), (nbr_inst[1]/nbr_inst[4], "#4940FA"),
    (nbr_inst[1]/nbr_inst[4], "#0F07C3"), (nbr_inst[2]/nbr_inst[4], "#0F07C3"),
    (nbr_inst[2]/nbr_inst[4], "#0A0660"), (nbr_inst[3]/nbr_inst[4], "#0A0660"),
    (nbr_inst[3]/nbr_inst[4], "#02002C"), (1, "#02002C")
]
# Concatener les données d'afrique et la sortie des requette sql
africa_data = pd.merge(africa_data, region_df, left_on='Zone géographique', right_on='Zone géographique')
# Grouper les domaines par région
zone_domaine_df = africa_data[['Zone géographique', 'Domaine']].drop_duplicates()
zone_domaine_df = zone_domaine_df.groupby(['Zone géographique'])['Domaine'].agg(lambda x: "".join("<br> &nbsp;&nbsp;&nbsp;&nbsp;" + x)).reset_index()
zone_domaine_df = zone_domaine_df.rename(columns={'Domaine': 'Domaines'})
africa_data = pd.merge(africa_data, zone_domaine_df, left_on='Zone géographique', right_on='Zone géographique')
# Ajouter cap-vert à sénégal
africa_data.loc[africa_data['pays_en'] == 'Senegal', 'Pays'] = 'Sénégal et Cap-Vert'
# Ajouter sao tomé et principe à gabon
africa_data.loc[africa_data['pays_en'] == 'Gabon', 'Pays'] = 'Gabon et Sao Tomé-et-Principe'
# Ajouter comores à madagascar
africa_data.loc[africa_data['pays_en'] == 'Madagascar', 'Pays'] = 'Madagascar et Comores'
fig_inst_reg = px.choropleth(
    africa_data,
    locations="Acronyme du pays",
    hover_name="Zone géographique",
    scope="africa",
    height=600,
    hover_data={'Pays': True, 'Nombre d\'institutions': True, 'Acronyme du pays': False, 'Zone géographique': False, 'Domaines': True},
    color='Nombre d\'institutions',
    color_continuous_scale=color_scale,
    animation_group='Zone géographique',
)
title='<b>Nombre des institutions régionales par régions africaines</b>'
fig_inst_reg.update_layout({
        'title': {
            'text': title,
            'x': 0.5,
            'xanchor': 'center',
            'yanchor': 'top',
            'font': {'size': 18},
        }
    })
right.plotly_chart(fig_inst_reg,use_container_width=True)


############################ Scatter chart #########################################
inst_pays= pd.DataFrame(count_inst_pays(), columns=['Acronyme', 'Domaine', 'Annee','nbr'])
fig_inst_pays=px.scatter(
    inst_pays,
    x='Annee',
    y="nbr",
    template="plotly_white",
    color='Domaine',
    color_discrete_map=domaine_color_map,
    text="Acronyme",
    height=600,
)
title="<b>Les institutions régionales en fonction de leur date de création et du nombre de pays concernés</b>"

fig_inst_pays.update_traces(marker_size=13,textposition='top center',hovertemplate='Annee:%{x}'+'<br> Nombre: %{y}')
fig_inst_pays.update_layout(
    xaxis_title="Années",
    yaxis_title="Nombre de pays concernés par l'institution",
    font=dict(size=13),
    showlegend=False,
)
fig_inst_pays.update_layout({
        'title': {
            'text': title,
            'x': 0.5,
            'xanchor': 'center',
            'yanchor': 'top',
            'font': {'size': 18},
        }
    })
st.plotly_chart(fig_inst_pays,use_container_width=True)


hide_st_style=""" 

    <style>
    #MainMenu {visibility:hidden;}
    footer {visibility:hidden;}
    header {visibility:hidden;}
    </style>
    """
