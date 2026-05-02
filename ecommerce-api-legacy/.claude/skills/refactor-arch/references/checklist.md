# Validation Checklist

## Phase 1 — Analysis {#phase-1-analysis}

- Language correctly detected
- Framework correctly detected
- Application domain accurately described
- Number of analyzed files matches reality

## Phase 2 — Audit {#phase-2-audit}

- Report follows the template defined in the reference files
- Each finding includes exact file and line numbers
- Findings are ordered by severity (CRITICAL → LOW)
- At least 5 findings identified
- Deprecated API detection included (if applicable)
- The process pauses and requests confirmation before Phase 3

## Phase 3 — Refactoring {#phase-3-refactoring}

- Directory structure follows the MVC pattern
- Configuration extracted into a config module (no hardcoding)
- Models created to abstract data
- Views/Routes separated for routing
- Controllers centralize application flow
- Centralized error handling
- Clear entry point
- Application starts without errors
- Original endpoints respond correctly

