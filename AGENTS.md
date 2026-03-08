
## Skills

Project skills are located in `.agents/skills/`.

### Before starting any task

1. **List available skills:**
   ```bash
   ls .agents/skills/
   ```

2. **Search for skills relevant to your task:**
   ```bash
   ls .agents/skills/ | grep -i "keyword"
   ```
   Try multiple terms if the first search returns nothing (e.g. `auth`, `clerk`, `jwt`, `login`).

3. **Read the SKILL.md files that apply:**
   ```bash
   cat .agents/skills/skill-name/SKILL.md
   ```
   If a SKILL.md references additional files (playbooks, scripts, references), read those too.

4. **If no relevant skill exists**, proceed with your own judgment. Do not block the task.

### Notes

- A task may require combining multiple skills (e.g. implementation + testing + deployment).
- Prefer the more specific skill over a generic one when both apply.
- Reading an extra SKILL.md costs little; missing a relevant one can cost a lot.