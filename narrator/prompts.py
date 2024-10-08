

def get_dialogue_promt(npc_personality, npc_description, npc_backstory, depth):
    DIALOGUE_PROMT = f"""
Context: 
In a game where the player acts as a sub-deity responsible for helping souls fulfill their last wishes before they move on to the afterlife, the player encounters a soul that is stuck in the mortal realm due to unfinished business.
Souls come and go, but the player must keep them in check.
The player is the only one capable of assisting them in completing their final wishes.
The player spends time with these souls, listens to their stories, and helps them find closure and move on.

NPC is:
Description: {npc_description}
Backstory: {npc_backstory}
Personality: {npc_personality}

Generate a dialogue tree with a depth of {depth}.

Dialogue Generation Guidelines:
1. The dialogue should evoke a longing for a better life.
2. The dialogue should provide the player with a sense of purpose.
3. The dialogue should be short and focused.
4. The dialogue should be friendly and engaging.
5. The dialogue should be clear and concise.
6. The dialogue should be informative and helpful.
7. The dialogue should be positive and encouraging.
8. The dialogue should stay relevant to the context of the story.
9. Dialogues should always stay short and on-point.
10. Clear communication is key in each interaction.

Rules:
1. The conversation must be deeply engaging and compelling.
2. The conversation should leave the player with a heightened sense of purpose.
3. The conversation should immerse the player and create an emotional impact.
4. The conversation should provide a conclusive or reflective ending.
5. The conversation always starts with an NPC dialogue.

The generated dialogue tree should adhere to the following JSON format for each node:
{{
    "npc_dialogue": "NPC's dialogue here",
    "player_dialogue_choices": {{
        "Player's dialogue choice 1": new_node,
        "Player's dialogue choice 2": new_node,
        "Player's dialogue choice 3": new_node
    }}
}}

Example:
{{
    "npc_dialogue": "It's been so long since I’ve seen the stars. How are they now?",
    "player_dialogue_choices": {{
        "They're as bright as ever. You’ll see them again soon.": {{
            "npc_dialogue": "I hope so. I still have one wish before I can rest.",
            "player_dialogue_choices": {{
                "What is your last wish?": {{
                    "npc_dialogue": "I just want to visit the place where I grew up, one last time.",
                    "player_dialogue_choices": {{}}
                }},
                "Do you feel ready to move on?": {{
                    "npc_dialogue": "Not yet... but maybe soon.",
                    "player_dialogue_choices": {{}}
                }}
            }}
        }},
        "They’re not the same without you.": {{
            "npc_dialogue": "That’s kind of you to say, but we all must move on.",
            "player_dialogue_choices": {{}}
        }},
        "I haven’t really looked at them lately.": {{
            "npc_dialogue": "I guess I’ll have to find peace without them.",
            "player_dialogue_choices": {{}}
        }}
    }}
}}
"""

    return DIALOGUE_PROMT

def get_mermaid_promt(data):
    MERMAID_PROMT = f"""
TASK : 
Generate a complete plantuml code for mindmap chart for conversation between player and npc.
NPC dialoge node will have prefix as 'NPC' and player dialogue node will have prefix as 'Player'.

DATA: 
{{{data}}}

RULES:
1. Return only PlantUML code.
ENSURE FULL CONVERSATION IS COVERED IN THE FLOW CHART.
2. ONLY RETURN PARSABLE PLANTUML CODE. DO NOT RETURN ANY OTHER TEXT.
3. DO NOT RETURN ANY CODE THAT IS NOT PARSABLE PLANTUML CODE.
4. This file should be passed as string and should be parsable by PLANTUML cli.
5. ENSURE THAT THE CODE IS CORRECT AND CAN BE PARSABLE BY PLANTUML CLI.

RETURN JSON FORMAT:
{{
    "plantuml": "code"
}}
"""

    return MERMAID_PROMT