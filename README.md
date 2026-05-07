# Excalidraw Diagram Generator

A coding agent skill that generates **properly bound** Excalidraw diagrams from natural language descriptions. Every shape has text that edits in-place, and every arrow follows its connected shapes when dragged.

## Supported Diagram Types

- **Flowcharts** — Sequential processes, workflows, decision trees
- **Relationship Diagrams** — Entity relationships, system components, dependencies
- **Mind Maps** — Concept hierarchies, brainstorming results, topic organization
- **Architecture Diagrams** — System design, module interactions, data flow
- **Data Flow Diagrams (DFD)** — Data flow visualization, data transformation processes
- **Business Flow (Swimlane)** — Cross-functional workflows, actor-based process flows
- **Class Diagrams** — Object-oriented design, class structures and relationships
- **Sequence Diagrams** — Object interactions over time, message flows
- **ER Diagrams** — Database entity relationships, data models

## Key Features

- **Bound text on all shapes & arrows** — Text uses `containerId` + `boundElements` so double-click editing works and text moves with its container
- **Arrow-to-shape bindings** — Every arrow uses `startBinding`/`endBinding` with bidirectional `boundElements` sync so arrows follow shapes when dragged
- **Python script toolkit** — `add-arrow.py` adds arrows with auto-computed bindings; `add-icon-to-diagram.py` integrates icon libraries; `split-excalidraw-library.py` processes `.excalidrawlib` files
- **8 ready-to-use templates** in `templates/` covering all diagram types

## Installation

```bash
npx skills add p-rp/excalidraw-diagram-generator
```

Or install globally:

```bash
npx skills add p-rp/excalidraw-diagram-generator -g -y
```

## Usage

Ask your coding agent:

> "Create an Excalidraw diagram showing the user registration flow"

The skill generates a `.excalidraw` file you can open at [excalidraw.com](https://excalidraw.com).

## File Structure

```
excalidraw-diagram-generator/
  SKILL.md                         # Complete skill workflow and guidance
  README.md
  references/
    excalidraw-schema.md           # Full Excalidraw JSON schema reference
    element-types.md               # Element type specs with binding patterns
  scripts/
    add-arrow.py                   # Create arrows with --from-id/--to-id bindings
    add-icon-to-diagram.py         # Integrate icon libraries
    split-excalidraw-library.py    # Process .excalidrawlib files
    README.md                      # Script documentation
    .gitignore
  templates/
    flowchart-template.excalidraw
    relationship-template.excalidraw
    mindmap-template.excalidraw
    data-flow-diagram-template.excalidraw
    business-flow-swimlane-template.excalidraw
    class-diagram-template.excalidraw
    sequence-diagram-template.excalidraw
    er-diagram-template.excalidraw
```

[![skills.sh](https://skills.sh/b/p-rp/excalidraw-diagram-generator)](https://skills.sh/p-rp/excalidraw-diagram-generator)
