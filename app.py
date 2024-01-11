import os
import json
from dotenv import load_dotenv
import google.generativeai as genai

load_dotenv()
api_key = os.getenv("API_KEY")

AUTO_PILOT = False

# save in md file
def store_file(fileName, type, value):
    with open(fileName, type) as file:
        json.dump(json.loads(value), file)


# AI
genai.configure(api_key=os.getenv("API_KEY"))
model = genai.GenerativeModel(model_name="gemini-pro")


def create_chapters_for_titls(title):
    print(f"Creating chapters for the eBook titled '{title}'")
    response = model.generate_content(contents=[
                                      "You are creative eBook writer give response in json object",
                                      f"write the chapter and subheading for the eBook titled {title}."
                                      "Make chapter names as the key and list of subheadings as vlues",
                                      "Give at least 10 Chapters and 4 subheading for each chapters.",

                                      ])
    value = response.text
    # removing backticks bcz in value we are getting in markdown formate ```{}``` in markdown you will get code in between ``````
    newValue = value.replace("json", '')
    # storing json data
    store_file("chapters.json", 'w', newValue)


def create_chapter_conent(eBook_title, chapter, subheading):
    print("--"*50)
    print(
        f"Creating.... content for chapter '{chapter}' with subHeading '{subheading}'")
    response = model.generate_content(contents=[
        'You are creative eBokk Writer.',
        f"Title of the eBook you writing is {eBook_title}. Each chapter of the eBook has subHeading.",
        f"write the content for the subheading titled '{subheading}'under the chapter titled {chapter}.  Be elaborate and clear. Include chapter name and subheading in response"
    ])

    print(response.text)
    return response.text



def main():
    title = input("Name of the Book : ")
    create_chapters_for_titls(title)
    satisfied = False

    while not satisfied:
        create_chapters_for_titls(title)
        satisfied = 'y' == input(
            "Are you satisfied with created chapters ? \n Press Y for yes  Press N for NO: ").lower()

    chapters = None
    with open('chapters.json') as chapters_fils:
        chapters = json.load(chapters_fils)\

    for ch, subHeadings in chapters.items():
        for sh in subHeadings:
            recreate = True
            while recreate:
                contents = create_chapter_conent(title, ch, sh)

                recreate = not AUTO_PILOT and 'r' == input(
                    "Press R to recreate the content if you are not satisfied, Press any other key to proceed to the next subHeading: "
                ).lower()

                if not recreate:
                    with open(f'{title}.txt', 'a') as eBook_file:
                        eBook_file.write(contents + "\n" + "**"*30 + "\n")

    print("---"*10)
    print(f"Completed.... {title}")

if __name__ == "__main__":
    main()
