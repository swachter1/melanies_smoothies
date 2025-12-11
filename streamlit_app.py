# Import python packages
import streamlit as st
import requests
from snowflake.snowpark.functions import col



# Write directly to the app
st.title(f":cup_with_straw: Customize your Smoothie:cup_with_straw: {st.__version__}")
st.write(
  "Choose the fruits you want in your custom smoothie."
)
    
#Name on Smoothie
name_on_smoothie = st.text_input("Name on Smoothie")

st.write("The name on your smoothie will be: ", name_on_smoothie)
#List of fruits from database
#Session style for SiS (Streamlit in Snowflake)
#session = get_active_session()

#Session style for SniS (Streamlit Not in Snowflake)
cnx = st.connection("snowflake")
session = cnx.session()

my_dataframe = session.table("smoothies.public.fruit_options").select(col('FRUIT_NAME'))
#st.dataframe(data=my_dataframe, use_container_width=True)

ingredients_list = st.multiselect("Choose up to 5 ingredients:", my_dataframe, max_selections=5)

#Ingredient List
if ingredients_list:

    ingredients_string=''
    for each_fruit in ingredients_list:
        ingredients_string += each_fruit + ' '

    #debug:
    #st.write(ingredients_string)

    my_insert_stmt = """ insert into smoothies.public.orders(INGREDIENTS, NAME_ON_ORDER)
            values ('""" + ingredients_string + """','""" + name_on_smoothie + """')"""

    #debug:
    #st.write(my_insert_stmt)
    #st.stop()

    time_to_insert = st.button("Submit order");
    
    if time_to_insert:
        session.sql(my_insert_stmt).collect()
        st.success('Your Smoothie is ordered, ' + name_on_smoothie + '!', icon="✅")

# New section to call Smoothiefroot API

smoothiefroot_response = requests.get("https://my.smoothiefroot.com/api/fruit/watermelon")
st.text(smoothiefroot_response)