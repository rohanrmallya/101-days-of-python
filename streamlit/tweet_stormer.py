import streamlit as st
import os
import traceback
from typing import Union
from openai import OpenAI
from pydantic import BaseModel
from dotenv import load_dotenv

load_dotenv(override=True, dotenv_path=".env")

## constants
DEFAULT_OPENAI_MODEL = "gpt-4o"


class Tweet(BaseModel):
    content: str


class GenerateTweetResponse(BaseModel):
    tweets: list[Tweet]


def validate_openai_api_key(openai_api_key: str) -> str:
    if not openai_api_key:
        st.error("❌ OpenAI API Key Not Found in .env File")
        st.stop()


def get_openai_client() -> OpenAI:
    try:
        openai_api_key = os.getenv("OPENAI_API_KEY")
        validate_openai_api_key(openai_api_key)
        return OpenAI(api_key=openai_api_key)
    except Exception as e:
        print(f"Failed to create OpenAI client. Error: {str(e)}")
        traceback.print_exc()


def generate_system_prompt(context: str, tweet_context: str, tweet_number: int) -> str:
    return f"""
    You are a highly skilled social media assistant specializing in creating engaging, concise, and impactful tweets.
    Generate {tweet_number} professional tweets based on the following information:
    Context: {context}
    Tweet Description: {tweet_context}
    Ensure each tweet is unique, follows best practices for social media engagement, and maintains a professional tone. Keep each tweet within 280 characters, including relevant hashtags and call-to-actions if necessary. Avoid repetition and align the language with the context provided.
    """


def generate_tweets(
    context: str, tweet_context: str, tweet_number: int
) -> Union[GenerateTweetResponse, None]:
    """
    Generates tweets based on the given context and tweet description."
    Args:
        context (str): The context for the tweets.
        tweet_context (str): The description of the tweets.
        tweet_number (int): The number of tweets to generate.
    Returns:
        str: The generated tweets.
    """

    try:
        openai_client = get_openai_client()
        system_prompt = generate_system_prompt(context, tweet_context, tweet_number)
        response = openai_client.beta.chat.completions.parse(
            model=DEFAULT_OPENAI_MODEL,
            messages=[
                {"role": "system", "content": system_prompt},
                {
                    "role": "user",
                    "content": f"Context: {context}\nTweet Context: {tweet_context}\n Generate {tweet_number} tweets.",
                },
            ],
            response_format=GenerateTweetResponse,
        )
        return response.choices[0].message.parsed
    except Exception as e:
        print(f"Failed to generate tweets. Error: {str(e)}")
        traceback.print_exc()
        return None


def refine_tweet(tweet: Tweet, refine_prompt: str, context="") -> Union[Tweet, None]:
    try:
        openai_client = get_openai_client()
        system_prompt = (
            "Refine the tweet based on the given instructions from the user."
        )
        response = openai_client.beta.chat.completions.parse(
            model=DEFAULT_OPENAI_MODEL,
            messages=[
                {"role": "system", "content": system_prompt},
                {
                    "role": "user",
                    "content": f"Context: {context}\nOriginal Tweet: {tweet.content}\n",
                },
            ],
            response_format=Tweet,
        )
        return response.choices[0].message.parsed
    except Exception as e:
        print(f"Failed to refine tweet. Error: {str(e)}")
        traceback.print_exc()
        return None


tweets_generated = []

if st.session_state.get("tweets_generated") is None:
    st.session_state["tweets_generated"] = tweets_generated


def main():
    st.set_page_config(page_title="Tweet Stormer 🚀", page_icon="🐦", layout="wide")

    st.title("🚀 Tweet Stormer 🐦")

    st.caption(
        "Tweet Stormer is a Twitter Bot that generates Tweets based on a given context."
    )

    st.sidebar.title("📝 Configuration")

    st.sidebar.text_input("🔑 X API Key")

    context = st.sidebar.text_input(
        "📝 Context", placeholder="Enter your context here..."
    )

    tweet_context = st.sidebar.text_area(
        "📝 Tweet Description", placeholder="Describe your tweet context here..."
    )

    tweet_number = st.sidebar.slider(
        "🔢 Number of Tweets", min_value=1, max_value=10, value=1
    )

    st.sidebar.markdown("---")

    tweets = st.session_state.tweets_generated

    if st.sidebar.button("🔄 Generate Tweets"):
        if not context or not tweet_context or not tweet_number:
            st.warning("❌ Please fill in all fields before generating tweets.")
        else:
            tweets_response = generate_tweets(context, tweet_context, tweet_number)

            if not tweets_response:
                st.error("❌ Failed to generate tweets. Please try again.")
                return

            st.session_state.tweets_generated = tweets_response.tweets
            st.rerun()

    if tweets and len(tweets) > 0:
        st.success("✅ Tweets Generated Successfully!")
        for idx, tweet in enumerate(tweets):
            st.markdown(f"🐦 {tweet.content}")
            post_tweet_button = st.button("🚀 Post Tweet", key=f"post_tweet_{idx}")
            refine_button = st.button("🔧 Refine Tweet", key=f"refine_{idx}")
            refine_input_prompt = st.text_area(
                "🔧 Refine Tweet",
                placeholder="Instructions to refine the tweet.",
                key=f"refine_input_{idx}",
            )
            if refine_button:
                refined_tweet = refine_tweet(tweet, refine_input_prompt, context)
                if refined_tweet:
                    st.session_state.tweets_generated[idx] = refined_tweet
                    st.success("✅ Tweet Refined Successfully!")
                    st.rerun()
            if post_tweet_button:
                st.success("✅ Tweet Posted Successfully! (TODO)")


if __name__ == "__main__":
    main()
