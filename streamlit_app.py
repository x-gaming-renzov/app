import streamlit as st
from narrator.dialogueGen import GetDialougeTree, getMermaid
import json
from PIL   import Image

st.title('XG Dialogue Tree Generator')

st.info('This is a simple app to generate dialogue trees using the XG format.')

with st.expander('How to use this app:'):
    st.write('''
    1. Enter Personality of NPC. It can be anything like moody, hilarious, etc.
    2. Give background of NPC. It could be why this npc is in the game, what they are doing, etc. You can also topics you want to cover in the conversation.
    3. Give description of NPC. It could be what they look like, what they wear, etc.
    ''')

st.header('Dialogue Tree Generator')
personality = st.text_input('Personality of NPC', key='personality')
description = st.text_area('Description of NPC', key='description')
background = st.text_area('Background of NPC', key='background')
depth = st.number_input('Depth of conversation', min_value=1, max_value=10, value=3, key='depth', help='Depth of conversation tree. Optional')
gen = st.button('Generate Dialogue Tree')

def temp_callback(dialuge_dict, depth, dialogue_container):
    #change text to random number
    if type(dialuge_dict) != dict:
        dialuge_dict = json.loads(dialuge_dict)
    
    dialogue_container.empty()
    
    npc_dialogue = dialuge_dict['npc_dialogue']
    st.write(f'NPC : {npc_dialogue}')
    player_dialogue = dialuge_dict['player_dialogue_choices']
    choice = st.radio('Player : ', list(player_dialogue.keys()))
    while choice:
        if choice == 'End conversation':
            break
        else:
            temp_callback(player_dialogue[choice], depth+1, dialogue_container)

if gen:
    status = st.status('Generating Dialogue Tree...')
    status.update(label='Brewing good stuff...')   
    dialogue_container = st.empty()
    dialoufe_tree = GetDialougeTree(personality, description, background, depth)
    dialoufe_tree = json.loads(dialoufe_tree)
    status.update(label='Smells good, Let me serve you...')
    print(dialoufe_tree)
    img = getMermaid(dialoufe_tree)
    with open("output.png", "wb") as image_file:
        image_file.write(img)
    pil_img = Image.open("output.png")
    wd, ht = pil_img.size
    dialogue_container.image(pil_img, width=wd)
    status.update(label='Is it good?', state="complete")
    like, dislike, download = dialogue_container.columns(3)
    like.button('Like')
    dislike.button('Dislike')
    download.download_button('Download', img, file_name='dialogue_tree.png')





