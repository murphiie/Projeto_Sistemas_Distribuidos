from motor.motor_asyncio import AsyncIOMotorClient
import os

# Esta URL será configurada depois no Docker.
MONGODB_URL = "mongodb://mongos:27017"

client = AsyncIOMotorClient(MONGODB_URL)
db = client.newsflow_db
collection = db.get_collection("artigos")

# Função auxiliar corrigida para evitar erro de campos ausentes
def artigo_helper(artigo) -> dict:
    return {
        "id": str(artigo["_id"]),
        "titulo": artigo.get("titulo", "Sem título"),
        "corpo": artigo.get("corpo", ""),
        "autor": artigo.get("autor", "Anônimo"),
        "category": artigo.get("categoria", "geral"),
        "data_publicacao": artigo.get("data_publicacao", "Data não informada")
    }
