from urllib.parse import quote_plus

# Replace these with your actual MongoDB username and password
username = "admin"
password = ""

encoded_username = quote_plus(username)
encoded_password = quote_plus(password)

print(
    f"Encoded URI: mongodb://{encoded_username}:{encoded_password}@hostname:port/database")
