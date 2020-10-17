# Blokus (Development currently ongoing)
A Python implementation of the Mattell game Blokus, with an option to add new AIs

Screenshots (P.S. The green box over current player's turn and AI's turn's text is pending for the next commit):

![blokus](https://user-images.githubusercontent.com/13799022/96349194-da8c0a80-10e8-11eb-8d1c-e29aa596f4c1.jpg)
![blokus_ai_turn](https://user-images.githubusercontent.com/13799022/96349209-fc858d00-10e8-11eb-9128-dc6793321e2b.JPG)
![blokus_invalid_move](https://user-images.githubusercontent.com/13799022/96349212-014a4100-10e9-11eb-9181-2c7167f324aa.JPG)

<b>1. Requirements:</b>
- Python
- Numpy
- Pygame

Download dependencies in a single line.
- Windows:
python -m pip install numpy pygame
- Ubuntu/Linux:
python3 -m pip install numpy pygame

Tested on:
- Python 3.7.3
- Numpy 1.18.4
- Pygame 1.9.6

<b>2. Rules:</b>

Refer to Mattell's official rules in the PDF named blokus-rules.pdf or here: http://service.mattel.com/instruction_sheets/R1984-0920.pdf

<b>3. Gameplay:</b>

From the command line, run the following.
- Windows:

cd \<the directory where you downloaded this respository\>

python blokus.py

- Ubuntu/Linux:

cd \<the directory where you downloaded this repository\>

python3 blokus.py

<b>4. Add your own AI</b>

Use the AIManager.py file to add your own AI.
