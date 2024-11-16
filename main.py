import streamlit as st
import os
from typing import Iterator
import time
from groq import Groq


def query_groq(client: Groq, prompt: str) -> str:
    stream = client.chat.completions.create(
    messages=[
        {
            "role": "user",
            "content": prompt,
        }
    ],
    model="llama3-8b-8192",
    stream=True
    )
    yield "Bot: "
    for chunk in stream:
        response = chunk.choices[0].delta.content
        if response is not None:
            yield response


def main():
    st.sidebar.markdown("# Main App")

    st.write("""
    # My Second LLM App With Streamlit!!
            
    This is a simple Question & Answer app, give it a try!
    """)

    messages = st.container(height=200)
    client = Groq(api_key=os.environ.get("GROQ_API_KEY"))

    if prompt := st.chat_input("Ask Me Something"):
        messages.chat_message("user").write(f"You: {prompt}")

        with st.status("Generating Response") as status:
            try:
                answer = query_groq(client, prompt)
                
            except Exception as e:
                st.exception(e)

            time.sleep(2)
            status.update(label="Done!", state="complete", expanded=False)
        with messages.chat_message("assistant"):
            st.write_stream(answer)
            
        # st.balloons()

if __name__ == "__main__":
    main()
