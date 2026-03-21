import asyncio
import threading
import customtkinter as ctk
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
    'NONE':       {'emoji': '✋', 'kolor': '#4a4a6a', 'akcja': 'Brak akcji'},
    'FLAT_HAND':  {'emoji': '🖐', 'kolor': '#1a6fa8', 'akcja': 'Play / Pause'},
    'LIKE':       {'emoji': '👍', 'kolor': '#1a8a4a', 'akcja': 'Głośniej'},
    'DISLIKE':    {'emoji': '👎', 'kolor': '#a83232', 'akcja': 'Ciszej'},
    'FIST':       {'emoji': '✊', 'kolor': '#a86b1a', 'akcja': 'Następny utwór'},
    'LOVE':       {'emoji': '🤟', 'kolor': '#a8186e', 'akcja': 'Poprzedni utwór'},
    'BREAKTIME':  {'emoji': '✌️', 'kolor': '#8a8a1a', 'akcja': 'Kliknięcie myszy'},
    'CROSSHANDS': {'emoji': '🤞', 'kolor': '#6a1aa8', 'akcja': 'Przewijanie w górę'},
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
ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

class SpatialKeyApp(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("SpatialKey")
        self.geometry("420x680")
        self.resizable(False, False)

        self.historia = []

        self._zbuduj_gui()

    def _zbuduj_gui(self):
        # Tytuł
        ctk.CTkLabel(
            self,
            text="SpatialKey",
            font=ctk.CTkFont(size=32, weight="bold")
        ).pack(pady=(30, 0))

        ctk.CTkLabel(
            self,
            text="Sterowanie gestami dłoni",
            font=ctk.CTkFont(size=13),
            text_color="gray"
        ).pack(pady=(4, 0))

        # Status połączenia
        self.status_frame = ctk.CTkFrame(self, corner_radius=10)
        self.status_frame.pack(pady=20, padx=30, fill='x')

        self.status_dot = ctk.CTkLabel(
            self.status_frame,
            text='●',
            font=ctk.CTkFont(size=16),
            text_color='#e74c3c'
        )
        self.status_dot.pack(side='left', padx=(15, 5), pady=12)

        self.status_label = ctk.CTkLabel(
            self.status_frame,
            text='Szukanie ESP32...',
            font=ctk.CTkFont(size=13)
        )
        self.status_label.pack(side='left', pady=12)

        # Karta gestu
        self.gest_card = ctk.CTkFrame(
            self,
            corner_radius=20,
            fg_color='#4a4a6a',
            height=220
        )
        self.gest_card.pack(pady=10, padx=30, fill='x')
        self.gest_card.pack_propagate(False)

        self.emoji_label = ctk.CTkLabel(
            self.gest_card,
            text='✋',
            font=ctk.CTkFont(size=72)
        )
        self.emoji_label.pack(pady=(25, 5))

        self.gest_label = ctk.CTkLabel(
            self.gest_card,
            text='NONE',
            font=ctk.CTkFont(size=24, weight="bold")
        )
        self.gest_label.pack()

        self.akcja_label = ctk.CTkLabel(
            self.gest_card,
            text='Brak akcji',
            font=ctk.CTkFont(size=14),
            text_color='gray'
        )
        self.akcja_label.pack(pady=(4, 20))

        # Historia
        ctk.CTkLabel(
            self,
            text="Historia gestów",
            font=ctk.CTkFont(size=13, weight="bold"),
            text_color="gray"
        ).pack(pady=(15, 5), anchor='w', padx=30)

        self.historia_label = ctk.CTkLabel(
            self,
            text='—',
            font=ctk.CTkFont(size=13),
            wraplength=360
        )
        self.historia_label.pack(anchor='w', padx=30)

        # Przyciski testowe
        ctk.CTkLabel(
            self,
            text="Test bez ESP32",
            font=ctk.CTkFont(size=13, weight="bold"),
            text_color="gray"
        ).pack(pady=(20, 8), anchor='w', padx=30)

        btn_frame = ctk.CTkFrame(self, fg_color="transparent")
        btn_frame.pack(padx=30, fill='x')

        for litera, gest in LETTER_TO_GESTURE.items():
            info = GESTURE_INFO[gest]
            btn = ctk.CTkButton(
                btn_frame,
                text=info['emoji'],
                font=ctk.CTkFont(size=20),
                width=44,
                height=44,
                corner_radius=10,
                fg_color=info['kolor'],
                hover_color=info['kolor'],
                command=lambda g=gest: self.aktualizuj_gest(g)
            )
            btn.pack(side='left', padx=3)

    def aktualizuj_status(self, polaczono, tekst):
        kolor = '#2ecc71' if polaczono else '#e74c3c'
        self.status_dot.configure(text_color=kolor)
        self.status_label.configure(text=tekst)

    def aktualizuj_gest(self, gest):
        info = GESTURE_INFO.get(gest, GESTURE_INFO['NONE'])

        self.gest_card.configure(fg_color=info['kolor'])
        self.emoji_label.configure(text=info['emoji'])
        self.gest_label.configure(text=gest)
        self.akcja_label.configure(text=info['akcja'])

        self.historia.append(info['emoji'])
        if len(self.historia) > 6:
            self.historia.pop(0)
        self.historia_label.configure(
            text='  →  '.join(self.historia)
        )

        if gest != 'NONE':
            wykonaj_akcje(gest)

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
