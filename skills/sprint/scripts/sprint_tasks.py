#!/usr/bin/env python3
# /// script
# requires-python = ">=3.12"
# dependencies = []
# ///
"""Sprint task CRUD operations for tasks.json files.

Usage:
    sprint_tasks.py init <file> --session <name> --objective <text>
    sprint_tasks.py list <file> [--status <status>] [--json]
    sprint_tasks.py get <file> <id> [--json]
    sprint_tasks.py ready <file> [--json]
    sprint_tasks.py update <file> <id> [--status <s>] [--name <n>] [--description <d>] [--criteria <c>] [--add-dep <dep>]
    sprint_tasks.py delete <file> <id>
    sprint_tasks.py graph <file>
    sprint_tasks.py worktree create <file> <brick-id> [--base <ref>]
    sprint_tasks.py worktree collect <file> <brick-id>
    sprint_tasks.py worktree cleanup <file> <brick-id>

Note: To add bricks, edit the tasks.json file directly and append to the "bricks" array.
"""

import json
import sys
import os
import subprocess
from datetime import datetime
from pathlib import Path

# Single source of truth for brick statuses
VALID_STATUSES = {"pending", "in_progress", "done", "passed", "failed", "skipped", "archived"}
DONE_STATUSES = {"done", "passed", "skipped", "archived"}


def load_tasks(path: str) -> dict:
    with open(path) as f:
        return json.load(f)


def save_tasks(path: str, data: dict):
    with open(path, "w") as f:
        json.dump(data, f, indent=2)
        f.write("\n")


def cmd_init(args: list[str]):
    """Create a new tasks.json file."""
    file_path = args[0]
    session = ""
    objective = ""
    i = 1
    while i < len(args):
        if args[i] == "--session" and i + 1 < len(args):
            session = args[i + 1]
            i += 2
        elif args[i] == "--objective" and i + 1 < len(args):
            objective = args[i + 1]
            i += 2
        else:
            i += 1

    if os.path.exists(file_path):
        print(f"Error: {file_path} already exists", file=sys.stderr)
        sys.exit(1)

    os.makedirs(os.path.dirname(file_path) or ".", exist_ok=True)

    data = {
        "session": session,
        "objective": objective,
        "created": datetime.now().strftime("%Y-%m-%d"),
        "status": "in_progress",
        "bricks": [],
    }
    save_tasks(file_path, data)
    print(f"Created {file_path}")

    # Create companion files
    base = file_path.replace(".tasks.json", "")
    progress_path = f"{base}.progress.md"
    if not os.path.exists(progress_path):
        with open(progress_path, "w") as f:
            ts = datetime.now().strftime("%Y-%m-%dT%H:%M")
            f.write(f"# Progress: {session}\n\n")
            f.write(f"## {ts} — [Sprint Created]\n")
            f.write(f"{objective}\n")
        print(f"Created {progress_path}")

    decisions_path = f"{base}.decisions.md"
    if not os.path.exists(decisions_path):
        with open(decisions_path, "w") as f:
            f.write(f"# Decisions: {session}\n\n")
            f.write("<!-- Capture architectural decisions, pattern choices, scope boundaries -->\n")
        print(f"Created {decisions_path}")

    objective_path = f"{base}.objective.md"
    if not os.path.exists(objective_path):
        with open(objective_path, "w") as f:
            f.write(f"# Objective: {session}\n\n")
            f.write(f"{objective}\n")
        print(f"Created {objective_path}")

    context_path = f"{base}.context.md"
    if not os.path.exists(context_path):
        with open(context_path, "w") as f:
            f.write(f"# Sprint Context — {session}\n\n")
            f.write("You are building [describe what you're building here].\n\n")
            f.write("## Architecture\n\n")
            f.write("[Describe the architecture and key patterns]\n\n")
            f.write("## Critical Constraints\n\n")
            f.write("[List constraints that must not be violated]\n\n")
            f.write("## What Already Exists\n\n")
            f.write("[List existing code/components this sprint builds on]\n\n")
            f.write("## What This Sprint Builds\n\n")
            f.write("[List new files and components]\n\n")
            f.write("## Key Types\n\n")
            f.write("[Important type definitions]\n\n")
            f.write("## Design Docs\n\n")
            f.write("[Links to design documentation]\n\n")
            f.write("## Testing\n\n")
            f.write("```bash\n# Commands to validate\n```\n")
        print(f"Created {context_path}")

    print("\nIMPORTANT: Read the above files before writing to them — the Write tool rejects writes to unread files.")


def cmd_list(args: list[str]):
    """List bricks, optionally filtered by status."""
    file_path = args[0]
    status_filter = None
    as_json = False
    i = 1
    while i < len(args):
        if args[i] == "--status" and i + 1 < len(args):
            status_filter = args[i + 1]
            i += 2
        elif args[i] == "--json":
            as_json = True
            i += 1
        else:
            i += 1

    data = load_tasks(file_path)
    bricks = data["bricks"]
    if status_filter:
        bricks = [b for b in bricks if b["status"] == status_filter]

    if as_json:
        print(json.dumps(bricks, indent=2))
        return

    if not bricks:
        print("No bricks found.")
        return

    # Summary table
    print(f"{'ID':<6} {'Status':<14} {'Type':<16} {'Deps':<12} Name")
    print("-" * 80)
    for b in bricks:
        deps = ",".join(b.get("depends_on", [])) or "-"
        btype = b.get("type", "-")
        print(f"{b['id']:<6} {b['status']:<14} {btype:<16} {deps:<12} {b['name']}")

    # Stats
    total = len(data["bricks"])
    by_status: dict[str, int] = {}
    for b in data["bricks"]:
        by_status[b["status"]] = by_status.get(b["status"], 0) + 1
    print(f"\nTotal: {total} | " + " | ".join(f"{k}: {v}" for k, v in sorted(by_status.items())))


def cmd_get(args: list[str]):
    """Get full details of a brick."""
    file_path = args[0]
    brick_id = args[1]
    as_json = "--json" in args

    data = load_tasks(file_path)
    brick = next((b for b in data["bricks"] if b["id"] == brick_id), None)
    if not brick:
        print(f"Error: Brick {brick_id} not found", file=sys.stderr)
        sys.exit(1)

    if as_json:
        print(json.dumps(brick, indent=2))
        return

    print(f"Brick {brick['id']}: {brick['name']}")
    print(f"Status: {brick['status']}")
    print(f"Type: {brick.get('type', '-')}")
    print(f"Depends on: {', '.join(brick.get('depends_on', [])) or 'none'}")
    if brick.get("tags"):
        print(f"Tags: {', '.join(brick['tags'])}")
    if brick.get("files"):
        print(f"Files: {', '.join(brick['files'])}")
    print(f"\nDescription:\n{brick.get('description', '-')}")
    print(f"\nAcceptance Criteria:\n{brick.get('acceptance_criteria', '-')}")


def cmd_ready(args: list[str]):
    """Get bricks ready for execution (deps met, status pending)."""
    file_path = args[0]
    as_json = "--json" in args

    data = load_tasks(file_path)
    done_ids = {b["id"] for b in data["bricks"] if b["status"] in DONE_STATUSES}

    ready = []
    for b in data["bricks"]:
        if b["status"] != "pending":
            continue
        deps = b.get("depends_on", [])
        if all(d in done_ids for d in deps):
            ready.append(b)

    if as_json:
        print(json.dumps(ready, indent=2))
        return

    if not ready:
        # Check if all done or blocked
        pending = [b for b in data["bricks"] if b["status"] == "pending"]
        in_progress = [b for b in data["bricks"] if b["status"] == "in_progress"]
        if not pending and not in_progress:
            print("Sprint complete! All bricks done.")
        elif pending:
            print(f"No bricks ready. {len(pending)} pending (blocked by dependencies), {len(in_progress)} in progress.")
        else:
            print(f"No pending bricks. {len(in_progress)} in progress.")
        return

    print(f"{len(ready)} brick(s) ready:\n")

    # Show file overlap analysis
    file_map: dict[str, list[str]] = {}
    for b in ready:
        for f in b.get("files", []):
            file_map.setdefault(f, []).append(b["id"])

    conflicts = {f: ids for f, ids in file_map.items() if len(ids) > 1}

    for b in ready:
        overlaps = []
        for f in b.get("files", []):
            if f in conflicts:
                others = [oid for oid in conflicts[f] if oid != b["id"]]
                if others:
                    overlaps.append(f"  FILE OVERLAP: {f} (shared with {', '.join(others)})")

        print(f"  [{b['id']}] {b['name']}")
        print(f"       Type: {b.get('type', '-')} | Files: {', '.join(b.get('files', [])) or 'none'}")
        for o in overlaps:
            print(f"       *** {o}")
        print()

    if conflicts:
        print("FILE CONFLICT MATRIX:")
        for f, ids in sorted(conflicts.items()):
            print(f"  {f} -> bricks {', '.join(ids)} (MUST BATCH)")
        print()
        print("Bricks sharing files must go to a single agent.")


def cmd_update(args: list[str]):
    """Update brick fields."""
    file_path = args[0]
    brick_id = args[1]

    data = load_tasks(file_path)
    brick = next((b for b in data["bricks"] if b["id"] == brick_id), None)
    if not brick:
        print(f"Error: Brick {brick_id} not found", file=sys.stderr)
        sys.exit(1)

    i = 2
    while i < len(args):
        if args[i] == "--status" and i + 1 < len(args):
            new_status = args[i + 1]
            if new_status not in VALID_STATUSES:
                print(f"Error: Invalid status '{new_status}'. Valid statuses: {', '.join(sorted(VALID_STATUSES))}", file=sys.stderr)
                sys.exit(1)
            brick["status"] = new_status
            i += 2
        elif args[i] == "--name" and i + 1 < len(args):
            brick["name"] = args[i + 1]
            i += 2
        elif args[i] == "--description" and i + 1 < len(args):
            brick["description"] = args[i + 1]
            i += 2
        elif args[i] == "--criteria" and i + 1 < len(args):
            brick["acceptance_criteria"] = args[i + 1]
            i += 2
        elif args[i] == "--add-dep" and i + 1 < len(args):
            dep = args[i + 1]
            if not any(b["id"] == dep for b in data["bricks"]):
                print(f"Error: Dependency {dep} not found", file=sys.stderr)
                sys.exit(1)
            brick.setdefault("depends_on", [])
            if dep not in brick["depends_on"]:
                brick["depends_on"].append(dep)
            i += 2
        elif args[i] == "--type" and i + 1 < len(args):
            brick["type"] = args[i + 1]
            i += 2
        elif args[i] == "--add-tag" and i + 1 < len(args):
            brick.setdefault("tags", [])
            if args[i + 1] not in brick["tags"]:
                brick["tags"].append(args[i + 1])
            i += 2
        elif args[i] == "--add-file" and i + 1 < len(args):
            brick.setdefault("files", [])
            if args[i + 1] not in brick["files"]:
                brick["files"].append(args[i + 1])
            i += 2
        elif args[i] == "--set-files" and i + 1 < len(args):
            brick["files"] = json.loads(args[i + 1])
            i += 2
        else:
            print(f"Unknown flag: {args[i]}", file=sys.stderr)
            sys.exit(1)

    save_tasks(file_path, data)
    print(f"Updated brick {brick_id}: {brick['name']} (status: {brick['status']})")


def cmd_delete(args: list[str]):
    """Delete a brick."""
    file_path = args[0]
    brick_id = args[1]

    data = load_tasks(file_path)

    # Check if any brick depends on this one
    dependents = [b["id"] for b in data["bricks"] if brick_id in b.get("depends_on", [])]
    if dependents:
        print(f"Error: Cannot delete {brick_id} — bricks {', '.join(dependents)} depend on it", file=sys.stderr)
        sys.exit(1)

    original_count = len(data["bricks"])
    data["bricks"] = [b for b in data["bricks"] if b["id"] != brick_id]

    if len(data["bricks"]) == original_count:
        print(f"Error: Brick {brick_id} not found", file=sys.stderr)
        sys.exit(1)

    save_tasks(file_path, data)
    print(f"Deleted brick {brick_id}")


def cmd_graph(args: list[str]):
    """Show dependency graph."""
    file_path = args[0]
    data = load_tasks(file_path)

    # Find roots (no dependencies)
    roots = [b for b in data["bricks"] if not b.get("depends_on")]
    by_id = {b["id"]: b for b in data["bricks"]}

    # Build reverse graph (id -> list of bricks that depend on it)
    dependents: dict[str, list[str]] = {}
    for b in data["bricks"]:
        for dep in b.get("depends_on", []):
            dependents.setdefault(dep, []).append(b["id"])

    status_icon = {
        "pending": "[ ]",
        "in_progress": "[~]",
        "done": "[+]",
        "passed": "[+]",
        "failed": "[!]",
        "skipped": "[-]",
        "archived": "[x]",
    }

    printed: set[str] = set()

    def print_tree(brick_id: str, indent: int = 0):
        if brick_id in printed:
            b = by_id.get(brick_id)
            if b:
                icon = status_icon.get(b["status"], "[?]")
                print(f"{'  ' * indent}{icon} {brick_id}: {b['name']} (see above)")
            return
        printed.add(brick_id)
        b = by_id.get(brick_id)
        if not b:
            return
        icon = status_icon.get(b["status"], "[?]")
        print(f"{'  ' * indent}{icon} {brick_id}: {b['name']}")
        for child_id in sorted(dependents.get(brick_id, [])):
            print_tree(child_id, indent + 1)

    for root in roots:
        print_tree(root["id"])

    # Show any orphans (in a cycle or missing from roots)
    orphans = [b["id"] for b in data["bricks"] if b["id"] not in printed]
    if orphans:
        print(f"\nOrphaned (possible cycle): {', '.join(orphans)}")


def _slugify(name: str) -> str:
    """Convert a name to a filesystem-safe slug."""
    import re
    slug = re.sub(r'[^\w\-]', '-', name.lower())
    slug = re.sub(r'-+', '-', slug).strip('-')
    return slug or 'default'


def _git_root(tasks_path: str) -> str:
    """Resolve the git repository root from a tasks file path."""
    result = subprocess.run(
        ["git", "rev-parse", "--show-toplevel"],
        capture_output=True,
        text=True,
        cwd=os.path.dirname(os.path.abspath(tasks_path)) or ".",
    )
    if result.returncode != 0:
        print(f"Error: git rev-parse failed: {result.stderr.strip()}", file=sys.stderr)
        sys.exit(1)
    return result.stdout.strip()


def _build_worktree_path(git_root: str, session_slug: str, brick_id: str) -> str:
    """Build worktree directory path (new format: session-namespaced)."""
    return os.path.join(git_root, ".worktrees", session_slug, f"brick-{brick_id}")


def _build_legacy_worktree_path(git_root: str, brick_id: str) -> str:
    """Build legacy worktree directory path (flat, no session namespace)."""
    return os.path.join(git_root, ".worktrees", f"brick-{brick_id}")


def _build_legacy_claude_worktree_path(git_root: str, session_slug: str, brick_id: str) -> str:
    """Build mentor-repo worktree path (.claude/worktrees) for migration."""
    return os.path.join(git_root, ".claude", "worktrees", session_slug, f"brick-{brick_id}")


def _build_branch_name(session: str, brick_id: str) -> str:
    """Build the git branch name for a brick."""
    return f"sprint/{session}/brick-{brick_id}"


def _worktree_paths(tasks_path: str, brick_id: str) -> tuple[str, str, str]:
    """Returns (git_root, worktree_path, branch_name).

    Uses session-namespaced paths under .worktrees/ for new worktrees.
    Falls back to legacy flat path and mentor-repo .claude/worktrees paths
    if they exist and the new path doesn't.
    """
    git_root = _git_root(tasks_path)
    data = load_tasks(tasks_path)
    session = data.get("session", "sprint")

    session_slug = _slugify(session)
    new_path = _build_worktree_path(git_root, session_slug, brick_id)
    legacy_path = _build_legacy_worktree_path(git_root, brick_id)
    claude_path = _build_legacy_claude_worktree_path(git_root, session_slug, brick_id)
    branch_name = _build_branch_name(session, brick_id)

    # Prefer new path; fall back to legacy locations if they exist and new doesn't
    if os.path.exists(new_path):
        worktree_path = new_path
    elif os.path.exists(legacy_path):
        worktree_path = legacy_path
    elif os.path.exists(claude_path):
        worktree_path = claude_path
    else:
        worktree_path = new_path  # Default to new format (for create)

    return git_root, worktree_path, branch_name


def cmd_worktree(args: list[str]):
    """Manage self-contained worktrees for sprint brick isolation."""
    if not args:
        print("Usage: worktree <create|collect|cleanup> <tasks-file> <brick-id> [options]", file=sys.stderr)
        sys.exit(1)

    subcmd = args[0]
    subargs = args[1:]

    subcmds = {
        "create": _worktree_create,
        "collect": _worktree_collect,
        "cleanup": _worktree_cleanup,
    }

    if subcmd not in subcmds:
        print(f"Unknown worktree subcommand: {subcmd}", file=sys.stderr)
        print("Valid subcommands: create, collect, cleanup", file=sys.stderr)
        sys.exit(1)

    subcmds[subcmd](subargs)


def _worktree_create(args: list[str]):
    """Create a git worktree for a brick branching from HEAD (or --base <ref>)."""
    if len(args) < 2:
        print("Usage: worktree create <tasks-file> <brick-id> [--base <ref>]", file=sys.stderr)
        sys.exit(1)

    tasks_path = args[0]
    brick_id = args[1]
    base_ref = "HEAD"

    i = 2
    while i < len(args):
        if args[i] == "--base" and i + 1 < len(args):
            base_ref = args[i + 1]
            i += 2
        else:
            i += 1

    data = load_tasks(tasks_path)
    brick = next((b for b in data["bricks"] if b["id"] == brick_id), None)
    if not brick:
        print(f"Error: Brick {brick_id} not found", file=sys.stderr)
        sys.exit(1)

    git_root, worktree_path, branch_name = _worktree_paths(tasks_path, brick_id)

    result = subprocess.run(
        ["git", "worktree", "add", worktree_path, "-b", branch_name, base_ref],
        capture_output=True,
        text=True,
        cwd=git_root,
    )
    if result.returncode != 0:
        print(f"Error: git worktree add failed:\n{result.stderr.strip()}", file=sys.stderr)
        sys.exit(1)

    print(worktree_path)


def _worktree_collect(args: list[str]):
    """Rebase and fast-forward a brick's worktree branch onto HEAD."""
    if len(args) < 2:
        print("Usage: worktree collect <tasks-file> <brick-id>", file=sys.stderr)
        sys.exit(1)

    tasks_path = args[0]
    brick_id = args[1]

    data = load_tasks(tasks_path)
    brick = next((b for b in data["bricks"] if b["id"] == brick_id), None)
    if not brick:
        print(f"Error: Brick {brick_id} not found", file=sys.stderr)
        sys.exit(1)

    git_root, worktree_path, branch_name = _worktree_paths(tasks_path, brick_id)
    
    # Resolve the main repository's HEAD to a concrete commit hash
    # This is critical because "HEAD" inside a worktree is the worktree's branch!
    main_commit_result = subprocess.run(
        ["git", "rev-parse", "HEAD"],
        capture_output=True,
        text=True,
        cwd=git_root
    )
    if main_commit_result.returncode != 0:
        print(f"Error: Could not resolve HEAD in main repo: {main_commit_result.stderr.strip()}", file=sys.stderr)
        sys.exit(1)
    main_commit = main_commit_result.stdout.strip()

    # PRE-CHECK 1: Worktree exists?
    if not os.path.exists(worktree_path):
        # Check if branch exists (stale state)
        branch_check = subprocess.run(
            ["git", "rev-parse", "--verify", branch_name],
            capture_output=True,
            cwd=git_root
        )
        if branch_check.returncode == 0:
            print(f"Warning: Worktree missing but branch {branch_name} exists. Cleaning up branch...")
            # Prune stale worktree metadata so git knows the worktree is gone
            subprocess.run(["git", "worktree", "prune"], cwd=git_root)
            subprocess.run(["git", "branch", "-D", branch_name], cwd=git_root)
            print("Done. Brick may have been partially collected or cleaned up.")
        else:
            print(f"Error: Worktree not found at {worktree_path}. Run 'worktree create' first.", file=sys.stderr)
        sys.exit(1)

    # PRE-CHECK 2: Worktree clean?
    status_result = subprocess.run(
        ["git", "status", "--porcelain"],
        capture_output=True,
        text=True,
        cwd=worktree_path
    )
    if status_result.stdout.strip():
        print("Error: Worktree has uncommitted changes. Commit or stash them first.", file=sys.stderr)
        print(status_result.stdout.strip(), file=sys.stderr)
        sys.exit(1)

    # PRE-CHECK 3: Has main moved? (Is main an ancestor of the brick branch?)
    ancestor_check = subprocess.run(
        ["git", "merge-base", "--is-ancestor", main_commit, branch_name],
        capture_output=True,
        cwd=git_root
    )
    
    if ancestor_check.returncode == 0:
        # Fast-forward path: main hasn't moved relative to branch
        print(f"Fast-forwarding {branch_name} into main...", flush=True)
    else:
        # Rebase path: main HAS moved, need to rebase worktree onto the resolved main commit
        print(f"Main has moved. Rebasing worktree {branch_name} onto {main_commit}...", flush=True)
        
        # MUST rebase from inside worktree
        rebase_result = subprocess.run(
            ["git", "rebase", main_commit],
            capture_output=True,
            text=True,
            cwd=worktree_path
        )
        
        if rebase_result.returncode != 0:
            # Rollback: always abort rebase on failure to leave repo clean
            subprocess.run(["git", "rebase", "--abort"], cwd=worktree_path)
            print(f"Error: Rebase failed (conflicts?). Worktree restored to original state.", file=sys.stderr)
            print(rebase_result.stderr.strip(), file=sys.stderr)
            print(f"\nResolve conflicts manually in: {worktree_path}", file=sys.stderr)
            sys.exit(1)

    # Merge into main (should be ff-only now)
    merge_result = subprocess.run(
        ["git", "merge", "--ff-only", branch_name],
        capture_output=True,
        text=True,
        cwd=git_root
    )
    if merge_result.returncode != 0:
        print(f"Error: git merge --ff-only failed:\n{merge_result.stderr.strip()}", file=sys.stderr)
        sys.exit(1)

    print(f"Successfully collected {branch_name} into main")
    
    # SUCCESS: cleanup
    print("Cleaning up worktree and branch...")
    _worktree_cleanup([tasks_path, brick_id])


def _worktree_cleanup(args: list[str]):
    """Remove a brick's worktree and its branch (idempotent)."""
    if len(args) < 2:
        print("Usage: worktree cleanup <tasks-file> <brick-id>", file=sys.stderr)
        sys.exit(1)

    tasks_path = args[0]
    brick_id = args[1]

    data = load_tasks(tasks_path)
    brick = next((b for b in data["bricks"] if b["id"] == brick_id), None)
    if not brick:
        print(f"Error: Brick {brick_id} not found", file=sys.stderr)
        sys.exit(1)

    git_root, worktree_path, branch_name = _worktree_paths(tasks_path, brick_id)

    # Remove worktree (ignore failure — may already be gone)
    remove_result = subprocess.run(
        ["git", "worktree", "remove", worktree_path, "--force"],
        capture_output=True,
        text=True,
        cwd=git_root,
    )
    if remove_result.returncode == 0:
        print(f"Removed worktree: {worktree_path}")
    else:
        print(f"Worktree already removed or missing: {worktree_path}")

    # Delete branch (ignore failure — may already be gone)
    branch_result = subprocess.run(
        ["git", "branch", "-D", branch_name],
        capture_output=True,
        text=True,
        cwd=git_root,
    )
    if branch_result.returncode == 0:
        print(f"Deleted branch: {branch_name}")
    else:
        print(f"Branch already deleted or missing: {branch_name}")


def usage():
    print(__doc__)
    sys.exit(1)


def main():
    if len(sys.argv) < 2:
        usage()

    cmd = sys.argv[1]
    args = sys.argv[2:]

    if not args and cmd != "help":
        usage()

    commands = {
        "init": cmd_init,
        "list": cmd_list,
        "get": cmd_get,
        "ready": cmd_ready,
        "update": cmd_update,
        "delete": cmd_delete,
        "graph": cmd_graph,
        "worktree": cmd_worktree,
    }

    if cmd not in commands:
        print(f"Unknown command: {cmd}", file=sys.stderr)
        usage()

    commands[cmd](args)


if __name__ == "__main__":
    main()
