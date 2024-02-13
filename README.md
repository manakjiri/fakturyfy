# Fakturyfy.py

Základní nástroj pro tvorbu faktur a správu subjektů pro OSVČ. Většinu implementace jsme sepsali během soukromého dvoudenního "hackathonu", jde o webovou nadstavbu nad forkem projektu [InvoiceGenerator](https://github.com/by-cx/InvoiceGenerator). Návrhy, opravy a vylepšení jsou vítány.

![priklad](/docs/faktura.png)

Službu můžete nasadit čistě lokálně nebo na Vaší lokální síti, **služba s žádným jiným způsobem nasazení nepočítá** - chybí login či jakékoliv jiné zabezpečení přístupu. Nesnažíme se stvořit další účetní systém, jde o jednoduchý nástroj.

Veškerá data jsou uložena v sqlite databázi (definice subjektů) a vygenerované faktury jsou ukládány přehledně do složek jako vygenerované soubory PDF.

## Instalace

[![Publish Docker image](https://github.com/manakjiri/fakturyfy/actions/workflows/docker-push.yaml/badge.svg?branch=main)](https://github.com/manakjiri/fakturyfy/actions/workflows/docker-push.yaml)

Celá služba je zabalena do jednoho docker containeru, jehož image je dostupný na [docker hub](https://hub.docker.com/repository/docker/manakjiri/fakturyfy), tudíž je možné ji spustit příkazem
```sh
docker run --rm --name fakturyfy --volume ./fakturyfy-data:/data --publish 8000 manakjiri/fakturyfy:main
```
služba bude dostupná na [http://localhost:8000/](http://localhost:8000/).

Služba uchovává uživatelská data v adresáři `/data` uvnitř containeru, **tuto cestu namapujte mimo container** skrze volume tak, jak je to v příkazu výše, cestu si upravte dle potřeby.
- Můžete ji například navést do NFS adresáře na lokálním NAS úložišti, které je ideálně navázáno na offsite backup a poskytuje rollback, tak to používáme my

Novou verzi můžete stáhnout pomocí `docker pull manakjiri/fakturyfy:main`, kód bude shodný s tím, který je aktuálně na [main](https://github.com/manakjiri/fakturyfy/tree/main).


## Ukázky

Správa faktur
![](/docs/sprava_faktur.png)
Tvorba faktury
![](/docs/tvorba_faktury.png)

Správa subjektů
![](/docs/sprava_subjektu.png)
Tvorba subjektu
![](/docs/tvorba_subjektu.png)

