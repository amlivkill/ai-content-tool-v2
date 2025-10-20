import streamlit as st

def main():
    st.title("🌐 My Content Tool")
    st.write("Basic version - working!")
    
    # Simple input
    name = st.text_input("Enter your name")
    if name:
        st.write(f"Hello {name}!")
    
    # Simple file upload
    file = st.file_uploader("Upload a file")
    if file:
        st.write(f"Uploaded: {file.name}")

if __name__ == "__main__":
    main()
