import streamlit as st
import requests

st.title("Natural Language to SQL")
st.write("Ask any question in plain English and get results from the database.")

question = st.text_input("Enter your question:")

if st.button("Run Query"):
    if question:
        with st.spinner("Generating SQL..."):
            response = requests.post(
                "http://localhost:8000/query",
                json={"question": question}
            )
            if response.status_code == 200:
                data = response.json()
                if "error" in data.get("result", {}):
                    st.error(f"SQL Error: {data['result']['error']}")
                else:
                    st.subheader("Generated SQL:")
                    st.code(data["sql"], language="sql")
                    st.subheader("Results:")
                    if len(data["result"]) == 0:
                        st.info("Query returned no results.")
                    else:
                        st.dataframe(data["result"])
            else:
                st.error("Backend error - please try again.")
                
    else:
        st.warning("Please enter a question.")