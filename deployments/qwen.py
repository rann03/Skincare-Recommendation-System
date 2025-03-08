import requests
import json

API_KEY = "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"  # Replace with your actual API key

def get_recommendations(skin_type, price_range, product_type, brand_pref, candidate_text, num_rec=3):
    # Construct the prompt to include explicit instructions
    prompt = (
        f"From the following list of skincare products, recommend {num_rec} products suitable for {skin_type} skin, "
        f"that are {product_type}s, with a preference for brand {brand_pref}, and within the price range ${price_range[0]}-${price_range[1]}.\n\n"
        f"Only use the products listed below for your recommendations:\n\n"
        f"{candidate_text}\n\n"
        f"Please select the best options from this list based on the criteria provided."
    )

    response = requests.post(
        url="https://openrouter.ai/api/v1/chat/completions",
        headers={
            "Authorization": f"Bearer {API_KEY}",
            "Content-Type": "application/json",
            "HTTP-Referer": "<YOUR_SITE_URL>",  # Optional
            "X-Title": "<YOUR_SITE_NAME>",      # Optional
        },
        data=json.dumps({
            "model": "qwen/qwen2.5-vl-72b-instruct:free",
            "messages": [
                {
                    "role": "user",
                    "content": prompt
                }
            ],
        })
    )

    if response.status_code == 200:
        return response.json()['choices'][0]['message']['content'].strip()
    else:
        return f"Error: {response.status_code} - {response.text}"

if __name__ == "__main__":
    # Example candidate text
    candidate_text = (
        "This product is Crème de la Mer from the brand LA MER. It is suitable for Combination and Dry and Normal and Oily and Sensitive skin types. It is priced at $175.\n"
        "This product is Oil-Free Moisturizer from the brand BrandY. It is suitable for Oily skin types. It is priced at $25.\n"
        "This product is Soothing Gel from the brand BrandZ. It is suitable for Sensitive skin types. It is priced at $18."
    )
    recs = get_recommendations("Oily", (15, 30), "Moisturizer", "BrandX", candidate_text)
    print("Generated Recommendations:\n", recs)