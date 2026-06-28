# 01_Source/plugins

This directory contains optional extension plugins.

## Purpose

To support optional or third-party plugins that implement external API hooks or integration tools without modifying the main platform core.

## Guidelines

- Plugins must implement a strict `IPlugin` interface defined under `01_Source/core/`.
- The platform must function correctly and compile even if this folder is empty.
