import streamlit as st
import pandas as pd
import requests
import re

def simple_scrape_website(url):
    """BeautifulSoup के बिना simple website scraping"""
    try:
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        }
        response = requests.get(url, timeout=10)
        
        # Simple title extraction using regex
        title_match = re.search(r'<title[^>]*>(.*?)</title>', response.text, re.IGNORECASE)
        title = title_match.group(1).strip() if title_match else "No Title Found"
        
        # Simple content extraction - remove HTML tags
        clean_text = re.sub(r'<[^>]+>', ' ', response.text)
        clean_text = re.sub(r'\s+', ' ', clean_text).strip()
        
        return {
            'success': True,
            'title': title,
            'content': clean_text[:3000],  # First 3000 characters
            'url': url,
            'content_length': len(clean_text)
        }
    except Exception as e:
        return {
            'success': False,
            'error': str(e),
            'url': url
        }

def main():
    st.title("🌐 URL Scraper + File Analyzer")
    st.markdown("**URLs से Data Scrape करें और Files Analyze करें**")
    
    # Tabs for different features
    tab1, tab2 = st.tabs(["🌐 URL Scraping", "📁 File Analysis"])
    
    with tab1:
        st.header("URLs से Content Scrape करें")
        
        url_input = st.text_area(
            "URLs डालें (एक line में एक URL)",
            placeholder="https://example.com\nhttps://example.org",
            height=100
        )
        
        if st.button("🚀 Scrape URLs", type="primary") and url_input:
            urls = [url.strip() for url in url_input.split('\n') if url.strip()]
            
            if urls:
                progress_bar = st.progress(0)
                status_text = st.empty()
                
                for i, url in enumerate(urls):
                    status_text.text(f"Scraping: {url}")
                    result = simple_scrape_website(url)
                    
                    if result['success']:
                        with st.expander(f"✅ {result['title']}", expanded=False):
                            st.write(f"**URL:** {result['url']}")
                            st.write(f"**Content Length:** {result['content_length']} characters")
                            st.write(f"**Content Preview:** {result['content'][:500]}...")
                            
                            # Download scraped content
                            st.download_button(
                                label="📥 Download Content",
                                data=result['content'],
                                file_name=f"scraped_{result['title'][:20]}.txt",
                                mime="text/plain",
                                key=f"url_{i}"
                            )
                    else:
                        st.error(f"❌ Failed: {result['url']}")
                        st.write(f"Error: {result['error']}")
                    
                    progress_bar.progress((i + 1) / len(urls))
                
                status_text.text("✅ Scraping completed!")
        else:
            st.info("👉 URLs डालें और Scrape बटन पर क्लिक करें")
    
    with tab2:
        st.header("Files Upload और Analyze करें")
        
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
                                st.write("**Columns:**")
                                for col in df.columns:
                                    st.write(f"- {col}")
                            
                            with col2:
                                st.subheader("🔍 Data Preview")
                                st.dataframe(df.head(10))
                            
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
                            
                            with col2:
                                st.subheader("🔍 Content Preview")
                                st.text_area("Content:", content[:1000] + "..." if len(content) > 1000 else content, 
                                           height=200, key=f"text_{file.name}")
                            
                            # Download text content
                            st.download_button(
                                label="📥 Download Analyzed Text",
                                data=content,
                                file_name=f"analyzed_{file.name}",
                                mime="text/plain"
                            )
                            
                        except Exception as e:
                            st.error(f"❌ Error reading text file: {str(e)}")
        else:
            st.info("👉 Files upload करें और analyze करें")

if __name__ == "__main__":
    main()
