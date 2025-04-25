import streamlit as st
import os
from typing import Iterator, List, Dict, Tuple
import time
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_groq import ChatGroq
from langchain_core.output_parsers import StrOutputParser


def tuplify(history: List[Dict[str, str]]) -> List[Tuple[str, str]]:
    return [(d['role'], d['content']) for d in history]


def stream_answer(answer: str) -> Iterator:
    yield f"Bot: "
    for word in answer.split():
        yield word + " "
        time.sleep(0.05)


def main():
    st.sidebar.markdown("# Main App")
    st.write("""
    # A Simple LLM App With Streamlit!!
            
    This is a simple Question & Answer app, give it a try!
    """)

    llm = ChatGroq(
                model="llama3-8b-8192",
                temperature=0,
                max_tokens=None,
                timeout=None,
                max_retries=2,
            )
    
    prompt = ChatPromptTemplate.from_messages(
        [
            ("system", "You are a helpful assistant."),
            MessagesPlaceholder("history"),
            ("human", "{question}")
        ]
    )

    chain = prompt | llm | StrOutputParser()


    if "messages" not in st.session_state:
        st.session_state.messages = []

    # Display chat messages from history on app rerun
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    # React to user input
    if question := st.chat_input("Ask me a question"):
        # Display user message in chat message container
        st.chat_message("user").markdown(f"Human: {question}")
        # Add user message to chat history
        st.session_state.messages.append({"role": "human", "content": f"Human: {question}"})

        history = tuplify(st.session_state.messages)

        answer = chain.invoke({
                    "history": history,
                    "question": question
        })

        # Display assistant response in chat message container
        with st.chat_message("ai"):
            st.write_stream(stream_answer(answer))
        # Add assistant response to chat history
        st.session_state.messages.append({"role": "ai", "content": answer})


if __name__ == "__main__":
    main()
