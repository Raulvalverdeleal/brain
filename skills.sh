#!/bin/bash
# skills.sh — Wrapper script for brain CLI operations
# Usage: skills.sh <command> [args]

BRAIN_CLI="${HOME}/.brain/brain_cli.py"

# Check if brain_cli.py exists
if [ ! -f "$BRAIN_CLI" ]; then
    echo "Error: brain_cli.py not found at $BRAIN_CLI"
    echo "Make sure Brain is installed at ~/.brain/"
    exit 1
fi

# Forward commands to brain_cli.py
case "$1" in
    sync)
        python3 "$BRAIN_CLI" sync
        ;;
    search)
        shift
        python3 "$BRAIN_CLI" search "$@"
        ;;
    info)
        shift
        python3 "$BRAIN_CLI" info "$@"
        ;;
    list)
        python3 "$BRAIN_CLI" list
        ;;
    build-index)
        python3 "$BRAIN_CLI" build-index
        ;;
    check)
        shift
        python3 "$BRAIN_CLI" check "$@"
        ;;
    help|--help|-h)
        echo "skills.sh — Brain skill management wrapper"
        echo ""
        echo "Usage: skills.sh <command> [args]"
        echo ""
        echo "Commands:"
        echo "  sync                   Pull registry and rebuild index if changed"
        echo "  search <query>         Search skills (use -term to exclude)"
        echo "  info <skill>           Show metadata and file tree for a skill"
        echo "  list                   List all skills in the registry"
        echo "  build-index            Rebuild index.json from skills on disk"
        echo "  check                  Validate frontmatter in all SKILL.md files"
        echo "  help                   Show this help message"
        echo ""
        echo "Examples:"
        echo "  skills.sh sync"
        echo "  skills.sh search 'react state management'"
        echo "  skills.sh info react-best-practices"
        ;;
    *)
        if [ -z "$1" ]; then
            echo "Error: No command specified"
            echo "Run 'skills.sh help' for usage information"
        else
            echo "Error: Unknown command '$1'"
            echo "Run 'skills.sh help' for usage information"
        fi
        exit 1
        ;;
esac
