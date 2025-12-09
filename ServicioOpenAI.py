from quart import Quart, request, jsonify
import os
import chromadb
import re
import globals
import numpy as np
import asyncio
from ChromaService import ChromaService
from logica import crear_mensajes

from chromadb import PersistentClient

app = Quart(__name__)

# Inicializar servicios de Chroma
chroma_service = ChromaService()
chroma_client = PersistentClient(path="local_db")

@app.route('/openAIservice', methods=['POST'])
async def openai_service():
    try:
        # Obtener JSON del request (async obligatorio)
        data = await request.get_json()
        mensaje = data.get("mensaje", "")
        globals.pregunta = mensaje

        if not mensaje:
            return jsonify({"error": "Falta el campo 'mensaje'"}), 400

        # Buscar en Chroma
        collection = chroma_service.get_or_create_collection(name="SamsungDemo")
        print(collection)

        resultado_chroma = collection.query(
            query_texts=[mensaje],
            n_results=3,
            include=["documents", "metadatas", "distances"]
        )

        # Generar respuesta LLM
        globals.documentos = resultado_chroma['documents'][0] if resultado_chroma['documents'] else []
        print(globals.documentos)
        await crear_mensajes()

        return jsonify({"respuesta": globals.resultado_final}), 200

    except Exception as e:
        return jsonify({
            "error": str(e),
            "mensaje": "Problemas al generar la respuesta del chatbot"
        }), 500


@app.route("/conteo", methods=["GET"])
async def conteo():
    try:
        collection = chroma_service.get_or_create_collection(name="SamsungDemo")
        cantidad = collection.count()

        return jsonify({"coleccion": "SamsungDemo", "conteo": cantidad}), 200

    except Exception as e:
        return jsonify({"error": str(e), "mensaje": "No se pudo obtener el conteo."}), 500


@app.route("/vista_previa", methods=["GET"])
async def vista_previa():
    try:
        collection = chroma_service.get_or_create_collection(name="SamsungDemo")
        peeked = collection.peek()

        if "embeddings" in peeked:
            peeked["embeddings"] = [e.tolist() for e in peeked["embeddings"]]

        return jsonify({
            "coleccion": "SamsungDemo",
            "items": {
                "ids": peeked.get("ids", []),
                "documents": peeked.get("documents", []),
                "metadatas": peeked.get("metadatas", []),
                "embeddings": peeked.get("embeddings", [])
            }
        })

    except Exception as e:
        return jsonify({"error": str(e), "mensaje": "No se pudo obtener vista previa."}), 500


@app.route("/documents", methods=["GET"])
async def obtener_documents():
    try:
        collection = chroma_service.get_or_create_collection(name="SamsungDemo")
        peeked = collection.peek()

        return jsonify({
            "coleccion": "SamsungDemo",
            "documents": peeked.get("documents", [])
        })

    except Exception as e:
        return jsonify({"error": str(e), "mensaje": "No se pudieron obtener los documentos."}), 500


def split_text(text, delimiter="## "):
    sections = re.split(rf'\n{delimiter}', text)
    return [s.strip() for s in sections if s.strip()]


@app.route('/cargar_archivo', methods=['POST'])
async def cargar_archivo_contexto():
    try:
        data = await request.get_json()
        id_empresa = data.get("id_empresa")

        if not id_empresa:
            return jsonify({"error": "Falta el parámetro 'id_empresa'"}), 400

        archivo_path = './Contextos/SamsungDemo.md'
        if not os.path.exists(archivo_path):
            return jsonify({"error": "El archivo no existe"}), 404

        with open(archivo_path, 'r', encoding='utf-8') as file:
            markdown_content = file.read()

        chunks = split_text(markdown_content)

        documentos_insertados = 0
        for i, chunk in enumerate(chunks):
            doc_id = f"{id_empresa}_{i+1}"

            chroma_service.upsert_data(
                collection_name=id_empresa,
                doc_id=doc_id,
                document=chunk
            )

            documentos_insertados += 1

        return jsonify({
            "mensaje": f"{documentos_insertados} secciones cargadas correctamente",
            "documentos_insertados": documentos_insertados
        })

    except Exception as e:
        return jsonify({"error": str(e), "mensaje": "No se pudo procesar el archivo."}), 500


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5001))
    app.run(host="0.0.0.0", port=port)
