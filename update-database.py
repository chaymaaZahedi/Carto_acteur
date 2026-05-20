import psycopg2

# ─── Connexion à la base de données Heroku ───────────────────────────────────
# DATABASE_URL = "postgresql://postgres.jaytoqzvceqtdqvcynoy:=E=QY]!{PjD53Mq@aws-0-REGION.pooler.supabase.com:5432/postgres"
DATABASE_URL = "postgresql://postgres.jaytoqzvceqtdqvcynoy:=E=QY]!{PjD53Mq@aws-0-eu-west-1.pooler.supabase.com:5432/postgres"

conn = psycopg2.connect(DATABASE_URL, sslmode="require")
cursor = conn.cursor()

# ─── Collez votre requête INSERT ici ─────────────────────────────────────────
sql = """
UPDATE institution 
SET acronyme_fr = 'BSR-AA'
WHERE id_institution = 'Inst74';
"""

# ─── Exécution ────────────────────────────────────────────────────────────────
try:
    cursor.execute(sql)
    conn.commit()
    print("✅ Insertion réussie !")
except Exception as e:
    conn.rollback()
    print(f"❌ Erreur : {e}")
finally:
    cursor.close()
    conn.close()
