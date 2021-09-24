import hashlib

def encrypt_hash(value: str) -> str:
  hash = hashlib.sha512()
  hash.update(value.encode('UTF-8'))
  
  return hash.hexdigest()