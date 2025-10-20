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
                
                if st.button(f"Analyze {file.name}", key=file.name):
                    # CSV files
                    if file.type == "text/csv":
                        try:
                            df = pd.read_csv(file)
                            st.success("✅ CSV analysis completed!")
                            st.write(f"**Rows:** {len(df)}")
                            st.write(f"**Columns:** {len(df.columns)}")
                            st.write("**Data Preview:**")
                            st.dataframe(df.head())
                            
                            # Download option
                            csv_data = df.to_csv(index=False)
                            st.download_button(
                                label="📥 Download Processed CSV",
                                data=csv_data,
                                file_name=f"processed_{file.name}",
                                mime="text/csv"
                            )
                        except Exception as e:
                            st.error(f"Error: {str(e)}")
                    
                    # TXT files
                    elif file.type == "text/plain":
                        try:
                            content = file.read().decode("utf-8")
                            st.success("✅ Text analysis completed!")
                            st.write(f"**Characters:** {len(content)}")
                            st.write(f"**Words:** {len(content.split())}")
                            st.write(f"**Lines:** {len(content.splitlines())}")
                            st.write(f"**Preview:** {content[:500]}...")
                            
                            # Download option
                            st.download_button(
                                label="📥 Download Text Content",
                                data=content,
                                file_name=f"content_{file.name}",
                                mime="text/plain"
                            )
                        except Exception as e:
                            st.error(f"Error: {str(e)}")

    # Coming soon features
    st.markdown("---")
    col1, col2 = st.columns(2)
    
    with col1:
        st.info("🌐 **URL Scraping** - Coming soon!")
    
    with col2:
        st.info("📝 **PDF Support** - Coming soon!")

if __name__ == "__main__":
    main()
