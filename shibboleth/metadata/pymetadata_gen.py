import random
import string
import subprocess

metadata_tmpl = """
<md:EntityDescriptor
    xmlns:ds="http://www.w3.org/2000/09/xmldsig#"
    xmlns:md="urn:oasis:names:tc:SAML:2.0:metadata"
    xmlns:spid="https://spid.gov.it/saml-extensions"
    entityID="{entityid}"
    ID="id-{id}">

    <ds:Signature Id="Signature1">
        <ds:SignedInfo>
            <ds:CanonicalizationMethod Algorithm="http://www.w3.org/2001/10/xml-exc-c14n#" />
            <ds:SignatureMethod Algorithm="http://www.w3.org/2001/04/xmldsig-more#rsa-sha256" />
            <ds:Reference URI="#id-{id}">
                <ds:Transforms>
                    <ds:Transform Algorithm="http://www.w3.org/2000/09/xmldsig#enveloped-signature" />
                    <ds:Transform Algorithm="http://www.w3.org/2001/10/xml-exc-c14n#" />
                </ds:Transforms>
                <ds:DigestMethod Algorithm="http://www.w3.org/2001/04/xmlenc#sha256" />
                    <ds:DigestValue />
            </ds:Reference>
        </ds:SignedInfo>
        <ds:SignatureValue />
        <ds:KeyInfo>
            <ds:X509Data>
                <ds:X509Certificate>{certificate_sign}</ds:X509Certificate>
            </ds:X509Data>
        </ds:KeyInfo>
    </ds:Signature>

    <md:SPSSODescriptor protocolSupportEnumeration="urn:oasis:names:tc:SAML:2.0:protocol" AuthnRequestsSigned="true" WantAssertionsSigned="true">
        <md:KeyDescriptor use="signing">
            <ds:KeyInfo>
                <ds:X509Data>
                    <ds:X509Certificate>{certificate_sign}</ds:X509Certificate>
                </ds:X509Data>
            </ds:KeyInfo>
        </md:KeyDescriptor>
        <md:KeyDescriptor use="encryption">
            <ds:KeyInfo>
                <ds:X509Data>
                    <ds:X509Certificate>{certificate_enc}</ds:X509Certificate>
                </ds:X509Data>
            </ds:KeyInfo>
        </md:KeyDescriptor>
        <md:SingleLogoutService Binding="urn:oasis:names:tc:SAML:2.0:bindings:HTTP-POST" Location="{entity_url}/{sso_post_path}"/>
        <md:NameIDFormat>
            urn:oasis:names:tc:SAML:2.0:nameid-format:transient
        </md:NameIDFormat>
        <md:AssertionConsumerService Binding="urn:oasis:names:tc:SAML:2.0:bindings:HTTP-POST" Location="{entity_url}/{acs_path}" index="0" isDefault="true"/>
        <md:AttributeConsumingService index="0">
        <md:ServiceName xml:lang="it">{metadata_url}</md:ServiceName>
        <md:RequestedAttribute Name="spidCode" isRequired="true"/>
        <md:RequestedAttribute Name="name" isRequired="true"/>
        <md:RequestedAttribute Name="familyName" isRequired="true"/>
        <md:RequestedAttribute Name="fiscalNumber" isRequired="true"/>
        <md:RequestedAttribute Name="email" isRequired="true"/>
        <md:RequestedAttribute Name="gender" isRequired="false"/>
        <md:RequestedAttribute Name="companyName" isRequired="false"/>
        <md:RequestedAttribute Name="registeredOffice" isRequired="false"/>
        <md:RequestedAttribute Name="ivaCode" isRequired="false"/>
        <md:RequestedAttribute Name="idCard" isRequired="false"/>
        <md:RequestedAttribute Name="digitalAddress" isRequired="false"/>
        <md:RequestedAttribute Name="placeOfBirth" isRequired="false"/>
        <md:RequestedAttribute Name="countyOfBirth" isRequired="false"/>
        <md:RequestedAttribute Name="dateOfBirth" isRequired="false"/>
        <md:RequestedAttribute Name="address" isRequired="false"/>
        <md:RequestedAttribute Name="mobilePhone" isRequired="false"/>
        <md:RequestedAttribute Name="expirationDate" isRequired="false"/>
        </md:AttributeConsumingService>
    </md:SPSSODescriptor>

    <md:Organization>
        <md:OrganizationName xml:lang="it">Example</md:OrganizationName>
        <md:OrganizationDisplayName xml:lang="it">Example</md:OrganizationDisplayName>
        <md:OrganizationURL xml:lang="it">http://www.example.it</md:OrganizationURL>
    </md:Organization>

    <md:ContactPerson contactType="other">
        <md:Extensions>
            <spid:VATNumber>IT12345678901</spid:VATNumber>
            <spid:FiscalCode>XYZABCAAMGGJ000W</spid:FiscalCode>
            <spid:Private/>
        </md:Extensions>
        <md:EmailAddress>tech-info@example.org</md:EmailAddress>
        <md:TelephoneNumber>+39 8475634785</md:TelephoneNumber>
    </md:ContactPerson>

</md:EntityDescriptor>
"""

# openssl x509 -outform der -in sp-cert.pem -out client.crt
# cert_pem have the content of client.ctr ...

cert_pem = """MIIEJzCCAo+gAwIBAgIUaoCRB+1HO/ohrrDKw++3orgFtEkwDQYJKoZIhvcNAQEL
BQAwGzEZMBcGA1UEAxMQc3AudGVzdHVuaWNhbC5pdDAeFw0yMDEwMTQxNTA3NDBa
Fw0zMDEwMTIxNTA3NDBaMBsxGTAXBgNVBAMTEHNwLnRlc3R1bmljYWwuaXQwggGi
MA0GCSqGSIb3DQEBAQUAA4IBjwAwggGKAoIBgQC2mQ2Mm5Yl6MW9j1DMIE6SueXC
UQfV4+ZMlND7K9QjYDcMkRtKNKbzKZjJxo6dgwQruLPoHoL+2VdNjC9ayeBZHAYA
GqIcgLj1lVfCmO2KaajxmiqDILC1iu5p0ZJ7fAqca8sGhq8DlbzLRrRfFGbUfZ72
EuKIZMVVtwVKnZAt6cLxHe9fTcpigQeKXAWXN7c5hlFOa231KNwKS2BNRifJnqaM
yeCoXnDvFwNsvqzOkcOJF65GYJpRBqBaJuTyXIlxDG1xLNbOdaapOP+35ZXnlZTx
Xxlmg+hVBkksES7Sc4aLSAUTk1nWtolGubog7CM0ZeUwN600jurqPtUuIPHjPbG5
VKlymKlwWHNyx/Ur0B+HyG+/HRSWOW6oASCBAybj9MlPmmzaEH2gBCW/Puu/PWei
Myg0N/X/zxDhbHL2CQn9Z2lP42T7+8E6kx5F1Ze0VVXwE7rRh+MP3GMl2wQvhHu2
wQkIN8zF3DqEw9HZPbaYzrfm7Z7XopOaxj4zCfUCAwEAAaNjMGEwQAYDVR0RBDkw
N4IQc3AudGVzdHVuaWNhbC5pdIYjaHR0cHM6Ly9zcC50ZXN0dW5pY2FsLml0L3No
aWJib2xldGgwHQYDVR0OBBYEFBXo0an9ZfL9bef0vE68XrAq5Or5MA0GCSqGSIb3
DQEBCwUAA4IBgQAdswwxLY+fx7VMeuZW4t1T/jXHtb10aX74h8k9jV/Nnd+C7DDs
I+SALSMBVTXOBuuQN7aeJyDQeJcjerpRPcuU90MV2S7m6BrWtUFEZHie5Tdh7t0n
9D7RId3iAWWnZ8b8tuJbIFqePuyMhrpENbub4Y1eruulS21Qm4jEskTBU9CEaLRX
U/XJTRN93+SCqwZwpro9FIUEhY97y4j7vvjGAQ3v6zv177z2PYbtWMkFW3pBYuYx
j/esSCys8RhL3A8LlAPzvJIQWeE+r55hxAm/HnORMpFVNLe7nsEaiOZdN4dZoDk5
cVyulYl9Y5DdwAxenZWvQrokJKl+nM68Hf1ZvnOBOuXUpDg7EIedwBPGmgktCE+2
y3Q1cBVLBMfXJDe5ObY6dRZMhq8tC34nZD6NRXeKf3VcWjDHAVJGPdRRU2cC5gg1
ZTE39f0eIamxP6Q5JFfBk9GvVw+QiOc7CiaC5uTrKBD+kIwSw7on9W6WZuxL1IcL
bm+NjH24TLN4Wj8=
"""

data = {
 'id': ''.join([random.choice(string.ascii_lowercase) for _ in range(16)]),
 'entity_url': 'https://sp.testunical.it',
 'entityid': 'https://sp.testunical.it/shibboleth',
 'metadata_url': 'https://sp.testunical.it/shibboleth',
 'certificate_sign': cert_pem,
 'certificate_enc': cert_pem,
 'sso_post_path': 'Shibboleth.sso/SLO/POST',
 'acs_path': 'Shibboleth.sso/SAML2/POST'
}

md = metadata_tmpl.format(**data)
metadata_file = open('pymetadata.xml', 'w')
metadata_file.write(md)
metadata_file.close()

# sign it

sign_cmd = "xmlsec1 --sign --insecure --privkey-pem sp-key.pem --id-attr:ID urn:oasis:names:tc:SAML:2.0:metadata:EntityDescriptor pymetadata.xml"
signed_metadata = subprocess.getoutput(sign_cmd)
print(signed_metadata)
metadata_file_sign = open('pymetadata_signed.xml', 'w')
metadata_file_sign.write(signed_metadata)
metadata_file_sign.close()

