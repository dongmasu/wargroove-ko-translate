# ModPacker 1.6.2 Analysis

Date: 2026-09-26

Source:
`references/Nexus/ModPacker-1.6.2.zip-1-1-6-2-1550065854/ModPacker-1.6.2/`

The JAR was extracted to `extract-ModPacker-1.6.2/`. The relevant classes
are:

- `me.andre111.halleytool.hpk.HalleyPK`
- `me.andre111.halleytool.hpk.io.HPKIO`
- `me.andre111.halleytool.hpk.io.HPKPacker`

## Encryption Finding

`HalleyPK.readHalleyPK` contains an embedded decryption path:

- If the first IV byte is zero, the payload is processed as-is.
- Otherwise it prints `Decrypting data...`.
- Cipher: `AES/CBC/NoPadding`.
- The embedded literal is `+Ohzep4z06NuKguNbFRz3w==`.
- The implementation uses the first 16 characters of that literal as the
  AES key bytes, rather than Base64-decoding the full literal.
- The pack IV is passed to `IvParameterSpec`.
- The decrypted data is then parsed as the asset payload region.

`HalleyPK.writeHalleyPK` preserves the pack IV in the output header. This
explains how ModPacker can unpack and repack protected Wargroove 1 packs.

## Scope

This confirms that ModPacker 1.6.2 has a hard-coded Halley pack decryption
implementation. It does not yet prove that the same key and exact behavior
are valid for every Wargroove 2 build. The current target is Windows
Wargroove 2 `v1.2.12`, build `#45031`; that build must be tested separately.

The conditional AES decrypt/encrypt behavior is now implemented in
`tools/halleypk.py`. It preserves the source IV and encrypted/plain mode.
Validation succeeded against the Windows Wargroove 2 pack, including a full
3,514-entry encrypted round-trip and a test pack with 24 added Korean
resources.

## AES Backend

The tool first tries a system `libcrypto` backend. On the current macOS
environment this is `/opt/homebrew/lib/libcrypto.dylib`, which provides the
AES CBC symbols needed for fast multi-megabyte processing. No external Python
package is required. If no supported system library is available, the bundled
pure-Python AES-128-CBC implementation is used as a slower fallback.
