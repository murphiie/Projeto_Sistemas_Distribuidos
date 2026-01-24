from fastapi import FastAPI, Body, HTTPException, status
from fastapi.encoders import jsonable_encoder
from typing import List
from bson import ObjectId

from database import collection, artigo_helper
from models import Artigo

# organizar por seções no Swagger
tags_metadata = [
    {
        "name": "Acervo Público",
        "description": "Exploração e leitura de notícias. Acesso livre ao conhecimento.",
    },
    {
        "name": "Gestão de Conteúdo",
        "description": "Operações de curadoria: inclusão e remoção de registros no banco distribuído.",
    },
    {
        "name": "Monitoramento",
        "description": "Verificação de saúde e conectividade do sistema.",
    }
]

app = FastAPI(
    title="📚 NewsFlow: Biblioteca Digital de Notícias",
    description="""
    ## Sistema de Gerenciamento de Conteúdo Distribuído (CMS)
    
    Este projeto implementa uma arquitetura de alta disponibilidade utilizando:
    * **Distribuição de Dados:** MongoDB Sharded Cluster (ConfigSvr, Shards e Mongos).
    * **Escalabilidade:** Sharding baseado em categorias para otimização de buscas.
    * **Performance:** Comunicação assíncrona com Python (Motor/FastAPI).
    
    **Curadoria do Projeto:** Geovana & Rafaela
    """,
    version="2.1.0",
    openapi_tags=tags_metadata,
    swagger_ui_parameters={
        "defaultModelsExpandDepth": -1,  
        "filter": True,                 
        "docExpansion": "list",        
    }
)

# 1. ROTA DE MONITORAMENTO
@app.get("/", tags=["Monitoramento"], summary="Status da Biblioteca")
async def root():
    """Retorna o estado operacional atual do sistema NewsFlow."""
    return {"status": "Online", "sistema": "NewsFlow CMS", "ambiente": "AWS Cloud"}

# 2. LISTAR TODOS OS ARTIGOS (GET)
@app.get("/artigos/", response_model=List[dict], tags=["Acervo Público"], summary="Consultar acervo completo")
async def listar_artigos():
    """Recupera todos os registros disponíveis na biblioteca digital com baixa latência."""
    artigos = []
    async for documento in collection.find():
        artigos.append(artigo_helper(documento))
    return artigos

# 3. BUSCAR POR CATEGORIA (GET)
@app.get("/artigos/categoria/{category}", response_model=List[dict], tags=["Acervo Público"], summary="Filtrar por estante (Categoria)")
async def buscar_por_categoria(category: str):
    """
    Realiza uma busca otimizada utilizando a **Shard Key**. 
    Esta operação é direcionada diretamente ao Shard responsável pela categoria informada.
    """
    artigos = []
    async for documento in collection.find({"category": category}):
        artigos.append(artigo_helper(documento))
    return artigos

# 4. CRIAR ARTIGO (POST)
@app.post("/artigos/", status_code=status.HTTP_201_CREATED, response_model=dict, tags=["Gestão de Conteúdo"], summary="Catalogar nova notícia")
async def criar_artigo(artigo: Artigo = Body(...)):
    """Insere um novo exemplar no banco de dados. O sistema distribui o dado automaticamente entre as instâncias de armazenamento."""
    artigo_dict = jsonable_encoder(artigo)
    novo_artigo = await collection.insert_one(artigo_dict)
    
    criado = await collection.find_one({
        "_id": novo_artigo.inserted_id,
        "category": artigo_dict["category"] 
    })
    
    if criado:
        return artigo_helper(criado)
    
    raise HTTPException(status_code=400, detail="Erro ao catalogar notícia")

# 5. DELETAR ARTIGO (DELETE)
@app.delete("/artigos/{id}", tags=["Gestão de Conteúdo"], summary="Remover registro do acervo")
async def deletar_artigo(id: str):
    """Exclui permanentemente um artigo através de seu identificador único (ID)."""
    if not ObjectId.is_valid(id):
        raise HTTPException(status_code=400, detail="Identificador inválido")
        
    delete_result = await collection.delete_one({"_id": ObjectId(id)})
    
    if delete_result.deleted_count == 1:
        return {"mensagem": "Registro removido com sucesso"}
        
    raise HTTPException(status_code=404, detail="Registro não encontrado no acervo")