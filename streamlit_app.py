# Import python packages
import streamlit as st
import snowflake.connector

st.title(f":cup_with_straw: Customize Your Smoothie :cup_with_straw:")

# Connexion directe Snowflake
@st.cache_resource
def get_snowflake_conn():
    return snowflake.connector.connect(
        account= 'BJSNGCA-OAB95177',
            user= 'JMDOUAMPO',
            password= 'Meira29!122812',  # Remplace par ton vrai mot de passe
            role= 'SYSADMIN',
            database= 'SMOOTHIES',
            schema= 'PUBLIC',
            client_session_keep_alive = 'true'
    )

try:
    conn = get_snowflake_conn()
     
except Exception as e:
    st.error(f"❌ Erreur: {e}")

 # decrire l'activite
    name_on_sorder = st.text_input("Name on Smoothie", "")
    st.write("The name on Smoothies will be", name_on_sorder)


    #Affichage du DataFr
    my_dataframe = session.table("smoothies.public.fruit_options").select(col("fruit_name"))
    #st.dataframe(data=my_dataframe, use_container_width=True)
    
    ingredients_list =  st.multiselect(
        "Choose up to 5 ingredients",
        my_dataframe,
        max_selections =5
    )
#st.write(ingredients_list)
#st.text(ingredients_list)

    if ingredients_list:
        ingredients_string =''
        for fruit_chosen in ingredients_list:
            ingredients_string+=fruit_chosen + ' '
            
        #my_insert_stmt = """ insert into smoothies.public.orders (ingredients, name_on_order) values('"""+ingredients_string+"""','"""+name_on_sorder+"""')"""
        my_insert_stmt = f"""INSERT INTO smoothies.public.orders (ingredients, name_on_order)VALUES ('{ingredients_string}', '{name_on_sorder}')"""
        
        time_to_insert = st.button('Submet Order')
            
        if time_to_insert:
            conn.sql(my_insert_stmt).collect()
            st.success('Your Smoothie is ordered, '+ name_on_sorder, icon="✅")
        
#my_dataframe = session.table("smoothies.public.orders").filter(col("ORDER_FILLED")==0).collect()     
