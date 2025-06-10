# Artifacts Directory

This directory contains artifact specifications - detailed instructions that AI coding assistants can use to build features for your Django-SvelteKit application.

## What is an Artifact?

An artifact is a comprehensive specification document that:
- Describes a feature or component in detail
- Provides implementation guidelines
- Includes code examples and patterns
- Contains enough information for an AI coder to implement the feature

## How to Use Artifacts

1. **Browse Available Artifacts**: Visit `/artifacts` in your application to see all available artifacts
2. **Select an Artifact**: Choose the feature you want to implement
3. **Feed to AI Coder**:
   - In Cursor: Press Cmd+K and reference the artifact file
   - In Windsurf: Use the AI command and mention the artifact
   - In GitHub Copilot: Include the artifact content as context
4. **Review & Deploy**: The AI will generate the implementation based on the specification

## Creating New Artifacts

To create a new artifact:

1. Create a new `.md` file in this directory
2. Follow this structure:
   ```markdown
   # Feature Name

   **Version:** 1.0.0
   **Category:** UI Components / Backend Features / etc.
   **Complexity:** Beginner / Intermediate / Advanced

   ## Overview
   Brief description of what this feature does

   ## Requirements
   - List of dependencies
   - Prerequisites

   ## Implementation Guide
   Step-by-step instructions

   ## Code Examples
   Complete, working code examples

   ## Usage
   How to use the feature once implemented
   ```

3. Add your artifact to the artifacts list in `/src/routes/(auth)/artifacts/+page.svelte`

## Available Artifacts

- **chatui-artifact.md** - A production-ready streaming chat interface with artifact support
