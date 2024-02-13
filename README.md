# Fakturyfy.py

Základní nástroj pro tvorbu faktur a správu subjektů pro OSVČ. Většinu implementace jsme sepsali během soukromého dvoudenního "hackathonu", jde o webovou nadstavbu nad forkem projektu [InvoiceGenerator](https://github.com/by-cx/InvoiceGenerator). Návrhy, opravy a vylepšení jsou vítány.

Službu můžete nasadit čistě lokálně nebo na Vaší lokální síti, **služba s žádným jiným způsobem nasazení nepočítá** - chybí login či jakékoliv jiné zabezpečení přístupu. Nesnažíme se stvořit další účetní systém, jde o jednoduchý nástroj.


## Instalace

Celá služba je zabalena do jednoho docker containeru, jehož image je dostupný na [docker hub](https://hub.docker.com/repository/docker/manakjiri/fakturyfy), tudíž je možné ji nasadit jedním příkazem
```sh
docker run manakjiri/fakturyfy:latest
```

Služba uchovává uživatelská data v adresáři `/data` uvnitř containeru, **tuto cestu namapujte mimo container** použitím funkce volume, tak jak je to v příkazu výše, cestu si upravte dle potřeby.
- Můžete ji například navést do NFS adresáře na lokálním NAS úložišti, které je ideálně navázáno na offsite backup a poskytuje rollback, tak to používáme my


