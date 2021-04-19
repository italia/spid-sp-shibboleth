Per una configurazione più future-proof prendere scaricare ed adattare i file originari da:

https://github.com/italia/spid-sp-access-button

La chiave del funzionamento sono i parametri GET 'entityID' (é lo entityID dello IdP url-encoded) e 'target' (dove ridirigere il risultato della autenticazione, sempre url-encoded).

Ad esempio un sp con entityID https://sp.example.org/sp per lanciare una autenticazione SPID con lo IdP di lepida e rimandare il browser in /secure:

<li class="spid-idp-button-link" data-idp="lepidaid">
                <a href="https://sp.example.org/Shibboleth.sso/Login?target=https%3A%2F%2Fsp.example.org%2Fsecure&entityID=https%3A%2F%2Fid.lepida.it%2Fidp%2Fshibboleth"><span class="spid-sr-only">Lepida ID</span><img src="img/spid-idp-lepidaid.svg" onerror="this.src='img/spid-idp-lepidaid.png'; this.onerror=null;" alt="Lepida ID" />
</a> 

Elenco dei content settings: https://wiki.shibboleth.net/confluence/display/SP3/ContentSettings .
