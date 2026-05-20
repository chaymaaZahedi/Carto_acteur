import psycopg2
import streamlit as st

#connection
def OpenConnection():
    return psycopg2.connect(
        host=st.secrets["postgres"]["host"],
        port=st.secrets["postgres"]["port"],
        user=st.secrets["postgres"]["user"],
        password=st.secrets["postgres"]["password"],
        dbname=st.secrets["postgres"]["dbname"],
        sslmode="require"
    )

#fetch


def fiche_institution(Nom_inst):
    conn = OpenConnection()
    c=conn.cursor()
    q1 = '''SELECT Nom_Institution,Acronyme_FR ,Acronyme_ENG,Date_creation,institution_mere,Nom_pays,libel_domaine,N.Type
            FROM institution I
			LEft join nature_juridique N on I.nature_juridique = N.idNature_juridique
			Left join pays P on I.id_pays = P.idPays
			left join domaine D on I.id_domaine = D.idDomaine
            WHERE Nom_Institution = %s
        '''
    c.execute(q1, (Nom_inst,))
    fiche_inst = c.fetchall()
    c.close()
    conn.close()
    return fiche_inst


def view_pays():
    conn = OpenConnection()
    c=conn.cursor()
    q='''   SELECT Nom_pays,Capitale,Libel_zone_geo
            FROM pays P,zone_geo Z
            WHERE Z.idZone_geo = P.ref_zone_geo
            ORDER BY Nom_pays'''
    c.execute(q)
    pays_data = c.fetchall()
    c.close()
    conn.close()
    return pays_data

def pays_institution(pays):
    conn = OpenConnection()
    c=conn.cursor()
    q1 = '''
            SELECT Nom_institution 
            FROM institution
            WHERE id_institution IN (
                SELECT Id_inst 
                FROM inst_pays
                WHERE idpays IN (
                    SELECT idpays 
                    FROM pays 
                    WHERE Nom_pays = %s
                )
            );
        '''
    c.execute(q1, (pays,))
    pays_inst = c.fetchall()
    c.close()
    conn.close()
    return pays_inst

def zone_institution(zone):
    conn = OpenConnection()
    c=conn.cursor()
    q1 = '''
            SELECT Nom_institution
            FROM institution
            WHERE id_institution IN (
                SELECT Id_inst 
                FROM inst_pays
                WHERE idpays IN (
                    SELECT idpays 
                    FROM pays 
                    WHERE ref_zone_geo IN (
                        SELECT idzone_geo 
                        FROM zone_geo
                        WHERE Libel_zone_geo = %s
                    )
                )
            );
        '''
    c.execute(q1, (zone,))
    zone_inst = c.fetchall()
    c.close()
    conn.close()
    return zone_inst

def view_article():
    conn = OpenConnection()
    c=conn.cursor()
    q='''   SELECT idArticle,Texte FROM article 
            Order BY idArticle;'''
    c.execute(q)
    article_data = c.fetchall()
    c.close()
    conn.close()
    return article_data

def view_domaine():
    conn = OpenConnection()
    c=conn.cursor()
    q='''   SELECT Libel_domaine FROM domaine;'''
    c.execute(q)
    domaine_data = c.fetchall()
    c.close()
    conn.close()
    return domaine_data

def domaine_institution(domaine):
    conn = OpenConnection()
    c=conn.cursor()
    q1 = '''SELECT Nom_institution
            FROM institution I
            WHERE I.id_domaine IN (SELECT Distinct(IdDomaine) FROM domaine WHERE libel_domaine = %s)
        '''
    c.execute(q1, (domaine,))
    domaine_inst = c.fetchall()
    c.close()
    conn.close()
    return domaine_inst

def view_all_data():
    conn = OpenConnection()
    c=conn.cursor()
    results = dict()
    col_results = dict()
    tables = ['domaine', 'type_compet', 'type_doc', 'zone_geo']
    for i in tables:
        # Retrieve column names
        q_col = "SELECT COLUMN_NAME FROM INFORMATION_SCHEMA.COLUMNS WHERE TABLE_NAME = \'" + str(i) + "\' AND COLUMN_KEY != 'PRI';"
        c.execute(q_col)
        res = c.fetchall()
        column_names = [str(column[0]) for column in res]

        # Construct the SELECT query with specific column names
        q = "SELECT " + ", ".join(column_names) + " FROM " + str(i)
        c.execute(q)
        r = c.fetchall()

        # Store the results and column names in dictionaries
        results[i] = r
        col_results[i] = column_names
    c.close()
    conn.close()
    return results, col_results


def institutions_parents():
    conn = OpenConnection()
    c=conn.cursor()
    q3= 'SELECT DISTINCT Nom_institution, institution_mere ,Libel_domaine, Acronyme_FR FROM institution I ,domaine D where institution_mere is not null and I.id_domaine = D.idDomaine;'
    c.execute(q3)
    inst=c.fetchall()
    c.close()
    conn.close()
    return inst

def institutions_parents_by_pays(pays):
    conn = OpenConnection()
    c = conn.cursor()
    q = '''
        SELECT DISTINCT I.Nom_institution, I.institution_mere, D.Libel_domaine, I.Acronyme_FR
        FROM institution I
        JOIN domaine D ON I.id_domaine = D.idDomaine
        JOIN inst_pays IP ON IP.id_inst = I.id_institution
        JOIN pays P ON IP.idPays = P.idPays
        WHERE I.institution_mere IS NOT NULL
        AND P.Nom_pays = %s;
    '''
    c.execute(q, (pays,))
    inst = c.fetchall()
    c.close()
    conn.close()
    return inst


def count_inst():
    conn = OpenConnection()
    c=conn.cursor()
    q1= 'select count(*) from institution'
    c.execute(q1)
    count_inst=c.fetchall()
    # q2= 'select count(*) from document'
    # c.execute(q2)
    # count_doc=c.fetchall()
    q3= 'select count(*) from article'
    c.execute(q3)
    count_art=c.fetchall()
    q4= 'select count(*) from Competence where type_compet= 2'
    c.execute(q4)
    count_inst_mer=c.fetchall()
    q5= 'select count(*) from Competence where type_compet= 1'
    c.execute(q5)
    count_inst_env=c.fetchall()
    c.close()
    conn.close()
    return count_inst, count_art, count_inst_mer, count_inst_env

def count_inst_compet(competence):
    conn = OpenConnection()
    c=conn.cursor()
    q1= 'select count(*) from Competence where type_compet= (select idType_compet from type_compet where type_compet = \''+competence+'\') '
    c.execute(q1)
    count_inst_compet=c.fetchall()
    c=conn.close()
    conn.close()
    return count_inst_compet


def aggregate_data():
    conn = OpenConnection()
    c=conn.cursor()
    q= 'SELECT Libel_domaine, count(Nom_Institution) as compte FROM institution I, domaine D where I.id_domaine = D.idDomaine group by Libel_domaine; '
    c.execute(q)
    inst_dom= c.fetchall()
    c.close()
    conn.close()
    return inst_dom

def aggregate_data_by_pays(pays):
    conn = OpenConnection()
    c = conn.cursor()
    q = '''
        SELECT D.Libel_domaine, COUNT(I.Nom_Institution) as compte
        FROM institution I
        JOIN domaine D ON I.id_domaine = D.idDomaine
        JOIN inst_pays IP ON IP.id_inst = I.id_institution
        JOIN pays P ON IP.idPays = P.idPays
        WHERE P.Nom_pays = %s
        GROUP BY D.Libel_domaine;
    '''
    c.execute(q, (pays,))
    inst_dom = c.fetchall()
    c.close()
    conn.close()
    return inst_dom

def aggregate_data_by_zone(zone):
    conn = OpenConnection()
    c=conn.cursor()
    q1= '''SELECT Libel_domaine, count(Nom_Institution) as compte  
    FROM institution I, domaine D , pays P, zone_geo Z, inst_pays IP
    where I.id_domaine = D.idDomaine 
    and IP.idPays = P.idPays 
    and P.ref_zone_geo = Z.idZone_geo
    and Z.idZone_geo in (select idZone_geo from zone_geo z1 where z1.Libel_zone_geo in '''+ str(zone) + ''')
    group by Libel_domaine; '''
    c.execute(q1)
    domaine_by_zone=c.fetchall()
    c.close()
    conn.close()
    return domaine_by_zone

def aggregate_data_by_zone1(zone):
    conn = OpenConnection()
    c=conn.cursor()
    q1= '''SELECT Libel_domaine, count(Nom_Institution) as compte  
    FROM institution I, domaine D , pays P, zone_geo Z, inst_pays IP
    where I.id_domaine = D.idDomaine 
    and IP.idPays = P.idPays 
    and P.ref_zone_geo = Z.idZone_geo
    and Z.idZone_geo = (select idZone_geo from zone_geo z1 where z1.Libel_zone_geo = '''+ str(zone) + ''')
    group by Libel_domaine; '''
    c.execute(q1)
    domaine_by_zone=c.fetchall()
    c.close()
    conn.close()
    return domaine_by_zone


def institution_by_year():
    conn = OpenConnection()
    c=conn.cursor()
    q= 'SELECT EXTRACT(YEAR FROM Date_creation) as Année, count(Nom_Institution) as compte  FROM institution  group by Année '
    c.execute(q)
    inst_year= c.fetchall()
    c.close()
    conn.close()
    return inst_year

def institution_by_year_by_pays(pays):
    conn = OpenConnection()
    c = conn.cursor()
    q = '''
        SELECT EXTRACT(YEAR FROM I.Date_creation) AS Annee, COUNT(I.Nom_Institution) AS compte
        FROM institution I
        JOIN inst_pays IP ON IP.id_inst = I.id_institution
        JOIN pays P ON IP.idPays = P.idPays
        WHERE P.Nom_pays = %s
        GROUP BY Annee
        ORDER BY Annee;
    '''
    c.execute(q, (pays,))
    inst_year = c.fetchall()
    c.close()
    conn.close()
    return inst_year

def cum_sum_inst():
    conn = OpenConnection()
    c=conn.cursor()
    q= '''with data as (
        select
            EXTRACT(YEAR FROM Date_creation) as year,
            count(id_Institution) as inst_count
        from institution
        group by year
        )
    
        select
        year,
        inst_count,
        sum(inst_count) over (order by year) as cumulative_sum
        from data;'''
        
    c.execute(q)
    cum_sum=c.fetchall()
    c.close()
    conn.close()
    return cum_sum

def cum_sum_inst_by_pays(pays):
    conn = OpenConnection()
    c = conn.cursor()
    q = '''
        WITH data AS (
            SELECT
                EXTRACT(YEAR FROM I.Date_creation) AS year,
                COUNT(I.id_institution) AS inst_count
            FROM institution I
            JOIN inst_pays IP ON IP.id_inst = I.id_institution
            JOIN pays P ON IP.idPays = P.idPays
            WHERE P.Nom_pays = %s
            GROUP BY year
        )
        SELECT
            year,
            inst_count,
            SUM(inst_count) OVER (ORDER BY year) AS cumulative_sum
        FROM data;
    '''
    c.execute(q, (pays,))
    cum_sum = c.fetchall()
    c.close()
    conn.close()
    return cum_sum

def count_inst_pays():
    conn = OpenConnection()
    c=conn.cursor()
    q= ''' SELECT I.Acronyme_FR, D.Libel_domaine , EXTRACT(YEAR FROM I.Date_creation) AS Annee, T.nbr_pays
            FROM institution AS I ,domaine AS D,(
                SELECT id_inst , COUNT(*) AS nbr_pays FROM inst_pays GROUP BY id_inst) AS T
            WHERE T.id_inst = I.id_Institution 
            AND I.id_domaine = D.idDomaine;  '''
    c.execute(q)
    count_inst=c.fetchall()
    c.close()
    conn.close()
    return count_inst

def document_by_year():
    conn = OpenConnection()
    c=conn.cursor()
    q = ''' SELECT  EXTRACT(YEAR FROM date_signature) as Date ,COUNT(*) AS nbr_doc 
            FROM document_derive WHERE date_signature IS NOT NULL
            GROUP BY date_signature 
            ORDER BY Date;'''
    c.execute(q)
    doc_year = c.fetchall()
    c.close()
    conn.close()
    return doc_year

def document_by_domaine():
    conn = OpenConnection()
    c=conn.cursor()
    q1 = ''' SELECT Libel_domaine , COUNT(*) as Compte
            FROM document_derive as doc , domaine as dm 
            WHERE doc.id_domaine = dm.idDomaine 
            AND doc.id_domaine IS NOT NULL
            GROUP BY Libel_domaine ;'''
    c.execute(q1)
    doc_domaine = c.fetchall()
    q2 = '''SELECT COUNT(*) as nbr_doc_domaine
            FROM document_derive as doc'''
    c.execute(q2)
    nbr_total_doc = c.fetchall()
    c.close()
    conn.close()
    return doc_domaine,nbr_total_doc

def select_institution():
    conn = OpenConnection()
    c=conn.cursor()
    q = ''' SELECT DISTINCT(Nom_Institution) FROM institution
            ORDER BY Nom_Institution
            '''
    c.execute(q)
    nom_inst = c.fetchall()
    c.close()
    conn.close()
    return nom_inst

def texte_institution(Nom_inst):
    conn = OpenConnection()
    c=conn.cursor()
    q1 = '''SELECT Nom_institution,Titre_document FROM institution I
            JOIN document_derive D on D.inst_adoptant = I.id_institution
            WHERE Nom_institution = %s
        '''
    c.execute(q1, (Nom_inst,))
    text_inst = c.fetchall()
    c.close()
    conn.close()
    return text_inst

def select_institution_docDerive():
    conn = OpenConnection()
    c=conn.cursor()
    q = ''' SELECT Distinct Nom_institution FROM institution I
            JOIN document_derive D on D.inst_adoptant = I.id_institution
            ORDER BY  Nom_institution
            '''
    c.execute(q)
    liste_inst = c.fetchall()
    c.close()
    conn.close()
    return liste_inst

def institution_siege():
    conn = OpenConnection()
    c=conn.cursor()
    q='select distinct(acronyme_fr), nom_pays, capitale from institution as i, pays as p where i.id_pays = p.idpays;'
    c.execute(q)
    inst_sie=c.fetchall()
    c.close()
    conn.close()
    return inst_sie

def institution_region():
    conn = OpenConnection()
    c=conn.cursor()
    q='''select id_inst, nom_pays, libel_zone_geo, libel_domaine from inst_pays as ip, pays as p, zone_geo as z, institution as i, domaine as d
        where p.ref_zone_geo = z.idzone_geo
        and ip.idpays = p.idpays
        and ip.id_inst = i.id_institution
        and i.id_domaine = d.iddomaine
        order by libel_zone_geo;'''
    c.execute(q)
    inst_reg=c.fetchall()
    c.close()
    conn.close()
    return inst_reg

def count_type_par_doc():
    conn = OpenConnection()
    c=conn.cursor()
    q='''(select T.type_doc,count(*) AS nbr_type
        FROM document_derive Dv , type_doc T
        WHERE Dv.type_doc = T.IdType_doc
        GROUP By T.type_doc)
        UNION (select T.type_doc,count(*) AS nbr_type
        FROM document_primaire Dp , type_doc T
        WHERE Dp.type_doc = T.IdType_doc
        GROUP By T.type_doc)
        '''
    c.execute(q)
    art_texte_type=c.fetchall()
    c.close()
    conn.close()
    return art_texte_type

def type_texte(type_document):
    conn = OpenConnection()
    c=conn.cursor()
    q='''(Select Titre_document FROM document_derive D
        WHERE D.type_doc IN (
        select idType_doc from type_doc
        WHERE type_doc = %s)
        AND Titre_document IS NOT NULL)
        UNION (Select Titre_document FROM document_primaire D
        WHERE D.type_doc IN (
        select idType_doc from type_doc
        WHERE type_doc = %s)
        AND Titre_document IS NOT NULL)
        '''
    c.execute(q ,(type_document,type_document))
    texte_type=c.fetchall()
    c.close()
    conn.close()
    return texte_type
