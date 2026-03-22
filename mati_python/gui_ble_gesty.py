import asyncio
import threading
import tkinter as tk
from tkinter import font
from bleak import BleakClient, BleakScanner
from bleak.backends.characteristic import BleakGATTCharacteristic
from pynput.keyboard import Key, Controller as KeyboardController
from pynput.mouse import Button, Controller as MouseController

# ============================================================
# KONFIGURACJA
# ============================================================
DEVICE_NAME = "ESP32_Button_Sender"
CHARACTERISTIC_UUID = "6E400003-B5A3-F393-E0A9-E50E24DCCA9E"

keyboard = KeyboardController()
mouse = MouseController()

# Mapowanie liter na gesty
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

# Ikony i kolory dla każdego gestu
GESTURE_INFO = {
    'NONE':       {'emoji': '✋', 'kolor': '#95a5a6', 'akcja': 'Brak akcji'},
    'FLAT_HAND':  {'emoji': '🖐', 'kolor': '#3498db', 'akcja': 'Play / Pause'},
    'LIKE':       {'emoji': '👍', 'kolor': '#2ecc71', 'akcja': 'Głośniej'},
    'DISLIKE':    {'emoji': '👎', 'kolor': '#e74c3c', 'akcja': 'Ciszej'},
    'FIST':       {'emoji': '✊', 'kolor': '#e67e22', 'akcja': 'Następny utwór'},
    'LOVE':       {'emoji': '🤟', 'kolor': '#e91e8c', 'akcja': 'Poprzedni utwór'},
    'BREAKTIME':  {'emoji': '✌️', 'kolor': '#f1c40f', 'akcja': 'Kliknięcie myszy'},
    'CROSSHANDS': {'emoji': '🤞', 'kolor': '#9b59b6', 'akcja': 'Przewijanie w górę'},
}

# ============================================================
# AKCJE
# ============================================================
def wykonaj_akcje(gest):
    if gest == 'FLAT_HAND':
        keyboard.press(Key.media_play_pause)
        keyboard.release(Key.media_play_pause)
    elif gest == 'LIKE':
        keyboard.press(Key.media_volume_up)
        keyboard.release(Key.media_volume_up)
    elif gest == 'DISLIKE':
        keyboard.press(Key.media_volume_down)
        keyboard.release(Key.media_volume_down)
    elif gest == 'FIST':
        keyboard.press(Key.media_next)
        keyboard.release(Key.media_next)
    elif gest == 'LOVE':
        keyboard.press(Key.media_previous)
        keyboard.release(Key.media_previous)
    elif gest == 'BREAKTIME':
        mouse.click(Button.left, 1)
    elif gest == 'CROSSHANDS':
        mouse.scroll(0, 3)

# ============================================================
# GUI
# ============================================================
class SpatialKeyGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("SpatialKey")
        self.root.geometry("400x550")
        self.root.configure(bg='#1a1a2e')
        self.root.resizable(False, False)

        self.historia = []
        self.aktualny_gest = 'NONE'

        self._zbuduj_gui()

    def _zbuduj_gui(self):
        # Tytuł
        tk.Label(
            self.root, text="SpatialKey",
            font=('Helvetica', 24, 'bold'),
            bg='#1a1a2e', fg='white'
        ).pack(pady=(20, 5))

        tk.Label(
            self.root, text="Sterowanie gestami dłoni",
            font=('Helvetica', 11),
            bg='#1a1a2e', fg='#7f8c8d'
        ).pack()

        # Status połączenia
        self.status_frame = tk.Frame(self.root, bg='#1a1a2e')
        self.status_frame.pack(pady=15)

        self.status_dot = tk.Label(
            self.status_frame, text='●',
            font=('Helvetica', 14),
            bg='#1a1a2e', fg='#e74c3c'
        )
        self.status_dot.pack(side='left', padx=5)

        self.status_label = tk.Label(
            self.status_frame, text='Szukanie ESP32...',
            font=('Helvetica', 12),
            bg='#1a1a2e', fg='white'
        )
        self.status_label.pack(side='left')

        # Karta gestu
        self.gest_frame = tk.Frame(
            self.root, bg='#95a5a6',
            width=300, height=200
        )
        self.gest_frame.pack(pady=10, padx=40, fill='x')
        self.gest_frame.pack_propagate(False)

        self.emoji_label = tk.Label(
            self.gest_frame, text='✋',
            font=('Helvetica', 64),
            bg='#95a5a6'
        )
        self.emoji_label.pack(pady=(20, 5))

        self.gest_label = tk.Label(
            self.gest_frame, text='NONE',
            font=('Helvetica', 20, 'bold'),
            bg='#95a5a6', fg='white'
        )
        self.gest_label.pack()

        self.akcja_label = tk.Label(
            self.gest_frame, text='Brak akcji',
            font=('Helvetica', 12),
            bg='#95a5a6', fg='white'
        )
        self.akcja_label.pack(pady=(2, 15))

        # Historia
        tk.Label(
            self.root, text="Historia gestów:",
            font=('Helvetica', 11, 'bold'),
            bg='#1a1a2e', fg='#7f8c8d'
        ).pack(pady=(15, 5), anchor='w', padx=40)

        self.historia_label = tk.Label(
            self.root, text='—',
            font=('Helvetica', 11),
            bg='#1a1a2e', fg='white',
            wraplength=320
        )
        self.historia_label.pack(padx=40, anchor='w')

        # Przyciski testowe
        tk.Label(
            self.root, text="Test bez ESP32:",
            font=('Helvetica', 11, 'bold'),
            bg='#1a1a2e', fg='#7f8c8d'
        ).pack(pady=(20, 8), anchor='w', padx=40)

        btn_frame = tk.Frame(self.root, bg='#1a1a2e')
        btn_frame.pack(padx=40, fill='x')

        for litera, gest in LETTER_TO_GESTURE.items():
            info = GESTURE_INFO[gest]
            btn = tk.Button(
                btn_frame,
                text=f"{info['emoji']}",
                font=('Helvetica', 18),
                bg='#16213e', fg='white',
                relief='flat', bd=0,
                cursor='hand2',
                command=lambda g=gest: self.aktualizuj_gest(g)
            )
            btn.pack(side='left', padx=3)

    def aktualizuj_status(self, polaczono, tekst):
        kolor = '#2ecc71' if polaczono else '#e74c3c'
        self.status_dot.configure(fg=kolor)
        self.status_label.configure(text=tekst)

    def aktualizuj_gest(self, gest):
        info = GESTURE_INFO.get(gest, GESTURE_INFO['NONE'])

        self.gest_frame.configure(bg=info['kolor'])
        self.emoji_label.configure(text=info['emoji'], bg=info['kolor'])
        self.gest_label.configure(text=gest, bg=info['kolor'])
        self.akcja_label.configure(text=info['akcja'], bg=info['kolor'])

        # Aktualizuj historię
        self.historia.append(gest)
        if len(self.historia) > 5:
            self.historia.pop(0)
        self.historia_label.configure(
            text=' → '.join(self.historia)
        )

        # Wykonaj akcję
        if gest != 'NONE':
            wykonaj_akcje(gest)

# ============================================================
# BLUETOOTH
# ============================================================
def notification_handler(characteristic, data, gui):
    litera = data.decode("utf-8").strip()
    gest = LETTER_TO_GESTURE.get(litera, 'NONE')
    gui.root.after(0, lambda: gui.aktualizuj_gest(gest))

async def run_ble(gui):
    gui.root.after(0, lambda: gui.aktualizuj_status(False, 'Szukanie ESP32...'))

    device = await BleakScanner.find_device_by_filter(
        lambda d, ad: d.name == DEVICE_NAME
    )

    if not device:
        gui.root.after(0, lambda: gui.aktualizuj_status(False, 'Nie znaleziono ESP32!'))
        return

    gui.root.after(0, lambda: gui.aktualizuj_status(False, 'Łączenie...'))

    async with BleakClient(device) as client:
        if client.is_connected:
            gui.root.after(0, lambda: gui.aktualizuj_status(True, f'Połączono z {DEVICE_NAME}'))

            await client.start_notify(
                CHARACTERISTIC_UUID,
                lambda c, d: notification_handler(c, d, gui)
            )

            try:
                while True:
                    await asyncio.sleep(1)
            except asyncio.CancelledError:
                pass
            finally:
                await client.stop_notify(CHARACTERISTIC_UUID)
        else:
            gui.root.after(0, lambda: gui.aktualizuj_status(False, 'Błąd połączenia!'))

def start_ble_thread(gui):
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    loop.run_until_complete(run_ble(gui))

# ============================================================
# MAIN
# ============================================================
if __name__ == "__main__":
    root = tk.Tk()
    gui = SpatialKeyGUI(root)

    # Uruchom Bluetooth w osobnym wątku
    ble_thread = threading.Thread(
        target=start_ble_thread,
        args=(gui,),
        daemon=True
    )
    ble_thread.start()

    root.mainloop()