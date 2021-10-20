# AKR-projekt

Instalace - Linux:
------------------
Posloupnost příkazů:\
-`git clone https://github.com/BorekZnovustvoritel/AKR-projekt`\
-`cd AKR-projekt`\
-`python3 -m venv ./venv`\
-`source venv/bin/activate`\
-`python3 -m pip install -r requirements.txt`\
-`python3 fact_proj.py`

Instalace - Windows:
--------------------
Posloupnost příkazů:\
-`git clone https://github.com/BorekZnovustvoritel/AKR-projekt`\
-`cd AKR-projekt`\
-`py -m venv ./venv`\
-`venv\Scripts\activate`\
-`py -m pip install -r requirements.txt`\
-`py fact_proj.py`

Před každým otevřením kódu je nutné v root adrsáři repa v git bashi zadat:
--------------------------------------------------------------------------
-`git checkout main` (Přepne se na větev `main`.)\
-`git pull origin/main` (Updatuje lokální kopii.)

Před každou úpravou kódu je dále nutné:
---------------------------------------
-`git branch [název větve, podle jména a problematiky, kterou chcete upravovat]` (Vytvoří větev.)\
-`git checkout [váš název větve]` (Přepne se na tuto větev.)
