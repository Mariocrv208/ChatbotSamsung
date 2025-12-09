import chromadb

class ChromaService:
    def __init__(self):
        self.client = chromadb.PersistentClient(path="./chroma_db")  # Guarda la BD localmente

    def get_or_create_collection(self, name="SamsungDemo"):
        return self.client.get_or_create_collection(name=name)

    def upsert_data(self, collection_name, doc_id, document):
        """Inserta o actualiza un documento en la colección de ChromaDB."""
        collection = self.get_or_create_collection(collection_name)
        collection.upsert(documents=[document], ids=[doc_id])

    def query(self, query_text, collection_name="SamsungDemo", n_results=3):
        """Busca datos en ChromaDB usando el texto de consulta."""
        collection = self.get_or_create_collection(collection_name)
        
        # Incluir metadatos y distancias
        results = collection.query(
            query_texts=[query_text], 
            n_results=n_results, 
            include=["documents", "metadatas", "distances"]
        )

        # Verificar si hay resultados
        if not results.get("documents") or not results["documents"][0]:
            return {"documents": [], "metadatas": [], "distances": []}

        return {
            "documents": results["documents"][0],
            "metadatas": results.get("metadatas", [])[0] if results.get("metadatas") else [],
            "distances": results.get("distances", [])[0] if results.get("distances") else []
        }


    def get_all_collections(self):
        """Obtiene todas las colecciones existentes en la base de datos."""
        return self.client.list_collections()  # Lista de colecciones disponibles

