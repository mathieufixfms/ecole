# -*- coding: utf-8 -*-

"""
Classe Address
"""

from dataclasses import dataclass, field
from typing import Optional



@dataclass
class Address:
    """Adresse d'une personne (enseignant ou élève)."""
    id: Optional[int] = field(default=None, init=False)
    street: str
    city: str
    postal_code: int
	
		

    def __str__(self) -> str:
        return f"adresse -> rue : {self.street}, code postal :  {self.postal_code}, ville : {self.city}"
