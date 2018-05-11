## Opusfile 0.7 ##

The opusfile and opusurl libraries provide a high-level API for
decoding and seeking within .opus files on disk or over http(s).

opusfile depends on libopus and libogg.
opusurl depends on opusfile and openssl.

Compiled for win32 with the mingw64 toolchain. Built with

  libogg 1.3.2
  libopus 1.1.1
  openssl 1.0.1q

Changes since the v0.6 release:
 - Add API to access and preserve binary metadata.
 - Add support for R128_ALBUM_GAIN metadata tag.
 - Better seeking with continued packets and multiplexed streams.
 - Portability and build fixes.

This release is backward-compatible with the previous
release but contains updates to conform with the latest
IETF Ogg Opus draft, important performance enhancements,
and bug fixes. We recommend all users upgrade.

The library is functional, but there are likely issues
we didn't find in our own testing. Please give feedback
in #opus on irc.freenode.net or at opus@xiph.org.

Programming documentation is available in
opusfile_api-0.7.pdf included with this package, and
online at https://opus-codec.org/docs/opusfile_api-0.7/
