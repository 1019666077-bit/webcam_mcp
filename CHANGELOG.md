# Changelog

All notable changes to this project are documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

## [0.2.1] - 2026-10-13

### Security

- Change the default SSE host from `0.0.0.0` to `127.0.0.1` so the server no
  longer binds to all interfaces (and thus the LAN) by default.
- Print a loud stderr warning at startup when `--host` is non-loopback, since
  the SSE transport is unauthenticated.
- Refuse to start SSE on a non-loopback host unless `WEBCAM_MCP_ALLOW_LAN=1`
  is set explicitly.

### Docs

- README: stop advertising `0.0.0.0` as the default, document the
  unauthenticated-SSE risk, and recommend stdio or loopback.
