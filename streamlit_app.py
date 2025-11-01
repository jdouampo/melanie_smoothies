# Import python packages
import streamlit as st
from snowflake.snowpark import Session
import requests
st.title(f":cup_with_straw: Customize Your Smoothie :cup_with_straw:")

# Configuration Snowflake
@st.cache_resource
def init_connection():
    return Session.builder.configs({
        "account": "BJSNGCA-OAB95177",
        "user": "JMDOUAMPO",
        "password": "Meira29!122812",
        "role": "SYSADMIN",
        "database": "SMOOTHIES",
        "schema": "PUBLIC"
    }).create()

try:
    session = init_connection()
    st.success("✅ Connected to Snowflake successfully!")
except Exception as e:
    st.error(f"❌ Error: {e}")

# Interface utilisateur
name_on_order = st.text_input("Name on Smoothie", "")
st.write("The name on Smoothie will be", name_on_order)

# Charger les fruits
try:
    #fruits_list = session.table("smoothies.public.fruit_options").select(col("fruit_name"),col("search_on"))
    fruits_list = session.table("smoothies.public.fruit_options").select("fruit_name", "search_on")
    pd_df = fruits_list.to_pandas()
    ingredients_list = st.multiselect(
        "Choose up to 5 ingredients",
        fruits_list,
        max_selections=5
    )
    if ingredients_list:
        ingredients_string = ''
        for fruit_chosen in ingredients_list:
            ingredients_string += fruit_chosen + ''
            
            search_on=pd_df.loc[pd_df['FRUIT_NAME'] == fruit_chosen, 'SEARCH_ON'].iloc[0]
            st.write('The search value for ', fruit_chosen,' is ', search_on, '.')

            st.subheader(fruit_chosen + " Nutrition information")
            smoothiefroot_response = requests.get("https://my.smoothiefroot.com/api/fruit/" + search_on)
            sf_df = st.dataframe(data=smoothiefroot_response.json(),use_container_width=True)
        
        # CORRECTION : URL correcte pour l'API
        #smoothiefroot_response = requests.get("https://my.smoothiefroot.com/api/fruit/" + fruit_chosen.lower())
        #if ingredients_list:
            #ingredients_string =''
           # for fruit_chosen in ingredients_list:
               # ingredients_string+=fruit_chosen + ' '
               # st.subheader(fruit_chosen+ " Nutrition information")
               # smoothiefroot_response = requests.get("https://my.smoothiefroot.com/api/fruit/watermelon"+fruit_chosen)
                #sf_df = st.dataframe(data=smoothiefroot_response.json(),use_container_width=True)
    #if ingredients_list and name_on_order:
       # ingredients_string = ' '.join(ingredients_list)
        #for fruit_chosen in ingredients_string:
            
        
        if st.button('Submit Order'):
            # Méthode avec SQL parameterisé (plus sécurisée)
            insert_sql = """
            INSERT INTO smoothies.public.orders (name_on_order, ingredients) 
            VALUES (:1, :2)
            """
            session.sql(insert_sql, params=[name_on_order, ingredients_string]).collect()
            
            st.success(f'Your Smoothie is ordered, {name_on_order}! ✅')
            

            smoothiefroot_response = requests.get("https://my.smoothiefroot.com/api/fruit/watermelon")
            #st.text(smoothiefroot_response.json())
            sf_df = st.dataframe(data=smoothiefroot_response.json(),use_container_width=True)


except Exception as e:
    st.error(f"Error: {e}")
