# Build input: existing Android host

`DroidPlay-0.6.0-arm64-v8a.apk` is used only as a source of already-compiled ARM64 native libraries and the self-test payload for the first NYO12 APK build.

It contains one prebuilt game host: `libdmhost_0100000011D90000.so` (Pokémon Brilliant Diamond profile). It does **not** make NYO12 a universal Switch emulator and it does not add BOTW or Mario Kart support.

Keep this file inside your private GitHub repository. Do not publish game data, keys, saves, or private build inputs in a public repository.
