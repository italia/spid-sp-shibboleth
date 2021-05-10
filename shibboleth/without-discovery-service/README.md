# Configuration for _Form_-based SessionInitiator

This Shibboleth SP configuration represents an alternative to the base strategy, which **does not require an external Discovery Service**.

__Note__: It represents just an example that should be customized on user needs.

It uses the `Form` SessionInitiator functionality (https://wiki.shibboleth.net/confluence/display/SP3/Form+SessionInitiator) provided by Shibboleth SP which 
allows configuring the SessionInitiator using a user-defined HTML form.

The file [shibboleth2.xml](shibboleth2.xml) contains the example configuration where the only modifications w.r.t. the original one contained in this repo
are the following:

From:
```
            <SessionInitiator type="SAML2"
                              id="Login"
                              Location="/Login"
                              isDefault="true"
                              outgoingBinding="urn:oasis:names:tc:SAML:profiles:SSO:request-init"
                              isPassive="false"
                              acsIndex="0"
                              acsByIndex="true"
                              signing="true">
                <samlp:AuthnRequest xmlns:samlp="urn:oasis:names:tc:SAML:2.0:protocol"
                                    xmlns:saml="urn:oasis:names:tc:SAML:2.0:assertion"
                                    ID="id..."
                                    Version="2.0"
                                    IssueInstant="2017-01-01T00:00:00Z"
                                    AttributeConsumingServiceIndex="0"
                                    ForceAuthn="true">
                    <!-- if NameQualifier is different from entityID, you need to update security-policy.xml -->
                    <saml:Issuer NameQualifier="https://{sp_fqdn}/shibboleth"
                                 Format="urn:oasis:names:tc:SAML:2.0:nameid-format:entity"
                    >https://{sp_fqdn}/shibboleth
                    </saml:Issuer>
                    <samlp:NameIDPolicy Format="urn:oasis:names:tc:SAML:2.0:nameid-format:transient"/>
                </samlp:AuthnRequest>
            </SessionInitiator>
```

To:
```
            <SessionInitiator type="Chaining" id="idpchooser" Location="/Login">
               <SessionInitiator type="SAML2" 
                                 id="Login" 
                                 outgoingBinding="urn:oasis:names:tc:SAML:profiles:SSO:request-init" 
                                 isPassive="false" 
                                 acsIndex="0" 
                                 acsByIndex="true" 
                                 signing="true">
                  <samlp:AuthnRequest xmlns:samlp="urn:oasis:names:tc:SAML:2.0:protocol"
                                    xmlns:saml="urn:oasis:names:tc:SAML:2.0:assertion"
                                    ID="id..."
                                    Version="2.0"
                                    IssueInstant="2017-01-01T00:00:00Z"
                                    AttributeConsumingServiceIndex="0"
                                    ForceAuthn="true">
                     <!-- if NameQualifier is different from entityID, you need to update security-policy.xml -->
                     <saml:Issuer NameQualifier="https://{sp_fqdn}/shibboleth"
                                 Format="urn:oasis:names:tc:SAML:2.0:nameid-format:entity"
                     >https://{sp_fqdn}/shibboleth
                     </saml:Issuer>
                     <samlp:NameIDPolicy Format="urn:oasis:names:tc:SAML:2.0:nameid-format:transient" />
                  </samlp:AuthnRequest>
               </SessionInitiator>
              
               <SessionInitiator type="Form" template="discoveryTemplate.html" />
            </SessionInitiator>          
```

### Explanation

Instead of using just a basic `SAML2` SessionInitiator, a `Chaining` SessionInitiator is used. It wraps the standard `SAML2` initiator (where `isDefault="true"` 
is absent) and the `Form` initiator, provided by an HTML file (in the example [discoveryTemplate.html](discoveryTemplate.html)) which contains the SPID button, 
along with a few lines of JS code.

Thus, as a Login Request is made, the Form template is shown to the user. Basing on their selection, the proper entityID for the 
chosen IDP (which must be a known one) is set and the control is passed back to the SAML2 initiator, which continues SSO as usual.
