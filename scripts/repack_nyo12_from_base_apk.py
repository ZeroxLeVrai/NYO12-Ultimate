#!/usr/bin/env python3
"""Build the NYO12 Java launcher APK around the already-built native payload in a base APK.

This is a packaging/rebranding build, not a native engine rebuild. The supplied base APK
must contain libnxloader.so, at least one libdmhost_<title ID>.so, libadrenotools.so,
libhook_impl.so, libmain_hook.so and assets/selftest/main.*.
"""
from __future__ import annotations
import argparse
import os
from pathlib import Path
import subprocess
import sys
import tempfile
import zipfile

ROOT = Path(__file__).resolve().parents[1]
DEFAULT_BASE = ROOT / "build-inputs" / "DroidPlay-0.6.0-arm64-v8a.apk"


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--sdk", default=os.environ.get("ANDROID_HOME") or os.environ.get("ANDROID_SDK_ROOT"), required=False)
    ap.add_argument("--base-apk", type=Path, default=DEFAULT_BASE)
    ap.add_argument("--out", type=Path, default=ROOT / "dist" / "NYO12-Ultimate-v0.1.0.apk")
    ap.add_argument("--keystore", type=Path, default=ROOT / ".build" / "nyo12-debug.jks")
    ap.add_argument("--version-name", default="0.1.0")
    ap.add_argument("--dry-run", action="store_true", help="validate the base APK and print the build command without compiling")
    a = ap.parse_args()
    if not a.sdk:
        ap.error("--sdk or ANDROID_HOME is required")
    if not a.base_apk.is_file():
        ap.error(f"base APK not found: {a.base_apk}")

    a.out.parent.mkdir(parents=True, exist_ok=True)
    a.keystore.parent.mkdir(parents=True, exist_ok=True)
    with tempfile.TemporaryDirectory(prefix="nyo12-apk-") as tmp:
        work = Path(tmp)
        with zipfile.ZipFile(a.base_apk) as z:
            names = set(z.namelist())
            required = [
                "lib/arm64-v8a/libnxloader.so",
                "lib/arm64-v8a/libadrenotools.so",
                "lib/arm64-v8a/libhook_impl.so",
                "lib/arm64-v8a/libmain_hook.so",
                "assets/selftest/main.patched.bin",
            ]
            missing = [n for n in required if n not in names]
            hosts = sorted(n for n in names if n.startswith("lib/arm64-v8a/libdmhost_") and n.endswith(".so"))
            if missing or not hosts:
                raise SystemExit(f"Base APK is missing required payload: {missing or 'no libdmhost_<id>.so'}")
            for name in required + hosts:
                target = work / name
                target.parent.mkdir(parents=True, exist_ok=True)
                target.write_bytes(z.read(name))
            for name in names:
                if name.startswith("assets/selftest/") and not name.endswith("/"):
                    target = work / name
                    target.parent.mkdir(parents=True, exist_ok=True)
                    target.write_bytes(z.read(name))

        cmd = [
            sys.executable, str(ROOT / "dm/android/tools/build_apk.py"),
            "--sdk", str(a.sdk),
            "--loader", str(work / "lib/arm64-v8a/libnxloader.so"),
            "--selftest", str(work / "assets/selftest"),
            "--lib", str(work / "lib/arm64-v8a/libadrenotools.so"),
            "--lib", str(work / "lib/arm64-v8a/libhook_impl.so"),
            "--lib", str(work / "lib/arm64-v8a/libmain_hook.so"),
            "--keystore", str(a.keystore),
            "--label", "NYO12 Ultimate",
            "--version-name", a.version_name,
            "--out", str(a.out.resolve()),
        ]
        for host in hosts:
            cmd.extend(["--so", str(work / host)])
        print("Packaging NYO12 around existing ARM64 native host(s):")
        for host in hosts:
            print(" -", Path(host).name)
        print("Note: this does not rebuild the native engine or add new game compatibility.")
        if a.dry_run:
            print("Build command validated (dry run).")
        else:
            subprocess.run(cmd, cwd=ROOT, check=True)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
