import hashlib

# Función para generar un hash SHA-256 de una cadena
def generate_hash(data):
    return hashlib.sha256(data.encode()).hexdigest()

# Función para verificar si un hash coincide con una cadena
def verify_hash(data, hash_value):
    return generate_hash(data) == hash_value
