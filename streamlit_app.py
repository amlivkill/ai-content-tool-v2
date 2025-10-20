import streamlit as st
import pandas as pd
import requests
from bs4 import BeautifulSoup
import io

def scrape_website(url):
    """Simple website content scraping"""
    try:
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        }
        response = requests.get(url, timeout=10)
        soup = BeautifulSoup(response.content, 'html.parser')
        
        # Remove scripts and styles
        for script in soup(["script", "style"]):
            script.decompose()
        
        # Get title
        title = soup.find('title')
        title_text = title.text.strip() if title else "No Title Found"
        
        # Get main content
        text = soup.get_text()
        lines = (line.strip() for line in text.splitlines())
        chunks = (phrase.strip() for line in lines for phrase in line.split("  "))
        clean_text = ' '.join(chunk for chunk in chunks if chunk)
        
        return {
            'success': True,
            'title': title_text,
            'content': clean_text[:5000],  # First 5000 characters
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
                    result = scrape_website(url)
                    
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

    # Coming soon features
    st.markdown("---")
    st.info("📝 **PDF Support** - Coming in next update! (PDF text extraction, multiple pages support)")

if __name__ == "__main__":
    main()
