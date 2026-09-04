"""
JobGuard Core Data Pipeline - Schema Enforcement & Type Guard Engine
Defines strongly-typed schema constraints, nullability checks, regex masks,
range boundaries, and custom structural validators for ingested job/offer data.
"""

import re
from typing import Dict, List, Optional, Any, Callable, Type, Union
from dataclasses import dataclass, field


class ValidationError(Exception):
    """Raised when record data violates schema constraints."""
    def __init__(self, field_name: str, message: str, value: Any = None):
        super().__init__(f"Validation failed for field '{field_name}': {message} (received: {value!r})")
        self.field_name = field_name
        self.message = message
        self.value = value


@dataclass
class FieldDefinition:
    name: str
    expected_type: Union[Type, Tuple[Type, ...]]
    required: bool = True
    nullable: bool = False
    min_length: Optional[int] = None
    max_length: Optional[int] = None
    min_value: Optional[Union[int, float]] = None
    max_value: Optional[Union[int, float]] = None
    regex_pattern: Optional[str] = None
    allowed_values: Optional[List[Any]] = None
    custom_validator: Optional[Callable[[Any], bool]] = None
    default_value: Any = None


class SchemaValidator:
    """Strict schema validator for JSON-like dictionary payloads."""

    def __init__(self, schema_name: str, allow_extra_fields: bool = True):
        self.schema_name = schema_name
        self.allow_extra_fields = allow_extra_fields
        self._fields: Dict[str, FieldDefinition] = {}
        self._compiled_regex: Dict[str, re.Pattern] = {}

    def add_field(self, field_def: FieldDefinition) -> "SchemaValidator":
        self._fields[field_def.name] = field_def
        if field_def.regex_pattern:
            self._compiled_regex[field_def.name] = re.compile(field_def.regex_pattern)
        return self

    def validate(self, record: Dict[str, Any]) -> Dict[str, Any]:
        """Validate input dictionary against schema rules; returns sanitized copy with defaults."""
        if not isinstance(record, dict):
            raise ValidationError("__root__", "Record must be a dictionary", record)

        sanitized: Dict[str, Any] = {}
        errors: List[str] = []

        # Check all defined fields
        for field_name, f_def in self._fields.items():
            if field_name not in record:
                if f_def.required and f_def.default_value is None:
                    errors.append(f"Required field '{field_name}' is missing")
                    continue
                sanitized[field_name] = f_def.default_value
                continue

            val = record[field_name]

            # Nullability check
            if val is None:
                if not f_def.nullable:
                    errors.append(f"Field '{field_name}' cannot be null")
                else:
                    sanitized[field_name] = None
                continue

            # Type check
            if not isinstance(val, f_def.expected_type):
                expected_names = (
                    f_def.expected_type.__name__
                    if isinstance(f_def.expected_type, type)
                    else ", ".join(t.__name__ for t in f_def.expected_type)
                )
                errors.append(f"Field '{field_name}' expected type {expected_names}, got {type(val).__name__}")
                continue

            # Length bounds for strings/sequences
            if isinstance(val, (str, list, dict, bytes)):
                if f_def.min_length is not None and len(val) < f_def.min_length:
                    errors.append(f"Field '{field_name}' length {len(val)} is below minimum {f_def.min_length}")
                if f_def.max_length is not None and len(val) > f_def.max_length:
                    errors.append(f"Field '{field_name}' length {len(val)} exceeds maximum {f_def.max_length}")

            # Numeric value bounds
            if isinstance(val, (int, float)):
                if f_def.min_value is not None and val < f_def.min_value:
                    errors.append(f"Field '{field_name}' value {val} is below minimum {f_def.min_value}")
                if f_def.max_value is not None and val > f_def.max_value:
                    errors.append(f"Field '{field_name}' value {val} exceeds maximum {f_def.max_value}")

            # Regex pattern matching for strings
            if isinstance(val, str) and field_name in self._compiled_regex:
                if not self._compiled_regex[field_name].search(val):
                    errors.append(f"Field '{field_name}' does not match pattern {f_def.regex_pattern}")

            # Enum allowed values
            if f_def.allowed_values is not None and val not in f_def.allowed_values:
                errors.append(f"Field '{field_name}' value {val!r} not in allowed options: {f_def.allowed_values}")

            # Custom validator function
            if f_def.custom_validator is not None:
                try:
                    if not f_def.custom_validator(val):
                        errors.append(f"Field '{field_name}' failed custom validation function")
                except Exception as ex:
                    errors.append(f"Field '{field_name}' custom validator error: {str(ex)}")

            sanitized[field_name] = val

        # Handle extra fields
        if not self.allow_extra_fields:
            for k in record:
                if k not in self._fields:
                    errors.append(f"Extraneous field '{k}' not permitted by strict schema")
        else:
            for k, v in record.items():
                if k not in sanitized:
                    sanitized[k] = v

        if errors:
            raise ValidationError(self.schema_name, "; ".join(errors))

        return sanitized


def create_job_posting_schema() -> SchemaValidator:
    """Pre-configured validator for job posting ingestion."""
    schema = SchemaValidator("JobPostingRecord")
    schema.add_field(FieldDefinition("title", expected_type=str, min_length=2, max_length=200))
    schema.add_field(FieldDefinition("company", expected_type=str, min_length=1, max_length=150))
    schema.add_field(FieldDefinition("description", expected_type=str, min_length=10, max_length=50000))
    schema.add_field(FieldDefinition("salary", expected_type=str, required=False, nullable=True, default_value=""))
    schema.add_field(FieldDefinition("email", expected_type=str, required=False, nullable=True, default_value=""))
    schema.add_field(FieldDefinition("website", expected_type=str, required=False, nullable=True, default_value=""))
    return schema
