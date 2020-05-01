# Terminal RFID

Aplikacja symuluje użycia kart i terminali RFID i rejestruje czas pracy pracowników. Aplikacja wykorzystuje protokół MQTT do komunikacji między klientami (terminalami) i serwerem.

## Instrukcja
Na początku należy uruchomić plik `database_handling.py` w celu utworzenia bazy danych z danymi testowym. Można zrezygnować z utworzenia bazy testowej - w takim wypadku utworzona zostanie pusta baza danych, a dodanie wszelkich danych będzie zależne od działań użytkownika. W przypadku, kiedy chcemy jedynie przetestować działanie programu zalecane jest jednak użycie danych testowych, co usprawni proces.

Następnie należy uruchomić plik `system_handling.py` i skonfigurować ustawienia systemu zgodnie za swoimi preferencjami.

Następnie należy uruchomić plik `server.py`

Następnie należy uruchomić klientów - terminale. W niniejszej symulacji należy uruchomić pliki `client1.py` oraz `client2.py`.

## Raporty

Raporty są generowane dla konkretnego pracownika do pliku csv i trafiają one do folderu reports. Przechowują one następujące informacje:

- *Entry date* – data wejścia pracownika do pracy
- *Entry time* – godzina wejścia pracownika do pracy
- *Entry card* – identyfikator karty, która została użyta przy wejściu do pracy
- *Entry terminal* – identyfikator terminala, który został użyty przy wejściu do pracy
- *Exit date* – data wyjścia pracownika z pracy
- *Exit time* – godzina wyjścia pracownika z pracy
- *Exit card* – identyfikator karty, która została użyta przy wyjściu z pracy
- *Exit terminal* – identyfikator terminala, który został użyty przy wyjściu z pracy
- *Work time* – czas od wejścia pracownika do pracy do wyjścia pracownika z pracy




