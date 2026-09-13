# Repurpose the food-tracker repo as the second brain

Date: 2026-09-13
Status: decided

## Context

Todd wanted a second brain and digital twin that any Claude session, on the laptop or in the cloud, could read. The only thing shared across sessions is a git repo. The food-tracker repo existed and he does not use the app.

## Options considered

- Build the brain in this repo. Fast, already wired to this session.
- Create a new dedicated repo. Cleaner name, keeps personal data out of an app repo.

## Decision

Build here. Todd said "I do not use food tracker, wipe that." The app was removed on the working branch. The repo name still says food-tracker; renaming on GitHub is a follow-up.

## Reasoning

Speed, and the repo is private. Structure: `CLAUDE.md` as the map and behavior rules, `brain/` for content, two northstars (business and personal), `brain/reference/` for verbatim sources and topic references.

## Outcome (fill in later)

Pending: merge to main, rename repo, import the laptop skill system.
