# Excalidraw JSON Schema Reference

This document describes the structure of Excalidraw `.excalidraw` files for diagram generation.

## Top-Level Structure

```typescript
interface ExcalidrawFile {
  type: "excalidraw";
  version: number;           // Always 2
  source: string;            // "https://excalidraw.com"
  elements: ExcalidrawElement[];
  appState: AppState;
  files: Record<string, any>; // Usually empty {}
}
```

## AppState

```typescript
interface AppState {
  viewBackgroundColor: string; // Hex color, e.g., "#ffffff"
  gridSize: number;            // Typically 20
}
```

## ExcalidrawElement Base Properties

All elements share these common properties:

```typescript
interface BaseElement {
  id: string;                  // Unique identifier
  type: ElementType;           // See Element Types below
  x: number;                   // X coordinate (pixels from top-left)
  y: number;                   // Y coordinate (pixels from top-left)
  width: number;               // Width in pixels
  height: number;              // Height in pixels
  angle: number;               // Rotation angle in radians (usually 0)
  strokeColor: string;         // Hex color, e.g., "#1e1e1e"
  backgroundColor: string;     // Hex color or "transparent"
  fillStyle: "solid" | "hachure" | "cross-hatch";
  strokeWidth: number;         // 1-4 typically
  strokeStyle: "solid" | "dashed" | "dotted";
  roughness: number;           // 0-2, controls hand-drawn effect (1 = default)
  opacity: number;             // 0-100
  groupIds: string[];          // IDs of groups this element belongs to
  frameId: null;               // Usually null
  index: string;               // Stacking order identifier
  roundness: Roundness | null;
  seed: number;                // Random seed for deterministic rendering
  version: number;             // Element version (increment on edit)
  versionNonce: number;        // Random number changed on edit
  isDeleted: boolean;          // Should be false
  boundElements: BoundElement[]; // Array of bound child elements (text on arrows/shapes)
  updated: number;             // Timestamp in milliseconds
  link: null;                  // External link (usually null)
  locked: boolean;             // Whether element is locked
}
```

## Bound Element Types

```typescript
interface BoundElement {
  id: string;                  // ID of the bound child element
  type: "text";                // Currently always "text"
}
```

## Text Binding (containerId)

When a text element is bound to a container (arrow, rectangle, etc.), it carries a `containerId`:

```typescript
interface BoundTextElement extends BaseElement {
  type: "text";
  containerId: string;         // ID of the parent container element
  originalText: string;        // Original text content
  autoResize: boolean;         // Whether text auto-resizes
  lineHeight: number;          // Line height multiplier (e.g., 1.25)
  text: string;
  fontSize: number;
  fontFamily: number;
  textAlign: "left" | "center" | "right";
  verticalAlign: "top" | "middle" | "bottom";
  roundness: null;
}
```

## Element Types

### Rectangle

```typescript
interface RectangleElement extends BaseElement {
  type: "rectangle";
  roundness: { type: 3 };      // 3 = rounded corners
}
```

Text on rectangles must use a **separate bound text element** (see Text Binding above). Do not set `text` properties directly on the shape.

**Example (rectangle with bound text):**
```json
{
  "id": "rect1",
  "type": "rectangle",
  "x": 100,
  "y": 100,
  "width": 200,
  "height": 100,
  "strokeColor": "#1e1e1e",
  "backgroundColor": "#a5d8ff",
  "boundElements": [{ "id": "rect1-text", "type": "text" }],
  "roundness": { "type": 3 }
}
```

**Matching bound text:**
```json
{
  "id": "rect1-text",
  "type": "text",
  "x": 140,
  "y": 137,
  "width": 120,
  "height": 25,
  "text": "My Box",
  "fontSize": 20,
  "fontFamily": 5,
  "textAlign": "center",
  "verticalAlign": "middle",
  "containerId": "rect1",
  "originalText": "My Box",
  "autoResize": true,
  "lineHeight": 1.25
}
```

### Ellipse

```typescript
interface EllipseElement extends BaseElement {
  type: "ellipse";
}
```

Text on ellipses must use a **separate bound text element** (same pattern as rectangle).

### Diamond

```typescript
interface DiamondElement extends BaseElement {
  type: "diamond";
}
```

Text on diamonds must use a **separate bound text element** (same pattern as rectangle).

### Arrow

```typescript
interface ArrowElement extends BaseElement {
  type: "arrow";
  points: [number, number][];  // Array of [x, y] coordinates relative to element
  startBinding: Binding | null;
  endBinding: Binding | null;
  startArrowhead: "arrow" | null;
  endArrowhead: "arrow" | null;
  lastCommittedPoint: [number, number] | null;
  roundness: { type: 2 } | null; // null = straight/elbow, type 2 = curved
}
```

**Example (with bound label):**
```json
{
  "id": "arrow1",
  "type": "arrow",
  "x": 100,
  "y": 100,
  "width": 200,
  "height": 0,
  "points": [
    [0, 0],
    [200, 0]
  ],
  "roundness": null,
  "startBinding": null,
  "endBinding": null,
  "boundElements": [{ "id": "arrow-label-1", "type": "text" }]
}
```

**Matching bound text element:**
```json
{
  "id": "arrow-label-1",
  "type": "text",
  "x": 178,
  "y": 87,
  "width": 44,
  "height": 25,
  "text": "flows",
  "fontSize": 16,
  "fontFamily": 5,
  "textAlign": "center",
  "verticalAlign": "middle",
  "containerId": "arrow1",
  "originalText": "flows",
  "autoResize": true,
  "lineHeight": 1.25
}
```

**Points explanation:**
- First point `[0, 0]` is relative to `(x, y)`
- Subsequent points are relative to the first point
- For straight horizontal arrow: `[[0, 0], [width, 0]]`
- For straight vertical arrow: `[[0, 0], [0, height]]`

### Line

```typescript
interface LineElement extends BaseElement {
  type: "line";
  points: [number, number][];
  startBinding: Binding | null;
  endBinding: Binding | null;
  roundness: { type: 2 } | null;
}
```

### Text

```typescript
interface TextElement extends BaseElement {
  type: "text";
  text: string;
  fontSize: number;
  fontFamily: number;
  textAlign: "left" | "center" | "right";
  verticalAlign: "top" | "middle" | "bottom";
  roundness: null;
  containerId: string | null;    // Parent container ID when bound
  originalText: string;          // Original text content
  autoResize: boolean;           // Auto-resize enabled
  lineHeight: number;            // Line height (e.g., 1.25)
}
```

**Example (standalone):**
```json
{
  "id": "text1",
  "type": "text",
  "x": 100,
  "y": 100,
  "width": 150,
  "height": 25,
  "text": "Hello World",
  "fontSize": 20,
  "fontFamily": 5,
  "textAlign": "left",
  "verticalAlign": "top",
  "roundness": null,
  "containerId": null,
  "originalText": "Hello World",
  "autoResize": true,
  "lineHeight": 1.25
}
```

**Example (bound to a shape/arrow — containerId set):**
See the Arrow section above for a bound text example.

**Width/Height calculation:**
- Width ≈ `text.length * fontSize * 0.6`
- Height ≈ `fontSize * 1.2 * numberOfLines`

## Bindings

Bindings connect arrows to shapes, so the arrow moves with the shape when dragged. A binding is **bidirectional** — both the arrow and the shape must reference each other.

### Binding Interface

```typescript
interface Binding {
  elementId: string;           // ID of the bound shape element
  focus: number;               // -1 to 1, position along that edge
  gap: number;                 // Distance from the shape edge (pixels)
}
```

### Binding Direction Rule

All arrows connecting shapes must use `startBinding` and `endBinding`. This requires **three parts** to be in sync:

1. **Arrow** carries `startBinding` and/or `endBinding` pointing to shape IDs
2. **Shapes** each have the arrow ID in their `boundElements` array as `{"id": "<arrow_id>", "type": "arrow"}`
3. Text can be bound to the arrow itself via `containerId` (separate from shape bindings)

### Focus Values by Edge Position

| Position on edge | focus |
|------------------|-------|
| Center | 0 |
| Top-left corner | ≈ -1 (for vertical edge), ≈ -1 (for horizontal edge) |
| Bottom-right corner | ≈ 1 |

### Complete Example: Arrow Between Two Shapes

```json
[
  {
    "id": "box-a",
    "type": "rectangle",
    "x": 150, "y": 150, "width": 180, "height": 80,
    "boundElements": [
      {"id": "box-a-text", "type": "text"},
      {"id": "arrow-1", "type": "arrow"}
    ]
  },
  {
    "id": "box-a-text",
    "type": "text",
    "x": 174, "y": 177, "width": 132, "height": 25,
    "text": "Process A",
    "fontSize": 20, "fontFamily": 5,
    "textAlign": "center", "verticalAlign": "middle",
    "containerId": "box-a",
    "originalText": "Process A",
    "autoResize": true, "lineHeight": 1.25
  },
  {
    "id": "box-b",
    "type": "rectangle",
    "x": 470, "y": 150, "width": 180, "height": 80,
    "boundElements": [
      {"id": "box-b-text", "type": "text"},
      {"id": "arrow-1", "type": "arrow"}
    ]
  },
  {
    "id": "box-b-text",
    "type": "text",
    "x": 494, "y": 177, "width": 132, "height": 25,
    "text": "Process B",
    "fontSize": 20, "fontFamily": 5,
    "textAlign": "center", "verticalAlign": "middle",
    "containerId": "box-b",
    "originalText": "Process B",
    "autoResize": true, "lineHeight": 1.25
  },
  {
    "id": "arrow-1",
    "type": "arrow",
    "x": 330, "y": 190, "width": 140, "height": 0,
    "points": [[0, 0], [140, 0]],
    "startBinding": {"elementId": "box-a", "focus": 0.0, "gap": 5},
    "endBinding": {"elementId": "box-b", "focus": 0.0, "gap": 5},
    "boundElements": [],
    "endArrowhead": "arrow"
  }
]
```

## Common Colors

| Color Name | Hex Code | Use Case |
|------------|----------|----------|
| Black | `#1e1e1e` | Default stroke |
| Light Blue | `#a5d8ff` | Primary entities |
| Light Green | `#b2f2bb` | Process steps |
| Yellow | `#ffd43b` | Important/Central |
| Light Red | `#ffc9c9` | Warnings/Errors |
| Cyan | `#96f2d7` | Secondary items |
| Transparent | `transparent` | No fill |
| White | `#ffffff` | Background |

## ID Generation

IDs should be unique strings. Common patterns:

```javascript
// Timestamp-based
const id = Date.now().toString(36) + Math.random().toString(36).substr(2);

// Sequential
const id = "element-" + counter++;

// Descriptive
const id = "step-1", "entity-user", "arrow-1-to-2";
```

## Seed Generation

Seeds are used for deterministic randomness in hand-drawn effect:

```javascript
const seed = Math.floor(Math.random() * 2147483647);
```

## Version and VersionNonce

```javascript
const version = 1;  // Increment when element is edited
const versionNonce = Math.floor(Math.random() * 2147483647);
```

## Coordinate System

- Origin `(0, 0)` is top-left corner
- X increases to the right
- Y increases downward
- All units are in pixels

## Recommended Spacing

| Context | Spacing |
|---------|---------|
| Horizontal gap between elements | 200-300px |
| Vertical gap between rows | 100-150px |
| Minimum margin from edge | 50px |
| Arrow-to-box clearance | 20-30px |

## Font Families

| ID | Name | Description |
|----|------|-------------|
| 1 | Virgil | Hand-drawn style (default) |
| 2 | Helvetica | Clean sans-serif |
| 3 | Cascadia | Monospace |
| 5 | Excalifont | Modern Excalidraw font (recommended for new diagrams) |

## Validation Rules

✅ **Required:**
- All IDs must be unique
- `type` must match actual element type
- `version` must be an integer ≥ 1
- `opacity` must be 0-100

⚠️ **Recommended:**
- Keep `roughness` at 1 for consistency
- Use `strokeWidth` of 2 for clarity
- Set `isDeleted` to `false`
- Set `locked` to `false`
- Keep `frameId`, `link` as `null`
- For arrow labels, use bound text with `containerId` and `boundElements` — not standalone text elements

## Complete Minimal Example

```json
{
  "type": "excalidraw",
  "version": 2,
  "source": "https://excalidraw.com",
  "elements": [
    {
      "id": "box1",
      "type": "rectangle",
      "x": 100,
      "y": 100,
      "width": 200,
      "height": 100,
      "angle": 0,
      "strokeColor": "#1e1e1e",
      "backgroundColor": "#a5d8ff",
      "fillStyle": "solid",
      "strokeWidth": 2,
      "strokeStyle": "solid",
      "roughness": 1,
      "opacity": 100,
      "groupIds": [],
      "frameId": null,
      "index": "a0",
      "roundness": { "type": 3 },
      "seed": 1234567890,
      "version": 1,
      "versionNonce": 987654321,
      "isDeleted": false,
      "boundElements": [{ "id": "box1-text", "type": "text" }],
      "updated": 1706659200000,
      "link": null,
      "locked": false
    },
    {
      "id": "box1-text",
      "type": "text",
      "x": 155,
      "y": 137,
      "width": 90,
      "height": 25,
      "angle": 0,
      "strokeColor": "#1e1e1e",
      "backgroundColor": "transparent",
      "fillStyle": "solid",
      "strokeWidth": 2,
      "strokeStyle": "solid",
      "roughness": 1,
      "opacity": 100,
      "groupIds": [],
      "frameId": null,
      "index": "a1",
      "roundness": null,
      "seed": 1234567891,
      "version": 1,
      "versionNonce": 987654322,
      "isDeleted": false,
      "boundElements": [],
      "updated": 1706659200000,
      "link": null,
      "locked": false,
      "text": "Hello",
      "fontSize": 20,
      "fontFamily": 5,
      "textAlign": "center",
      "verticalAlign": "middle",
      "containerId": "box1",
      "originalText": "Hello",
      "autoResize": true,
      "lineHeight": 1.25
    },
    {
      "id": "arrow1",
      "type": "arrow",
      "x": 300,
      "y": 150,
      "width": 150,
      "height": 0,
      "angle": 0,
      "strokeColor": "#1e1e1e",
      "backgroundColor": "transparent",
      "fillStyle": "solid",
      "strokeWidth": 2,
      "strokeStyle": "solid",
      "roughness": 1,
      "opacity": 100,
      "groupIds": [],
      "frameId": null,
      "index": "a2",
      "roundness": null,
      "seed": 1234567892,
      "version": 1,
      "versionNonce": 987654323,
      "isDeleted": false,
      "boundElements": [{ "id": "arrow-label-1", "type": "text" }],
      "updated": 1706659200000,
      "link": null,
      "locked": false,
      "points": [[0, 0], [150, 0]],
      "startBinding": null,
      "endBinding": null
    },
    {
      "id": "arrow-label-1",
      "type": "text",
      "x": 354,
      "y": 138,
      "width": 42,
      "height": 25,
      "angle": 0,
      "strokeColor": "#1e1e1e",
      "backgroundColor": "transparent",
      "fillStyle": "solid",
      "strokeWidth": 2,
      "strokeStyle": "solid",
      "roughness": 1,
      "opacity": 100,
      "groupIds": [],
      "frameId": null,
      "index": "a3",
      "roundness": null,
      "seed": 1234567893,
      "version": 1,
      "versionNonce": 987654324,
      "isDeleted": false,
      "boundElements": [],
      "updated": 1706659200000,
      "link": null,
      "locked": false,
      "text": "flows",
      "fontSize": 16,
      "fontFamily": 5,
      "textAlign": "center",
      "verticalAlign": "middle",
      "containerId": "arrow1",
      "originalText": "flows",
      "autoResize": true,
      "lineHeight": 1.25
    }
  ],
  "appState": {
    "viewBackgroundColor": "#ffffff",
    "gridSize": 20
  },
  "files": {}
}
```
