# 📋 Frontend Modernization Project Plan

**Goal:** Upgrade Next.js 13.5 → 14.x+, modernize dependencies, migrate to Bun & Biome  
**Estimated Duration:** 8-12 weeks  
**Status:** 📋 Planning  
**Created:** January 30, 2026

---

## 📊 Current State Analysis

### Codebase Metrics
| Metric | Count |
|--------|-------|
| Total TypeScript/JSX files | 381 |
| React Components | 240 |
| Pages (Pages Router) | 48 |
| Test files | 2 |
| `getServerSideProps` usage | 42 files |
| `getInitialProps` usage | 2 files |
| `next/router` imports | 21 files |
| `@mui/styles` usage | 245 files |
| `date-fns` imports | 479 files |

### Current Versions vs Latest
| Package | Current | Latest | Gap | Priority |
|---------|---------|--------|-----|----------|
| **next** | 13.5.11 | 16.1.6 | 3 major | 🔴 Critical |
| **react** | 18.2.0 | 19.2.4 | 1 major | 🔴 Critical |
| **typescript** | 4.9.5 | 5.9.3 | 1 major | 🟡 High |
| **@mui/material** | 5.11.15 | 7.3.7 | 2 major | 🔴 Critical |
| **@mui/styles** | 5.11.13 | 6.4.8 (deprecated) | 1 major | 🔴 Critical |
| **@mui/x-date-pickers** | 6.0.3 | 8.26.0 | 2 major | 🟡 High |
| **date-fns** | 2.12.0 | 4.1.0 | 2 major | 🟡 High |
| **eslint** | 8.0.0 | 9.39.2 | 1 major | 🟢 Medium |
| **prettier** | 2.2.0 | 3.8.1 | 1 major | 🟢 Medium |
| **@sentry/react** | 7.46.0 | 10.38.0 | 3 major | 🟡 High |
| **dotenv** | 8.2.0 | 17.2.3 | 9 major | 🟢 Low |
| **universal-cookie** | 4.0.3 | 8.0.1 | 4 major | 🟢 Medium |

### Deprecated/Legacy Packages
| Package | Status | Action |
|---------|--------|--------|
| `@zeit/next-css` | Deprecated (Zeit → Vercel) | Remove (built into Next.js) |
| `@mui/styles` | Deprecated in MUI v5+ | Migrate to `styled()` or `sx` prop |
| `enzyme` | Deprecated | Remove (using React Testing Library) |
| `enzyme-adapter-react-16` | Legacy | Remove |
| `react-ga` | Legacy | Consolidate to `react-ga4` only |
| `babel-plugin-lodash` | Optional | Evaluate need with tree-shaking |

---

## 🎯 Project Structure

### Phase Overview
| Phase | Name | Duration | Dependencies |
|-------|------|----------|--------------|
| 1 | Tooling Modernization | 1 week | None |
| 2 | TypeScript 5 Upgrade | 0.5 week | Phase 1 |
| 3 | React 19 Preparation | 1 week | Phase 2 |
| 4 | MUI v6/v7 Migration | 3 weeks | Phase 3 |
| 5 | Next.js 14 Upgrade | 1 week | Phase 4 |
| 6 | Next.js 15/16 Upgrade | 1-2 weeks | Phase 5 |
| 7 | Dependency Updates | 1 week | Phase 6 |
| 8 | Testing & Validation | 1-2 weeks | Phase 7 |

---

## 🏛️ Phase 1: Tooling Modernization (Bun + Biome)
*Duration: 1 week* | **Status: 📋 Not Started**

### Epic 1.1: Migrate from Yarn to Bun

#### Why Bun?
| Benefit | Impact |
|---------|--------|
| **17× faster** than Yarn for installs | Faster CI/CD |
| **Native TypeScript** support | No transpilation needed |
| **Built-in test runner** | Replace Jest |
| **Drop-in npm compatibility** | Minimal migration effort |
| **bun.lock already exists** | Partially prepared |

#### Tasks

| Task | Subtasks | Est. Hours | Status |
|------|----------|------------|--------|
| **1.1.1 Verify Bun compatibility** | • Run `bun install` with existing package.json<br>• Test `bun run dev`<br>• Test `bun run build`<br>• Document any failures | 2h | ⬜ |
| **1.1.2 Update package.json scripts** | • Replace `yarn` → `bun` in scripts<br>• Update CI/CD scripts<br>• Update documentation | 1h | ⬜ |
| **1.1.3 Remove Yarn artifacts** | • Delete `yarn.lock` (keep `bun.lock`)<br>• Remove `.yarnrc` if exists<br>• Update `.gitignore` | 0.5h | ⬜ |
| **1.1.4 Update CI/CD** | • Update GitHub Actions to use Bun<br>• Add `bun ci` for frozen lockfile<br>• Test CI pipeline | 2h | ⬜ |
| **1.1.5 Update developer docs** | • Update README.md<br>• Update CONTRIBUTING.md<br>• Update local-env-setup.md | 1h | ⬜ |

#### Rollback Plan
```bash
# If Bun causes issues:
rm bun.lock
yarn install
# Revert package.json script changes
```

---

### Epic 1.2: Migrate from ESLint + Prettier to Biome

#### Why Biome?
| Benefit | Impact |
|---------|--------|
| **10-25× faster** than ESLint + Prettier | Instant feedback |
| **Single config file** | `biome.json` replaces `.eslintrc.js` + `.prettierrc.json` |
| **Single dependency** | Replace 10+ packages |
| **80%+ rule compatibility** | CLI migration tool available |
| **Integrated formatter + linter** | One tool, one pass |

#### Current Linting Stack (to be replaced)
```json
{
  "devDependencies": {
    "eslint": "^8.0.0",
    "eslint-config-next": "^13.5.11",
    "eslint-import-resolver-typescript": "^4.4.4",
    "eslint-plugin-import": "^2.32.0",
    "eslint-plugin-react": "^7.16.0",
    "eslint-watch": "^7.0.0",
    "@eslint/eslintrc": "^3.3.3",
    "@eslint/js": "^9.39.1",
    "@next/eslint-plugin-next": "^16.0.6",
    "prettier": "2.2.0"
  }
}
```
**→ Replace with single `@biomejs/biome` package**

#### Tasks

| Task | Subtasks | Est. Hours | Status |
|------|----------|------------|--------|
| **1.2.1 Install Biome** | • Run `bun add -D @biomejs/biome`<br>• Initialize with `bunx biome init` | 0.5h | ⬜ |
| **1.2.2 Migrate ESLint config** | • Run `bunx biome migrate eslint`<br>• Review generated `biome.json`<br>• Manually adjust rules as needed | 2h | ⬜ |
| **1.2.3 Migrate Prettier config** | • Run `bunx biome migrate prettier`<br>• Verify formatting rules match<br>• Test with sample files | 1h | ⬜ |
| **1.2.4 Configure Next.js rules** | • Add Next.js-specific rules<br>• Configure `nursery` rules for React<br>• Set up `overrides` for test files | 2h | ⬜ |
| **1.2.5 Update package.json scripts** | • `lint` → `biome lint .`<br>• `format` → `biome format . --write`<br>• `check` → `biome check .`<br>• Add `lint:fix` → `biome check . --write` | 0.5h | ⬜ |
| **1.2.6 Apply formatting to codebase** | • Run `biome format . --write`<br>• Run `biome lint . --write`<br>• Review and commit changes | 2h | ⬜ |
| **1.2.7 Remove old linting packages** | • Remove ESLint packages from package.json<br>• Remove Prettier<br>• Delete `.eslintrc.js`, `.prettierrc.json` | 1h | ⬜ |
| **1.2.8 Update VS Code settings** | • Add Biome extension recommendation<br>• Update `.vscode/settings.json`<br>• Configure format on save | 0.5h | ⬜ |
| **1.2.9 Update CI/CD** | • Replace `yarn lint` → `bun run lint`<br>• Add Biome CI check | 1h | ⬜ |

#### Biome Configuration Template
```json
{
  "$schema": "https://biomejs.dev/schemas/1.9.0/schema.json",
  "organizeImports": {
    "enabled": true
  },
  "linter": {
    "enabled": true,
    "rules": {
      "recommended": true,
      "correctness": {
        "noUnusedVariables": "error",
        "noUnusedImports": "error"
      },
      "suspicious": {
        "noExplicitAny": "warn"
      },
      "style": {
        "useConst": "error",
        "noNonNullAssertion": "warn"
      }
    }
  },
  "formatter": {
    "enabled": true,
    "indentStyle": "space",
    "indentWidth": 2,
    "lineWidth": 100,
    "lineEnding": "lf"
  },
  "javascript": {
    "formatter": {
      "quoteStyle": "double",
      "trailingCommas": "es5"
    }
  },
  "files": {
    "ignore": ["node_modules", ".next", "devlink", "public"]
  }
}
```

#### VS Code Settings
```json
{
  "editor.defaultFormatter": "biomejs.biome",
  "editor.formatOnSave": true,
  "[javascript]": { "editor.defaultFormatter": "biomejs.biome" },
  "[typescript]": { "editor.defaultFormatter": "biomejs.biome" },
  "[typescriptreact]": { "editor.defaultFormatter": "biomejs.biome" },
  "editor.codeActionsOnSave": {
    "quickfix.biome": "explicit",
    "source.organizeImports.biome": "explicit"
  }
}
```

---

## 🏛️ Phase 2: TypeScript 5 Upgrade
*Duration: 0.5 week* | **Status: 📋 Not Started** | **Depends on: Phase 1**

### Epic 2.1: Upgrade TypeScript 4.9 → 5.x

#### Breaking Changes in TypeScript 5
| Change | Impact | Remediation |
|--------|--------|-------------|
| `lib.d.ts` changes | Type errors possible | Review and fix |
| Stricter decorator metadata | None (not using decorators) | N/A |
| `--target ES2022` | Better `async/await` | Update tsconfig |
| `moduleResolution: bundler` | New option for Next.js | Update tsconfig |

#### Tasks

| Task | Subtasks | Est. Hours | Status |
|------|----------|------------|--------|
| **2.1.1 Upgrade TypeScript** | • Run `bun add -D typescript@^5.9`<br>• Run `bun add -D @types/node@^22`<br>• Run `bun add -D @types/react@^18` | 0.5h | ⬜ |
| **2.1.2 Update tsconfig.json** | • Set `"target": "ES2022"`<br>• Set `"module": "ESNext"`<br>• Set `"moduleResolution": "bundler"`<br>• Enable `"verbatimModuleSyntax"` | 1h | ⬜ |
| **2.1.3 Fix type errors** | • Run `bun run check-types`<br>• Fix any new errors<br>• Update type assertions if needed | 4h | ⬜ |
| **2.1.4 Test build** | • Run `bun run build`<br>• Verify no runtime errors<br>• Test in development mode | 1h | ⬜ |

---

## 🏛️ Phase 3: React 19 Preparation
*Duration: 1 week* | **Status: 📋 Not Started** | **Depends on: Phase 2**

### Epic 3.1: Audit React 19 Compatibility

#### React 19 Breaking Changes
| Change | Impact | Files Affected |
|--------|--------|----------------|
| `ReactDOM.render` removed | Must use `createRoot` | Already using createRoot ✅ |
| `defaultProps` deprecated | Use default parameters | Check all components |
| `propTypes` deprecated | Use TypeScript | Already migrated ✅ |
| String refs removed | Already removed | N/A ✅ |
| `forwardRef` simplified | Optional refactor | Review components |
| New JSX transform | Already using | N/A ✅ |

#### Tasks

| Task | Subtasks | Est. Hours | Status |
|------|----------|------------|--------|
| **3.1.1 Audit defaultProps usage** | • Search for `Component.defaultProps`<br>• List all occurrences<br>• Plan migration to default parameters | 2h | ⬜ |
| **3.1.2 Check third-party compatibility** | • Review MUI v5 → React 19 support<br>• Check react-mentions, react-share, etc.<br>• Document incompatible packages | 4h | ⬜ |
| **3.1.3 Update @types/react** | • Upgrade to `@types/react@^19`<br>• Fix any type errors<br>• Test component rendering | 4h | ⬜ |
| **3.1.4 Upgrade React** | • Run `bun add react@^19 react-dom@^19`<br>• Test application<br>• Fix breaking changes | 8h | ⬜ |

---

## 🏛️ Phase 4: MUI v6/v7 Migration
*Duration: 3 weeks* | **Status: 📋 Not Started** | **Depends on: Phase 3**

### 🔴 Critical: @mui/styles Deprecation

**`@mui/styles` is DEPRECATED** and will be removed in MUI v6+. This affects **245 files** in the codebase.

#### Current Pattern (to be replaced)
```typescript
import makeStyles from "@mui/styles/makeStyles";

const useStyles = makeStyles((theme) => ({
  root: {
    padding: theme.spacing(2),
  },
}));
```

#### Target Pattern (Option A: styled())
```typescript
import { styled } from "@mui/material/styles";

const Root = styled("div")(({ theme }) => ({
  padding: theme.spacing(2),
}));
```

#### Target Pattern (Option B: sx prop)
```typescript
<Box sx={{ p: 2 }}>
  {/* content */}
</Box>
```

### Epic 4.1: Analyze @mui/styles Usage

| Task | Subtasks | Est. Hours | Status |
|------|----------|------------|--------|
| **4.1.1 Inventory makeStyles usage** | • Count files using `makeStyles`<br>• Categorize by complexity<br>• Identify theme dependencies | 4h | ⬜ |
| **4.1.2 Create migration strategy** | • Simple styles → `sx` prop<br>• Complex styles → `styled()`<br>• Theme-dependent → keep pattern | 2h | ⬜ |
| **4.1.3 Create codemod scripts** | • Auto-convert simple cases<br>• Generate migration report<br>• Test on sample files | 8h | ⬜ |

### Epic 4.2: Migrate Components (Batch 1 - Simple)

| Task | Subtasks | Est. Hours | Status |
|------|----------|------------|--------|
| **4.2.1 Migrate utility components** | • Buttons, Icons, Typography<br>• Simple layouts<br>• ~50 files | 16h | ⬜ |
| **4.2.2 Test migrated components** | • Visual regression testing<br>• Theme switching test<br>• Mobile responsiveness | 4h | ⬜ |

### Epic 4.3: Migrate Components (Batch 2 - Complex)

| Task | Subtasks | Est. Hours | Status |
|------|----------|------------|--------|
| **4.3.1 Migrate form components** | • Input fields, selects<br>• Date pickers<br>• ~30 files | 12h | ⬜ |
| **4.3.2 Migrate layout components** | • Headers, footers, sidebars<br>• Cards, dialogs<br>• ~40 files | 16h | ⬜ |
| **4.3.3 Migrate page components** | • Hub pages, project pages<br>• Profile, settings<br>• ~50 files | 20h | ⬜ |

### Epic 4.4: Upgrade MUI Packages

| Task | Subtasks | Est. Hours | Status |
|------|----------|------------|--------|
| **4.4.1 Upgrade to MUI v6** | • `bun add @mui/material@^6`<br>• Remove `@mui/styles`<br>• Fix breaking changes | 8h | ⬜ |
| **4.4.2 Upgrade @mui/x-date-pickers** | • Upgrade to v7/v8<br>• Update API usage<br>• Fix date formatting | 4h | ⬜ |
| **4.4.3 Optional: Upgrade to MUI v7** | • Only if stable<br>• Review changelog<br>• Test thoroughly | 8h | ⬜ |

---

## 🏛️ Phase 5: Next.js 14 Upgrade
*Duration: 1 week* | **Status: 📋 Not Started** | **Depends on: Phase 4**

### Breaking Changes: 13.5 → 14.x
| Change | Impact | Remediation |
|--------|--------|-------------|
| Node.js 18.17+ required | Already on Node 24 ✅ | N/A |
| `next export` removed | Using `output: 'export'` | Update next.config.js |
| Minimum React 18.2 | Already using ✅ | N/A |
| ImageResponse import changed | Check usage | Update imports |
| `next/server` import changes | Check middleware | Update imports |

#### Tasks

| Task | Subtasks | Est. Hours | Status |
|------|----------|------------|--------|
| **5.1.1 Upgrade Next.js** | • `bun add next@^14`<br>• Update eslint-config-next<br>• Update @next/bundle-analyzer | 2h | ⬜ |
| **5.1.2 Update next.config.js** | • Replace `next export` usage<br>• Review experimental flags<br>• Update image config | 2h | ⬜ |
| **5.1.3 Fix breaking changes** | • Update imports<br>• Fix deprecated APIs<br>• Test all pages | 8h | ⬜ |
| **5.1.4 Test SSR** | • Test all 48 pages<br>• Verify getServerSideProps<br>• Check hydration | 8h | ⬜ |

---

## 🏛️ Phase 6: Next.js 15/16 Upgrade
*Duration: 1-2 weeks* | **Status: 📋 Not Started** | **Depends on: Phase 5**

### Breaking Changes: 14.x → 15.x → 16.x

| Change | Version | Impact | Remediation |
|--------|---------|--------|-------------|
| React 19 required | 15.0+ | Already upgraded in Phase 3 | N/A |
| Async Request APIs | 15.0+ | `params`, `searchParams` async | Use `await` |
| Caching default changes | 15.0+ | fetch() not cached by default | Explicit caching |
| `next/dynamic` changes | 15.0+ | ssr option renamed | Update options |
| Geo/IP removed from Middleware | 15.0+ | Check middleware usage | Use alternatives |
| Runtime defaults changed | 16.0+ | Edge as default for some | Verify runtime |

#### Tasks

| Task | Subtasks | Est. Hours | Status |
|------|----------|------------|--------|
| **6.1.1 Upgrade to Next.js 15** | • `bun add next@^15`<br>• Run codemod: `bunx @next/codemod@canary upgrade latest` | 2h | ⬜ |
| **6.1.2 Fix async params** | • Update pages with params<br>• Use `await` for searchParams<br>• Test dynamic routes | 8h | ⬜ |
| **6.1.3 Review caching** | • Audit fetch() calls<br>• Add explicit caching where needed<br>• Test data freshness | 4h | ⬜ |
| **6.1.4 Upgrade to Next.js 16** | • `bun add next@^16`<br>• Fix any new breaking changes<br>• Test thoroughly | 8h | ⬜ |
| **6.1.5 Performance validation** | • Run Lighthouse audits<br>• Check Core Web Vitals<br>• Compare with baseline | 4h | ⬜ |

---

## 🏛️ Phase 7: Dependency Updates
*Duration: 1 week* | **Status: 📋 Not Started** | **Depends on: Phase 6**

### Epic 7.1: Update Major Dependencies

| Package | Current → Target | Breaking Changes | Est. Hours |
|---------|------------------|------------------|------------|
| **date-fns** | 2.12 → 4.1 | New import structure | 8h |
| **@sentry/react** | 7.46 → 10.x | New API, smaller bundle | 4h |
| **universal-cookie** | 4.0 → 8.0 | API changes | 2h |
| **@react-google-maps/api** | 1.13 → 2.20 | Hook-based API | 4h |
| **react-avatar-editor** | 11.0 → 14.0 | Canvas API changes | 2h |
| **react-loader-spinner** | 3.1 → 8.0 | Component API changed | 2h |
| **react-share** | 4.4 → 5.2 | New components | 1h |
| **react-youtube** | 7.14 → 10.1 | React 18+ features | 1h |

#### Tasks

| Task | Subtasks | Est. Hours | Status |
|------|----------|------------|--------|
| **7.1.1 Update date-fns** | • `bun add date-fns@^4`<br>• Update 479 import statements<br>• Fix locale imports<br>• Test date formatting | 8h | ⬜ |
| **7.1.2 Update Sentry** | • `bun add @sentry/react@^10`<br>• Update initialization<br>• Update error boundaries<br>• Test error reporting | 4h | ⬜ |
| **7.1.3 Update remaining packages** | • Batch update minor packages<br>• Fix any breaking changes<br>• Run tests | 8h | ⬜ |

### Epic 7.2: Remove Deprecated Packages

| Package | Action | Replacement |
|---------|--------|-------------|
| `@zeit/next-css` | Remove | Built into Next.js |
| `enzyme` | Remove | Already using Testing Library |
| `enzyme-adapter-react-16` | Remove | N/A |
| `react-ga` | Remove | Consolidate to `react-ga4` |
| `next-compose-plugins` | Remove | Use native config |
| `babel-plugin-lodash` | Evaluate | Tree-shaking may suffice |

---

## 🏛️ Phase 8: Testing & Validation
*Duration: 1-2 weeks* | **Status: 📋 Not Started** | **Depends on: Phase 7**

### Epic 8.1: Automated Testing

| Task | Subtasks | Est. Hours | Status |
|------|----------|------------|--------|
| **8.1.1 Setup Bun test runner** | • Configure `bun test`<br>• Migrate Jest config<br>• Run existing tests | 4h | ⬜ |
| **8.1.2 Add critical path tests** | • Authentication flows<br>• Project CRUD<br>• Organization CRUD<br>• Hub navigation | 16h | ⬜ |
| **8.1.3 Visual regression tests** | • Set up Playwright<br>• Screenshot key pages<br>• Compare before/after | 8h | ⬜ |

### Epic 8.2: Manual Testing

| Test Area | Test Cases | Status |
|-----------|------------|--------|
| **Authentication** | Sign up, sign in, sign out, password reset | ⬜ |
| **Projects** | Create, edit, delete, search, filter | ⬜ |
| **Organizations** | Create, edit, members, permissions | ⬜ |
| **Hubs** | Browse, filter, hub-specific content | ⬜ |
| **Chat** | Send messages, notifications | ⬜ |
| **Mobile** | All above on mobile viewport | ⬜ |
| **Themes** | Custom hub themes, default theme | ⬜ |
| **SSR** | All pages render server-side | ⬜ |
| **SEO** | Meta tags, structured data | ⬜ |

### Epic 8.3: Performance Validation

| Metric | Baseline | Target | Status |
|--------|----------|--------|--------|
| **Lighthouse Performance** | TBD | 90+ | ⬜ |
| **First Contentful Paint** | TBD | < 1.8s | ⬜ |
| **Largest Contentful Paint** | TBD | < 2.5s | ⬜ |
| **Time to Interactive** | TBD | < 3.8s | ⬜ |
| **Bundle Size (JS)** | TBD | -20% | ⬜ |
| **Build Time** | TBD | -30% | ⬜ |
| **Install Time** | ~60s (Yarn) | ~5s (Bun) | ⬜ |

---

## 📋 Risk Assessment

### High Risk Items
| Risk | Probability | Impact | Mitigation |
|------|-------------|--------|------------|
| MUI v6 migration breaks styles | High | High | Incremental migration, visual testing |
| React 19 breaks third-party libs | Medium | High | Check compatibility before upgrade |
| Next.js 15+ caching changes | Medium | High | Extensive testing, explicit caching |
| date-fns v4 import changes | High | Medium | Codemod scripts, batch updates |

### Medium Risk Items
| Risk | Probability | Impact | Mitigation |
|------|-------------|--------|------------|
| Biome rule differences | Medium | Medium | Review and tune config |
| Bun compatibility issues | Low | Medium | Keep Yarn as fallback |
| TypeScript 5 stricter checks | Medium | Low | Fix incrementally |

### Rollback Procedures
1. **Git tags** at each phase completion
2. **Feature branches** for each phase
3. **Bun → Yarn fallback** script
4. **Biome → ESLint fallback** config kept temporarily

---

## 📅 Timeline (Gantt-style)

```
Week 1:  [Phase 1: Bun + Biome                    ]
Week 2:  [P2: TS5][    Phase 3: React 19         ]
Week 3-5:[        Phase 4: MUI Migration          ]
Week 6:  [Phase 5: Next.js 14                     ]
Week 7-8:[Phase 6: Next.js 15/16                  ]
Week 9:  [Phase 7: Dependencies                   ]
Week 10-11: [Phase 8: Testing & Validation        ]
Week 12: [Buffer / Fixes / Polish                 ]
```

---

## 📊 Success Metrics

| Metric | Target |
|--------|--------|
| All 48 pages load without errors | ✅ |
| All 240 components render correctly | ✅ |
| Lighthouse Performance Score | 90+ |
| Build time reduction | 30%+ |
| Install time reduction | 90%+ (Yarn → Bun) |
| Lint/format time reduction | 90%+ (ESLint → Biome) |
| Zero deprecated packages | ✅ |
| TypeScript strict mode passing | ✅ |
| All critical paths tested | ✅ |

---

## 📝 Decision Log

| Decision | Date | Rationale |
|----------|------|-----------|
| Keep Pages Router (not App Router) | 2026-01-30 | 48 pages, 42 getServerSideProps - too much refactoring |
| Bun over pnpm | 2026-01-30 | Already has bun.lock, 17× faster, built-in TypeScript |
| Biome over ESLint 9 flat config | 2026-01-30 | 10-25× faster, single dependency, better DX |
| MUI v6 before v7 | 2026-01-30 | v7 may be too new, v6 is stable step |

---

## 🔗 References

- [Next.js Upgrade Guide](https://nextjs.org/docs/pages/guides/upgrading)
- [MUI Migration to v6](https://mui.com/material-ui/migration/upgrade-to-v6/)
- [Biome Migration Guide](https://biomejs.dev/guides/migrate-eslint-prettier/)
- [Bun Documentation](https://bun.sh/docs)
- [React 19 Release Notes](https://react.dev/blog/2024/12/05/react-19)
- [TypeScript 5.x Release Notes](https://www.typescriptlang.org/docs/handbook/release-notes/typescript-5-0.html)
- [date-fns v3/v4 Migration](https://date-fns.org/v3/docs/Change-Log)

---

## ✅ Pre-Flight Checklist

Before starting:
- [ ] Communicate plan to team
- [ ] Set up staging environment
- [ ] Create baseline performance metrics
- [ ] Tag current `master` as `pre-modernization`
- [ ] Schedule maintenance window for final merge

---

*Last Updated: January 30, 2026*
