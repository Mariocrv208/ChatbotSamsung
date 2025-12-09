from StructsChatgpt import Encabezado
from collections import namedtuple
from openai import OpenAI
import os
from dotenv import load_dotenv
import asyncio

# Cargar variables de entorno
load_dotenv()
api_key = os.getenv("OPENAI_KEY")

# Crear cliente OpenAI
client = OpenAI(api_key=api_key)


def ConsumirChatgpt(mensajesNuevos):
    # ISNTANCIAS DE CLASES OBJETO PARA MANEJO DE DATOS
    encabezado = Encabezado("")

    # RETORNO DE ARMADO DE DATOS PARA CONSUMO DE SERVICIO
    completion = client.chat.completions.create(
        model=encabezado.model,
        messages= mensajesNuevos,
        max_completion_tokens=encabezado.max_tokens
        
    )

    response_json = completion.choices[0].message.content

    return response_json

