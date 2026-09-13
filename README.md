# Second Brain

A personal knowledge base designed to be read by Claude Code in any session.

## Using it on your laptop

1. Install Claude Code if you have not already: https://code.claude.com/docs/en/overview
2. Clone this repo:
   ```
   git clone https://github.com/mpennyai-jpg/food-tracker.git second-brain
   cd second-brain
   ```
3. Start Claude inside the folder:
   ```
   claude
   ```
   Claude reads `CLAUDE.md` automatically and knows where everything lives.
4. Dump information in chat and ask Claude to file it. Then commit and push:
   ```
   git add -A && git commit -m "Add notes" && git push
   ```
5. In any other session (laptop, web, phone), pull first so you have the latest:
   ```
   git pull
   ```

## Layout

See `CLAUDE.md` for the full map. Short version: `brain/` holds everything, sorted by topic, with `brain/inbox/` for anything unsorted.

## Privacy

Keep this repository private. Do not commit passwords, account numbers, or anything you would not want stored on GitHub.
