import streamlit as st
import pandas as pd
import io

def main():
    st.title("📁 File Content Analyzer")
    st.markdown("**Files Upload करें और Analyze करें**")
    
    # File upload section
    uploaded_files = st.file_uploader(
        "CSV, TXT files select करें",
        type=['csv', 'txt'],
        accept_multiple_files=True
    )
    
    if uploaded_files:
        st.success(f"✅ {len(uploaded_files)} file(s) uploaded!")
        
        for file in uploaded_files:
            with st.expander(f"📄 {file.name}", expanded=True):
                st.write(f"**File Type:** {file.type}")
                st.write(f"**Size:** {file.size / 1024:.1f} KB")
                
                # CSV File Analysis
                if file.type == "text/csv":
                    try:
                        df = pd.read_csv(file)
                        
                        col1, col2 = st.columns(2)
                        
                        with col1:
                            st.subheader("📊 CSV Statistics")
                            st.write(f"**Rows:** {len(df)}")
                            st.write(f"**Columns:** {len(df.columns)}")
                            st.write(f"**Total Cells:** {len(df) * len(df.columns)}")
                            
                            # Column names
                            st.write("**Columns:**")
                            for col in df.columns:
                                st.write(f"- {col}")
                        
                        with col2:
                            st.subheader("🔍 Data Preview")
                            st.dataframe(df.head(10))
                        
                        # Data summary
                        st.subheader("📈 Data Summary")
                        col1, col2 = st.columns(2)
                        
                        with col1:
                            numeric_cols = df.select_dtypes(include=['number']).columns
                            if len(numeric_cols) > 0:
                                st.write("**Numeric Columns:**")
                                for col in numeric_cols:
                                    st.write(f"- {col}")
                        
                        with col2:
                            text_cols = df.select_dtypes(include=['object']).columns
                            if len(text_cols) > 0:
                                st.write("**Text Columns:**")
                                for col in text_cols:
                                    st.write(f"- {col}")
                        
                        # Download processed data
                        csv_data = df.to_csv(index=False)
                        st.download_button(
                            label="📥 Download Processed CSV",
                            data=csv_data,
                            file_name=f"analyzed_{file.name}",
                            mime="text/csv"
                        )
                        
                    except Exception as e:
                        st.error(f"❌ Error reading CSV: {str(e)}")
                
                # TXT File Analysis
                elif file.type == "text/plain":
                    try:
                        content = file.read().decode("utf-8")
                        
                        col1, col2 = st.columns(2)
                        
                        with col1:
                            st.subheader("📝 Text Statistics")
                            st.write(f"**Characters:** {len(content)}")
                            st.write(f"**Words:** {len(content.split())}")
                            st.write(f"**Lines:** {len(content.splitlines())}")
                            st.write(f"**Paragraphs:** {len([p for p in content.split('\n\n') if p.strip()])}")
                            
                            # Word frequency (simple)
                            words = content.lower().split()
                            word_count = {}
                            for word in words[:100]:  # First 100 words
                                if word.isalpha():
                                    word_count[word] = word_count.get(word, 0) + 1
                            
                            if word_count:
                                st.write("**Common Words:**")
                                for word, count in list(word_count.items())[:5]:
                                    st.write(f"- {word}: {count}")
                        
                        with col2:
                            st.subheader("🔍 Content Preview")
                            st.text_area("Content:", content[:1000] + "..." if len(content) > 1000 else content, height=200, key=f"text_{file.name}")
                        
                        # Download text content
                        st.download_button(
                            label="📥 Download Analyzed Text",
                            data=content,
                            file_name=f"analyzed_{file.name}",
                            mime="text/plain"
                        )
                        
                    except Exception as e:
                        st.error(f"❌ Error reading text file: {str(e)}")

    # Coming soon features
    st.markdown("---")
    st.subheader("🚀 Coming Soon Features")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.info("🌐 **URL Scraping**")
        st.write("- Auto content extraction")
        st.write("- Multiple URLs support")
        st.write("- Web scraping")
    
    with col2:
        st.info("📝 **PDF Support**")
        st.write("- PDF text extraction")
        st.write("- Multiple pages support")
        st.write("- Table detection")

if __name__ == "__main__":
    main()
