# Import python packages
import streamlit as st
import snowflake.connector

st.title(f":cup_with_straw: Customize Your Smoothie :cup_with_straw:")
st.write("Choose the fruits you want in your custom Smoothie!")

# Connexion directe Snowflake
@st.cache_resource
def get_snowflake_conn():
    return snowflake.connector.connect(
        account: 'BJSNGCA-OAB95177',
            user: 'JMDOUAMPO',
            password: 'Meira29!122812',  # Remplace par ton vrai mot de passe
            role: 'SYSADMIN',
            database: 'SMOOTHIES',
            schema: 'PUBLIC',
            client_session_keep_alive : 'true'
    )

try:
    conn = get_snowflake_conn()
    cursor = conn.cursor()
    st.success("✅ Connexion Snowflake établie !")
    
    # Test de connexion
    cursor.execute("SELECT CURRENT_DATABASE(), CURRENT_SCHEMA()")
    db, schema = cursor.fetchone()
    st.write(f"📊 Base de données: {db}, Schéma: {schema}")
    
    # Votre application...
    name_on_order = st.text_input('Name on Smoothie:')
    st.write('The name on your Smoothie will be:', name_on_order)
    
    # Exemple: Lister les tables
    cursor.execute("SHOW TABLES IN SMOOTHIES.PUBLIC")
    tables = cursor.fetchall()
    st.write("📋 Tables disponibles:")
    for table in tables:
        st.write(f"- {table[1]}")
        
    cursor.close()
    
except Exception as e:
    st.error(f"❌ Erreur: {e}")
    st.info("""
    **Vérifie:**
    1. Ton mot de passe Snowflake
    2. Que le warehouse 'COMPUTE_WH' existe
    3. Que ton compte est actif
    """)
