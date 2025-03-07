import streamlit as st
import os
import traceback
from openai import OpenAI
import pydantic as pydantic
from dotenv import load_dotenv

load_dotenv(override=True, dotenv_path=".env")

openai_api_key = os.getenv("OPENAI_API_KEY")
if not openai_api_key:
    st.error("❌ OpenAI API Key Not Found in .env File")
    st.stop()

openai_client = OpenAI(api_key=openai_api_key)
    
DEFAULT_OPENAI_MODEL = "gpt-3.5-turbo"

def generate_system_prompt(context=str, tweet_context=str, tweet_number=int) -> str:
        return f"""
    You are a highly skilled social media assistant specializing in creating engaging, concise, and impactful tweets.
    Generate {tweet_number} professional tweets based on the following information:
    Context: {context}
    Tweet Description: {tweet_context}
    Ensure each tweet is unique, follows best practices for social media engagement, and maintains a professional tone. Keep each tweet within 280 characters, including relevant hashtags and call-to-actions if necessary. Avoid repetition and align the language with the context provided.
    """

SYSTEM_PROMPT = generate_system_prompt(context=str, tweet_context=str, tweet_number=int)    

def generate_tweets(context=str, tweet_context=str, tweet_number=int) -> str:
        """"
        Generates tweets based on the given context and tweet description."
        Args:
            context (str): The context for the tweets.
            tweet_context (str): The description of the tweets.
            tweet_number (int): The number of tweets to generate.
        Returns:
            str: The generated tweets.
        """

        try:
            response = openai_client.chat.completions.create(
                model=DEFAULT_OPENAI_MODEL,
                messages=[
                    {"role": "system", "content": SYSTEM_PROMPT},
                    {"role": "user", "content": f"Context: {context}\nTweet Context: {tweet_context}\nTweet Number: {tweet_number}"}
                ]
            )
            return response.choices[0].message.content
        except Exception as e:
            print(f"Failed to generate tweets. Error: {str(e)}")
            traceback.print_exc()
    
def main():  
        st.set_page_config(page_title="Tweet Stormer 🚀", page_icon="🐦", layout="wide") 

        st.title("🚀 Tweet Stormer 🐦")

        st.caption("Tweet Stormer is a Twitter Bot that generates Tweets based on a given context.")

        st.sidebar.title("📝 Configuration")

        st.sidebar.text_input("🔑 X API Key")

        context = st.sidebar.text_input("📝 Context", placeholder="Enter your context here...")

        tweet_context = st.sidebar.text_area("📝 Tweet Description", placeholder="Describe your tweet context here...")

        tweet_number = st.sidebar.slider("🔢 Number of Tweets", min_value=1, max_value=10, value=1)

        st.sidebar.markdown("---")

        if st.sidebar.button("🔄 Generate Tweets"):
            if not context or not tweet_context or not tweet_number:
                st.warning("❌ Please fill in all fields before generating tweets.")
            else:
                tweets = generate_tweets(context, tweet_context, tweet_number)
                if tweets:  
                    for tweet in tweets.split("\n"):
                        st.write(tweet)

if __name__ == "__main__":
    main()