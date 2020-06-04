# Symulator Terminali RFID

Aplikacja symuluje użycia kart i terminali RFID i rejestruje czas pracy pracowników. Aplikacja wykorzystuje protokół MQTT do komunikacji między klientami (terminalami) i serwerem.

## Instalacja i konfiguracja

W celu uruchomienia programu konieczne jest zainstalowanie na maszynie brokera Mosquitto oraz
OpenSSL. Wymagana jest również odpowiednia konfiguracja brokera. Dokładne instrukcje można znaleźć tutaj:
[configuration.md](configuration.md)

## Uruchomienie symulatora - przykładowa procedura testowa



1. Otworzyć plik **config_file.py** np. za pomocą ulubionego edytora tekstowego. Następnie zmienić wartość pola ***broker*** na nazwę hosta.
2. Uruchomić plik **database_handling.py**.
Zostanie utworzona baza danych ***system_database.db*** z danymi testowymi.
Przy kolejnych uruchomieniach programu można pominąć ten krok.
3. Uruchomić plik **system_handling.py**.
Zostanie wyświetlone okienko ***System Handling***.
Za pomocą tego prostego interfejsu graficznego można zarządzać systemem i obserwować zmiany
w jego konfiguracji. Dodanie nowego terminala rejestruje terminal w bazie danych, jednak do
przetestowania jego działania, musimy ten terminal podłączyć. W niniejszej symulacji oznacza to
konieczność utworzenia pliku, którego treść może być skopiowana z pliku client.py ze
zmodyfikowanym jedynie terminal_id, na zgodny z dodanym.
Z poziomu tego interfejsu można również wygenerować raporty czasu pracy pracowników. Raporty
w formacie plików ***csv*** trafiają do katalogu **reports**.

**Przykładowy raport:**
```
Entry date,Entry time,Entry card,Entry terminal,Exit date,Exit time,Exit card,Exit terminal,Work time
14.04.2020,12:01:11,"[176, 111, 225, 37, 27]",T1,14.04.2020,20:10:15,"[176, 111, 225, 37, 27]",T2,8:09:04
15.04.2020,20:05:02,"[217, 125, 80, 211, 39]",T2,16.04.2020,04:01:11,"[217, 125, 80, 211, 39]",T1,7:56:09
17.04.2020,08:01:21,"[217, 125, 80, 211, 39]",T1,17.04.2020,16:11:09,"[217, 125, 80, 211, 39]",T2,8:09:48
18.04.2020,08:00:42,"[217, 125, 80, 211, 39]",T1,18.04.2020,16:02:01,"[217, 125, 80, 211, 39]",T1,8:01:19
07.05.20,14:08:13,"[176, 111, 225, 37, 27]",T1,07.05.20,14:08:25,"[176, 111, 225, 37, 27]",T1,0:00:12
```
4. Po ewentualnym dokonaniu zmian należy zamknąć okienko ***System Handling***.
5. Uruchomić **server.py**.
Zostanie wyświetlone okienko Server, na którym można obserwować komunikaty
otrzymywane od podłączonych do systemu terminali.

6. Uruchomić **client.py**, i/lub inne pliki, które symulują działanie terminali.

***UWAGA!***
***Program wykorzystuje moduł keyboard i może być konieczna jego instalacja:***

`pip install keyboard`

Dla każdego terminala zostanie wyświetlone okienko ***ClientT<terminal_id>***.
Aby zasymulować przyłożenie karty do terminala należy najpierw ustawić focus na okienko
odpowiadające terminalowi, którego chcemy używać. Następnie należy wybrać używaną
kartę, a potem wcisnąć spację na klawiaturze. Spowoduje to wysłanie przez wybranego klienta
(wybrany terminal) informacji o swoim identyfikatorze i identyfikatorze użytej karty. Serwer
otrzyma wiadomość, jeśli nadawca wiadomości (terminal) jest podłączony do systemu.
Następnie nastąpi zapisanie logu do bazy danych z informacjami o czasie, karcie, terminalu
i pracowniku.
Zaznaczenie opcji ***Unknown card*** symuluje użycie nieznanej systemowi karty. Id takiej karty
jest losowe, choć w praktyce byłoby ono odczytane z karty.
Na tym etapie można już obserwować
komunikację klientów z serwerem za
pośrednictwem otworzonego wcześniej okienka
***Server***.

7. Zamknąć okna klientów poprzez wciśnięcie
przycisku ***esc*** na klawiaturze

8. Zamknąć okno ***Server***.

## Aneks
W katalogu **app** znajdują się pliki z właściwym kodem aplikacji:
- **config_file.py** – plik, który umożliwia skonfigurowanie programu tak, by uruchamiał się na wybranej maszynie
- **database_handling.py** – w tym pliku znajdują się funkcje do tworzenia bazy danych systemu, a także edycji oraz odczytu z tej bazy danych. Po uruchomieniu tego pliku utworzona zostanie testowa baza danych.
- **system_handling.py** – moduł umożliwiający zarządzanie systemem. W tym pliku znajdują się funkcje do zarządzania systemem . Po uruchomieniu tego pliku wyświetli się okienko z prostym interfejsem użytkownika pozwalające m.in. na przyłączenie do systemu lub usunięcie z systemu terminali, przypisanie karty do pracownika, usunięcie przypisania karty do pracownika, wygenerowanie raportu czasu pracy pracownika.
- **server.py** – część serwera pełniąca rolę brokera. W tym pliku znajdują się funkcje konieczne do przetworzenia wiadomości od klientów. Po uruchomieniu tego pliku wyświetli się proste okienko, w którym będą wyświetlane wiadomości od przyłączonych klientów.
- **client.py** – w tym pliku znajduje się kod, który byłby implementowany na rzeczywistych terminalach RFID. Po uruchomieniu tego pliku wyświetli się proste okienko umożliwiające symulację przyłożenia karty do terminala.
- **reports_handling.py** – w tym pliku znajdują się funkcje umożliwiające wygenerowanie raportu czasu pracy pracownika.

W katalogu **conf_files** znajdują się pliki konfiguracyjne, które są konieczne do prawidłowego działania programu działania programu.