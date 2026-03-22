import asyncio
import threading
import json
import os
import customtkinter as ctk
from bleak import BleakClient, BleakScanner
from pynput.keyboard import Key, Controller as KeyboardController
from pynput.mouse import Button, Controller as MouseController

# ============================================================
# KONFIGURACJA
# ============================================================
DEVICE_NAME = "ESP32_Button_Sender"
CHARACTERISTIC_UUID = "6E400003-B5A3-F393-E0A9-E50E24DCCA9E"
CONFIG_FILE = "config.json"

keyboard = KeyboardController()
mouse = MouseController()

LETTER_TO_GESTURE = {
    'a': 'NONE',
    'b': 'FLAT_HAND',
    'c': 'LIKE',
    'd': 'DISLIKE',
    'e': 'FIST',
    'f': 'LOVE',
    'g': 'BREAKTIME',
    'h': 'CROSSHANDS',
}

GESTURE_INFO = {
    'NONE':       {'emoji': '✋', 'kolor': '#4a4a6a'},
    'FLAT_HAND':  {'emoji': '🖐', 'kolor': '#1a6fa8'},
    'LIKE':       {'emoji': '👍', 'kolor': '#1a8a4a'},
    'DISLIKE':    {'emoji': '👎', 'kolor': '#a83232'},
    'FIST':       {'emoji': '✊', 'kolor': '#a86b1a'},
    'LOVE':       {'emoji': '🤟', 'kolor': '#a8186e'},
    'BREAKTIME':  {'emoji': '✌️', 'kolor': '#8a8a1a'},
    'CROSSHANDS': {'emoji': '🤞', 'kolor': '#6a1aa8'},
}

# Wszystkie dostępne akcje
DOSTEPNE_AKCJE = {
    'Nic':                 None,
    'Play / Pause':        lambda: (keyboard.press(Key.media_play_pause), keyboard.release(Key.media_play_pause)),
    'Głośniej':            lambda: (keyboard.press(Key.media_volume_up), keyboard.release(Key.media_volume_up)),
    'Ciszej':              lambda: (keyboard.press(Key.media_volume_down), keyboard.release(Key.media_volume_down)),
    'Następny utwór':      lambda: (keyboard.press(Key.media_next), keyboard.release(Key.media_next)),
    'Poprzedni utwór':     lambda: (keyboard.press(Key.media_previous), keyboard.release(Key.media_previous)),
    'Kliknięcie myszy':    lambda: mouse.click(Button.left, 1),
    'Scroll w górę':       lambda: mouse.scroll(0, 3),
    'Scroll w dół':        lambda: mouse.scroll(0, -3),
    'Print Screen':        lambda: (keyboard.press(Key.print_screen), keyboard.release(Key.print_screen)),
    'Kopiuj (Ctrl+C)':     lambda: (keyboard.press(Key.ctrl), keyboard.press('c'), keyboard.release('c'), keyboard.release(Key.ctrl)),
    'Wklej (Ctrl+V)':      lambda: (keyboard.press(Key.ctrl), keyboard.press('v'), keyboard.release('v'), keyboard.release(Key.ctrl)),
    'Cofnij (Ctrl+Z)':     lambda: (keyboard.press(Key.ctrl), keyboard.press('z'), keyboard.release('z'), keyboard.release(Key.ctrl)),
    'Strzałka w górę':     lambda: (keyboard.press(Key.up), keyboard.release(Key.up)),
    'Strzałka w dół':      lambda: (keyboard.press(Key.down), keyboard.release(Key.down)),
    'Strzałka w lewo':     lambda: (keyboard.press(Key.left), keyboard.release(Key.left)),
    'Strzałka w prawo':    lambda: (keyboard.press(Key.right), keyboard.release(Key.right)),
    'Zamknij okno (Alt+F4)': lambda: (keyboard.press(Key.alt), keyboard.press(Key.f4), keyboard.release(Key.f4), keyboard.release(Key.alt)),
    'Minimalizuj (Win+D)': lambda: (keyboard.press(Key.cmd), keyboard.press('d'), keyboard.release('d'), keyboard.release(Key.cmd)),
    'Spacja':              lambda: (keyboard.press(Key.space), keyboard.release(Key.space)),
    'Enter':               lambda: (keyboard.press(Key.enter), keyboard.release(Key.enter)),
    'Escape':              lambda: (keyboard.press(Key.esc), keyboard.release(Key.esc)),
}

# Domyślna konfiguracja
DOMYSLNA_KONFIGURACJA = {
    'NONE':       'Nic',
    'FLAT_HAND':  'Play / Pause',
    'LIKE':       'Głośniej',
    'DISLIKE':    'Ciszej',
    'FIST':       'Następny utwór',
    'LOVE':       'Poprzedni utwór',
    'BREAKTIME':  'Kliknięcie myszy',
    'CROSSHANDS': 'Scroll w górę',
}

# ============================================================
# ZAPIS / ODCZYT KONFIGURACJI
# ============================================================
def wczytaj_konfiguracje():
    if os.path.exists(CONFIG_FILE):
        try:
            with open(CONFIG_FILE, 'r', encoding='utf-8') as f:
                return json.load(f)
        except:
            pass
    return DOMYSLNA_KONFIGURACJA.copy()

def zapisz_konfiguracje(config):
    with open(CONFIG_FILE, 'w', encoding='utf-8') as f:
        json.dump(config, f, ensure_ascii=False, indent=2)

# ============================================================
# GUI
# ============================================================
ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

class SpatialKeyApp(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("SpatialKey")
        self.geometry("460x720")
        self.resizable(False, False)

        self.historia = []
        self.konfiguracja = wczytaj_konfiguracje()
        self.dropdowns = {}

        self._zbuduj_gui()

    def _zbuduj_gui(self):
        # Tytuł
        ctk.CTkLabel(
            self,
            text="SpatialKey",
            font=ctk.CTkFont(size=32, weight="bold")
        ).pack(pady=(20, 0))

        ctk.CTkLabel(
            self,
            text="Sterowanie gestami dłoni",
            font=ctk.CTkFont(size=13),
            text_color="gray"
        ).pack(pady=(4, 10))

        # Zakładki
        self.tabs = ctk.CTkTabview(self, width=420, height=580)
        self.tabs.pack(padx=20, pady=5, fill='both', expand=True)

        self.tabs.add("Dashboard")
        self.tabs.add("Konfiguracja")

        self._zbuduj_dashboard()
        self._zbuduj_konfiguracje()

    def _zbuduj_dashboard(self):
        tab = self.tabs.tab("Dashboard")

        # Status
        status_frame = ctk.CTkFrame(tab, corner_radius=10)
        status_frame.pack(pady=10, padx=10, fill='x')

        self.status_dot = ctk.CTkLabel(
            status_frame, text='●',
            font=ctk.CTkFont(size=16),
            text_color='#e74c3c'
        )
        self.status_dot.pack(side='left', padx=(15, 5), pady=12)

        self.status_label = ctk.CTkLabel(
            status_frame,
            text='Szukanie ESP32...',
            font=ctk.CTkFont(size=13)
        )
        self.status_label.pack(side='left', pady=12)

        # Karta gestu
        self.gest_card = ctk.CTkFrame(
            tab, corner_radius=20,
            fg_color='#4a4a6a', height=200
        )
        self.gest_card.pack(pady=10, padx=10, fill='x')
        self.gest_card.pack_propagate(False)

        self.emoji_label = ctk.CTkLabel(
            self.gest_card, text='✋',
            font=ctk.CTkFont(size=64)
        )
        self.emoji_label.pack(pady=(20, 5))

        self.gest_label = ctk.CTkLabel(
            self.gest_card, text='NONE',
            font=ctk.CTkFont(size=22, weight="bold")
        )
        self.gest_label.pack()

        self.akcja_label = ctk.CTkLabel(
            self.gest_card, text='Nic',
            font=ctk.CTkFont(size=13),
            text_color='gray'
        )
        self.akcja_label.pack(pady=(4, 15))

        # Historia
        ctk.CTkLabel(
            tab, text="Historia gestów",
            font=ctk.CTkFont(size=12, weight="bold"),
            text_color="gray"
        ).pack(pady=(10, 4), anchor='w', padx=10)

        self.historia_label = ctk.CTkLabel(
            tab, text='—',
            font=ctk.CTkFont(size=12),
            wraplength=380
        )
        self.historia_label.pack(anchor='w', padx=10)

        # Przyciski testowe
        ctk.CTkLabel(
            tab, text="Test bez ESP32",
            font=ctk.CTkFont(size=12, weight="bold"),
            text_color="gray"
        ).pack(pady=(15, 6), anchor='w', padx=10)

        btn_frame = ctk.CTkFrame(tab, fg_color="transparent")
        btn_frame.pack(padx=10, fill='x')

        for litera, gest in LETTER_TO_GESTURE.items():
            info = GESTURE_INFO[gest]
            ctk.CTkButton(
                btn_frame,
                text=info['emoji'],
                font=ctk.CTkFont(size=18),
                width=44, height=44,
                corner_radius=10,
                fg_color=info['kolor'],
                hover_color=info['kolor'],
                command=lambda g=gest: self.aktualizuj_gest(g)
            ).pack(side='left', padx=3)

    def _zbuduj_konfiguracje(self):
        tab = self.tabs.tab("Konfiguracja")

        ctk.CTkLabel(
            tab,
            text="Przypisz akcję do każdego gestu:",
            font=ctk.CTkFont(size=13),
            text_color="gray"
        ).pack(pady=(10, 8), anchor='w', padx=10)

        lista_akcji = list(DOSTEPNE_AKCJE.keys())

        for gest, info in GESTURE_INFO.items():
            row = ctk.CTkFrame(tab, corner_radius=8, fg_color=info['kolor'])
            row.pack(pady=4, padx=10, fill='x')

            # Emoji i nazwa gestu
            ctk.CTkLabel(
                row,
                text=f"{info['emoji']}  {gest}",
                font=ctk.CTkFont(size=13, weight="bold"),
                width=160,
                anchor='w'
            ).pack(side='left', padx=12, pady=10)

            # Dropdown z akcjami
            dropdown = ctk.CTkOptionMenu(
                row,
                values=lista_akcji,
                width=200,
                font=ctk.CTkFont(size=12),
                command=lambda val, g=gest: self._zmien_akcje(g, val)
            )
            dropdown.set(self.konfiguracja.get(gest, 'Nic'))
            dropdown.pack(side='right', padx=12, pady=10)
            self.dropdowns[gest] = dropdown

        # Przyciski
        btn_frame = ctk.CTkFrame(tab, fg_color="transparent")
        btn_frame.pack(pady=15, padx=10, fill='x')

        ctk.CTkButton(
            btn_frame,
            text="Zapisz konfigurację",
            font=ctk.CTkFont(size=13, weight="bold"),
            height=40,
            command=self._zapisz
        ).pack(side='left', expand=True, fill='x', padx=(0, 5))

        ctk.CTkButton(
            btn_frame,
            text="Przywróć domyślne",
            font=ctk.CTkFont(size=13),
            height=40,
            fg_color='gray',
            hover_color='#555555',
            command=self._przywroc_domyslne
        ).pack(side='right', expand=True, fill='x', padx=(5, 0))

        self.save_label = ctk.CTkLabel(
            tab, text='',
            font=ctk.CTkFont(size=12),
            text_color='#2ecc71'
        )
        self.save_label.pack()

    def _zmien_akcje(self, gest, akcja):
        self.konfiguracja[gest] = akcja

    def _zapisz(self):
        zapisz_konfiguracje(self.konfiguracja)
        self.save_label.configure(text='✓ Zapisano!')
        self.after(2000, lambda: self.save_label.configure(text=''))

    def _przywroc_domyslne(self):
        self.konfiguracja = DOMYSLNA_KONFIGURACJA.copy()
        for gest, dropdown in self.dropdowns.items():
            dropdown.set(self.konfiguracja.get(gest, 'Nic'))
        zapisz_konfiguracje(self.konfiguracja)
        self.save_label.configure(text='✓ Przywrócono domyślne!')
        self.after(2000, lambda: self.save_label.configure(text=''))

    def aktualizuj_status(self, polaczono, tekst):
        kolor = '#2ecc71' if polaczono else '#e74c3c'
        self.status_dot.configure(text_color=kolor)
        self.status_label.configure(text=tekst)

    def aktualizuj_gest(self, gest):
        info = GESTURE_INFO.get(gest, GESTURE_INFO['NONE'])
        akcja_nazwa = self.konfiguracja.get(gest, 'Nic')

        self.gest_card.configure(fg_color=info['kolor'])
        self.emoji_label.configure(text=info['emoji'])
        self.gest_label.configure(text=gest)
        self.akcja_label.configure(text=akcja_nazwa)

        self.historia.append(info['emoji'])
        if len(self.historia) > 6:
            self.historia.pop(0)
        self.historia_label.configure(text='  →  '.join(self.historia))

        # Wykonaj akcję z konfiguracji
        akcja_fn = DOSTEPNE_AKCJE.get(akcja_nazwa)
        if akcja_fn:
            try:
                akcja_fn()
            except Exception as e:
                print(f"Błąd akcji: {e}")

# ============================================================
# BLUETOOTH
# ============================================================
def notification_handler(characteristic, data, app):
    litera = data.decode("utf-8").strip()
    gest = LETTER_TO_GESTURE.get(litera, 'NONE')
    app.after(0, lambda: app.aktualizuj_gest(gest))

async def run_ble(app):
    app.after(0, lambda: app.aktualizuj_status(False, 'Szukanie ESP32...'))

    device = await BleakScanner.find_device_by_filter(
        lambda d, ad: d.name == DEVICE_NAME
    )

    if not device:
        app.after(0, lambda: app.aktualizuj_status(False, 'Nie znaleziono ESP32!'))
        return

    app.after(0, lambda: app.aktualizuj_status(False, 'Łączenie...'))

    async with BleakClient(device) as client:
        if client.is_connected:
            app.after(0, lambda: app.aktualizuj_status(True, f'Połączono z {DEVICE_NAME}'))
            await client.start_notify(
                CHARACTERISTIC_UUID,
                lambda c, d: notification_handler(c, d, app)
            )
            try:
                while True:
                    await asyncio.sleep(1)
            except asyncio.CancelledError:
                pass
            finally:
                await client.stop_notify(CHARACTERISTIC_UUID)
        else:
            app.after(0, lambda: app.aktualizuj_status(False, 'Błąd połączenia!'))

def start_ble_thread(app):
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    loop.run_until_complete(run_ble(app))

# ============================================================
# MAIN
# ============================================================
if __name__ == "__main__":
    app = SpatialKeyApp()

    ble_thread = threading.Thread(
        target=start_ble_thread,
        args=(app,),
        daemon=True
    )
    ble_thread.start()

    app.mainloop()
