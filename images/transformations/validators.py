from typing import Any, Union, Tuple, Type, Optional

Numeric = Union[int, float]


class ConfigValidator:
    def __init__(self, key: str):
        self.key = key

    def _error(self, value_name: str, message: str) -> str:
        """Return a formatted error message."""
        return f"{self.key} '{value_name}' {message}"

    def _ensure_type(self, value: Any, types: tuple[type, ...], value_name: str):
        """Raise if `value` is not an instance of any `types`."""
        if not isinstance(value, types):
            allowed = ", ".join(t.__name__ for t in types)
            raise TypeError(self._error(value_name=value_name, message=f"must be of type(s): {allowed}; got {type(value).__name__}"))

    def validate_dictionary(self, config_dict: dict) -> dict:
        """Ensure the configuration is a dict and return it."""
        self._ensure_type(value=config_dict, types=(dict,), value_name="config_dict")
        return config_dict

    def validate_required_keys(self, config_dict: dict, required: list[str]) -> None:
        """Ensure each name in `required` is a key in the config dict."""
        for field in required:
            if field not in config_dict:
                raise ValueError(self._error(value_name="object", message=f"missing required configuration key '{field}'"))

    def validate_number(
        self,
        value: Any,
        value_name: str = "Value",
        allowed_types: Tuple[Type, ...] = (int, float),
        min_value: Numeric = None,
        max_value: Numeric = None,
    ) -> Numeric:
        """Ensure `value` is numeric within optional bounds."""
        self._ensure_type(value=value, types=allowed_types, value_name=value_name)
        if min_value is not None and value < min_value:
            raise ValueError(self._error(value_name=value_name, message=f"must be >= {min_value}; got {value}"))
        if max_value is not None and value > max_value:
            raise ValueError(self._error(value_name=value_name, message=f"must be <= {max_value}; got {value}"))
        return value

    def validate_number_tuple(
            self,
            value: Any,
            length: int,
            value_name: str = "Value",
            allowed_types: Tuple[Type, ...] = (int, float)
    ) -> tuple[Numeric, Numeric]:
        """Ensure a list/tuple of `length` positive ints and return it as a tuple."""
        self._ensure_type(value=value, types=(tuple, list), value_name=value_name)
        if len(value) != length:
            raise TypeError(self._error(
                value_name=value_name,
                message=f"must be a tuple of {length} ints; got {value!r}"
            ))
        for element in value:
            self._ensure_type(value=element, types=allowed_types, value_name=value_name)
        if any(element <= 0 for element in value):
            raise ValueError(self._error(
                value_name=value_name,
                message=f"values must be positive; got {value!r}"
            ))
        return value

    def validate_choice(self, value: Any, options: list[str], value_name: str = "Value") -> str:
        """Validate `value` is a string in `options` and return it uppercase."""
        self._ensure_type(value=value, types=(str,), value_name=value_name)
        normalized = value.upper()
        if normalized not in options:
            raise ValueError(self._error(value_name=value_name, message=f"must be one of {options}; got {value!r}"))
        return normalized

    def validate_optional_bool(self, value: Any, value_name: str = "Value") -> bool:
        """
        Accepts a bool or None (returning False). Raises if provided value is non‐bool.
        """
        if value is None:
            return False
        self._ensure_type(value=value, types=(bool,), value_name=value_name)
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
                raise TypeError(self._error(
                    value_name=value_name,
                    message="must not be null"
                ))

        if multiple:
            if isinstance(value, str):
                items = [value]
            elif isinstance(value, list):
                if not all(isinstance(v, str) for v in value):
                    raise TypeError(self._error(
                        value_name=value_name,
                        message="must be a list of strings"
                    ))
                items = value
            else:
                raise TypeError(self._error(
                    value_name=value_name,
                    message="must be a string or a list of strings"
                ))
        else:
            if not isinstance(value, str):
                raise TypeError(self._error(
                    value_name=value_name,
                    message="must be a string"
                ))
            items = [value]

        if allowed is not None:
            for item in items:
                if item not in allowed:
                    raise ValueError(self._error(
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
        self._ensure_type(value=value, types=(int, str, tuple, list), value_name=value_name)

        if isinstance(value, (tuple, list)):
            color_tuple = tuple(value)
            if len(color_tuple) not in (3, 4):
                raise ValueError(self._error(value_name=value_name, message=f"must be 3- or 4-length tuple; got {color_tuple!r}"))
            for channel in color_tuple:
                self._ensure_type(value=channel, types=(int, str), value_name=value_name)
            return color_tuple

        return value

    def validate_border(self, value: Any, value_name: str = "Value") -> tuple[int, int, int, int]:
        """Normalize border as a non-negative 4-tuple of ints."""
        if isinstance(value, int):
            if value < 0:
                raise ValueError(self._error(value_name=value_name, message=f"must be non-negative; got {value}"))
            return (value,) * 4

        if isinstance(value, (tuple, list)):
            if len(value) != 4 or not all(isinstance(v, int) for v in value):
                raise TypeError(self._error(value_name=value_name, message=f"must be a 4-tuple of ints; got {value!r}"))
            if any(v < 0 for v in value):
                raise ValueError(self._error(value_name=value_name, message=f"values must be non-negative; got {value!r}"))
            return tuple[int, int, int, int](value)

        raise TypeError(self._error(value_name=value_name, message=f"must be an int or 4-tuple of ints; got {type(value).__name__}"))

    def validate_centering(
        self,
        value: Any,
        value_name: str = "Value",
    ) -> tuple[float, float]:
        """
        Validate that `value` is a 2-tuple (or list) of numbers between 0.0 and 1.0.
        Returns it normalized as a (float, float) tuple.
        """
        self._ensure_type(value=value, types=(tuple, list), value_name=value_name)
        if len(value) != 2:
            raise TypeError(self._error(
                value_name=value_name,
                message=f"must be a tuple of two numbers; got {value!r}"
            ))

        center_x, center_y = value
        self._ensure_type(value=center_x, types=(int, float), value_name=value_name)
        self._ensure_type(value=center_y, types=(int, float), value_name=value_name)

        if not (0.0 <= center_x <= 1.0 and 0.0 <= center_y <= 1.0):
            raise ValueError(self._error(
                value_name=value_name,
                message=f"values must be between 0.0 and 1.0; got {value!r}"
            ))

        return float(center_x), float(center_y)

    def validate_crop_box(
        self,
        left: int, upper: int, right: int, lower: int,
        img_width: int,
        img_height: int
    ) -> tuple[int, int, int, int]:
        """
        Ensure 0 ≤ left < right ≤ img_width and 0 ≤ upper < lower ≤ img_height.
        All parameters must be ints.
        """
        for name, coord in (("left", left), ("upper", upper),
                            ("right", right), ("lower", lower)):
            self._ensure_type(value=coord, types=(int,), value_name=name)
        if not (0 <= left < right <= img_width):
            raise ValueError(
                f"{self.key} invalid horizontal crop coords: "
                f"0 ≤ left({left}) < right({right}) ≤ width({img_width})"
            )
        if not (0 <= upper < lower <= img_height):
            raise ValueError(
                f"{self.key} invalid vertical crop coords: "
                f"0 ≤ upper({upper}) < lower({lower}) ≤ height({img_height})"
            )
        return left, upper, right, lower
