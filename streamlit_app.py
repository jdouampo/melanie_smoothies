import streamlit as st

st.title(f":cup_with_straw: Customize Your Smoothie :cup_with_straw:")
st.write("Choose the fruits you want in your custom Smoothie!")

# Gestion de la connexion Snowflake
@st.cache_resource
def init_connection():
    try:
        # Essayer d'abord la méthode Streamlit
        return st.connection("snowflake").session()
    except:
        st.error("""
        ⚠️ Configuration Snowflake manquante !
        
        Ajoutez dans votre fichier `.streamlit/config.toml` :
        ```toml
        [connections.snowflake]
        account = "BJSNGCA-OAB95177"
        user = "JMDOUAMPO"
        password = "votre_mot_de_passe"
        role = "SYSADMIN"
        warehouse = "COMPUTE_WH"
        database = "SMOOTHIES"
        schema = "PUBLIC"
        ```
        """)
        return None

session = init_connection()

if session:
    st.success("✅ Connexion Snowflake établie !")
    
    # Votre application continue ici
    name_on_order = st.text_input('Name on Smoothie:')
    st.write('The name on your Smoothie will be:', name_on_order)
    
    # Exemple d'utilisation de la session
    fruits_df = session.table("SMOOTHIES.PUBLIC.FRUITS").limit(5).collect()
    st.write("Quelques fruits disponibles:", fruits_df)
