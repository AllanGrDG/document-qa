import streamlit as st
import google.generativeai as genai

# Show title and description.
st.title("📄 Document question answering with Gemini")
st.write(
    "Upload a document below and ask a question about it – Gemini will answer! "
    "To use this app, you need to provide a Google Gemini API key, which you can get [here](https://aistudio.google.com/app/apikey). "
)

# Ask user for their Google Gemini API key via `st.text_input`.
# Alternatively, you can store the API key in `./.streamlit/secrets.toml` and access it
# via `st.secrets`, see https://docs.streamlit.io/develop/concepts/connections/secrets-management
gemini_api_key = st.text_input("Google Gemini API Key", type="password")
if not gemini_api_key:
    st.info("Please add your Google Gemini API key to continue.", icon="🗝️")
else:
    # Configure the Gemini API client.
    try:
        genai.configure(api_key=gemini_api_key)
    except Exception as e:
        st.error(f"Failed to configure Gemini API: {e}")


    # Let the user upload a file via `st.file_uploader`.
    uploaded_file = st.file_uploader(
        "Upload a document (.txt or .md)", type=("txt", "md")
    )

    # Ask the user for a question via `st.text_area`.
    question = st.text_area(
        "Now ask a question about the document!",
        placeholder="Can you give me a short summary?",
        disabled=not uploaded_file,
    )

    if uploaded_file and question:
        # Process the uploaded file and question.
        document = uploaded_file.read().decode()
        
        # Create the prompt for the model.
        prompt = f"Here's a document: {document}\n\n---\n\nBased on this document, please answer the following question: {question}"

        # Select the Gemini model.
        # Using gemini-1.5-flash-preview-0514 for its speed and context window.
        model = genai.GenerativeModel('gemini-1.5-flash')

        # Generate an answer using the Gemini API with streaming.
        try:
            stream = model.generate_content(prompt, stream=True)

            # Stream the response to the app using `st.write_stream`.
            # We need to adapt the generator to yield strings.
            def stream_generator(stream):
                for chunk in stream:
                    if chunk.text:
                        yield chunk.text
            
            st.write_stream(stream_generator(stream))

        except Exception as e:
            st.error(f"An error occurred while generating the response: {e}")

