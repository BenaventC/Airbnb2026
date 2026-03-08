# Skill: English Notebook Narrative Style (AirBnB_NLP4socialscience)

## Goal
Translate and upgrade notebook text cells into polished, academic-quality English while preserving technical intent.

## When to use
- User asks to translate notebook text to English
- User asks for cleaner, more elegant section titles
- User asks for fuller markdown explanations in pipeline notebooks

## Scope
This skill applies to Markdown cells:
- Notebook title cells
- Section headings
- Explanatory paragraphs
- Mermaid section intros and captions

Code logic must not be changed unless explicitly requested.

## Required Writing Rules
1. Use clear, fluent, professional English.
2. Use elegant section titles (informative, concise, non-generic).
3. Expand short notes into complete, well-structured prose (2-4 sentences when relevant).
4. Preserve the original scientific/technical meaning.
5. Keep domain-specific terms accurate (runtime, CO2, enrichment, left join, etc.).
6. Keep numbering stable unless the user asks for renumbering.

## Style Guide
- Prefer active voice.
- Prefer action-oriented headings.
- Keep tone formal but readable.
- Avoid unnecessary buzzwords.
- Use consistent terminology across all sections.

## Translation Checklist
- Main notebook title translated and refined.
- All markdown section titles translated.
- All markdown explanatory paragraphs translated.
- Mermaid intro/caption text translated.
- No leftover French in markdown cells.

## Optional Extension (Only if user asks)
Translate text embedded in code cells:
- docstrings
- code comments
- print labels
