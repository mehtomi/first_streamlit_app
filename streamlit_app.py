import streamlit
import pandas
import requests
import snowflake.connector
from urllib.error import URLError

streamlit.title('My Parents New Healthy Diner')

streamlit.text('🥑🥑🥑 Kauramaitoa, kiitos! olen vegaani 🥑🥑🥑')

streamlit.header('Breakfast Menu')
streamlit.text('🍞 Omega 3 & Blueberry Oatmeal')
streamlit.text('🥣 Kale, Spinach & Rocket Smoothie')
streamlit.text('🐔 Hard-Boiled Free-Range Egg')

streamlit.header('🍌🥭 Build Your Own Fruit Smoothie 🥝🍇')

my_fruit_list = pandas.read_csv("https://uni-lab-files.s3.us-west-2.amazonaws.com/dabw/fruit_macros.txt")
my_fruit_list = my_fruit_list.set_index('Fruit')

# Let's put a pick list here so they can pick the fruit they want to include
fruits_selected = streamlit.multiselect("Pick some fruits:", list(my_fruit_list.index),['Apple','Banana'] )
fruits_to_show = my_fruit_list.loc[fruits_selected]


# Display the table on the page.
streamlit.dataframe(fruits_to_show)

# Määritetään funktio
def get_fruityvice_data(this_fruit_choice):
      fruityvice_response = requests.get("https://fruityvice.com/api/fruit/" + fruit_choice)
      # normalisoidaan json data
      fruityvice_normalized = pandas.json_normalize(fruityvice_response.json())
      # tehdään siitä joku nätti taulukko
      return fruityvice_normalized

# Käyttäjä voi kirjoittaa hedelmän
streamlit.header('Fruityvice Fruit Advice')
try:
  fruit_choice = streamlit.text_input('What fruit would you like information about?')
  if not fruit_choice:
      streamlit.error("Please help to select a fruit to get information.")
  else:
      back_from_function = get_fruityvice_data(fruit_choice)
      streamlit.dataframe(back_from_function)
      
except URLError as e:
      streamlit.error()

streamlit.write('The user entered ', fruit_choice)

streamlit.header("The fruit load list contains:")
#Snowfale related functions
def get_fruit_load_list():
      with my_cnx.cursor() as my_cur:
           my_cur.execute("select * from fruit_load_list")
           return my_cur.fetchall()

streamlit.header("View our Fruit List - Add Your Favorites")
#Add a button to load fruit load list
if streamlit.button('Get Fruit Load List'):
      my_cnx = snowflake.connector.connect(**streamlit.secrets["snowflake"])
      my_data_rows = get_fruit_load_list()
      my_cnx.close()
      streamlit.dataframe(my_data_rows)

# Käyttäjä voi kirjoittaa toisen hedelmän
# streamlit.header('What fruit would you like to add?')

def insert_row_snowflake(new_fruit):
      with my_cnx.cursor() as my_cur:
           my_cur.execute("insert into fruit_load_list values ('" + new_fruit +"')")
           return streamlit.write('Thanks for adding: ', add_my_fruit)
      
add_my_fruit = streamlit.text_input('What fruit would you like to add?')
if streamlit.button('Add a Fruit to the List'):
      my_cnx = snowflake.connector.connect(**streamlit.secrets["snowflake"])
      back_from_function = insert_row_snowflake(add_my_fruit)
      my_cnx.close()
      streamlit.text(back_from_function)


      
#katkaistaan koodi hetkeksi tähän
streamlit.stop()
