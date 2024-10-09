import json
import uuid
from io import BytesIO
from pathlib import Path

import streamlit as st
from PIL import Image

from narrator.dialogueGen import GetDialougeTree, getMermaid

# Function to generate a unique session ID
def generate_session_id():
    return str(uuid.uuid4())

# Function to save session data
def save_session_data(session_id, input_data, output_data, liked):
    data = {
        "input": input_data,
        "output": output_data,
        "liked": liked
    }
    
    file_name = "like.json" if liked else "dislike.json"
    file_path = Path(file_name)
    
    if file_path.exists():
        with open(file_path, "r") as f:
            existing_data = json.load(f)
    else:
        existing_data = {}
    
    existing_data[session_id] = data
    
    with open(file_path, "w") as f:
        json.dump(existing_data, f, indent=2)

# Function to handle like/dislike button clicks
def handle_feedback(liked):
    session_id = generate_session_id()

    input_data = {
        "personality": st.session_state.personality,
        "description": st.session_state.description,
        "background": st.session_state.background,
        "depth": st.session_state.depth
    }
    
    save_session_data(
        session_id,
        input_data,
        st.session_state.dialogue_tree,
        liked
    )
    
    if liked:
        st.success("Thank you for your positive feedback!")
    else:
        st.warning("We're sorry you didn't like the result. We'll work on improving it!")

def generate_dialogue_tree(personality, description, background, depth):
    return json.loads(GetDialougeTree(personality, description, background, depth))

def generate_mermaid_image(dialogue_tree):
    return getMermaid(dialogue_tree)

def display_dialogue(dialogue_dict):
    if not isinstance(dialogue_dict, dict):
        dialogue_dict = json.loads(dialogue_dict)
    
    # Initialize session state for conversation history if it doesn't exist
    if 'conversation_history' not in st.session_state:
        st.session_state.conversation_history = []
        st.session_state.current_dialogue = dialogue_dict
    
    # Display conversation history
    for npc, player in st.session_state.conversation_history:
        st.write(f'NPC: {npc}')
        st.write(f'You: {player}')
    
    # Display current NPC dialogue
    npc_dialogue = st.session_state.current_dialogue['npc_dialogue']
    st.write(f'NPC: {npc_dialogue}')
    
    player_choices = st.session_state.current_dialogue['player_dialogue_choices']
    
    if player_choices:
        choice = st.selectbox('Choose your response:', list(player_choices.keys()) + ['End conversation'])
        
        if st.button('Next'):
            if choice and choice != 'End conversation':
                # Add current dialogue to history
                st.session_state.conversation_history.append((npc_dialogue, choice))
                # Move to next dialogue
                st.session_state.current_dialogue = player_choices[choice]
                st.rerun()  # Changed from st.experimental_rerun()
            else:
                st.write("End of conversation.")
                # Reset conversation state
                st.session_state.conversation_history = []
                st.session_state.current_dialogue = dialogue_dict

    else:
        st.write("End of conversation.")
        # Reset conversation state
        st.session_state.conversation_history = []
        st.session_state.current_dialogue = dialogue_dict


def main():
    st.title('XG Dialogue Tree Generator')
    st.info('This is a simple app to generate dialogue trees using the XG format.')

    # Initialize session state variables
    if 'session_id' not in st.session_state:
        st.session_state.session_id = generate_session_id()
    if 'personality' not in st.session_state:
        st.session_state.personality = ""
    if 'description' not in st.session_state:
        st.session_state.description = ""
    if 'background' not in st.session_state:
        st.session_state.background = ""
    if 'depth' not in st.session_state:
        st.session_state.depth = 3

    with st.expander('How to use this app:'):
        st.write('''
        1. Enter Personality of NPC. It can be anything like moody, hilarious, etc.
        2. Give background of NPC. It could be why this npc is in the game, what they are doing, etc. You can also include topics you want to cover in the conversation.
        3. Give description of NPC. It could be what they look like, what they wear, etc.
        ''')

    st.header('Dialogue Tree Generator')

    with st.form("dialogue_input"):
        personality = st.text_input('Personality of NPC', key='personality')
        description = st.text_area('Description of NPC', key='description')
        background = st.text_area('Background of NPC', key='background')
        depth = st.number_input('Depth of conversation', min_value=1, max_value=10, value=3, key='depth', help='Depth of conversation tree. Optional')
        submit_button = st.form_submit_button('Generate Dialogue Tree')

    if submit_button:
        if not all([personality, description, background]):
            st.error("Please fill in all fields before generating the dialogue tree.")
        else:
            with st.spinner('Generating Dialogue Tree...'):
                try:
                    dialogue_tree = generate_dialogue_tree(personality, description, background, depth)
                    img_bytes = generate_mermaid_image(dialogue_tree)

                    # Store dialogue tree and image in session state
                    st.session_state.dialogue_tree = dialogue_tree
                    st.session_state.img_bytes = img_bytes

                except Exception as e:
                    st.error(f"An error occurred: {str(e)}")

    if 'dialogue_tree' in st.session_state and 'img_bytes' in st.session_state:
        dialogue_container = st.container()
        with dialogue_container:
            display_dialogue(st.session_state.dialogue_tree)

        img = Image.open(BytesIO(st.session_state.img_bytes))
        st.image(img, use_column_width=True)

        col1, col2, col3, col4 = st.columns(4)
        with col1:
            download_png(st.session_state.img_bytes)
        with col2:
            download_json(st.session_state.dialogue_tree)
        with col3:
            if st.button("Like"):
                handle_feedback(liked=True)
        with col4:
            if st.button("Dislike"):
                handle_feedback(liked=False)

def download_png(img_bytes):
    st.download_button(
        label="Download PNG",
        data=img_bytes,
        file_name="dialogue_tree.png",
        mime="image/png"
    )

def download_json(dialogue_tree):
    st.download_button(
        label="Download JSON",
        data=json.dumps(dialogue_tree, indent=2),
        file_name="dialogue_tree.json",
        mime="application/json"
    )

if __name__ == "__main__":
    main()
