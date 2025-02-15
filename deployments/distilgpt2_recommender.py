import torch
from transformers import AutoTokenizer, AutoModelForCausalLM

MODEL_NAME = "distilgpt2"


tokenizer = AutoTokenizer.from_pretrained(MODEL_NAME, use_fast=False)
model = AutoModelForCausalLM.from_pretrained(MODEL_NAME)
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
model.to(device)

def get_recommendations(skin_type, price_range, ingredient_pref, candidate_text, num_rec=3):
    prompt = f"Recommend {num_rec} skincare products for {skin_type} skin with {ingredient_pref} in the price range {price_range}."
    
    
    inputs = tokenizer(prompt, return_tensors="pt", truncation=True, max_length=1024 - 100).to(device)
    
    
    output = model.generate(**inputs, max_new_tokens=50, do_sample=True, temperature=0.7)
    generated_text = tokenizer.decode(output[0], skip_special_tokens=True)
    
   
    recommendation_text = generated_text[len(prompt):].strip()
    
    return recommendation_text

if __name__ == "__main__":
    candidate_text = ("1. Name: Hydrating Cream. Brand: BrandX. Ingredients: aloe, hyaluronic acid, vitamin E. Price: $20.\n"
                      "2. Name: Oil-Free Moisturizer. Brand: BrandY. Ingredients: glycerin, niacinamide. Price: $25.\n"
                      "3. Name: Soothing Gel. Brand: BrandZ. Ingredients: cucumber extract, calendula. Price: $18.")
    recs = get_recommendations("Oily", "$15-$30", "aloe", candidate_text)
    print("Generated Recommendations:\n", recs)