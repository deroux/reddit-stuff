# I was kidnapped as a little girl and survived. AMA
# At 7 years old I was kidnapped by my mothers drug dealer. He knew I was starving and asked if I wanted to get groceries with him. I knew we were not going back at some point. I remember him getting gas and thinking I could run to the pay phone and call 911. Except I knew he would catch me. He pornographed me and tried to sell me on several occasions. At one point, a female noticed me traveling with a much older male and reported me to the police. My own mother had yet to report me missing. Days had gone by at this point. He knew she was reporting him and he fled. I remember thinking I was going to die. He drugged me and the next thing I remember was waking up naked to firemen wrapping me in aluminum blankets to cover my naked body. I was later told that I was payment for a drug debt my mother owed. I have no idea what happened to my kidnapper. I do know he hurt other kids because he told me about them. I know the statistics of me surviving this are extremely rare. I've never met a kidnapping survivor. I'm thankful every day to be alive.
import sys
from itertools import chain

import spacy

"""
ID	Category name
1	Film & Animation
2	Autos & Vehicles
10	Music
15	Pets & Animals
17	Sports
19	Travel & Events
20	Gaming
22	People & Blogs
23	Comedy
24	Entertainment
25	News & Politics
26	Howto & Style
27	Education
28	Science & Technology
29	Nonprofits & Activism
"""
def getCategory(keywords): 
    return str(24)
    
nlp = spacy.load("en_core_web_lg")
text = """I was kidnapped as a little girl and survived. AMA
At 7 years old I was kidnapped by my mothers drug dealer. He knew I was starving and asked if I wanted to get groceries with him. I knew we were not going back at some point. I remember him getting gas and thinking I could run to the pay phone and call 911. Except I knew he would catch me. He pornographed me and tried to sell me on several occasions. At one point, a female noticed me traveling with a much older male and reported me to the police. My own mother had yet to report me missing. Days had gone by at this point. He knew she was reporting him and he fled. I remember thinking I was going to die. He drugged me and the next thing I remember was waking up naked to firemen wrapping me in aluminum blankets to cover my naked body. I was later told that I was payment for a drug debt my mother owed. I have no idea what happened to my kidnapper. I do know he hurt other kids because he told me about them. I know the statistics of me surviving this are extremely rare. I've never met a kidnapping survivor. I'm thankful every day to be alive.
"""
doc = nlp(text)
# print(doc.ents)
keywords = ','.join(map(str, chain.from_iterable(doc.ents)))
category = getCategory(doc.ents)

# TODO: find some way to categorize
with open("info_0.txt", "a") as file:
    file.write('\n')
    file.write(keywords + "\n")  # keywords
    file.write(category + "\n")
