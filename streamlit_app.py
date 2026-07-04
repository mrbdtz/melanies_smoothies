# Import python packages
import streamlit as st
from snowflake.snowpark.functions import col
import requests 

# Write directly to the app
st.title(f":cup_with_straw: Customize Your Smoothie! :cup_with_straw:")
st.write(
  """Chose the fruits you want in your custom Smoothie!
  """
)

name_on_order = st.text_input('Name on Smoothie:')
st.write('The name on your Smoothie will be: ', name_on_order)

cnx = st.connection('snowflake')
session = cnx.session()
my_dataframe = session.table('smoothies.public.fruit_options').select(col('FRUIT_NAME'))
#st.dataframe(data=my_dataframe, use_container_width=True)

ingredients_list = st.multiselect(
    'Choose up to 5 ingredients:'
    , my_dataframe
    , max_selections = 5
)

if ingredients_list:
    st.write(ingredients_list)
    st.text(ingredients_list)

    for fruit_chosen in ingredients_list:
      st.subheader(fruit_chosen + ' Nutrition Information')
      search_on_result = session.sql("select search_on from smoothies.public.fruit_options where fruit_name = '" + fruit_chosen + "'").collect()
      search_on = search_on_result[0]['SEARCH_ON']
      smoothiefroot_response = requests.get("https://my.smoothiefroot.com/api/fruit/" + search_on)
      sf_df = st.dataframe(data=smoothiefroot_response.json(), use_container_width=True)
  
    ingredients_string = ' '.join(ingredients_list)
    
    #st.write(ingredients_string)

    my_insert_stmt = """ insert into smoothies.public.orders(ingredients, name_on_order)
                    values ('""" + ingredients_string + """','""" + name_on_order + """')"""

    #st.write(my_insert_stmt)
    #st.stop()

    time_to_insert = st.button('Submit Order')

    if time_to_insert:
        session.sql(my_insert_stmt).collect()
        st.success('Your Smoothie is ordered!', icon="✅")
