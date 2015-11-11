TLS Extended Master Secret Extension Checker
============================================

This script is designed for detection of servers without support for the RFC7627 and therefore potentially vulnerable to the TLS Triple Handshake Attack (CVE-2015-6112). It attempts to negotiate using each relevant protocol version  (TLSv1, TLSv1.1, and TLSv1.2) advertising a comprehensive set of ciphers and the TLS Extended Master Secret Extension.  Servers not responding with support for this extension are considered potentially vulnerable.

Changes:

v0.1 - Initial commit 

This offline tool is not supported and is provided for informational purposes only.
This tool uses Python – license information is available here: http://opensource.org/licenses/Python-2.0
