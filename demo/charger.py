import socket, hashlib, hmac, time, sys

SECRET_REAL = b"AEGIS_SECRET_EV_V1"
SECRET_FAKE = b"HACKER_WRONG_KEY_99"
PORT        = 9999
HOST        = "127.0.0.1"

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

def header(mode):
    styles = {
        "legit":  (G, "CERTIFIED EV CHARGER",   "Using correct secret key"),
        "rogue":  (R, "ROGUE CHARGER",           "Using forged/wrong key  "),
    }
    col, title, sub = styles[mode]
    print(f"""
{col}{B}╔══════════════════════════════════════╗
║  {title:<36}║
║  {sub:<36}║
╚══════════════════════════════════════╝{X}
""")

def connect(mode):
    header(mode)
    s = socket.socket()
    try:
        s.connect((HOST, PORT))
    except ConnectionRefusedError:
        print(f"  {R}Gateway not running. Start gate.py first.{X}\n")
        return

    log("→", "CONNECT", "Connected to AEGIS Gateway", C)

    # Receive nonce
    nonce = s.recv(64).decode().strip()
    log("←", "NONCE  ", f"Challenge received:  {B}{nonce}{X}", Y)
    time.sleep(0.5)

    # Compute response
    if mode == "legit":
        token = hmac.new(SECRET_REAL, nonce.encode(), hashlib.sha256).hexdigest()
        label = "CERTIFIED"
        log("⚙", "COMPUTE", "Signing with real secret key...", G)
    elif mode == "rogue":
        token = hmac.new(SECRET_FAKE, nonce.encode(), hashlib.sha256).hexdigest()
        label = "ROGUE"
        log("⚙", "COMPUTE", "Signing with forged key...", R)

    time.sleep(0.3)
    log("→", "SEND   ", "Transmitting token to gateway...", C)
    print(f"       {D}{token[:48]}...{X}")
    s.send(f"{label}|{token}".encode())
    time.sleep(0.3)

    # Read result
    result = s.recv(64).decode()
    print()
    if result == "GRANTED":
        log("✓", "RESULT ", "GATEWAY GRANTED ACCESS", G)
        print(f"\n  {G}{B}  ██ CHARGING STARTED ██{X}\n")
    else:
        log("✗", "RESULT ", "GATEWAY DENIED ACCESS", R)
        print(f"\n  {R}{B}  ██ BLOCKED BY GATEWAY ██{X}\n")

    s.close()

def menu():
    print(f"""
{C}{B}  SELECT CHARGER MODE:{X}
  {G}[1]{X} Legitimate charger   {D}(correct key){X}
  {R}[2]{X} Rogue charger        {D}(wrong key){X}
  {D}[0]{X} Exit
""")
    return input(f"  {C}Mode: {X}").strip()

while True:
    choice = menu()
    if choice == "1":   connect("legit")
    elif choice == "2": connect("rogue")
    elif choice == "0": break
    input(f"\n  {D}Press ENTER for next attempt...{X}\n")
