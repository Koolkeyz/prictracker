from typing import List, Optional, Dict, Any, Union
from pydantic import BaseModel, EmailStr


class EmailSchema(BaseModel):
    email: List[EmailStr]
    body: Optional[Dict[str, Any]] = None
    
