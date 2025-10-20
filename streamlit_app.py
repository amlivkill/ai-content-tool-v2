import streamlit as st

def main():
    st.title("🌐 URL & File Content Tool")
    st.success("✅ App is working! Adding new features...")
    
    # Tab 1: URL Input (Simple)
    tab1, tab2 = st.tabs(["🌐 URLs", "📁 Files"])
    
    with tab1:
        st.header("URLs से Content लें")
        url = st.text_input("Website URL डालें")
        if url:
            st.info(f"URL entered: {url}")
            st.write("🔜 URL scraping feature coming soon!")
            
            # Simple URL display
            if st.button("Show URL Info"):
                st.write(f"**URL:** {url}")
                st.write("**Status:** ✅ URL recorded successfully")
                st.write("**Next Step:** Content scraping will be added in next update")
    
    with tab2:
        st.header("Files Upload करें")
        uploaded_file = st.file_uploader("TXT or CSV file choose करें", type=['txt', 'csv'])
        
        if uploaded_file is not None:
            st.success(f"✅ {uploaded_file.name} uploaded successfully!")
            
            # File info
            col1, col2 = st.columns(2)
            with col1:
                st.write(f"**Name:** {uploaded_file.name}")
                st.write(f"**Type:** {uploaded_file.type}")
            with col2:
                st.write(f"**Size:** {uploaded_file.size} bytes")
                st.write(f"**Size:** {uploaded_file.size / 1024:.1f} KB")
            
            # Simple content display for TXT files
            if uploaded_file.type == "text/plain":
                content = uploaded_file.read().decode("utf-8")
                st.text_area("File Content:", content[:1000] + "..." if len(content) > 1000 else content, height=200)
                st.write(f"**Total Characters:** {len(content)}")
            
            elif uploaded_file.type == "text/csv":
                st.info("📊 CSV data analysis coming in next update!")
                st.write("Currently we can only show file information")
                
            # Download button
            st.download_button(
                label="📥 Download File Info",
                data=f"File: {uploaded_file.name}\nSize: {uploaded_file.size} bytes\nType: {uploaded_file.type}",
                file_name="file_info.txt",
                mime="text/plain"
            )

    # Coming soon features
    st.markdown("---")
    st.subheader("🚀 Coming Soon Features:")
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.write("🌐 **URL Scraping**")
        st.write("Auto content extraction")
    
    with col2:
        st.write("📊 **CSV Analysis**") 
        st.write("Data preview & stats")
    
    with col3:
        st.write("📝 **PDF Support**")
        st.write("PDF text extraction")

if __name__ == "__main__":
    main()
