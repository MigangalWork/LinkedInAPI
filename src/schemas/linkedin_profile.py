from pydantic import BaseModel, field_validator
from datetime import datetime

class ProfileSchema(BaseModel):
    url: str
    last_description: str
    is_active: bool | None = None

    @field_validator('url')
    def validate_field_name(cls, value):
        if not value.startswith('https://www.linkedin.com'):
            raise ValueError('Field name must start with "https://www.linkedin.com"')
        return value
    
class ProfileSchemaModel(ProfileSchema):
    id: int
    created_at: datetime
    updated_at: datetime
