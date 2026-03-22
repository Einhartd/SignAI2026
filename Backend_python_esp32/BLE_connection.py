import asyncio
from bleak import BleakClient, BleakScanner

# Nazwa musi być identyczna z tą w kodzie ESP32!
DEVICE_NAME = "SignAI_Gesture_Interface"
CHARACTERISTIC_UUID = "6E400003-B5A3-F393-E0A9-E50E24DCCA9E"


def notification_handler(sender, data):
    """Wywoływane, gdy ESP32 wyśle bajt przez Bluetooth."""
    try:
        # Dekodujemy otrzymany bajt na znak (char)
        char_received = data.decode('utf-8')
        print(f"-> GEST ODEBRANY: {char_received} (kod ASCII: {data[0]})")
    except Exception as e:
        print(f"-> Odebrano nieczytelne dane: {data.hex()}")


async def main():
    print(f"[*] Szukanie urządzenia '{DEVICE_NAME}'...")

    device = await BleakScanner.find_device_by_filter(
        lambda d, ad: d.name == DEVICE_NAME, timeout=10.0
    )

    if not device:
        print("[!] Nie znaleziono urządzenia. Upewnij się, że ESP32 działa.")
        return

    print(f"[*] Znaleziono: {device.address}. Łączenie...")

    async with BleakClient(device) as client:
        if client.is_connected:
            print("[+] POŁĄCZONO! Nasłuchuję gestów...")

            # Start subskrypcji powiadomień
            await client.start_notify(CHARACTERISTIC_UUID, notification_handler)

            # Pętla podtrzymująca działanie programu
            try:
                while True:
                    await asyncio.sleep(1)
            except KeyboardInterrupt:
                print("\n[*] Rozłączanie...")
                await client.stop_notify(CHARACTERISTIC_UUID)


if __name__ == "__main__":
    asyncio.run(main())