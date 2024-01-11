import os
import json
from dotenv import load_dotenv
import google.generativeai as genai


load_dotenv()
api_key = os.getenv("API_KEY")

genai.configure(api_key=os.getenv("API_KEY"))
model = genai.GenerativeModel(model_name="gemini-pro")


def create_chapters_for_titls(title):
    print(f"Creating chapters for the eBook titled '{title}'")
    response = model.generate_content(contents=[
                                      "You are creative eBook writer give response as JSON.",
                                      f"write the chapter and subheading for the eBook titled {title}."
                                      "Make chapter names as the key and list of subheadings as vlues",
                                      "Give at least 10 Chapters and 4 subheading for each chapters."
                                      ])
    # storing json data in Markdown File, don't worry it show in json formate 
    with open("chapters.json", "w") as chapters_File:
        # chapters_File.write(response.text)
        json.dump(json.loads(response.text), chapters_File)

def create_chapter_conent(eBook_title, chapter, subheading):
    print("--"*50)
    print(f"Creating.... content for chapter '{chapter}' with subHeading '{subheading}'")
    response = model.generate_content(contents=[
        'You are creative eBokk Writer.',
        f"Title of the eBook you writing is {chapter}. Be elaborate and clear. Include chapter name and subheading"
    ])

create_chapters_for_titls("Computer Science")
