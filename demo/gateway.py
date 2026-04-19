import socket, hashlib, hmac, os, time, sys

SECRET    = b"AEGIS_SECRET_EV_V1"
PORT      = 9999
G  = "\033[92m"
R  = "\033[91m"
Y  = "\033[93m"
C  = "\033[96m"
D  = "\033[90m"
B  = "\033[1m"
X  = "\033[0m"

def log(symbol, label, msg, colour):
    print(f"  {colour}{B}{symbol} [{label}]{X}  {colour}{msg}{X}")
    time.sleep(0.4)

def header():
    print(f"""
{C}{B}╔══════════════════════════════════════╗
║       AEGIS SECURITY GATEWAY         ║
║       Vehicle BMS — Layer 2          ║
╚══════════════════════════════════════╝{X}
  {D}Listening on port {PORT}...{X}
""")

def verify(token, nonce):
    expected = hmac.new(SECRET, nonce.encode(), hashlib.sha256).hexdigest()
    return token.strip() == expected

def run():
    header()
    srv = socket.socket()
    srv.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    srv.bind(("0.0.0.0", PORT))
    srv.listen(5)

    while True:
        conn, addr = srv.accept()
        print(f"\n  {D}{'─'*38}{X}")
        log("→", "CONNECT", f"Charger connected from {addr[0]}", C)

        # Issue nonce
        nonce = os.urandom(4).hex()
        log("⟳", "NONCE  ", f"Issuing challenge:  {B}{nonce}{X}", Y)
        conn.send(nonce.encode())
        time.sleep(0.3)

        # Receive token
        data = conn.recv(256).decode().strip()
        label, token = data.split("|") if "|" in data else ("?", data)
        log("←", "TOKEN  ", f"Received from [{label}]", C)
        print(f"       {D}{token[:48]}...{X}")
        time.sleep(0.5)

        # Verify
        log("⚙", "VERIFY ", "Running HMAC-SHA256 check...", Y)
        time.sleep(0.6)

        if verify(token, nonce):
            log("✓", "RESULT ", "TOKEN VERIFIED — MOSFET ON", G)
            print(f"\n  {G}{B}  ██ CHARGING AUTHORISED ██{X}\n")
            conn.send(b"GRANTED")
        else:
            log("✗", "RESULT ", "TOKEN MISMATCH — ACCESS DENIED", R)
            print(f"\n  {R}{B}  ██ CONNECTION BLOCKED  ██{X}\n")
            conn.send(b"DENIED")

        conn.close()

run()
