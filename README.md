1. Virtual enviromnent venv (tworzenie wirtualnego środowiska i aktywacja)
```
   python -m venv .venv
   .venv\Scripts\activate.bat
   deactivate
```
2. Instalowanie zależności w projekcie (w wirtualnym środowisku) 
```bash
pip install -r requirements.txt
```
3. odpalanie zewnętrznych skyrptów (np ruff, pytest)
```
ruff check 
ruff format
```
4. jak uruchomić aplikację (przykładowe wywołanie)
```
python main.py
```
