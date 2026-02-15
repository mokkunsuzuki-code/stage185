# MIT License © 2025 Motohiro Suzuki
from sdk.api import session_new, send_frame

# Stage178-A minimal: handshake_complete is per-ProtocolCore instance.
# So we demonstrate the fail-closed property within a single core state machine.
node = session_new("server", handshake_complete=False)

# 1) fail-closed proof: APP_DATA before HS must be rejected
try:
    send_frame(node, "APP_DATA", b"should-fail")
    print("[UNEXPECTED] APP_DATA accepted before handshake (BUG)")
except Exception as e:
    print("[OK] APP_DATA rejected before handshake:", type(e).__name__, str(e))

# 2) handshake (same core)
hs = send_frame(node, "HS")
print("[OK] HS response:", hs)

# 3) now APP_DATA must pass (same core)
resp = send_frame(node, "APP_DATA", b"hello-stage185")
print("[OK] APP_DATA response:", resp)
