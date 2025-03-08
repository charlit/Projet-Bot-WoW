# Projet-Bot-WoW

Bienvenue dans **Projet Bot WoW** ! 🎮

Ce projet est un bot développé pour **World of Warcraft** (WoW) afin d'automatiser les combats. Ce bot a été conçu pour améliorer l'expérience de jeu des utilisateurs et leur faire gagner du temps. Cependant il est en développement.

Voici ce que va afficher l'Addon sur WOW
![Addon](https://github.com/charlit/Projet-Bot-WoW/blob/main/screenshots/screen_2025-03-07_13-45-03.png)

Voila ce que ca va detecter Tesseract
![Tesseract](https://github.com/charlit/Projet-Bot-WoW/blob/main/screenshots/threshold_2025-03-07_13-45-03.png)

## 🚀 Fonctionnalités

- 📸 Capture automatique de l'écran via `mss`
- 🔍 Extraction des informations du jeu avec `pytesseract` (OCR)
- 🎯 Sélection et attaque automatique des cibles
- 🔄 Gestion de la vie, mana et position du personnage
- 🤖 Automatisation des combats avec `pyautogui`
- 🖥️ Détection automatique de la fenêtre de WoW

---

## 🛠️ Installation

### 1️⃣ Prérequis

Avant de commencer, assure-toi d'avoir installé :

- **Python 3.x** → [Télécharge ici](https://www.python.org/downloads/)
- **Tesseract-OCR** → [Télécharge ici](https://github.com/UB-Mannheim/tesseract/wiki)

Après installation, configure le chemin de Tesseract dans le script :

```python
pytesseract.pytesseract.tesseract_cmd = r'C:\Users\lesma\Documents\script python\Tesseract-OCR\tesseract.exe'
## Capture d'écran


