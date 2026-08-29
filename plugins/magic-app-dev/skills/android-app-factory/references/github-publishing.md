# GitHub Publishing

Remote creation is a distinct externally mutating phase. The local generator never performs it.

## Preflight

Before "--apply":

1. Confirm the user requested remote creation.
2. Run "gh auth status".
3. Confirm both local repositories are clean, on "main", and contain at least one commit.
4. Confirm the intended visibility: Android private, legal public.
5. Run the publisher without "--apply" and show the resolved plan if names are surprising.

## Publisher

~~~bash
python3 scripts/publish_github.py \
  --workspace /absolute/path/to/<slug> \
  --apply
~~~

The publisher:

- Reads repository names and GitHub owner from the private app specification.
- Creates the Android remote as private and the legal remote as public.
- Adds "origin" and pushes "main".
- Configures Pages for the legal repository from "main" and "/".
- Verifies visibility and reports the Pages URL.

## Existing Remotes

The publisher is resumable only when an existing GitHub repository already matches the expected owner, name, visibility, and local "origin".

If an unrelated repository already uses either name, stop. Do not change its visibility, force-push, adopt it, or delete it.

If the first repository was created and the second step failed, keep the successful repository and rerun after resolving the failure. Never delete a remote automatically as rollback.
