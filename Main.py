import cv2
import pytesseract
import numpy as np
import mss
import time
import pygetwindow as gw
import pyautogui
import re

# Tesseract Path
pytesseract.pytesseract.tesseract_cmd = r'C:\Users\lesma\Documents\script python\Tesseract-OCR\tesseract.exe'

last_log_time = time.time()

# Variables
hp = ""
mana = ""
pos = {"x": 0, "y": 0}
target = ""
target_hp = ""

def get_window_position():
    windows = gw.getWindowsWithTitle("World of Warcraft")
    if windows:
        win = windows[0]
        return {"top": win.top, "left": win.left, "width": win.width, "height": win.height}
    return None

def activate_window():
    windows = gw.getWindowsWithTitle("World of Warcraft")
    if windows:
        win = windows[0]
        win.activate()

def capture_screen(zone):
    with mss.mss() as sct:
        screenshot = sct.grab(zone)
        img = np.array(screenshot)
        img = cv2.cvtColor(img, cv2.COLOR_BGRA2BGR)
        return img

def extract_text(img):
    img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    img = cv2.threshold(img, 127, 255, cv2.THRESH_BINARY)[1]
    text = pytesseract.image_to_string(img, config='--psm 6')
    #print(f"[DEBUG] Tesseract Extraction:\n{text}")  # Affiche ce que Tesseract voit
    return text.strip()

def clean_text(text):
    text = text.replace("O", "0")
    text = text.replace("l", "1")
    text = text.replace("I", "1")
    text = text.replace("Vie", "HP")  # Corrige les fautes fréquentes
    text = re.sub(r"[^\x00-\x7F]+", "", text)  # Supprime les caractères spéciaux
    return text

def extract_info_from_text(text):
    global hp, mana, pos, target, target_hp

    # Reset
    hp = ""
    mana = ""
    pos = {"x": 0, "y": 0}
    target = ""
    target_hp = ""

    text = clean_text(text)
    lines = text.split("\n")

    for line in lines:
        # HP Personnage
        if "HP:" in line and "Mana:" in line:
            hp_match = re.search(r"HP:(\d+)/(\d+)", line)
            if hp_match:    
                hp = f"{hp_match.group(1)}/{hp_match.group(2)}"
        
        # MANA
        mana_match = re.search(r"Mana: (\d+)/(\d+)", line)
        if mana_match:
            mana = f"{mana_match.group(1)}/{mana_match.group(2)}"

        # Position
        pos_match = re.search(r"Pos: X=(-?\d+\.\d+) Y=(-?\d+\.\d+)", line)
        if pos_match:
            pos["x"] = float(pos_match.group(1))
            pos["y"] = float(pos_match.group(2))

        # Nom Target
        target_match = re.search(r"Target: (.+)", line)
        if target_match:
            target = target_match.group(1).strip()

        # HP TARGET
        target_hp_match = re.search(r"Target Vie: (\d+)/(\d+)", line)
        if target_hp_match:
            target_hp = f"{target_hp_match.group(1)}/{target_hp_match.group(2)}"

    print(f"[SPECTRE] HP:{hp} Mana:{mana} Pos:X={pos['x']} Y={pos['y']}")
    print("---------------------------------------")
    print(f"- HP du personnage : {hp if hp else 'Non détecté'}")
    print(f"- MANA du personnage : {mana if mana else 'Non détecté'}")
    #print(f"- POS : X={pos['x']} Y={pos['y']}")
    #print("---------------------------------")
    #print(f"- NOM TARGET : {target if target else 'Aucune cible'}")
    #print(f"- HP TARGET : {target_hp if target_hp else 'Non détecté'}")
    #print("----------------------------------------")

def fight():
    global target, target_hp
    while True:
        activate_window()
        extract_info_from_text(extract_text(capture_screen(get_window_position())))  # Mise à jour des variables
        print(target+"  "+target_hp)
        if not target:
            pyautogui.press("tab")  # Sélectionner une cible
            time.sleep(0.5)  # Laisser le temps au jeu de répondre
        elif target:
            pyautogui.press("a")  # Attaquer
            time.sleep(0.2)
        if not target:
            print("[INFO] Cible éliminée, recherche d'une nouvelle cible...")
            #loot()
            pyautogui.press("tab")
            time.sleep(2) 

def loot():
    print("[INFO] Looting...")
    activate_window()
    screen_width, screen_height = pyautogui.size()
    center_x, center_y = screen_width // 2, screen_height // 2
    pyautogui.click(x=center_x, y=center_y, button='right')
    time.sleep(1)  # Pause pour le loot

while True:
    zone = get_window_position()
    if zone:    
        zone["top"] += 500
        zone["left"] += 1300
        zone["width"] = 600
        zone["height"] = 100
        zone["left"] -= 75
        zone["width"] += 75

        img = capture_screen(zone)
        text = extract_text(img)

        current_time = time.time()
        if text != "" and current_time - last_log_time >= 1:
            extract_info_from_text(text)
            last_log_time = current_time

    fight()
    time.sleep(0.3)
