#!/usr/bin/env python3
"""
Relais local CORS pour Apis Intel — Veille Copernicus SAR
=========================================================

Pourquoi ce script ?
  Un fichier HTML ouvert en local ne peut pas appeler directement
  https://apis-intel.com : le navigateur bloque la requête (politique CORS)
  et affiche « Failed to fetch ». Ce relais tourne sur votre machine,
  reçoit les appels de l'application, les transmet à Apis Intel et
  renvoie la réponse avec les en-têtes CORS nécessaires.

Utilisation
-----------
  1. Ouvrir le Terminal (macOS : Cmd+Espace → « Terminal »)
  2. Lancer :
         python3 apis-proxy.py
     (ou, si le fichier est dans Téléchargements :
          python3 ~/Downloads/apis-proxy.py )
  3. Laisser cette fenêtre ouverte pendant l'utilisation.
  4. Dans l'application, onglet « 🔗 Liaisons » → Serveur :
     choisir « Relais local (http://127.0.0.1:8787) ».

  Arrêter le relais : Ctrl+C dans le Terminal.

Options
-------
  --port 8787            port d'écoute (défaut 8787)
  --upstream https://api.apis-intel.io   serveur Apis Intel visé
                         (défaut : https://apis-intel.com)

Sécurité
--------
  • N'écoute que sur 127.0.0.1 : inaccessible depuis l'extérieur.
  • Ne stocke ni ne journalise votre jeton : il est seulement relayé.
  • Aucune dépendance à installer (bibliothèque standard Python).
"""

import argparse
import json
import ssl
import sys
import urllib.error
import urllib.request
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer

ARGS = None
ALLOWED_PREFIXES = ("/api/v3/",)          # on ne relaie que l'API v3
TIMEOUT = 60


class ProxyHandler(BaseHTTPRequestHandler):
    server_version = "ApisRelay/1.0"

    # ------------------------------------------------------------------ utils
    def _cors(self):
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Access-Control-Allow-Methods", "GET, POST, OPTIONS")
        self.send_header("Access-Control-Allow-Headers",
                         "Authorization, Content-Type, X-Requested-With")
        self.send_header("Access-Control-Max-Age", "86400")

    def _send(self, code, body=b"", ctype="application/json; charset=utf-8"):
        self.send_response(code)
        self.send_header("Content-Type", ctype)
        self.send_header("Content-Length", str(len(body)))
        self._cors()
        self.end_headers()
        if body:
            self.wfile.write(body)

    def _err(self, code, msg):
        self._send(code, json.dumps({"error": msg}).encode())

    def log_message(self, fmt, *a):                      # journal compact
        sys.stderr.write("  %s\n" % (fmt % a))

    # ------------------------------------------------------------- handlers
    def do_OPTIONS(self):                                # préflight CORS
        self._send(204, b"", "text/plain")

    def do_GET(self):
        if self.path in ("/", "/health"):
            return self._send(200, json.dumps({
                "status": "ok", "relay": "Apis Intel",
                "upstream": ARGS.upstream}).encode())
        self._relay("GET")

    def do_POST(self):
        self._relay("POST")

    # --------------------------------------------------------------- relais
    def _relay(self, method):
        if not self.path.startswith(ALLOWED_PREFIXES):
            return self._err(404, "Chemin non relayé : %s (attendu /api/v3/...)" % self.path)

        url = ARGS.upstream.rstrip("/") + self.path
        length = int(self.headers.get("Content-Length") or 0)
        payload = self.rfile.read(length) if length else None

        req = urllib.request.Request(url, data=payload, method=method)
        req.add_header("Content-Type",
                       self.headers.get("Content-Type", "application/json"))
        req.add_header("Accept", "application/json")
        req.add_header("User-Agent", "veille-sar-relay/1.0")
        auth = self.headers.get("Authorization")
        if auth:
            req.add_header("Authorization", auth)      # jeton relayé tel quel

        print("→ %s %s" % (method, url))
        try:
            ctx = ssl.create_default_context()
            with urllib.request.urlopen(req, timeout=TIMEOUT, context=ctx) as r:
                body = r.read()
                ctype = r.headers.get("Content-Type", "application/json")
                print("← %s (%d octets)" % (r.status, len(body)))
                self._send(r.status, body, ctype)

        except urllib.error.HTTPError as e:             # erreur renvoyée par l'API
            body = e.read() or json.dumps({"error": str(e)}).encode()
            print("← HTTP %s" % e.code)
            self._send(e.code, body,
                       e.headers.get("Content-Type", "application/json"))

        except Exception as e:                          # réseau, DNS, TLS…
            print("✗ %s" % e)
            self._err(502, "Relais : %s" % e)


def main():
    global ARGS
    ap = argparse.ArgumentParser(description="Relais CORS local pour Apis Intel")
    ap.add_argument("--port", type=int, default=8787)
    ap.add_argument("--upstream", default="https://apis-intel.com",
                    help="https://apis-intel.com (défaut) ou https://api.apis-intel.io")
    ARGS = ap.parse_args()

    srv = ThreadingHTTPServer(("127.0.0.1", ARGS.port), ProxyHandler)
    print("=" * 62)
    print("  Relais Apis Intel actif")
    print("  Écoute   : http://127.0.0.1:%d" % ARGS.port)
    print("  Vers     : %s" % ARGS.upstream)
    print("  À régler dans l'app : onglet « Liaisons » → Serveur →")
    print("                        « Relais local (http://127.0.0.1:%d) »" % ARGS.port)
    print("  Arrêter  : Ctrl+C")
    print("=" * 62)
    try:
        srv.serve_forever()
    except KeyboardInterrupt:
        print("\nRelais arrêté.")
        srv.server_close()


if __name__ == "__main__":
    main()
