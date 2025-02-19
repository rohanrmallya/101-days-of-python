import streamlit as st
import openai
import os
from dotenv import load_dotenv
import json
load_dotenv()

openai.api_key = os.getenv('OPENAI_API_KEY')
DEFAULT_OPENAI_MODEL = "gpt-4"

def get_recipes_from_ingredients(ingredients, num_recipes=5):
    system_prompt = f"""
Create {num_recipes} unique and delicious recipes using the following ingredients: {ingredients}.
Provide the output **strictly** in this JSON format:
[
  {{
    "name": "Recipe Name",
    "ingredients": ["ingredient1", "ingredient2", ...],
    "steps": ["Step 1", "Step 2", ...]
  }},
  ...
]
Do not include any additional text or explanations.
"""
    try:
        response = openai.chat.completions.create(
            model=DEFAULT_OPENAI_MODEL,
            messages=[
                {"role": "system", "content": system_prompt},
            ],
            temperature=0.84,
        )
        recipes = json.loads(response.choices[0].message.content)
        return recipes
    except Exception as e:
        st.error(f"Error fetching recipe data: {e}")
        return None


def display_recipes(recipes):
    num_columns = 3  
    columns = st.columns(num_columns)
    
    for idx, recipe in enumerate(recipes):
        col = columns[idx % num_columns]  
        with col:
            st.subheader(f"🍽️ Recipe {idx + 1}: {recipe.get('name', 'Unnamed Recipe')}")
            st.write("**Ingredients:**")
            for ingredient in recipe.get('ingredients', []):
                st.write(f"- {ingredient}")
            
            st.write("**Instructions:**")
            for step_num, step in enumerate(recipe.get('steps', []), 1):
                st.write(f"{step_num}. {step}")

            st.markdown("---") 


def main():
    st.set_page_config(page_title="Modern Recipe Generator", layout="wide")
    st.title("🍳 Recipe Generator")
    st.write("Generate delicious recipes based on your ingredients with AI.")

    ingredients = st.text_input("🎤 Ingredients (comma-separated)")
    num_recipes = st.slider("Number of recipes to generate", 1, 10, 5)

    if st.button("Generate Recipes"):
        if not ingredients:
            st.warning("Please enter ingredients.")
        elif ',' not in ingredients:
            st.warning("Please separate ingredients with commas.")
        else:
            with st.spinner("Generating recipes..."):
                recipes = get_recipes_from_ingredients(ingredients, num_recipes)
            if recipes:
                st.success("Recipes generated successfully!")
                display_recipes(recipes)

    st.markdown(
        """
        <style>
        .bottom-right {
            position: fixed;
            bottom: 10px;
            right: 15px;
            font-size: 0.9em;
            color: gray;
        }
        </style>
        <div class="bottom-right">
            Made with ⚡ at 'The Hackers Playbook' ©. All rights reserved.
        </div>
        """,
        unsafe_allow_html=True
                )


if __name__ == "__main__":
    main()
