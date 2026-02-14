# Review Dimensions

Checklist for each review agent. Include the relevant checklist in each agent's prompt.

## 1. Codebase Consistency

Search the codebase to verify the spec aligns with established patterns:

- **Naming**: Do proposed file names, component names, and variables match existing conventions? (Check PascalCase for components, camelCase for functions, file naming patterns in the same directory.)
- **File placement**: Are new files placed in the correct directories per the architecture? (Check architecture.md module boundaries.)
- **Module boundaries**: Does the spec respect separation of concerns? (Simulation logic in `game/`, rendering in `render/`, UI in `ui/`.)
- **Store usage**: Does the spec correctly use existing store patterns? (Check whether it adds state where it shouldn't, or duplicates existing state.)
- **Import patterns**: Are proposed imports consistent with how other files in the same directory import?
- **Component patterns**: Do proposed React/R3F components follow the same structure as existing ones? (Hooks usage, prop patterns, ref patterns.)
- **Style/palette**: Do proposed colors, sizes, or UI elements match the project's visual palette from AGENTS.md?

## 2. Code Reuse

Search for existing code the spec could leverage instead of building from scratch:

- **Existing components**: Are there similar R3F or React components already in the codebase that could be extended or composed?
- **Utility functions**: Are there existing helpers in `game/` or `render/` that cover functionality the spec proposes to reimplement?
- **Shared patterns**: Does the codebase already have an established pattern for the type of feature the spec describes? (e.g., animation patterns, HUD card patterns, selection/hover patterns.)
- **Store selectors**: Are there existing store selectors or derived values that the spec could use?
- **Constants/configs**: Are there existing constants (tick rates, sizes, colors) the spec should reference instead of hardcoding?
- **Geometry/material reuse**: Are there existing Three.js geometries or materials that could be shared?

For each reuse opportunity: cite the existing file path and function/component name.

## 3. Performance (CPU/GPU)

Evaluate the spec's proposed implementation for performance pitfalls:

- **Render loop work**: Does any proposed `useFrame` work scale with entity count? Flag O(n) per-frame operations.
- **Geometry allocation**: Does the spec create geometry every frame or on every state change? Should it reuse/pool instead?
- **Material instances**: Does the spec propose creating new materials per instance where shared materials would work?
- **React re-renders**: Will the proposed state reads cause excessive React re-renders? Should zustand selectors be narrower?
- **Draw calls**: Does the spec increase draw call count significantly? Could instancing help?
- **Shader complexity**: Are proposed shaders or visual effects more complex than needed?
- **Event handling**: Does the spec add per-frame raycasts or expensive pointer event handling?
- **Memory**: Does the spec propose patterns that could leak (creating objects in render loops, uncleared refs)?

## 4. Scope & Complexity

Evaluate whether the spec is appropriately scoped:

- **File count**: How many new files does the spec propose? Flag if >3 new files — consider whether some could be merged.
- **Cross-cutting changes**: Does the spec touch many existing files? Flag if modifications span >4 existing files.
- **300-line rule**: Based on the described functionality, will any proposed file likely exceed 300 lines? Suggest splits.
- **Dependency chain**: Does the spec introduce circular or deep dependency chains between modules?
- **Feature creep**: Does the spec include functionality that could be deferred to a follow-up spec?
- **Unclear requirements**: Are any sections ambiguous enough to cause implementation confusion?
- **Out of scope alignment**: Does the "Out of Scope" section adequately bound the work?

## 5. Testability

Evaluate whether the spec's features can be tested:

- **Determinism**: Are the proposed behaviors deterministic and testable without timing/animation dependencies?
- **State isolation**: Can the game state changes be tested independently of rendering?
- **Simulation vs render**: Is there a clear boundary between testable simulation logic and visual-only behavior?
- **Edge cases**: Does the spec address edge cases that tests should cover? (Empty states, boundaries, null targets, multi-tile entities.)
- **Test file placement**: Per AGENTS.md, tests should be colocated (e.g., `__tests__/`). Flag if the spec implies test-unfriendly patterns.
- **Mock boundaries**: Can external dependencies (pointer events, Three.js renderer) be reasonably mocked?
