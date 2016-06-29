#!/bin/bash

init() {
    WORK="./work"
    CA_TMPL="${WORK}/ca.tmpl"
    CA_KEY="${WORK}/ca-key.pem"
    CA_CERT="./ca.pem"
    USER="$1"
    USER_TMPL="${WORK}/${USER}.tmpl"
    USER_KEY="${WORK}/${USER}-key.pem"
    USER_CERT="${WORK}/${USER}.pem"
    USER_P12="./${USER}.p12"
    REVOKED_CERT="${WORK}/revoked.pem"
    CRL_TMPL="${WORK}/crl.tmpl"
    CRL_CERT="./crl.pem"

    # Ensure working directory
    [[ -d $WORK ]] || mkdir -p $WORK

    # CA Template
    [[ -f $CA_TMPL ]] || cat << _EOF_ > $CA_TMPL
cn = "VPN CA"
serial = 1
expiration_days = 3650
ca
signing_key
cert_signing_key
crl_signing_key
_EOF_

    # CA Private Key
    [[ -f $CA_KEY ]] || certtool --generate-privkey --outfile $CA_KEY

    # CA Certificate
    [[ -f $CA_CERT ]] || certtool --generate-self-signed --load-privkey $CA_KEY --template $CA_TMPL --outfile $CA_CERT
}

generate() {
    # User Template
    cat << _EOF_ > $USER_TMPL
cn = "$USER"
expiration_days = 3650
signing_key
tls_www_client
_EOF_

    # User Private Key
    certtool --generate-privkey --outfile $USER_KEY

    # User Certificate
    certtool --generate-certificate --load-privkey $USER_KEY --load-ca-certificate $CA_CERT --load-ca-privkey $CA_KEY --template $USER_TMPL --outfile $USER_CERT

    # Export User Certificate
    certtool --to-p12 --pkcs-cipher 3des-pkcs12 --load-privkey $USER_KEY --load-certificate $USER_CERT --outfile $USER_P12 --outder
}

revoke() {
    # Copy User Certificate to Revoked Certificate
    cat $USER_CERT >> $REVOKED_CERT

    # CRL Template
    [[ -f $CRL_TMPL ]] || cat << _EOF_ > $CRL_TMPL
crl_next_update = 3650
crl_number = 1
_EOF_

    # CRL Certificate
    certtool --generate-crl --load-certificate $REVOKED_CERT --load-ca-privkey $CA_KEY --load-ca-certificate $CA_CERT --template $CRL_TMPL --outfile $CRL_CERT
}

case $1 in
    generate)
        init $2
        generate
        ;;
    revoke)
        init $2
        revoke
        ;;
    *)
        echo "\
Usage:
    $0 generate USER
    $0 revoke USER
"
esac
