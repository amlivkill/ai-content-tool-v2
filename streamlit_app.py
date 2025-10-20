import streamlit as st
import pandas as pd

st.set_page_config(
    page_title="File Content Analyzer", 
    page_icon="📁",
    layout="wide"
)

def main():
    st.title("📁 File Content Analyzer")
    st.markdown("**Files Upload करें और Analyze करें**")
    
    # File upload section
    uploaded_files = st.file_uploader(
        "PDF, CSV, TXT files select करें",
        type=['pdf', 'csv', 'txt'],
        accept_multiple_files=True
    )
    
    if uploaded_files:
        st.success(f"✅ {len(uploaded_files)} file(s) uploaded!")
        
        for file in uploaded_files:
            with st.expander(f"📄 {file.name}", expanded=True):
                st.write(f"**File Type:** {file.type}")
                st.write(f"**Size:** {file.size / 1024:.1f} KB")
                
                if st.button(f"Analyze {file.name}", key=file.name):
                    # CSV files
                    if file.type == "text/csv":
                        try:
                            df = pd.read_csv(file)
                            st.success("✅ CSV analysis completed!")
                            st.write(f"**Rows:** {len(df)}")
                            st.write(f"**Columns:** {len(df.columns)}")
                            st.dataframe(df.head())
                        except Exception as e:
                            st.error(f"Error: {str(e)}")
                    
                    # TXT files
                    elif file.type == "text/plain":
                        try:
                            content = file.read().decode("utf-8")
                            st.success("✅ Text analysis completed!")
                            st.write(f"**Characters:** {len(content)}")
                            st.write(f"**Words:** {len(content.split())}")
                            st.write(f"**Preview:** {content[:500]}...")
                        except Exception as e:
                            st.error(f"Error: {str(e)}")
                    
                    # PDF files (coming soon)
                    elif file.type == "application/pdf":
                        st.info("📝 PDF support coming in next update!")
                    
                    else:
                        st.info("This file type will be supported soon!")

    # URL section (coming soon)
    st.markdown("---")
    st.info("🌐 **URL Scraping Feature** - Coming in the next update!")

if __name__ == "__main__":
    main()
