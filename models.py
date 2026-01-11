from pydantic import BaseModel, Field
from datetime import datetime


class Artigo(BaseModel):
    titulo: str
    corpo: str
    autor: str
    category: str  
    data_publicacao: str

    class Config:
        json_schema_extra = {
            "example": {
                "titulo": "Sistemas Distribuídos na Prática",
                "corpo": "Conteúdo detalhado sobre escalabilidade...",
                "autor": "Geovana Rodrigues",
                "category": "Tecnologia", 
                "data_publicacao": "2026-01-11" 
            }
        }