# MIT License © 2025 Motohiro Suzuki
from __future__ import annotations

import inspect
import importlib

CANDIDATE_MODULES = [
    "qsp.session",
    "qsp.minicore",
    "qsp.rekey_engine",
    "qsp.rekey",
    "qsp.handshake",
    "qsp.core",
]

KEY_METHOD_HINTS = ["send", "recv", "rekey", "handshake", "accept", "frame", "encrypt", "decrypt", "pack", "unpack"]


def dump_module(modname: str) -> None:
    m = importlib.import_module(modname)
    print(f"\n=== {modname} ===")
    classes = []
    funcs = []
    for name, obj in sorted(vars(m).items()):
        if inspect.isclass(obj):
            classes.append((name, obj))
        elif inspect.isfunction(obj):
            funcs.append((name, obj))

    if funcs:
        print("functions:")
        for name, fn in funcs:
            if any(h in name.lower() for h in KEY_METHOD_HINTS):
                print(" -", name)

    if classes:
        print("classes:")
        for cname, C in classes:
            print(f" - {cname}")
            # public callables
            methods = []
            for n, o in sorted(vars(C).items()):
                if callable(o) and not n.startswith("_"):
                    if any(h in n.lower() for h in KEY_METHOD_HINTS):
                        methods.append(n)
            if methods:
                print("   methods:", ", ".join(methods))


def main():
    print("Stage178 API inspector (focus: send/recv/rekey/handshake)")
    for mod in CANDIDATE_MODULES:
        try:
            dump_module(mod)
        except Exception as e:
            print(f"\n=== {mod} ===")
            print("  (import failed)", repr(e))


if __name__ == "__main__":
    main()
