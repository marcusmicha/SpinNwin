import streamlit as st
import yaml
from pathlib import Path
from game import Game

rules = yaml.safe_load(Path('config.yml').read_text())
level_config = yaml.safe_load(Path('level-config.yml').read_text())

st.title('Spin and Win')
vip_level = st.slider('What VIP level are you?', 1, 7, 1)
nb_of_rounds = st.slider('How many rounds do you want to play?', 1, 200, 1)
if st.button('Play !'):
    spinwin = Game(rules,level_config, number_of_rounds=nb_of_rounds, vip_level=vip_level)
    spinwin.start()
    total, average, rewards, min_reward, max_reward = spinwin.results()
    st.write("The minimun allowed", min_reward)
    st.write("The maximun allowed", max_reward)
    st.write("Your reward", average)
