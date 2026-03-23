## Schemat działania

1. ESP32 zostaje połączone z Nucleo przy użyciu UARTa
   1. baudrate
   2. ile bitów
   3. parity?
2. Skrypt w Pythonie odpowiada za znalezienie ESP32 
   1. wybranie jakiejs nazwy idk
3. \


## Format wiadomości Nucleo $\rightarrow$ ESP32

Co będziemy dostawać z sieci?
    Osiem prawdopodobieństw na to jaki znak został pokazany, na tej podstawie możemy przepuszczać cały bitstream z Nucleo dalej, ale ma to taką wadę że jak będziemy chcieli to zrobić po BLE to będziemy niepotrzebnie obciążać komunikację $\rightarrow$ dlatego warto by było ją uprościć w taki sposób aby to Nucleo decydowało jaki znak został pokazany, a nastęnie została wysłana wiadomość np. cyfra od 0 do 7 albo jakieś litery TBD nie jest to teraz istotne
    

 