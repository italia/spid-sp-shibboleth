# spid-sp-shibboleth
Middleware SPID basato su Shibboleth

Questo progetto contiene un setup dimostrativo composto dai seguenti componenti:

- Shibboleth SP
- Progetto PHP di esempio
- Configurazione di Apache2 con mod_shib
- installazione di [spid-sp-test](https://github.com/italia/spid-sp-test)

I seguenti passaggi saranno descritti:

1. eseguire spid-saml-check tramite Docker
2. scaricare i metadata di spid-saml-check nella directory `/etc/shibboleth/metadata/spid-saml-check.xml`, come definito in shibboleth2.xml
3. creare i metadata e firmarli


