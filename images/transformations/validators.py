from typing import Any, Union, Tuple, Type, Optional

Numeric = Union[int, float]


class ConfigValidator:
    def __init__(self, key: str):
        self.key = key

    def error(self, value_name: str, message: str) -> str:
        """Return a formatted error message."""
        return f"{self.key} '{value_name}' {message}"

    def ensure_type(self, value: Any, types: tuple[type, ...], value_name: str):
        """Raise if `value` is not an instance of any `types`."""
        if not isinstance(value, types):
            allowed = ", ".join(t.__name__ for t in types)
            raise TypeError(self.error(value_name=value_name, message=f"must be of type(s): {allowed}; got {type(value).__name__}"))

    def validate_dictionary(self, config_dict: dict) -> dict:
        """Ensure the configuration is a dict and return it."""
        self.ensure_type(value=config_dict, types=(dict,), value_name="config_dict")
        return config_dict

    def validate_required_keys(self, config_dict: dict, required: list[str]) -> None:
        """Ensure each name in `required` is a key in the config dict."""
        for field in required:
            if field not in config_dict:
                raise ValueError(self.error(value_name="object", message=f"missing required configuration key '{field}'"))

    def validate_number(
        self,
        value: Any,
        value_name: str = "Value",
        allowed_types: Tuple[Type, ...] = (int, float),
        min_value: Numeric = None,
        max_value: Numeric = None,
    ) -> Numeric:
        """Ensure `value` is numeric within optional bounds."""
        self.ensure_type(value=value, types=allowed_types, value_name=value_name)
        if min_value is not None and value < min_value:
            raise ValueError(self.error(value_name=value_name, message=f"must be >= {min_value}; got {value}"))
        if max_value is not None and value > max_value:
            raise ValueError(self.error(value_name=value_name, message=f"must be <= {max_value}; got {value}"))
        return value

    def validate_number_tuple(
            self,
            value: Any,
            length: int,
            value_name: str = "Value",
            min_value: Numeric = None,
            max_value: Numeric = None,
            allowed_types: Tuple[Type, ...] = (int, float)
    ) -> tuple[Numeric, Numeric]:
        """Ensure a list/tuple of `length` positive ints and return it as a tuple."""
        self.ensure_type(value=value, types=(tuple, list), value_name=value_name)
        if len(value) != length:
            raise TypeError(self.error(
                value_name=value_name,
                message=f"must be a tuple of {length} ints; got {value!r}"
            ))
        for element in value:
            self.validate_number(
                value=element,
                allowed_types=allowed_types,
                value_name=value_name,
                min_value=min_value,
                max_value=max_value
            )
        if any(element < 0 for element in value):
            raise ValueError(self.error(
                value_name=value_name,
                message=f"values must be positive; got {value!r}"
            ))
        return value

    def validate_choice(self, value: Any, options: list[str], value_name: str = "Value") -> str:
        """Validate `value` is a string in `options` and return it uppercase."""
        self.ensure_type(value=value, types=(str,), value_name=value_name)
        normalized = value.upper()
        if normalized not in options:
            raise ValueError(self.error(value_name=value_name, message=f"must be one of {options}; got {value!r}"))
        return normalized

    def validate_optional_bool(self, value: Any, value_name: str = "Value") -> bool:
        """
        Accepts a bool or None (returning False). Raises if provided value is non‐bool.
        """
        if value is None:
            return False
        self.ensure_type(value=value, types=(bool,), value_name=value_name)
        return value

    def validate_str(
        self,
        value: Any,
        *,
        value_name: str = "Value",
        optional: bool = False,
        multiple: bool = False,
        allowed: Optional[list[str]] = None,
    ) -> Union[None, str, list[str]]:
        """
        Validate a str (or list of str) according to the flags:

        - optional: if True, allow `value` to be None
        - multiple: if True, allow list[str]; otherwise only a single str
        - allowed: if provided, each str must be in this list

        Returns:
          - None                if `optional` and `value is None`
          - str                 if not `multiple`
          - list[str]           if `multiple`
        Raises:
          - TypeError or ValueError with a standardized message
        """
        if value is None:
            if optional:
                return None
            else:
                raise TypeError(self.error(
                    value_name=value_name,
                    message="must not be null"
                ))

        if multiple:
            if isinstance(value, str):
                items = [value]
            elif isinstance(value, list):
                if not all(isinstance(v, str) for v in value):
                    raise TypeError(self.error(
                        value_name=value_name,
                        message="must be a list of strings"
                    ))
                items = value
            else:
                raise TypeError(self.error(
                    value_name=value_name,
                    message="must be a string or a list of strings"
                ))
        else:
            if not isinstance(value, str):
                raise TypeError(self.error(
                    value_name=value_name,
                    message="must be a string"
                ))
            items = [value]

        if allowed is not None:
            for item in items:
                if item not in allowed:
                    raise ValueError(self.error(
                        value_name=value_name,
                        message=f"must be one of {allowed}; got '{item}'"
                    ))

        return items if multiple else items[0]

    def validate_color(
        self,
        value: Any,
        value_name: str = "Value"
    ) -> Union[int, str, Tuple[int, ...]]:
        """Validate color as int, str, or 3-/4-length tuple."""
        self.ensure_type(value=value, types=(int, str, tuple, list), value_name=value_name)

        if isinstance(value, (tuple, list)):
            color_tuple = tuple(value)
            if len(color_tuple) not in (3, 4):
                raise ValueError(self.error(value_name=value_name, message=f"must be 3- or 4-length tuple; got {color_tuple!r}"))
            for channel in color_tuple:
                self.ensure_type(value=channel, types=(int, str), value_name=value_name)
            return color_tuple

        return value
