# Import python packages
import streamlit as st
import snowflake.connector
from snowflake.snowpark import Session

st.title(f":cup_with_straw: Customize Your Smoothie :cup_with_straw:")

# Connexion directe Snowflake
@st.cache_resource
def get_snowflake_conn():
    return snowflake.connector.connect(
        account='BJSNGCA-OAB95177',
        user='JMDOUAMPO',
        password='Meira29!122812',  # Remplace par ton vrai mot de passe
        role='SYSADMIN',
        database='SMOOTHIES',
        schema='PUBLIC',
        client_session_keep_alive='true'
    )

try:
    conn = get_snowflake_conn()
    # Create Snowpark session from connection
    session = Session.builder.configs({"connection": conn}).create()
    st.success("✅ Connected to Snowflake successfully!")
     
except Exception as e:
    st.error(f"❌ Erreur: {e}")

# decrire l'activite
name_on_sorder = st.text_input("Name on Smoothie", "")
st.write("The name on Smoothies will be", name_on_sorder)

# Affichage du DataFrame
try:
    my_dataframe = session.table("smoothies.public.fruit_options").select("fruit_name")
    #st.dataframe(data=my_dataframe, use_container_width=True)
    
    ingredients_list = st.multiselect(
        "Choose up to 5 ingredients",
        my_dataframe.to_pandas()['FRUIT_NAME'].tolist(),
        max_selections=5
    )

    #st.write(ingredients_list)
    #st.text(ingredients_list)

    if ingredients_list:
        ingredients_string = ''
        for fruit_chosen in ingredients_list:
            ingredients_string += fruit_chosen + ' '
            
        # Using parameterized query to prevent SQL injection
        my_insert_stmt = """INSERT INTO smoothies.public.orders (ingredients, name_on_sorder) 
                            VALUES (%s, %s)"""
        
        time_to_insert = st.button('Submit Order')
            
        if time_to_insert:
            # Execute with parameters
            cursor = conn.cursor()
            cursor.execute(my_insert_stmt, (ingredients_string.strip(), name_on_sorder))
            cursor.close()
            
            st.success('Your Smoothie is ordered, '+ name_on_sorder, icon="✅")

except Exception as e:
    st.error(f"Error loading fruits: {e}")

# Optional: Display recent orders
if st.checkbox("Show recent orders"):
    try:
        recent_orders = session.sql("SELECT * FROM smoothies.public.orders ORDER BY ordered_at DESC LIMIT 10").collect()
        if recent_orders:
            st.write("Recent Orders:")
            for order in recent_orders:
                st.write(f"- {order['NAME_ON_ORDER']}: {order['INGREDIENTS']}")
        else:
            st.write("No orders found.")
    except Exception as e:
        st.error(f"Error loading orders: {e}")
