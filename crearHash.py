import bcrypt
from models.usuarios import Usuario

password = "admin123"
us = Usuario()

hash = us.encriptar_psw(password)

print(hash)

# $2b$12$NP0gvrNDX.M9QaX/LeE87OA64Ys9qVxaz7zShvmcz9pkofr4JUWhy