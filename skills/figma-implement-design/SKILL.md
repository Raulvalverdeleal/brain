---
name: figma-implement-design
dependencies: figma-mcp frontend-developer
description: Takes a Figma file and an optional PRD, and builds the full application — tokens, UI kit, pixel-faithful layout, mocked API layer, and clean build.
---

# figma-implement-design

## Config

```yaml
prd_file:        ?               # AGENTS.md | PRD.md | the project guidelines...
file_key:        ?               # extracted from Figma URL: figma.com/file/FILE_KEY/...
framework:       ?           # react | vue | svelte | vanilla
language:        ?      # typescript | javascript
styling:         ?        # css-modules | tailwind | styled-components | css
components_dir:  ?
pages_dir:       ?
styles_dir:      ?
public_dir:      ?
mock_dir:        ?
services_dir:    ?
router:          ?
package_manager: ?
dev_command:     ?
build_command:   ?
```

Any variable set to `?` → ask the user → update this block → continue.

---

## 0. Pre-flight

Before touching any code:

```bash
# Confirm the project is initialized
ls package.json || echo "MISSING — scaffold first"

# Confirm Figma MCP is available
# (figma_read_file should respond without error)
```

If the project does not exist yet, scaffold it according to `framework` and `language` before proceeding.

Confirm with the user:
- Is there a PRD? If yes, where?
- Are there multiple Figma pages? Which ones are in scope?
- Any existing design system or component library to integrate with?

---

## 1. Read the Figma file

```
figma_read_file(file_key, depth=2)
```

Get an overview: pages, top-level frames, overall structure.
Then drill into each in-scope page:

```
figma_read_nodes(file_key, node_ids=[page_frame_ids], depth=3)
```

> **Tip — node IDs:** Figma URLs use hyphens (`1-23`). The API requires colons (`1:23`). Always convert.  
> **Tip — styles:** `figma_extract_styles` only returns tokens if the file uses named Figma Styles. If it returns empty, inspect `.fills` directly on nodes via `figma_read_nodes`.

---

## 2. Map Figma → PRD (skip if no PRD)

If `prd_file` exists, read it. Extract: features, user flows, data entities, external integrations.

Build a correspondence table:

| Figma Screen | Frame ID | PRD Feature | Route | Notes |
|---|---|---|---|---|

Flag gaps:
- ❌ PRD feature with no Figma screen → confirm with user: skip or design a stub?
- ❌ Figma screen with no PRD feature → confirm: in scope or decorative?

**Present this map to the user and wait for confirmation before continuing.**

If there is no PRD, derive routes and features directly from Figma frame names.

---

## 3. Design tokens

```
figma_extract_styles(file_key, types=["FILL", "TEXT", "EFFECT", "GRID"])
```

Generate `{{styles_dir}}/tokens.css`:

```css
:root {
  /* Colors */
  --color-<semantic-name>: #HEX;

  /* Typography */
  --font-family-<n>: 'Name', fallback;
  --font-size-<n>: Xpx;
  --font-weight-<n>: N;
  --line-height-<n>: X;
  --letter-spacing-<n>: Xem;

  /* Spacing — 4px base grid */
  --space-1: 4px;
  --space-2: 8px;
  --space-3: 12px;
  --space-4: 16px;
  --space-6: 24px;
  --space-8: 32px;
  --space-12: 48px;
  --space-16: 64px;

  /* Radii */
  --radius-<n>: Xpx;

  /* Shadows */
  --shadow-<n>: X;

  /* Z-index scale */
  --z-base: 0;
  --z-overlay: 100;
  --z-modal: 200;
  --z-toast: 300;
}
```

Rules:
- **Never overwrite** if the file already exists — only append missing tokens.
- If `figma_extract_styles` returns empty for a type, extract values directly from nodes and name them by role (e.g. `--color-primary`, `--color-surface`).
- No hardcoded values anywhere in the codebase — CSS variables only.

---

## 4. Assets — download before continuing

Identify all exportable nodes:

```
figma_read_nodes(file_key, node_ids=[all_frame_ids], depth=2)
```

Collect: `VECTOR`, `BOOLEAN_OPERATION`, frames that are icons or illustrations.

```
figma_export_images(file_key, node_ids=[svg_ids],  format="svg")
figma_export_images(file_key, node_ids=[raster_ids], format="png", scale=2)
```

> ⚠️ Export URLs expire in ~30 minutes. Download immediately.

```bash
curl -o {{public_dir}}/icons/<name>.svg  "<url>"
curl -o {{public_dir}}/images/<name>.png "<url>"
```

Verify:
```bash
ls {{public_dir}}/icons {{public_dir}}/images
```

**Do not continue to step 5 until this passes.**

---

## 5. Mock layer

Everything external gets a mock. No real API calls, no real auth, no real payments.

### 5a. Mock data

Create `{{mock_dir}}/data/<feature>.ts` with realistic, representative data. No Lorem ipsum.

Rules:
- At least 5–10 items for lists.
- Include edge cases: long strings, empty states, error states.
- Mirror the real API shape exactly (so swapping the mock for real calls later requires zero refactoring).

### 5b. API service layer

Create `{{services_dir}}/<feature>.service.ts`:

```ts
// All functions simulate network latency
const delay = (ms = 300) => new Promise(r => setTimeout(r, ms))

export async function getItems(): Promise<Item[]> {
  await delay()
  return mockItems
}

export async function createItem(payload: CreateItemInput): Promise<Item> {
  await delay(500)
  return { id: crypto.randomUUID(), ...payload, createdAt: new Date().toISOString() }
}
```

All service functions must:
- Return the correct TypeScript types.
- Simulate realistic latency (`300–600ms`).
- Support an optional error simulation flag for testing error states.

### 5c. Auth mock

```ts
// src/mocks/auth.mock.ts
export const mockUser = {
  id: '1',
  name: 'Alex Johnson',
  email: 'alex@example.com',
  avatar: '/images/avatar.png',
  role: 'admin',
}

export function useAuth() {
  return { user: mockUser, isAuthenticated: true, login: async () => {}, logout: async () => {} }
}
```

Login flow: form visible, submit → redirect to dashboard, no credentials validated.

### 5d. Third-party integrations

| Integration type | Mock approach |
|---|---|
| Payment (Stripe, etc.) | Form visible, submit → `console.log(payload)` + success state |
| Maps | `<div>` sized correctly + placeholder |
| Charts/analytics | Static data from mock, correct dimensions |
| File upload | `<input type="file">` → stores in component state, no upload |
| Email / SMS | Form submits → success toast, nothing sent |
| OAuth | Button visible → redirect to `/dashboard` directly |

Standard placeholder component for non-implementable integrations:

```tsx
// src/components/IntegrationPlaceholder.tsx
interface Props { name: string; height?: number }

export function IntegrationPlaceholder({ name, height = 320 }: Props) {
  return (
    <div
      style={{ background: 'var(--color-surface-secondary)', height,
               display: 'flex', alignItems: 'center', justifyContent: 'center',
               borderRadius: 'var(--radius-md)', border: '2px dashed var(--color-border)' }}
      aria-label={`${name} — pending integration`}
    >
      <span style={{ color: 'var(--color-text-tertiary)', fontSize: 'var(--font-size-sm)' }}>
        {name} — pending integration
      </span>
    </div>
  )
}
```

---

## 6. UI Kit

```
figma_search_components(file_key)
```

For each component, drill into it:

```
figma_read_nodes(file_key, node_ids=[component_id], depth=4)
```

Create `{{components_dir}}/<ComponentName>.tsx`:

Requirements per component:
- One prop per variant and state (`intent`, `size`, `isLoading`, `isDisabled`, `isSelected`…).
- All variants via conditional classes — never duplicated JSX.
- Interactive states: hover/focus via CSS; `isLoading` renders a spinner and blocks interaction; `isDisabled` uses `aria-disabled` and `pointer-events: none`.
- CSS variables only — no hardcoded values.
- If the node has a `description`, it takes precedence over visual interpretation.
- Export named + default.

Component checklist:
- [ ] Atoms: Button, Input, Select, Checkbox, Radio, Toggle, Badge, Tag, Avatar, Icon, Spinner
- [ ] Layout: Card, Modal, Drawer, Tooltip, Popover, Dropdown
- [ ] Feedback: Toast/Snackbar, Alert, EmptyState, ErrorState, LoadingState, Skeleton
- [ ] Navigation: Navbar, Sidebar, Breadcrumb, Tabs, Pagination

Build only what exists in Figma — do not invent components.

---

## 7. Routing and shell

Set up all routes from the mapping table as stubs first, then fill them in step 8.

```tsx
// Protected routes grant access unconditionally in this phase
function PrivateRoute({ children }: { children: ReactNode }) {
  return <>{children}</>
}
```

Route structure:
- `/` → redirect to main entry point
- `/*` → `<NotFound />` with a "Go back" link
- All routes must be reachable without credentials.

---

## 8. Screen layout

Order: shell/global layout → happy path screens → secondary screens → empty/error/loading states.

For each screen:

```
figma_read_nodes(file_key, node_ids=[frame_id], depth=3)
```

If a section has `childCount > 0` and needs more detail:
```
figma_read_nodes(file_key, node_ids=[section_id], depth=4)
```

**Apply Figma values literally:**

| Property | Rule |
|---|---|
| `text` | Exact copy — never paraphrase or invent |
| `borderRadius` | Exact value in px, via CSS variable |
| `fill` | Exact hex, mapped to CSS variable |
| `width` FIXED | `width: Npx` |
| `width` FILL | `width: 100%` |
| `width` HUG | `width: fit-content` |
| `layoutMode` HORIZONTAL | `display: flex; flex-direction: row` |
| `layoutMode` VERTICAL | `display: flex; flex-direction: column` |
| `primaryAxisAlignItems` | `justify-content` |
| `counterAxisAlignItems` | `align-items` |
| `itemSpacing` | `gap` |
| `padding` | `padding: top right bottom left` |

Additional rules:
- If `wSizing`/`hSizing` is absent, use box dimensions as a reference, not fixed values.
- Node `description` overrides visual interpretation.
- Responsive: if Figma has mobile/tablet variants, implement all breakpoints.
- Animations: `{/* TODO: animate — <description> */}` with a static fallback; never block layout for animation.

For each screen, implement all states visible in Figma:
- ✅ Default / happy path
- ⬜ Loading (use Skeleton components)
- ❌ Error (use ErrorState component)
- 📭 Empty (use EmptyState component)

---

## 9. Forms

Every form must:
- Validate required fields client-side before submit.
- Show inline error messages per field.
- Disable the submit button while submitting (`isLoading` state).
- Show success feedback (toast or inline) after submission.
- Call the mock service, not a real endpoint.

```tsx
async function handleSubmit(data: FormData) {
  setIsLoading(true)
  try {
    await mockService.submit(data)
    showToast({ type: 'success', message: 'Saved successfully' })
  } catch {
    showToast({ type: 'error', message: 'Something went wrong. Try again.' })
  } finally {
    setIsLoading(false)
  }
}
```

---

## 10. Build and verify

```bash
{{package_manager}} install
{{dev_command}}
```

Fix compilation errors in order. No `@ts-ignore` or `any` without an explanatory comment.

Then run:
```bash
{{build_command}}
```

Production build must have zero errors.

### Final checklist

**Functional**
- [ ] Zero console errors or warnings
- [ ] All routes reachable; `/*` returns a 404 page
- [ ] Full happy path navigable end to end without credentials
- [ ] All forms validate required fields and show errors
- [ ] All mocked actions return visible feedback (toast, state change, redirect)
- [ ] Loading states visible during async operations
- [ ] Empty states visible when lists have no data
- [ ] Error states visible (simulate via error flag in mock)

**Visual fidelity**
- [ ] Typography matches Figma (family, weight, size, line-height)
- [ ] Colors match Figma (no hardcoded values)
- [ ] Spacing matches Figma (padding, gap, margin)
- [ ] Border radii match Figma
- [ ] Icons and images loaded and sized correctly
- [ ] Responsive: layout holds at 375px (mobile), 768px (tablet), 1280px (desktop)

**Accessibility**
- [ ] All `<img>` have meaningful `alt` text
- [ ] Placeholders have `aria-label`
- [ ] App is fully keyboard-navigable (Tab, Enter, Escape, Arrow keys where applicable)
- [ ] Focus ring visible on all interactive elements
- [ ] Color contrast meets WCAG AA minimum

---

## 11. HANDOFF.md

Generate at project root:

```md
# Handoff

## Implemented screens
- [x] Screen name — route `/path`

## Mocks pending real integration
| File | What's mocked | Integration needed |
|---|---|---|
| src/services/payments.service.ts | Stripe checkout | Stripe SDK + backend endpoint |

## Out-of-scope features
- Feature X: no Figma design provided, excluded by agreement with user.

## Animation TODOs
- `src/pages/Home.tsx:42` — hero entrance animation (fade + slide up)

## Known gaps
- Any divergence between PRD and what was built, with reason.
```