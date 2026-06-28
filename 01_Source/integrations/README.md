# 01_Source/integrations

This directory houses third-party service connections and integrations.

## Purpose

To manage API connectors, authentication layers, and external service contracts (such as Notion, Slack, Spotify, GitHub, etc.) that do not require tool mechanics.

## Guidelines

- All integrations must be wrapped in clean abstractions so business logic remains agnostic of the exact API payload formats.
