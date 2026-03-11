---
name: skill-zipper
description: Compresses skills by removing verbosity while preserving usability. Use when a skill's token count is too high.
---

# Skill Zipper

Compresses a skill's SKILL.md into a minimal, token-efficient version that remains fully actionable.

## When to Use

- A skill's SKILL.md exceeds ~1500 tokens
- Multiple skills need to be installed but token budget is limited
- The skill contains verbose explanations, redundant sections, or extensive examples

## Compression Strategy

### 1. Strip Frontmatter to Essentials

Keep only:
- `name`
- `description`
- `dependencies` (if any)

Remove: `risk`, `source`, `date_added`, and any custom fields.

### 2. Remove These Entirely

- Philosophy/intro paragraphs
- "When to use" sections (redundant with description)
- Extensive code examples (keep 1 if critical, discard rest)
- Markdown formatting overhead (## headers → bold keywords)
- Redundant explanations of well-known concepts
- Extended lists where concise bullets suffice

### 3. Aggressive Text Compression

| Original | Compressed |
|---|---|
| "This skill embodies the principles of X by Author Name. Use it to transform..." | "Applies X principles." |
| Step-by-step numbered procedures | Concise numbered list |
| Multiple examples demonstrating same point | Single representative example |
| Links to external documentation | Remove (agent can search) |
| "### Section Name" headers | **Section Name** (bold inline) |

### 4. Preserve Critical Sections

- Required commands/scripts and their exact syntax
- Required env vars (but strip descriptions)
- Specific file paths or naming conventions
- Any "watch out for" or "common mistakes" warnings
- Tool names and their purposes

### 5. Formatting Rules

- Use bold for key terms: **do one thing**
- Use inline code for commands: `npm run build`
- Use compact lists: `- small functions - descriptive names - no side effects`
- No emoji
- No decorative sections

## Output Template

```markdown
---
name: skill-name
description: One sentence. When to use this skill.
dependencies: dep1 dep2
---

**Purpose**: Brief statement

**Key Principles** (3-5 bullets max):
- Principle 1
- Principle 2

**Required Tools**: tool1, tool2

**Commands**:
- `command syntax` — what it does
- `command syntax` — what it does

**Watch Out**:
- Common mistake 1
- Common mistake 2

**File Structure** (if relevant):
```
path/to/file — purpose
```
```

## Example: Before → After

### Before (182 tokens)
```markdown
# Clean Code Skill

This skill embodies the principles of "Clean Code" by Robert C. Martin (Uncle Bob). Use it to transform "code that works" into "code that is clean."

## When to Use
Use this skill when:
- Writing new code: To ensure high quality from the start.
- Reviewing Pull Requests: To provide constructive, principle-based feedback.
- Refactoring legacy code: To identify and remove code smells.

## 1. Meaningful Names
- **Use Intention-Revealing Names**: `elapsedTimeInDays` instead of `d`.
- **Avoid Disinformation**: Don't use `accountList` if it's actually a `Map`.
- **Make Meaningful Distinctions**: Avoid `ProductData` vs `ProductInfo`.

## 2. Functions
- **Small!**: Functions should be shorter than you think.
- **Do One Thing**: A function should do only one thing, and do it well.
...
```

### After (68 tokens)
```markdown
---
name: clean-code
description: Applies Clean Code principles for readable, maintainable code.
---

**Principles**: meaningful names • do one thing • small functions • no side effects • descriptive names

**Names**: intention-revealing (elapsedTimeInDays not d) • pronounceable • classes=nouns methods=verbs

**Functions**: <20 lines • 0-2 args • describe what not how

**Comments**: rewrite bad code • explain in code not comments • keep legal/todo

**Errors**: exceptions not codes • try-catch first • no null returns
```

## Workflow

1. Read the original SKILL.md
2. Identify what's essential vs verbose
3. Apply compression rules above
4. Verify compressed version still enables the agent to complete the skill's purpose
5. Replace original with compressed version

## Testing Compression Quality

After compression, verify the agent can still:
1. Identify when to use the skill
2. Execute the core workflow without guessing
3. Know which tools to use and their basic syntax
4. Avoid critical mistakes

If any verification fails, restore critical information.
