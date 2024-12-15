import http.client
import requests


def fetch_joke():
    response = requests.get(
        "https://icanhazdadjoke.com/",
        headers={"Accept": "application/json"}
    )
    if response.status_code == 200:
        joke = response.json().get("joke")
        return joke
    return "Oops! I couldn't fetch a joke right now. But welcome!"

print(fetch_joke())



# image generation

# def get_welcome_image():
#     url = "https://nekos.best/api/v2/welcome"

#     try:
#         response = requests.get(url)

#         if response.status_code == 200:
#             data = response.json()
#             image_url = data["url"]  # Extract the image URL from the response
#             print("Welcome image generated successfully!")
#             print(f"Image URL: {image_url}")
#             return image_url
#         else:
#             print("Failed to fetch welcome image. Response:")
#             print(response.text)
#     except Exception as e:
#         print(f"An error occurred: {e}")

# # Call the function
# welcome_image_url = get_welcome_image()

# # Optional: Use the image URL in your Discord bot
# if welcome_image_url:
#     print(f"Generated Welcome Image URL: {welcome_image_url}")

