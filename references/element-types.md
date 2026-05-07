# Excalidraw Element Types Guide

Detailed specifications for each Excalidraw element type with visual examples and use cases.

## Element Type Overview

| Type | Visual | Primary Use | Text Support |
|------|--------|-------------|--------------|
| `rectangle` | □ | Boxes, containers, process steps | ✅ Yes |
| `ellipse` | ○ | Emphasis, terminals, states | ✅ Yes |
| `diamond` | ◇ | Decision points, choices | ✅ Yes |
| `arrow` | → | Directional flow, relationships | ✅ Yes (bound text) |
| `line` | — | Connections, dividers | ❌ No |
| `text` | A | Labels, annotations, titles | ✅ (Its purpose) |

---

## Rectangle

**Best for:** Process steps, entities, data stores, components

### Properties

Shapes (rectangle, ellipse, diamond) require a **separate bound text element** for text. The container (`boundElements`) and text (`containerId`) reference each other:

```typescript
// Container (shape)
{
  type: "rectangle",
  id: "box1",
  boundElements: [{ id: "box1-text", type: "text" }]
}

// Bound text (separate element)
{
  type: "text",
  id: "box1-text",
  text: "Step Name",
  fontSize: 20,
  fontFamily: 5,
  textAlign: "center",
  verticalAlign: "middle",
  containerId: "box1",
  originalText: "Step Name",
  autoResize: true,
  lineHeight: 1.25
}
```

### Use Cases

| Scenario | Configuration |
|----------|---------------|
| **Process step** | Green background (`#b2f2bb`), centered text |
| **Entity/Object** | Blue background (`#a5d8ff`), medium size |
| **System component** | Light color, descriptive text |
| **Data store** | Gray/white, database-like label |

### Size Guidelines

| Content | Width | Height |
|---------|-------|--------|
| Single word | 120-150px | 60-80px |
| Short phrase (2-4 words) | 180-220px | 80-100px |
| Sentence | 250-300px | 100-120px |

### Example

```json
{
  "type": "rectangle",
  "id": "rect1",
  "x": 100,
  "y": 100,
  "width": 200,
  "height": 80,
  "backgroundColor": "#b2f2bb",
  "boundElements": [{ "id": "rect1-text", "type": "text" }],
  "roundness": { "type": 3 }
}
```

**Matching bound text:**
```json
{
  "type": "text",
  "id": "rect1-text",
  "x": 122,
  "y": 127,
  "width": 156,
  "height": 25,
  "text": "Validate Input",
  "fontSize": 20,
  "fontFamily": 5,
  "textAlign": "center",
  "verticalAlign": "middle",
  "containerId": "rect1",
  "originalText": "Validate Input",
  "autoResize": true,
  "lineHeight": 1.25
}
```

---

## Ellipse

**Best for:** Start/end points, states, emphasis circles

### Properties

```typescript
// Same binding pattern as rectangle — separate bound text element required
{
  type: "ellipse",
  id: "ellipse1",
  boundElements: [{ id: "ellipse1-text", type: "text" }]
}
```

### Use Cases

| Scenario | Configuration |
|----------|---------------|
| **Flow start** | Light green, "Start" text |
| **Flow end** | Light red, "End" text |
| **State** | Soft color, state name |
| **Highlight** | Bright color, emphasis text |

### Size Guidelines

For circular shapes, use `width === height`:

| Content | Diameter |
|---------|----------|
| Icon/Symbol | 60-80px |
| Short text | 100-120px |
| Longer text | 150-180px |

### Example

```json
{
  "type": "ellipse",
  "id": "ellipse1",
  "x": 100,
  "y": 100,
  "width": 120,
  "height": 120,
  "backgroundColor": "#d0f0c0",
  "boundElements": [{ "id": "ellipse1-text", "type": "text" }]
}
```

**Matching bound text:**
```json
{
  "type": "text",
  "id": "ellipse1-text",
  "x": 135,
  "y": 147,
  "width": 50,
  "height": 25,
  "text": "Start",
  "fontSize": 18,
  "fontFamily": 5,
  "textAlign": "center",
  "verticalAlign": "middle",
  "containerId": "ellipse1",
  "originalText": "Start",
  "autoResize": true,
  "lineHeight": 1.25
}
```

---

## Diamond

**Best for:** Decision points, conditional branches

### Properties

```typescript
// Same binding pattern as rectangle — separate bound text element required
{
  type: "diamond",
  id: "diamond1",
  boundElements: [{ id: "diamond1-text", type: "text" }]
}
```

### Use Cases

| Scenario | Text Example |
|----------|--------------|
| **Yes/No decision** | "Is Valid?", "Exists?" |
| **Multiple choice** | "Type?", "Status?" |
| **Conditional** | "Score > 50?" |

### Size Guidelines

Diamonds need more space than rectangles for the same text:

| Content | Width | Height |
|---------|-------|--------|
| Yes/No | 120-140px | 120-140px |
| Short question | 160-180px | 160-180px |
| Longer question | 200-220px | 200-220px |

### Example

```json
{
  "type": "diamond",
  "id": "diamond1",
  "x": 100,
  "y": 100,
  "width": 150,
  "height": 150,
  "backgroundColor": "#ffe4a3",
  "boundElements": [{ "id": "diamond1-text", "type": "text" }]
}
```

**Matching bound text:**
```json
{
  "type": "text",
  "id": "diamond1-text",
  "x": 152,
  "y": 162,
  "width": 46,
  "height": 25,
  "text": "Valid?",
  "fontSize": 18,
  "fontFamily": 5,
  "textAlign": "center",
  "verticalAlign": "middle",
  "containerId": "diamond1",
  "originalText": "Valid?",
  "autoResize": true,
  "lineHeight": 1.25
}
```

---

## Arrow

**Best for:** Flow direction, relationships, dependencies

### Properties

```typescript
{
  type: "arrow",
  points: [[0, 0], [endX, endY]],  // Relative coordinates
  roundness: { type: 2 },          // Curved
  startBinding: null,              // Or { elementId, focus, gap } — must sync with shape
  endBinding: null,                // Or { elementId, focus, gap } — must sync with shape
  startArrowhead: null,            // Optional arrowhead at start
  endArrowhead: "arrow"            // Arrowhead at end
}
```

### Arrow Directions

#### Horizontal (Left to Right) — bound to shapes

```json
[
  {
    "id": "box1",
    "type": "rectangle",
    "x": 100, "y": 120,
    "width": 150, "height": 60,
    "boundElements": [
      {"id": "box1-text", "type": "text"},
      {"id": "arrow1", "type": "arrow"}
    ]
  },
  {
    "id": "box2",
    "type": "rectangle",
    "x": 350, "y": 120,
    "width": 150, "height": 60,
    "boundElements": [
      {"id": "box2-text", "type": "text"},
      {"id": "arrow1", "type": "arrow"}
    ]
  },
  {
    "type": "arrow",
    "id": "arrow1",
    "x": 250, "y": 150,
    "width": 100, "height": 0,
    "points": [[0, 0], [100, 0]],
    "startBinding": {"elementId": "box1", "focus": 0.0, "gap": 5},
    "endBinding": {"elementId": "box2", "focus": 0.0, "gap": 5},
    "endArrowhead": "arrow"
  }
]
```

#### Vertical (Top to Bottom) — bound to shapes

```json
[
  {
    "id": "box-a",
    "type": "rectangle",
    "x": 200, "y": 100, "width": 150, "height": 60,
    "boundElements": [{ "id": "arrow-v", "type": "arrow" }]
  },
  {
    "id": "box-b",
    "type": "rectangle",
    "x": 200, "y": 250, "width": 150, "height": 60,
    "boundElements": [{ "id": "arrow-v", "type": "arrow" }]
  },
  {
    "type": "arrow",
    "id": "arrow-v",
    "x": 275, "y": 160,
    "width": 0, "height": 90,
    "points": [[0, 0], [0, 90]],
    "startBinding": {"elementId": "box-a", "focus": 0.0, "gap": 5},
    "endBinding": {"elementId": "box-b", "focus": 0.0, "gap": 5},
    "endArrowhead": "arrow"
  }
]
```

#### Diagonal

```json
{
  "x": 100,
  "y": 100,
  "width": 200,
  "height": 150,
  "points": [[0, 0], [200, 150]]
}
```

### Arrow to Shape Binding

When an arrow connects two shapes, use `startBinding`/`endBinding` on the arrow **and** add the arrow ID to each shape's `boundElements`. This bidirectional reference makes the arrow follow shapes when dragged.

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
    "id": "box-b",
    "type": "rectangle",
    "x": 470, "y": 150, "width": 180, "height": 80,
    "boundElements": [
      {"id": "box-b-text", "type": "text"},
      {"id": "arrow-1", "type": "arrow"}
    ]
  },
  {
    "type": "arrow",
    "id": "arrow-1",
    "x": 330, "y": 190,
    "width": 140, "height": 0,
    "points": [[0, 0], [140, 0]],
    "startBinding": {"elementId": "box-a", "focus": 0.0, "gap": 5},
    "endBinding": {"elementId": "box-b", "focus": 0.0, "gap": 5},
    "boundElements": [],
    "endArrowhead": "arrow"
  }
]
```

**Binding rules:**
- `focus`: -1 to 1 — position along the edge (0 = center)
- `gap`: pixels from shape edge (typically 1-10)
- Both arrow and shape must reference each other
- Arrow labels use `containerId` on a separate text element (separate from shape bindings)

### Arrow Styles

| Style | `strokeStyle` | `strokeWidth` | Use Case |
|-------|---------------|---------------|----------|
| **Normal flow** | `"solid"` | 2 | Standard connections |
| **Optional/Weak** | `"dashed"` | 2 | Optional paths |
| **Important** | `"solid"` | 3-4 | Emphasized flow |
| **Dotted** | `"dotted"` | 2 | Indirect relationships |

### Adding Arrow Labels (Bound Text)

Arrow labels must use **bound text** — a separate text element linked to the arrow via `containerId`/`boundElements`. This ensures the label moves with the arrow when dragged and supports double-click editing.

```json
[
  {
    "type": "arrow",
    "id": "arrow1",
    "x": 100,
    "y": 150,
    "width": 200,
    "height": 0,
    "points": [[0, 0], [200, 0]],
    "boundElements": [{"id": "arrow-label-1", "type": "text"}]
  },
  {
    "type": "text",
    "id": "arrow-label-1",
    "x": 180,
    "y": 137,
    "width": 40,
    "height": 25,
    "text": "sends",
    "fontSize": 14,
    "fontFamily": 5,
    "textAlign": "center",
    "verticalAlign": "middle",
    "containerId": "arrow1",
    "originalText": "sends",
    "autoResize": true,
    "lineHeight": 1.25
  }
]
```

---

## Line

**Best for:** Non-directional connections, dividers, borders

### Properties

```typescript
{
  type: "line",
  points: [[0, 0], [x2, y2], [x3, y3], ...],
  roundness: null  // Or { type: 2 } for curved
}
```

### Use Cases

| Scenario | Configuration |
|----------|---------------|
| **Divider** | Horizontal, thin stroke |
| **Border** | Closed path (polygon) |
| **Connection** | Multi-point path |
| **Underline** | Short horizontal line |

### Multi-Point Line Example

```json
{
  "type": "line",
  "x": 100,
  "y": 100,
  "points": [
    [0, 0],
    [100, 50],
    [200, 0]
  ]
}
```

---

## Text

**Best for:** Labels, titles, annotations, standalone text

### Properties

```typescript
{
  type: "text",
  text: "Label text",
  fontSize: 20,
  fontFamily: 1,        // 1=Virgil, 2=Helvetica, 3=Cascadia
  textAlign: "left",
  verticalAlign: "top"
}
```

### Font Sizes by Purpose

| Purpose | Font Size |
|---------|-----------|
| **Main title** | 28-36 |
| **Section header** | 24-28 |
| **Element label** | 18-22 |
| **Annotation** | 14-16 |
| **Small note** | 12-14 |

### Width/Height Calculation

```javascript
// Approximate width
const width = text.length * fontSize * 0.6;

// Approximate height (single line)
const height = fontSize * 1.2;

// Multi-line
const lines = text.split('\n').length;
const height = fontSize * 1.2 * lines;
```

### Text Positioning

| Position | textAlign | verticalAlign | Use Case |
|----------|-----------|---------------|----------|
| **Top-left** | `"left"` | `"top"` | Default labels |
| **Centered** | `"center"` | `"middle"` | Titles |
| **Bottom-right** | `"right"` | `"bottom"` | Footnotes |

### Example: Title

```json
{
  "type": "text",
  "x": 100,
  "y": 50,
  "width": 400,
  "height": 40,
  "text": "System Architecture",
  "fontSize": 32,
  "fontFamily": 2,
  "textAlign": "center",
  "verticalAlign": "top"
}
```

### Example: Annotation

```json
{
  "type": "text",
  "x": 150,
  "y": 200,
  "width": 100,
  "height": 20,
  "text": "User input",
  "fontSize": 14,
  "fontFamily": 1,
  "textAlign": "left",
  "verticalAlign": "top"
}
```

---

## Combining Elements

### Pattern: Labeled Box

```json
[
  {
    "type": "rectangle",
    "id": "box1",
    "x": 100,
    "y": 100,
    "width": 200,
    "height": 100,
    "boundElements": [{ "id": "box1-text", "type": "text" }],
    "roundness": { "type": 3 }
  },
  {
    "type": "text",
    "id": "box1-text",
    "x": 131,
    "y": 137,
    "width": 138,
    "height": 25,
    "text": "Component",
    "fontSize": 20,
    "fontFamily": 5,
    "textAlign": "center",
    "verticalAlign": "middle",
    "containerId": "box1",
    "originalText": "Component",
    "autoResize": true,
    "lineHeight": 1.25
  }
]
```

### Pattern: Connected Boxes

```json
[
  {
    "type": "rectangle",
    "id": "box1",
    "x": 100,
    "y": 100,
    "width": 150,
    "height": 80,
    "boundElements": [{ "id": "box1-text", "type": "text" }],
    "roundness": { "type": 3 }
  },
  {
    "type": "text",
    "id": "box1-text",
    "x": 133,
    "y": 127,
    "width": 84,
    "height": 25,
    "text": "Step 1",
    "fontSize": 20,
    "fontFamily": 5,
    "textAlign": "center",
    "verticalAlign": "middle",
    "containerId": "box1",
    "originalText": "Step 1",
    "autoResize": true,
    "lineHeight": 1.25
  },
  {
    "type": "arrow",
    "id": "arrow1",
    "x": 250,
    "y": 140,
    "width": 100,
    "height": 0,
    "points": [[0, 0], [100, 0]],
    "boundElements": [],
    "endArrowhead": "arrow"
  },
  {
    "type": "rectangle",
    "id": "box2",
    "x": 350,
    "y": 100,
    "width": 150,
    "height": 80,
    "boundElements": [{ "id": "box2-text", "type": "text" }],
    "roundness": { "type": 3 }
  },
  {
    "type": "text",
    "id": "box2-text",
    "x": 383,
    "y": 127,
    "width": 84,
    "height": 25,
    "text": "Step 2",
    "fontSize": 20,
    "fontFamily": 5,
    "textAlign": "center",
    "verticalAlign": "middle",
    "containerId": "box2",
    "originalText": "Step 2",
    "autoResize": true,
    "lineHeight": 1.25
  }
]
```

### Pattern: Decision Tree

```json
[
  {
    "type": "diamond",
    "id": "decision",
    "x": 100,
    "y": 100,
    "width": 140,
    "height": 140,
    "boundElements": [
      { "id": "decision-text", "type": "text" },
      { "id": "yes-arrow", "type": "arrow" }
    ]
  },
  {
    "type": "text",
    "id": "decision-text",
    "x": 146,
    "y": 157,
    "width": 48,
    "height": 25,
    "text": "Valid?",
    "fontSize": 18,
    "fontFamily": 5,
    "textAlign": "center",
    "verticalAlign": "middle",
    "containerId": "decision",
    "originalText": "Valid?",
    "autoResize": true,
    "lineHeight": 1.25
  },
  {
    "type": "arrow",
    "id": "yes-arrow",
    "x": 240,
    "y": 170,
    "width": 60,
    "height": 0,
    "points": [[0, 0], [60, 0]],
    "boundElements": [{ "id": "yes-label", "type": "text" }],
    "endArrowhead": "arrow"
  },
  {
    "type": "text",
    "id": "yes-label",
    "x": 258,
    "y": 157,
    "width": 24,
    "height": 25,
    "text": "Yes",
    "fontSize": 14,
    "fontFamily": 5,
    "textAlign": "center",
    "verticalAlign": "middle",
    "containerId": "yes-arrow",
    "originalText": "Yes",
    "autoResize": true,
    "lineHeight": 1.25
  },
  {
    "type": "rectangle",
    "id": "yes-box",
    "x": 300,
    "y": 140,
    "width": 120,
    "height": 60,
    "boundElements": [{ "id": "yes-box-text", "type": "text" }],
    "roundness": { "type": 3 }
  },
  {
    "type": "text",
    "id": "yes-box-text",
    "x": 315,
    "y": 157,
    "width": 90,
    "height": 25,
    "text": "Process",
    "fontSize": 18,
    "fontFamily": 5,
    "textAlign": "center",
    "verticalAlign": "middle",
    "containerId": "yes-box",
    "originalText": "Process",
    "autoResize": true,
    "lineHeight": 1.25
  }
]
```

---

---

## Text Binding

Excalidraw supports binding text elements to container shapes (arrows, rectangles, ellipses, diamonds) so the text moves and edits as part of the container.

### How It Works

Two elements are linked by referencing each other's IDs:

1. **Container element** (arrow, rectangle, ellipse, diamond) — has a `boundElements` array containing `{"id": "<text_id>", "type": "text"}` entries for each bound text
2. **Text element** — has `containerId: "<container_id>"` pointing to its parent container

### Binding a Text Label to an Arrow

```json
[
  {
    "type": "arrow",
    "id": "arrow1",
    "x": 100,
    "y": 200,
    "width": 200,
    "height": 0,
    "points": [[0, 0], [200, 0]],
    "boundElements": [{"id": "label1", "type": "text"}]
  },
  {
    "type": "text",
    "id": "label1",
    "x": 178,
    "y": 187,
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
]
```

### Binding a Text Label to a Shape

All shapes (rectangles, ellipses, diamonds) use bound text elements — the same pattern as arrows. The container's `boundElements` references the text ID, and the text element's `containerId` references the container.

```json
[
  {
    "type": "rectangle",
    "id": "box1",
    "x": 100,
    "y": 100,
    "width": 200,
    "height": 80,
    "boundElements": [{ "id": "box1-text", "type": "text" }],
    "roundness": { "type": 3 }
  },
  {
    "type": "text",
    "id": "box1-text",
    "x": 140,
    "y": 127,
    "width": 120,
    "height": 25,
    "text": "My Box",
    "fontSize": 18,
    "fontFamily": 5,
    "textAlign": "center",
    "verticalAlign": "middle",
    "containerId": "box1",
    "originalText": "My Box",
    "autoResize": true,
    "lineHeight": 1.25
  }
]
```

### Key Rules

- **Always** set `fontFamily: 5` (Excalifont) on bound text elements
- Match `textAlign` and `verticalAlign` between container and text
- Use `"middle"` vertical alignment for centered labels
- Set `autoResize: true` and `lineHeight: 1.25` on the text element
- Position text centered in the container:
  - `text.x` ≈ `shape.x + (shape.width - estimatedTextWidth) / 2`
  - `text.y` ≈ `shape.y + (shape.height - 25) / 2`
  - Estimated text width ≈ `text.length * fontSize * 0.6`
- Never use standalone (unbound) text elements for labels on arrows or shapes

## Summary

| When you need... | Use this element |
|------------------|------------------|
| Process box | `rectangle` + bound `text` |
| Decision point | `diamond` + bound `text` |
| Flow direction | `arrow` |
| Arrow label | `text` bound via `containerId` + `boundElements` |
| Shape label | `rectangle`/`ellipse`/`diamond` + bound `text` |
| Title/Header | `text` (standalone, large font) |
| Non-directional link | `line` |
| Divider | `line` (horizontal) |
