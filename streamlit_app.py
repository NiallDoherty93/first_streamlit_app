import streamlit
import pandas
import requests
import snowflake.connector
from urllib.error import URLError

streamlit.title('My parents new healthy diner')

streamlit.header('Breakfast Menu')
streamlit.text('🥣 Omega 3 & Blueberry Oatmeal')
streamlit.text('🥗 Kale, Spinach & Rocket Smoothie')
streamlit.text('🐔  Hard-Boiled Free-Range Egg')
streamlit.text('🥑🍞Avocado Toast Egg')

streamlit.header('🍌🥭 Build Your Own Fruit Smoothie 🥝🍇')


#import pandas
my_fruit_list = pandas.read_csv("https://uni-lab-files.s3.us-west-2.amazonaws.com/dabw/fruit_macros.txt")
streamlit.dataframe(my_fruit_list)


# Let's put a pick list here so they can pick the fruit they want to include 
#streamlit.multiselect("Pick some fruits:", list(my_fruit_list.index))
#streamlit.multiselect("Pick some fruits: ", list(my_fruit_list.index),['Avocado', 'Strawberries'])
#fruits_selected = streamlit.multiselect("Pick some fruits: ", list(my_fruit_list.index), [:2])
fruits_selected = streamlit.multiselect("Pick some fruits: ", list(my_fruit_list.index), my_fruit_list.index[:2].tolist())
fruits_to_show = my_fruit_list.loc[fruits_selected]

# Display the table on the page.

#my_fruit_list = my_fruit_list.set_index('Fruit')
streamlit.dataframe(fruits_to_show)


streamlit.header("Fruityvice Fruit Advice!")
try:
    fruit_choice = streamlit.text_input('What fruit would you like information about?')
    if not fruit_choice:
         streamlit.error("please select a fruit to get information.")
    else:
         fruityvice_response = requests.get("https://fruityvice.com/api/fruit/" + fruit_choice)
         fruityvice_normalized = pandas.json_normalize(fruityvice_response.json())
         streamlit.dataframe(fruityvice_normalized)

except URLError as e:
    streamlit.error()
        
#streamlit.write('The user entered ', fruit_choice)

#import requests
#fruityvice_response = requests.get("https://fruityvice.com/api/fruit/" + fruit_choice)
# write your own comment -what does the next line do? 
#fruityvice_normalized = pandas.json_normalize(fruityvice_response.json())
# write your own comment - what does this do?
#streamlit.dataframe(fruityvice_normalized)

streamlit.stop()

#import snowflake.connector
my_cnx = snowflake.connector.connect(**streamlit.secrets["snowflake"])
my_cur = my_cnx.cursor()
my_cur.execute("select * from fruit_load_list")
my_data_rows = my_cur.fetchall()
streamlit.header("The fuit load list contains")
streamlit.dataframe(my_data_rows)

#streamlit.header("What fuit would you like to add?")
new_fruit = streamlit.text_input('What fruit would you like to add?' ,'')
streamlit.write('Thanks for adding ', new_fruit)

# Add the new fruit to the list directly (no need for if statement)
#my_data_rows.append(new_fruit)
my_data_rows.append((new_fruit,) + tuple(row[1:] for row in my_data_rows))
streamlit.dataframe(my_data_rows)
#test

# Display the updated fruit list
#st.write("Updated Fruit List:", fruit_load_list)

my_cur.execute("insert into fruit_load_list values ('from streamlit')")
 


 


