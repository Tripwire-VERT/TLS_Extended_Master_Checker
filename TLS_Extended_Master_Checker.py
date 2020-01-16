#!/usr/bin/env python

import sys
import socket
import time
import struct

strTitle = "Tripwire VERT TLS Triple Handshake Detection Tool (Extended Master Secret Extension Checker) v0.1"
if len(sys.argv) < 2:
    print("%s by Tripwire VERT (@TripwireVERT)\nUsage: %s <host> [port=443]" % (strTitle, sys.argv[0]))
    quit()
else:
    strHost = sys.argv[1]
    if len(sys.argv) > 2:
        try:
            iPort = int(sys.argv[2])
        except:
            print("%s\nUsage: %s <host> [port=443]" % (strTitle, sys.argv[0]))
            quit()
    else:
        iPort = 443

print("***%s***\nBrought to you by Tripwire VERT (@TripwireVERT)" % (strTitle))

dSSL = {"SSLv3": b"\x03\x00", "TLSv1": b"\x03\x01", "TLSv1.1": b"\x03\x02", "TLSv1.2": b"\x03\x03"}

# The following is a complete list of ciphers for the SSLv3 family up to TLSv1.2
ssl3_cipher = dict()
ssl3_cipher[b"\x00\x00"] = "TLS_NULL_WITH_NULL_NULL"
ssl3_cipher[b"\x00\x01"] = "TLS_RSA_WITH_NULL_MD5"
ssl3_cipher[b"\x00\x02"] = "TLS_RSA_WITH_NULL_SHA"
ssl3_cipher[b"\x00\x03"] = "TLS_RSA_EXPORT_WITH_RC4_40_MD5"
ssl3_cipher[b"\x00\x04"] = "TLS_RSA_WITH_RC4_128_MD5"
ssl3_cipher[b"\x00\x05"] = "TLS_RSA_WITH_RC4_128_SHA"
ssl3_cipher[b"\x00\x06"] = "TLS_RSA_EXPORT_WITH_RC2_CBC_40_MD5"
ssl3_cipher[b"\x00\x07"] = "TLS_RSA_WITH_IDEA_CBC_SHA"
ssl3_cipher[b"\x00\x08"] = "TLS_RSA_EXPORT_WITH_DES40_CBC_SHA"
ssl3_cipher[b"\x00\x09"] = "TLS_RSA_WITH_DES_CBC_SHA"
ssl3_cipher[b"\x00\x0a"] = "TLS_RSA_WITH_3DES_EDE_CBC_SHA"
ssl3_cipher[b"\x00\x0b"] = "TLS_DH_DSS_EXPORT_WITH_DES40_CBC_SHA"
ssl3_cipher[b"\x00\x0c"] = "TLS_DH_DSS_WITH_DES_CBC_SHA"
ssl3_cipher[b"\x00\x0d"] = "TLS_DH_DSS_WITH_3DES_EDE_CBC_SHA"
ssl3_cipher[b"\x00\x0e"] = "TLS_DH_RSA_EXPORT_WITH_DES40_CBC_SHA"
ssl3_cipher[b"\x00\x0f"] = "TLS_DH_RSA_WITH_DES_CBC_SHA"
ssl3_cipher[b"\x00\x10"] = "TLS_DH_RSA_WITH_3DES_EDE_CBC_SHA"
ssl3_cipher[b"\x00\x11"] = "TLS_DHE_DSS_EXPORT_WITH_DES40_CBC_SHA"
ssl3_cipher[b"\x00\x12"] = "TLS_DHE_DSS_WITH_DES_CBC_SHA"
ssl3_cipher[b"\x00\x13"] = "TLS_DHE_DSS_WITH_3DES_EDE_CBC_SHA"
ssl3_cipher[b"\x00\x14"] = "TLS_DHE_RSA_EXPORT_WITH_DES40_CBC_SHA"
ssl3_cipher[b"\x00\x15"] = "TLS_DHE_RSA_WITH_DES_CBC_SHA"
ssl3_cipher[b"\x00\x16"] = "TLS_DHE_RSA_WITH_3DES_EDE_CBC_SHA"
ssl3_cipher[b"\x00\x17"] = "TLS_DH_anon_EXPORT_WITH_RC4_40_MD5"
ssl3_cipher[b"\x00\x18"] = "TLS_DH_anon_WITH_RC4_128_MD5"
ssl3_cipher[b"\x00\x19"] = "TLS_DH_anon_EXPORT_WITH_DES40_CBC_SHA"
ssl3_cipher[b"\x00\x1a"] = "TLS_DH_anon_WITH_DES_CBC_SHA"
ssl3_cipher[b"\x00\x1b"] = "TLS_DH_anon_WITH_3DES_EDE_CBC_SHA"
ssl3_cipher[b"\x00\x1c"] = "SSL_FORTEZZA_KEA_WITH_NULL_SHA"
ssl3_cipher[b"\x00\x1d"] = "SSL_FORTEZZA_KEA_WITH_FORTEZZA_CBC_SHA"
ssl3_cipher[b"\x00\x1e"] = "SSL_FORTEZZA_KEA_WITH_RC4_128_SHA"
ssl3_cipher[b"\x00\x1E"] = "TLS_KRB5_WITH_DES_CBC_SHA"
ssl3_cipher[b"\x00\x1F"] = "TLS_KRB5_WITH_3DES_EDE_CBC_SHA"
ssl3_cipher[b"\x00\x20"] = "TLS_KRB5_WITH_RC4_128_SHA"
ssl3_cipher[b"\x00\x21"] = "TLS_KRB5_WITH_IDEA_CBC_SHA"
ssl3_cipher[b"\x00\x22"] = "TLS_KRB5_WITH_DES_CBC_MD5"
ssl3_cipher[b"\x00\x23"] = "TLS_KRB5_WITH_3DES_EDE_CBC_MD5"
ssl3_cipher[b"\x00\x24"] = "TLS_KRB5_WITH_RC4_128_MD5"
ssl3_cipher[b"\x00\x25"] = "TLS_KRB5_WITH_IDEA_CBC_MD5"
ssl3_cipher[b"\x00\x26"] = "TLS_KRB5_EXPORT_WITH_DES_CBC_40_SHA"
ssl3_cipher[b"\x00\x27"] = "TLS_KRB5_EXPORT_WITH_RC2_CBC_40_SHA"
ssl3_cipher[b"\x00\x28"] = "TLS_KRB5_EXPORT_WITH_RC4_40_SHA"
ssl3_cipher[b"\x00\x29"] = "TLS_KRB5_EXPORT_WITH_DES_CBC_40_MD5"
ssl3_cipher[b"\x00\x2A"] = "TLS_KRB5_EXPORT_WITH_RC2_CBC_40_MD5"
ssl3_cipher[b"\x00\x2B"] = "TLS_KRB5_EXPORT_WITH_RC4_40_MD5"
ssl3_cipher[b"\x00\x2C"] = "TLS_PSK_WITH_NULL_SHA"
ssl3_cipher[b"\x00\x2D"] = "TLS_DHE_PSK_WITH_NULL_SHA"
ssl3_cipher[b"\x00\x2E"] = "TLS_RSA_PSK_WITH_NULL_SHA"
ssl3_cipher[b"\x00\x2F"] = "TLS_RSA_WITH_AES_128_CBC_SHA"
ssl3_cipher[b"\x00\x30"] = "TLS_DH_DSS_WITH_AES_128_CBC_SHA"
ssl3_cipher[b"\x00\x31"] = "TLS_DH_RSA_WITH_AES_128_CBC_SHA"
ssl3_cipher[b"\x00\x32"] = "TLS_DHE_DSS_WITH_AES_128_CBC_SHA"
ssl3_cipher[b"\x00\x33"] = "TLS_DHE_RSA_WITH_AES_128_CBC_SHA"
ssl3_cipher[b"\x00\x34"] = "TLS_DH_anon_WITH_AES_128_CBC_SHA"
ssl3_cipher[b"\x00\x35"] = "TLS_RSA_WITH_AES_256_CBC_SHA"
ssl3_cipher[b"\x00\x36"] = "TLS_DH_DSS_WITH_AES_256_CBC_SHA"
ssl3_cipher[b"\x00\x37"] = "TLS_DH_RSA_WITH_AES_256_CBC_SHA"
ssl3_cipher[b"\x00\x38"] = "TLS_DHE_DSS_WITH_AES_256_CBC_SHA"
ssl3_cipher[b"\x00\x39"] = "TLS_DHE_RSA_WITH_AES_256_CBC_SHA"
ssl3_cipher[b"\x00\x3A"] = "TLS_DH_anon_WITH_AES_256_CBC_SHA"
ssl3_cipher[b"\x00\x3B"] = "TLS_RSA_WITH_NULL_SHA256"
ssl3_cipher[b"\x00\x3C"] = "TLS_RSA_WITH_AES_128_CBC_SHA256"
ssl3_cipher[b"\x00\x3D"] = "TLS_RSA_WITH_AES_256_CBC_SHA256"
ssl3_cipher[b"\x00\x3E"] = "TLS_DH_DSS_WITH_AES_128_CBC_SHA256"
ssl3_cipher[b"\x00\x3F"] = "TLS_DH_RSA_WITH_AES_128_CBC_SHA256"
ssl3_cipher[b"\x00\x40"] = "TLS_DHE_DSS_WITH_AES_128_CBC_SHA256"
ssl3_cipher[b"\x00\x41"] = "TLS_RSA_WITH_CAMELLIA_128_CBC_SHA"
ssl3_cipher[b"\x00\x42"] = "TLS_DH_DSS_WITH_CAMELLIA_128_CBC_SHA"
ssl3_cipher[b"\x00\x43"] = "TLS_DH_RSA_WITH_CAMELLIA_128_CBC_SHA"
ssl3_cipher[b"\x00\x44"] = "TLS_DHE_DSS_WITH_CAMELLIA_128_CBC_SHA"
ssl3_cipher[b"\x00\x45"] = "TLS_DHE_RSA_WITH_CAMELLIA_128_CBC_SHA"
ssl3_cipher[b"\x00\x46"] = "TLS_DH_anon_WITH_CAMELLIA_128_CBC_SHA"
ssl3_cipher[b"\x00\x60"] = "TLS_RSA_EXPORT1024_WITH_RC4_56_MD5"
ssl3_cipher[b"\x00\x61"] = "TLS_RSA_EXPORT1024_WITH_RC2_CBC_56_MD5"
ssl3_cipher[b"\x00\x62"] = "TLS_RSA_EXPORT1024_WITH_DES_CBC_SHA"
ssl3_cipher[b"\x00\x63"] = "TLS_DHE_DSS_EXPORT1024_WITH_DES_CBC_SHA"
ssl3_cipher[b"\x00\x64"] = "TLS_RSA_EXPORT1024_WITH_RC4_56_SHA"
ssl3_cipher[b"\x00\x65"] = "TLS_DHE_DSS_EXPORT1024_WITH_RC4_56_SHA"
ssl3_cipher[b"\x00\x66"] = "TLS_DHE_DSS_WITH_RC4_128_SHA"
ssl3_cipher[b"\x00\x67"] = "TLS_DHE_RSA_WITH_AES_128_CBC_SHA256"
ssl3_cipher[b"\x00\x68"] = "TLS_DH_DSS_WITH_AES_256_CBC_SHA256"
ssl3_cipher[b"\x00\x69"] = "TLS_DH_RSA_WITH_AES_256_CBC_SHA256"
ssl3_cipher[b"\x00\x6A"] = "TLS_DHE_DSS_WITH_AES_256_CBC_SHA256"
ssl3_cipher[b"\x00\x6B"] = "TLS_DHE_RSA_WITH_AES_256_CBC_SHA256"
ssl3_cipher[b"\x00\x6C"] = "TLS_DH_anon_WITH_AES_128_CBC_SHA256"
ssl3_cipher[b"\x00\x6D"] = "TLS_DH_anon_WITH_AES_256_CBC_SHA256"
ssl3_cipher[b"\x00\x80"] = "TLS_GOSTR341094_WITH_28147_CNT_IMIT"
ssl3_cipher[b"\x00\x81"] = "TLS_GOSTR341001_WITH_28147_CNT_IMIT"
ssl3_cipher[b"\x00\x82"] = "TLS_GOSTR341094_WITH_NULL_GOSTR3411"
ssl3_cipher[b"\x00\x83"] = "TLS_GOSTR341001_WITH_NULL_GOSTR3411"
ssl3_cipher[b"\x00\x84"] = "TLS_RSA_WITH_CAMELLIA_256_CBC_SHA"
ssl3_cipher[b"\x00\x85"] = "TLS_DH_DSS_WITH_CAMELLIA_256_CBC_SHA"
ssl3_cipher[b"\x00\x86"] = "TLS_DH_RSA_WITH_CAMELLIA_256_CBC_SHA"
ssl3_cipher[b"\x00\x87"] = "TLS_DHE_DSS_WITH_CAMELLIA_256_CBC_SHA"
ssl3_cipher[b"\x00\x88"] = "TLS_DHE_RSA_WITH_CAMELLIA_256_CBC_SHA"
ssl3_cipher[b"\x00\x89"] = "TLS_DH_anon_WITH_CAMELLIA_256_CBC_SHA"
ssl3_cipher[b"\x00\x8A"] = "TLS_PSK_WITH_RC4_128_SHA"
ssl3_cipher[b"\x00\x8B"] = "TLS_PSK_WITH_3DES_EDE_CBC_SHA"
ssl3_cipher[b"\x00\x8C"] = "TLS_PSK_WITH_AES_128_CBC_SHA"
ssl3_cipher[b"\x00\x8D"] = "TLS_PSK_WITH_AES_256_CBC_SHA"
ssl3_cipher[b"\x00\x8E"] = "TLS_DHE_PSK_WITH_RC4_128_SHA"
ssl3_cipher[b"\x00\x8F"] = "TLS_DHE_PSK_WITH_3DES_EDE_CBC_SHA"
ssl3_cipher[b"\x00\x90"] = "TLS_DHE_PSK_WITH_AES_128_CBC_SHA"
ssl3_cipher[b"\x00\x91"] = "TLS_DHE_PSK_WITH_AES_256_CBC_SHA"
ssl3_cipher[b"\x00\x92"] = "TLS_RSA_PSK_WITH_RC4_128_SHA"
ssl3_cipher[b"\x00\x93"] = "TLS_RSA_PSK_WITH_3DES_EDE_CBC_SHA"
ssl3_cipher[b"\x00\x94"] = "TLS_RSA_PSK_WITH_AES_128_CBC_SHA"
ssl3_cipher[b"\x00\x95"] = "TLS_RSA_PSK_WITH_AES_256_CBC_SHA"
ssl3_cipher[b"\x00\x96"] = "TLS_RSA_WITH_SEED_CBC_SHA"
ssl3_cipher[b"\x00\x97"] = "TLS_DH_DSS_WITH_SEED_CBC_SHA"
ssl3_cipher[b"\x00\x98"] = "TLS_DH_RSA_WITH_SEED_CBC_SHA"
ssl3_cipher[b"\x00\x99"] = "TLS_DHE_DSS_WITH_SEED_CBC_SHA"
ssl3_cipher[b"\x00\x9A"] = "TLS_DHE_RSA_WITH_SEED_CBC_SHA"
ssl3_cipher[b"\x00\x9B"] = "TLS_DH_anon_WITH_SEED_CBC_SHA"
ssl3_cipher[b"\x00\x9C"] = "TLS_RSA_WITH_AES_128_GCM_SHA256"
ssl3_cipher[b"\x00\x9D"] = "TLS_RSA_WITH_AES_256_GCM_SHA384"
ssl3_cipher[b"\x00\x9E"] = "TLS_DHE_RSA_WITH_AES_128_GCM_SHA256"
ssl3_cipher[b"\x00\x9F"] = "TLS_DHE_RSA_WITH_AES_256_GCM_SHA384"
ssl3_cipher[b"\x00\xA0"] = "TLS_DH_RSA_WITH_AES_128_GCM_SHA256"
ssl3_cipher[b"\x00\xA1"] = "TLS_DH_RSA_WITH_AES_256_GCM_SHA384"
ssl3_cipher[b"\x00\xA2"] = "TLS_DHE_DSS_WITH_AES_128_GCM_SHA256"
ssl3_cipher[b"\x00\xA3"] = "TLS_DHE_DSS_WITH_AES_256_GCM_SHA384"
ssl3_cipher[b"\x00\xA4"] = "TLS_DH_DSS_WITH_AES_128_GCM_SHA256"
ssl3_cipher[b"\x00\xA5"] = "TLS_DH_DSS_WITH_AES_256_GCM_SHA384"
ssl3_cipher[b"\x00\xA6"] = "TLS_DH_anon_WITH_AES_128_GCM_SHA256"
ssl3_cipher[b"\x00\xA7"] = "TLS_DH_anon_WITH_AES_256_GCM_SHA384"
ssl3_cipher[b"\x00\xA8"] = "TLS_PSK_WITH_AES_128_GCM_SHA256"
ssl3_cipher[b"\x00\xA9"] = "TLS_PSK_WITH_AES_256_GCM_SHA384"
ssl3_cipher[b"\x00\xAA"] = "TLS_DHE_PSK_WITH_AES_128_GCM_SHA256"
ssl3_cipher[b"\x00\xAB"] = "TLS_DHE_PSK_WITH_AES_256_GCM_SHA384"
ssl3_cipher[b"\x00\xAC"] = "TLS_RSA_PSK_WITH_AES_128_GCM_SHA256"
ssl3_cipher[b"\x00\xAD"] = "TLS_RSA_PSK_WITH_AES_256_GCM_SHA384"
ssl3_cipher[b"\x00\xAE"] = "TLS_PSK_WITH_AES_128_CBC_SHA256"
ssl3_cipher[b"\x00\xAF"] = "TLS_PSK_WITH_AES_256_CBC_SHA384"
ssl3_cipher[b"\x00\xB0"] = "TLS_PSK_WITH_NULL_SHA256"
ssl3_cipher[b"\x00\xB1"] = "TLS_PSK_WITH_NULL_SHA384"
ssl3_cipher[b"\x00\xB2"] = "TLS_DHE_PSK_WITH_AES_128_CBC_SHA256"
ssl3_cipher[b"\x00\xB3"] = "TLS_DHE_PSK_WITH_AES_256_CBC_SHA384"
ssl3_cipher[b"\x00\xB4"] = "TLS_DHE_PSK_WITH_NULL_SHA256"
ssl3_cipher[b"\x00\xB5"] = "TLS_DHE_PSK_WITH_NULL_SHA384"
ssl3_cipher[b"\x00\xB6"] = "TLS_RSA_PSK_WITH_AES_128_CBC_SHA256"
ssl3_cipher[b"\x00\xB7"] = "TLS_RSA_PSK_WITH_AES_256_CBC_SHA384"
ssl3_cipher[b"\x00\xB8"] = "TLS_RSA_PSK_WITH_NULL_SHA256"
ssl3_cipher[b"\x00\xB9"] = "TLS_RSA_PSK_WITH_NULL_SHA384"
ssl3_cipher[b"\x00\xBA"] = "TLS_RSA_WITH_CAMELLIA_128_CBC_SHA256"
ssl3_cipher[b"\x00\xBB"] = "TLS_DH_DSS_WITH_CAMELLIA_128_CBC_SHA256"
ssl3_cipher[b"\x00\xBC"] = "TLS_DH_RSA_WITH_CAMELLIA_128_CBC_SHA256"
ssl3_cipher[b"\x00\xBD"] = "TLS_DHE_DSS_WITH_CAMELLIA_128_CBC_SHA256"
ssl3_cipher[b"\x00\xBE"] = "TLS_DHE_RSA_WITH_CAMELLIA_128_CBC_SHA256"
ssl3_cipher[b"\x00\xBF"] = "TLS_DH_anon_WITH_CAMELLIA_128_CBC_SHA256"
ssl3_cipher[b"\x00\xC0"] = "TLS_RSA_WITH_CAMELLIA_256_CBC_SHA256"
ssl3_cipher[b"\x00\xC1"] = "TLS_DH_DSS_WITH_CAMELLIA_256_CBC_SHA256"
ssl3_cipher[b"\x00\xC2"] = "TLS_DH_RSA_WITH_CAMELLIA_256_CBC_SHA256"
ssl3_cipher[b"\x00\xC3"] = "TLS_DHE_DSS_WITH_CAMELLIA_256_CBC_SHA256"
ssl3_cipher[b"\x00\xC4"] = "TLS_DHE_RSA_WITH_CAMELLIA_256_CBC_SHA256"
ssl3_cipher[b"\x00\xC5"] = "TLS_DH_anon_WITH_CAMELLIA_256_CBC_SHA256"
ssl3_cipher[b"\x00\x00"] = "TLS_EMPTY_RENEGOTIATION_INFO_SCSV"
ssl3_cipher[b"\xc0\x01"] = "TLS_ECDH_ECDSA_WITH_NULL_SHA"
ssl3_cipher[b"\xc0\x02"] = "TLS_ECDH_ECDSA_WITH_RC4_128_SHA"
ssl3_cipher[b"\xc0\x03"] = "TLS_ECDH_ECDSA_WITH_3DES_EDE_CBC_SHA"
ssl3_cipher[b"\xc0\x04"] = "TLS_ECDH_ECDSA_WITH_AES_128_CBC_SHA"
ssl3_cipher[b"\xc0\x05"] = "TLS_ECDH_ECDSA_WITH_AES_256_CBC_SHA"
ssl3_cipher[b"\xc0\x06"] = "TLS_ECDHE_ECDSA_WITH_NULL_SHA"
ssl3_cipher[b"\xc0\x07"] = "TLS_ECDHE_ECDSA_WITH_RC4_128_SHA"
ssl3_cipher[b"\xc0\x08"] = "TLS_ECDHE_ECDSA_WITH_3DES_EDE_CBC_SHA"
ssl3_cipher[b"\xc0\x09"] = "TLS_ECDHE_ECDSA_WITH_AES_128_CBC_SHA"
ssl3_cipher[b"\xc0\x0a"] = "TLS_ECDHE_ECDSA_WITH_AES_256_CBC_SHA"
ssl3_cipher[b"\xc0\x0b"] = "TLS_ECDH_RSA_WITH_NULL_SHA"
ssl3_cipher[b"\xc0\x0c"] = "TLS_ECDH_RSA_WITH_RC4_128_SHA"
ssl3_cipher[b"\xc0\x0d"] = "TLS_ECDH_RSA_WITH_3DES_EDE_CBC_SHA"
ssl3_cipher[b"\xc0\x0e"] = "TLS_ECDH_RSA_WITH_AES_128_CBC_SHA"
ssl3_cipher[b"\xc0\x0f"] = "TLS_ECDH_RSA_WITH_AES_256_CBC_SHA"
ssl3_cipher[b"\xc0\x10"] = "TLS_ECDHE_RSA_WITH_NULL_SHA"
ssl3_cipher[b"\xc0\x11"] = "TLS_ECDHE_RSA_WITH_RC4_128_SHA"
ssl3_cipher[b"\xc0\x12"] = "TLS_ECDHE_RSA_WITH_3DES_EDE_CBC_SHA"
ssl3_cipher[b"\xc0\x13"] = "TLS_ECDHE_RSA_WITH_AES_128_CBC_SHA"
ssl3_cipher[b"\xc0\x14"] = "TLS_ECDHE_RSA_WITH_AES_256_CBC_SHA"
ssl3_cipher[b"\xc0\x15"] = "TLS_ECDH_anon_WITH_NULL_SHA"
ssl3_cipher[b"\xc0\x16"] = "TLS_ECDH_anon_WITH_RC4_128_SHA"
ssl3_cipher[b"\xc0\x17"] = "TLS_ECDH_anon_WITH_3DES_EDE_CBC_SHA"
ssl3_cipher[b"\xc0\x18"] = "TLS_ECDH_anon_WITH_AES_128_CBC_SHA"
ssl3_cipher[b"\xc0\x19"] = "TLS_ECDH_anon_WITH_AES_256_CBC_SHA"
ssl3_cipher[b"\xC0\x1A"] = "TLS_SRP_SHA_WITH_3DES_EDE_CBC_SHA"
ssl3_cipher[b"\xC0\x1B"] = "TLS_SRP_SHA_RSA_WITH_3DES_EDE_CBC_SHA"
ssl3_cipher[b"\xC0\x1C"] = "TLS_SRP_SHA_DSS_WITH_3DES_EDE_CBC_SHA"
ssl3_cipher[b"\xC0\x1D"] = "TLS_SRP_SHA_WITH_AES_128_CBC_SHA"
ssl3_cipher[b"\xC0\x1E"] = "TLS_SRP_SHA_RSA_WITH_AES_128_CBC_SHA"
ssl3_cipher[b"\xC0\x1F"] = "TLS_SRP_SHA_DSS_WITH_AES_128_CBC_SHA"
ssl3_cipher[b"\xC0\x20"] = "TLS_SRP_SHA_WITH_AES_256_CBC_SHA"
ssl3_cipher[b"\xC0\x21"] = "TLS_SRP_SHA_RSA_WITH_AES_256_CBC_SHA"
ssl3_cipher[b"\xC0\x22"] = "TLS_SRP_SHA_DSS_WITH_AES_256_CBC_SHA"
ssl3_cipher[b"\xC0\x23"] = "TLS_ECDHE_ECDSA_WITH_AES_128_CBC_SHA256"
ssl3_cipher[b"\xC0\x24"] = "TLS_ECDHE_ECDSA_WITH_AES_256_CBC_SHA384"
ssl3_cipher[b"\xC0\x25"] = "TLS_ECDH_ECDSA_WITH_AES_128_CBC_SHA256"
ssl3_cipher[b"\xC0\x26"] = "TLS_ECDH_ECDSA_WITH_AES_256_CBC_SHA384"
ssl3_cipher[b"\xC0\x27"] = "TLS_ECDHE_RSA_WITH_AES_128_CBC_SHA256"
ssl3_cipher[b"\xC0\x28"] = "TLS_ECDHE_RSA_WITH_AES_256_CBC_SHA384"
ssl3_cipher[b"\xC0\x29"] = "TLS_ECDH_RSA_WITH_AES_128_CBC_SHA256"
ssl3_cipher[b"\xC0\x2A"] = "TLS_ECDH_RSA_WITH_AES_256_CBC_SHA384"
ssl3_cipher[b"\xC0\x2B"] = "TLS_ECDHE_ECDSA_WITH_AES_128_GCM_SHA256"
ssl3_cipher[b"\xC0\x2C"] = "TLS_ECDHE_ECDSA_WITH_AES_256_GCM_SHA384"
ssl3_cipher[b"\xC0\x2D"] = "TLS_ECDH_ECDSA_WITH_AES_128_GCM_SHA256"
ssl3_cipher[b"\xC0\x2E"] = "TLS_ECDH_ECDSA_WITH_AES_256_GCM_SHA384"
ssl3_cipher[b"\xC0\x2F"] = "TLS_ECDHE_RSA_WITH_AES_128_GCM_SHA256"
ssl3_cipher[b"\xC0\x30"] = "TLS_ECDHE_RSA_WITH_AES_256_GCM_SHA384"
ssl3_cipher[b"\xC0\x31"] = "TLS_ECDH_RSA_WITH_AES_128_GCM_SHA256"
ssl3_cipher[b"\xC0\x32"] = "TLS_ECDH_RSA_WITH_AES_256_GCM_SHA384"
ssl3_cipher[b"\xC0\x33"] = "TLS_ECDHE_PSK_WITH_RC4_128_SHA"
ssl3_cipher[b"\xC0\x34"] = "TLS_ECDHE_PSK_WITH_3DES_EDE_CBC_SHA"
ssl3_cipher[b"\xC0\x35"] = "TLS_ECDHE_PSK_WITH_AES_128_CBC_SHA"
ssl3_cipher[b"\xC0\x36"] = "TLS_ECDHE_PSK_WITH_AES_256_CBC_SHA"
ssl3_cipher[b"\xC0\x37"] = "TLS_ECDHE_PSK_WITH_AES_128_CBC_SHA256"
ssl3_cipher[b"\xC0\x38"] = "TLS_ECDHE_PSK_WITH_AES_256_CBC_SHA384"
ssl3_cipher[b"\xC0\x39"] = "TLS_ECDHE_PSK_WITH_NULL_SHA"
ssl3_cipher[b"\xC0\x3A"] = "TLS_ECDHE_PSK_WITH_NULL_SHA256"
ssl3_cipher[b"\xC0\x3B"] = "TLS_ECDHE_PSK_WITH_NULL_SHA384"
ssl3_cipher[b"\xfe\xfe"] = "SSL_RSA_FIPS_WITH_DES_CBC_SHA"
ssl3_cipher[b"\xfe\xff"] = "SSL_RSA_FIPS_WITH_3DES_EDE_CBC_SHA"
ssl3_cipher[b"\xff\xe0"] = "SSL_RSA_FIPS_WITH_3DES_EDE_CBC_SHA"
ssl3_cipher[b"\xff\xe1"] = "SSL_RSA_FIPS_WITH_DES_CBC_SHA"


def getSSLRecords(strBuf):
    lstRecords = []
    if len(strBuf) >= 9:
        sslStatus = struct.unpack(">BHHI", strBuf[0:9])
        iType = (sslStatus[3] & (0xFF000000)) >> 24
        iRecordLen = sslStatus[3] & (0x00FFFFFF)
        iShakeProtocol = sslStatus[0]
        strRecord = strBuf[9 : 9 + iRecordLen]
        iSSLLen = sslStatus[2]
        # log(2,"iSSLLen == %d, len(strBuf) == %d, iRecordLen == %d",iSSLLen,len(strBuf),iRecordLen)
        if iRecordLen + 5 < iSSLLen:
            # log(2,"Multiple Handshakes")
            lstRecords.append((iShakeProtocol, iType, strRecord))
            iLoopStopper = 0
            iNextOffset = iRecordLen + 9
            while iNextOffset < len(strBuf):
                iLoopStopper += 1
                iCount = 0
                while (iNextOffset + 4) > len(strBuf) and iCount < 5:
                    # log(2,"Need more data to fill buffer")
                    iCount += 1
                    rule.waitForData()
                    if len(rule.buffer) > 0:
                        strBuf += rule.buffer
                if (iNextOffset + 4) > len(strBuf):
                    # log(2,"End of message")
                    break
                iTypeAndLen = struct.unpack(">I", strBuf[iNextOffset : iNextOffset + 4])[0]
                iRecordLen = iTypeAndLen & (0x00FFFFFF)
                iType = (iTypeAndLen & (0xFF000000)) >> 24
                strRecord = strBuf[iNextOffset + 4 : iNextOffset + 4 + iRecordLen]
                lstRecords.append((iShakeProtocol, iType, strRecord))
                iNextOffset += iRecordLen + 4
                if iLoopStopper > 8:
                    break
            return lstRecords
        elif iRecordLen + 9 < len(strBuf):
            # log(2,"Multiple Records")
            lstRecords.append((iShakeProtocol, iType, strRecord))
            iNextOffset = iRecordLen + 9
            iLoopStopper = 0
            while iNextOffset + 6 < len(strBuf):
                iLoopStopper += 1
                iShakeProtocol = struct.unpack(">B", strBuf[iNextOffset : iNextOffset + 1])[0]
                iRecordLen = struct.unpack(">H", strBuf[iNextOffset + 3 : iNextOffset + 5])[0]
                iType = struct.unpack(">B", strBuf[iNextOffset + 5 : iNextOffset + 6])[0]
                strRecord = strBuf[iNextOffset + 6 : iRecordLen + iNextOffset + 6]

                # log(2,"iShakeProto == %d, iRecordLen == %d, iType == %d",iShakeProtocol,iRecordLen,iType)
                lstRecords.append((iShakeProtocol, iType, strRecord))
                iNextOffset += iRecordLen + 5
                if iLoopStopper > 8:
                    break
            return lstRecords
        elif iRecordLen + 9 == len(strBuf):
            # log(2,"Single record")
            sslStatus = checkSSLHeader(strBuf)
            lstRecords.append((sslStatus[0], sslStatus[2], strRecord))
            return lstRecords
    return None


def checkSSLHeader(strBuf):
    if len(strBuf) >= 6:
        sslStatus = struct.unpack(">BHHI", strBuf[0:9])
        iType = (sslStatus[3:4] & (0xFF000000)) >> 24
        iRecordLen = sslStatus[3:4] & (0x00FFFFFF)
        iShakeProtocol = sslStatus[0:1]
        iSSLLen = sslStatus[2:3]
        return (iShakeProtocol, iSSLLen, iType, iRecordLen)
    return None


def makeHello(strSSLVer):
    TLS_EXTENDED_MASTER = b"\x00\x04\x00\x17\x00\x00"
    r = b"\x16"  # Message Type 22
    r += dSSL[strSSLVer]
    strCiphers = b""
    for c in ssl3_cipher.keys():
        strCiphers += c
    dLen = 43 + len(strCiphers) + len(TLS_EXTENDED_MASTER)
    r += struct.pack("!H", dLen)
    h = b"\x01"
    strPlen = struct.pack("!L", dLen - 4)
    h += strPlen[1:]
    h += dSSL[strSSLVer]
    rand = struct.pack("!L", int(time.time()))
    rand += b"\x36\x24\x34\x16\x27\x09\x22\x07\xd7\xbe\xef\x69\xa1\xb2"
    rand += b"\x37\x23\x14\x96\x27\xa9\x12\x04\xe7\xce\xff\xd9\xae\xbb"
    h += rand
    h += b"\x00"  # No Session ID
    h += struct.pack("!H", len(strCiphers))
    h += strCiphers
    h += b"\x01\x00"
    h += TLS_EXTENDED_MASTER
    return r + h


iVulnCount = 0
for strVer in ["TLSv1.2", "TLSv1.1", "TLSv1"]:
    strHello = makeHello(strVer)
    strLogPre = "[%s] %s:%d" % (strVer, strHost, iPort)
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        s.connect((strHost, iPort))
        s.settimeout(5)
    except:
        print("Failure connecting to %s:%d." % (strHost, iPort))
        quit()
    s.send(strHello)
    # print("Sending %s Client Hello" % (strVer))
    iCount = 0
    fServerHello = False
    fCert = False
    fKex = False
    fHelloDone = False
    while iCount < 5:
        iCount += 1
        try:
            recv = s.recv(2048)
        except:
            continue
        lstRecords = getSSLRecords(recv)
        # strLogMessage = "iCount = %d; lstRecords = %s" % (iCount,lstRecords)
        # log(2,strLogMessage)
        if lstRecords != None and len(lstRecords) > 0:
            for (iShakeProtocol, iType, strRecord) in lstRecords:
                if iShakeProtocol == 22:
                    if iType == 2:
                        fServerHello = True
                        strServerHello = strRecord
                    elif iType == 11:
                        fCert = True
                    elif iType == 12:
                        fKex = True
                    elif iType == 14:
                        fHelloDone = True
            if fServerHello and fCert:
                break
        else:
            # log(2, "Handshake missing or invalid.  Aborting.")
            continue
    if not (fServerHello and fCert):
        print("%s Invalid handshake." % (strLogPre))
    elif len(recv) > 0:
        if strServerHello.endswith(b"\x04\x00\x17\x00\x00"):
            fVuln = False
        else:
            fVuln = True
        try:
            s.send(b"\x15" + dSSL[strVer] + b"\x00\x02\x01\x00")
        except socket.error:
            print("Connection closed by server.")
        if fVuln:
            print("[%s] %s:%d is vulnerable to TLS triple handshake (Extended ClientHello rejected)" % (strVer, strHost, iPort))
            iVulnCount += 1
        else:
            print("[%s] %s:%d responded with support for Extended Master Secret TLS Extension" % (strVer, strHost, iPort))
    else:
        print("[%s] No response from %s:%d" % (strVer, strHost, iPort))
    try:
        s.close()
    except:
        pass
if iVulnCount > 0:
    print("***This System Exhibits Potentially Vulnerable Behavior***")
    quit(1)
else:
    print("No need to patch. (Server indicates support for TLS Extended Master Secret)")
    quit(0)
