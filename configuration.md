# Konfiguracja
W celu uruchomienia programu konieczne jest zainstalowanie na maszynie brokera Mosquitto oraz
OpenSSL. Wymagane jest również konfiguracja, której kolejne etapy są przedstawione poniżej.
1. W celu wygenerowania kluczy dla certyfikatu uwierzytelnienia (CA) w terminalu należy wydać
polecenie:
`openssl genrsa -des3 -out ca.key 2048`
2. W celu utworzenia certyfikatu uwierzytelnienia (CA) za pomocą uprzednio utworzonych kluczy
należy wydać polecenie:
`openssl req -new -x509 -days 1826 -key ca.key -out ca.crt`
3. W celu utworzenia pary kluczy, która będzie używana przez broker należy wydać polecenie:
`openssl genrsa -out server.key 2048`
4. W celu utworzenie żądania podpisania certyfikatu należy wydać polecenie:
`openssl req -new -out server.csr -key server.key`
Podczas wypełniania formularza należy podać wartość pola *„Common Name”* jako
nazwę maszyny, na której działa Mosquitto, np.: *DESKTOP-9P31MIM* 
5. W celu zweryfikowania i podpisania certyfikatu serwera należy wydać polecenie:
`openssl x509 -req -in server.csr -CA ca.crt -Cakey`
Po wykonaniu powyższych kroków powstaną pliki:

**ca.crt, ca.key, ca.srl, server.crt, server.csr, server.key**
6. W folderze instalacyjnym Mosquitto należy dodać folder certs i skopiować do niego pliki
**ca.crt, server.crt i server.key.**
7. Do folderu app, w którym znajdują się pliki programu skopiować plik **ca.crt**.
8. Do folderu instalacyjnego Mosquitto dodać załączone do programu pliki **passwd.conf** oraz
**aclfile.conf** (znajdują się one w folderze **conf_files**).

9. W folderze instalacyjnym Mosquitto znajduje się plik **mosquitto.conf**, w którym należy
dokonać następujących zmian:
 - W sekcji __*# Default listener*__:
```
[…]
# Port to use for the default listener.
port 8883
```
- W sekcji ***# Certificate based SSL/TLS support*** należy podać ścieżki do plików **ca.crt,
server.crt, server.key**, na przykład:
```
[…]
cafile c:\Program Files\mosquitto\certs\ca.crt
#capath
# Path to the PEM encoded server certificate.
certfile c:\Program Files\mosquitto\certs\server.crt
# Path to the PEM encoded keyfile.
keyfile c:\Program Files\mosquitto\certs\server.key
```
- W sekcji ***# Security***:
```
[…]
allow_anonymous false
```
- W sekcji ***# Default authentication and topic access control*** należy podać ścieżkę do
pliku **passwd.conf**, na przykład:
```
[…]
password_file c:\Program Files\mosquitto\passwd.conf
```
- W sekcji ***# Default authentication and topic access control*** należy podać ścieżkę do
pliku **aclfile.conf**, na przykład:
```
[…]
acl_file c:\Program Files\mosquitto\aclfile.conf
```

10. Zrestartować usługę Mosquitto Broker.