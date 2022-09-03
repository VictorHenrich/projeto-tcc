from typing import Any, Mapping


class Representation:
    def __handle_string(self) -> str:
        property_publics: Mapping[str, Any] = {
            prop: value
            for prop, value in self.__dict__.items()
            if not prop.startswith('_')
        }

        repr_string: str = f"<{self.__class__.__name__}"

        for prop, value in property_publics.items():
            repr_string += f" {prop}={value} "

        repr_string += ">"

        return repr_string

    def __repr__(self) -> str:
        return self.__handle_string()

    def __str__(self) -> str:
        return self.__handle_string()

        
        