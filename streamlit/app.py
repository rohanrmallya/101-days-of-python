import streamlit as st
import sys
import os
from streamlit_extras.app_logo import add_logo
from streamlit_extras.metric_cards import style_metric_cards
from streamlit_extras.stylable_container import stylable_container
from book_summarizer import summarize_text, get_book_metadata, generate_markdown

sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# Page Configuration
st.set_page_config(page_title="AI Book Summarizer", page_icon="📚", layout="wide")

# Add Custom App Logo
add_logo("https://cdn-icons-png.flaticon.com/512/2232/2232688.png", height=120)

st.title("📚 AI-Powered Book Summarizer")

# Sidebar Design
with stylable_container("sidebar-container", css_styles="background-color: #F7F7F7; padding: 20px; border-radius: 10px;"):
    book_name = st.text_input("Enter Book Name", placeholder="e.g. Atomic Habits")
    generate = st.button("Generate Summary")

if generate:
    if book_name:
        with st.spinner("Fetching Book Metadata and Generating Summary..."):
            metadata = get_book_metadata(book_name)
            summary = summarize_text(f"Summarize the book: {book_name}")
            markdown = generate_markdown(book_name, metadata, summary)

            st.success("✅ Summary Generated Successfully!")
            st.download_button("📥 Download Markdown Summary", markdown, f"{book_name}.md")

            # Display Book Info
            st.subheader("Book Information")
            style_metric_cards(border_left_color="#2E8B57", box_shadow=True)
            col1, col2, col3 = st.columns([1, 1, 1])
            col1.metric("Title", metadata['Title'])
            col2.metric("Author", metadata['Author'])
            col3.metric("Pages", metadata['Pages'])

            st.markdown(
                """
                <style>
                div[data-testid="stMetric"] > div {
                    color: black !important;
                    text-align: center;
                    padding: 10px;
                    background: #F0F0F0;
                    border-radius: 10px;
                    margin-bottom: 20px;
                }
                </style>
                """,
                unsafe_allow_html=True,
            )

            st.subheader("Summary Preview")
            st.markdown(markdown)
        
    else:
        st.error("Please enter the book name before generating the summary.")

# Footer
st.markdown("---")
st.caption("Made with ⚡ at 'The Hackers Playbook' ©. All rights reserved.")
