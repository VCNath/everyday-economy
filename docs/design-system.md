# Everyday Economy Design System

Phase 8 introduces a clear/glass visual system for Everyday Economy. The goal is a premium, trustworthy dashboard that feels modern without becoming noisy.

## Palette

- Primary blue: `#2563EB`
- Deep blue: `#1D4ED8`
- Cyan highlight: `#38BDF8`
- Positive green: `#22C55E`
- Background: `#F8FBFF`
- Soft background: `#EEF6FF`
- Primary text: `#0F172A`
- Secondary text: `#475569`
- Positive: `#16A34A`
- Warning: `#F59E0B`
- Negative: `#EF4444`

Dark mode uses a navy/slate base with the same blue, cyan, and green accents.

## Theme Strategy

The app uses MUI for theme infrastructure and selected primitives, while keeping the custom Everyday Economy CSS visual language. The root theme provider writes `data-theme="light|dark"` to the document and persists the chosen mode in local storage.

Light mode is the primary public-facing experience. Dark mode is fully supported and should remain readable, calm, and operational.

## Glass Surfaces

Default app panels use:

- translucent white or slate background
- `backdrop-filter: blur(20px)`
- soft blue-tinted border
- soft shadow
- radius between `14px` and `24px`

Use glass surfaces for dashboard cards, page headers, map drawers, auth cards, account cards, and admin panels. Avoid putting cards inside cards unless the inner element is a repeated item or a tool surface.

## Typography and Spacing

- Headings are confident but not oversized inside operational pages.
- Hero-scale type is reserved for the landing page and major page hero surfaces.
- Standard section gap is `16px` to `24px`.
- Tables and admin views may stay dense, but rows need enough vertical rhythm to scan.

## Components

Phase 8 adds reusable UI primitives:

- `GlassCard`
- `SectionHeader`
- `PageHero`
- `StatusPill`
- `TrendPill`
- `DataTable`
- `FilterBar`
- `LoadingSkeleton`

Existing `.panel`, `.button`, `.badge`, `.compact-table`, and trust badge classes are restyled to match the new system so older pages inherit the polish without route rewrites.

## Trust Badges

Trust metadata should be visible but visually quieter than the metric value. Use compact badges for:

- freshness
- estimated values
- cached values
- source
- coverage score

Never rely on colour alone. Pair colour with text labels such as `Healthy`, `Estimated`, `Cached`, or `Partial coverage`.

## Motion

Motion should feel responsive and restrained:

- card hover lift
- button press/hover states
- tab and pill transitions
- skeleton loading shimmer

The app respects `prefers-reduced-motion` by shortening transitions and animations.

## Accessibility

- Keep visible focus states.
- Preserve labels for forms and controls.
- Icon-only buttons require `aria-label`.
- Tables need headers.
- Status must be expressed with text, not colour only.
- Mobile tap targets should remain comfortable and text should not clip.

## Implementation Notes

MUI is used as the component library foundation, but the product look is custom. Do not import MUI Icons; use `lucide-react` to stay consistent with the existing icon system.
