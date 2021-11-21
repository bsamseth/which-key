from typing import Any, Optional

from pydantic import BaseModel, Extra, Field


class WhichKeyConfig(BaseModel):
    action_templates: dict[str, str]
    default_template: str
    template_variables: dict[str, str]
    width: int = 300
    height: int = 100
    x: float = Field(0.5, ge=0, le=1)
    y: float = Field(0.5, ge=0, le=1)


class BindingsConfig(BaseModel):
    label: Optional[str]
    action: Optional[str]
    template: Optional[str]

    def __init__(self, *args: Any, **kwargs: Any) -> None:
        new_kwargs = {
            k: (BindingsConfig(**v) if len(k) == 1 and isinstance(v, dict) else v)
            for k, v in kwargs.items()
        }
        super().__init__(*args, **new_kwargs)

    class Config:
        extra = Extra.allow


class Config(BaseModel):
    which_key: WhichKeyConfig
    leader: BindingsConfig
