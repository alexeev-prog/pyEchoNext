# дай угадаю, кто то украл твой сладкий рулет?
from typing import Any, Callable, Dict, List, Optional, Type


class BaseField:
    """This class describes the Base Field.

    Field is a one input data. Field must be have a:
    1. Datatype - any Type
    2. Default value (only if this field is optional)
    3. max_length - max length of value for field
    4. desc - description text of field
    5. exclude - exclude this field from model json
    6. transformer - a transformer (convert value datatype) callable object
    7. dependencies - fields-dependencies
    8. name - name of field
    """

    def __init__(
        self,
        name: str,
        datatype: Type,
        nullable: bool = False,
        default: Optional[Any] = None,
        max_length: Optional[int] = None,
        desc: Optional[str] = None,
        exclude: bool = False,
        transformer: Optional[Callable[[Any], Any]] = None,
        dependencies: Optional[List[str]] = None,
    ) -> None:
        self.name = name
        self.nullable = nullable
        self.datatype: Type = datatype
        self.default: Any | None = default
        self.max_length: int | None = max_length
        self.desc: str | None = desc
        self.exclude: bool = exclude
        self.transformer: Callable[[Any], Any] | None = transformer
        self.dependencies: List[str] | None = dependencies

    def fast_validate(self, value: Any) -> bool:
        """Fast validation of field value

        Args:
            value (Any): value of field.

        Returns:
            bool: True if all conditions is right, otherwise False
        """
        conditions = [isinstance(value, self.datatype), len(value) <= max_length]

        return all(conditions)

    def validate(self, value: Any, context: Optional[Dict[str, Any]] = None) -> Any:
        """Validate field value

        Args:
            value (Any): value for validating
            context (Dict[str, Any]): context with data for validate dependenc fields. Defaults to None.

        Raises:
            ValueError: is field is None (and not nullable) or field have invalid dependencies

        Returns:
            Any: validated and transformed value
        """
        if value is None and self.default is None and not nullable:
            raise ValueError(f'Field "{self.name}" is required and must not be none')

        if not isinstance(value, self.datatype):
            value = self._type_case(value)

        self._check_type(value)
        self._check_length(value)

        if self.transformer:
            value = self.transformer(value)

        if context:
            for dependency in self.dependencies:
                if dependency in context and not self._validate_dependency(
                    value, context[dependency]
                ):
                    raise ValueError(
                        f"Field '{self.name}' is invalid based on dependency {dependency}."
                    )

        return value
