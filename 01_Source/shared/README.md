# 01_Source/shared

This directory contains cross-cutting shared code, utilities, helpers, and data structures.

## Purpose

To house utility modules that do not contain business logic or architectural state, such as date formatters, math utilities, string parsers, file system walk helpers, and basic logging configurations.

## Guidelines

- Code here must be completely stateless (or purely functional) and have zero dependencies on other directories in `01_Source/`.
