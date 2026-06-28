# 01_Source/tests

This directory houses the comprehensive test suites for Project NOVA.

## Purpose

To manage all test files, test fixtures, unit tests, integration tests, mock environments, and verification suites.

## Guidelines

- Code layout under `tests/` should mirror the layout of `01_Source/` (e.g., `tests/engines/`, `tests/services/`, etc.).
- Unit tests must mock all external calls and run quickly.
- Integration tests must be run in sandboxed environments or under explicit permission flags.
