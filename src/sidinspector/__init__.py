"""SIDInspector toolkit interface contracts."""

from .interface import (
    GENERATOR_OUTPUTS_REQUIRED,
    INTERACTIONS_REQUIRED,
    ITEM_METADATA_REQUIRED,
    SID_ASSIGNMENTS_REQUIRED,
    AuditSidTables,
    TableContract,
    missing_columns,
    validate_columns,
)
__all__ = [
    "AuditSidTables",
    "GENERATOR_OUTPUTS_REQUIRED",
    "INTERACTIONS_REQUIRED",
    "ITEM_METADATA_REQUIRED",
    "SID_ASSIGNMENTS_REQUIRED",
    "TableContract",
    "missing_columns",
    "preflight_inputs",
    "validate_columns",
]


def preflight_inputs(*args, **kwargs):
    """Lazily run the preflight helper without preloading the CLI module."""

    from .preflight import preflight_inputs as _preflight_inputs

    return _preflight_inputs(*args, **kwargs)
