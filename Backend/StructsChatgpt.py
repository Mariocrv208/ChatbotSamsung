import json

class Encabezado:
    def __init__(self, prompt):
        self.model = "gpt-5-nano-2025-08-07"
        self.prompt = prompt
        self.max_tokens = 600
        self.temperature = 0.5
        self.stop = "None"
        
class Config:
    def __init__(self, Authorization):
        self.Authorization = Authorization
        
class Respuesta:
    def __init__(self, content, actions, quick_replies):
        self.version = "v2"
        self.content = content  # Ahora `content` es una instancia de la clase `Contenido`
        self.actions = actions
        self.quick_replies = quick_replies

    def to_dict(self):
        return {
            "version": self.version,
            "content": self.content.to_dict(),
            "actions": self.actions,
            "quick_replies": self.quick_replies
        }

class Contenido:
    def __init__(self, mensajes):
        self.mensajes = mensajes

    def to_dict(self):
        return {
            "mensajes": self.mensajes.to_dict()
        }

class Mensajes:
    def __init__(self, type, text):
        self.type = type
        self.text = text

    def to_dict(self):
        return {
            "type": self.type,
            "text": self.text
        }
