from motor.motor_asyncio import AsyncIOMotorClient
import os

MONGODB_URL = os.getenv("MONGODB_URL", "mongodb://localhost:27017")

# 2. Criamos o cliente usando a variável
client = AsyncIOMotorClient(MONGODB_URL)
db = client.newsflow_db
collection = db.get_collection("artigos")

# Função auxiliar para formatar os documentos do MongoDB (que usam _id) 
def artigo_helper(artigo) -> dict:
    return {
        "id": str(artigo["_id"]),
        "titulo": artigo["titulo"],
        "corpo": artigo["corpo"],
        "autor": artigo["autor"],
        "category": artigo.get("category", artigo.get("categoria", "Sem Categoria")),
        "data_publicacao": artigo["data_publicacao"]
    }