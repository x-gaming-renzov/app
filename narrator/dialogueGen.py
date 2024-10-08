import narrator.LLM as LLM
import narrator.prompts as prompts

import subprocess
import os, json

def generate_mermaid_diagram(mermaid_code, output_file):
    # Create a temporary Mermaid file
    with open("temp_diagram.mmd", "w") as file:
        file.write(mermaid_code)
    
    try:
        # Call the Mermaid CLI to generate the image
        result = subprocess.run(["mmdc", "-i", "temp_diagram.mmd", "-o", output_file], check=True)
        print("Diagram generated successfully:", output_file)
        
        # Read and return the image content
        with open(output_file, 'rb') as image_file:
            image_data = image_file.read()
        return image_data

    except subprocess.CalledProcessError as e:
        print("Error generating diagram:", e)
        return None
    finally:
        # Clean up the temporary Mermaid file
        if os.path.exists("temp_diagram.mmd"):
            #os.remove("temp_diagram.mmd")
            pass

from plantuml import PlantUML

def generate_diagram(plantuml_code):
    p = PlantUML(url='http://www.plantuml.com/plantuml/img/')
    data = p.processes(plantuml_text=plantuml_code)
    return data

def GetDialougeTree(personality, description, background, depth):
    llm = LLM.LLM()
    prompt = prompts.get_dialogue_promt(personality, description, background, depth)
    response = llm.send_message(prompt, model='gpt-4o')
    return response

def getMermaid(data):
    try:
        llm = LLM.LLM()
        prompt = prompts.get_mermaid_promt(data)
        response = llm.send_message(prompt)
        response = json.loads(response)
        print(response['plantuml'])
        img =  generate_diagram(response['plantuml'])
        with open("output.png", "wb") as image_file:
            image_file.write(img)
        return img
    except Exception as e:
        print("Error generating Mermaid diagram:")
        return getMermaid(data)