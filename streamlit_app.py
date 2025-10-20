import streamlit as st
import requests
from bs4 import BeautifulSoup
import pandas as pd
import PyPDF2
import io

# Page configuration
st.set_page_config(
    page_title="URL & File Content Extractor",
    page_icon="🌐",
    layout="wide"
)

def scrape_url(url):
    """URL से content scrape करें"""
    try:
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        }
        response = requests.get(url, headers=headers, timeout=10)
        soup = BeautifulSoup(response.content, 'html.parser')
        
        # Remove scripts and styles
        for script in soup(["script", "style"]):
            script.decompose()
        
        # Get title and content
        title = soup.find('title')
        title_text = title.text.strip() if title else "No Title"
        
        # Get text content
        text = soup.get_text()
        lines = (line.strip() for line in text.splitlines())
        chunks = (phrase.strip() for line in lines for phrase in line.split("  "))
        text = ' '.join(chunk for chunk in chunks if chunk)
        
        return {
            'success': True,
            'title': title_text,
            'content': text[:3000],  # First 3000 characters
            'url': url
        }
    except Exception as e:
        return {
            'success': False,
            'error': str(e),
            'url': url
        }

def extract_pdf_content(file):
    """PDF file से content निकालें"""
    try:
        pdf_reader = PyPDF2.PdfReader(file)
        text = ""
        for page in pdf_reader.pages:
            text += page.extract_text() + "\n"
        return {
            'success': True,
            'content': text,
            'pages': len(pdf_reader.pages)
        }
    except Exception as e:
        return {
            'success': False,
            'error': str(e)
        }

def extract_csv_content(file):
    """CSV file से data निकालें"""
    try:
        df = pd.read_csv(file)
        return {
            'success': True,
            'dataframe': df,
            'rows': len(df),
            'columns': len(df.columns),
            'column_names': list(df.columns)
        }
    except Exception as e:
        return {
            'success': False,
            'error': str(e)
        }

def extract_txt_content(file):
    """TXT file से content निकालें"""
    try:
        content = file.read().decode("utf-8")
        return {
            'success': True,
            'content': content,
            'characters': len(content),
            'words': len(content.split()),
            'lines': len(content.splitlines())
        }
    except Exception as e:
        return {
            'success': False,
            'error': str(e)
        }

def main():
    st.title("🌐 URL & File Content Extractor")
    st.markdown("**URLs से Data Scrape करें और Files Upload करें**")
    
    # Initialize session state
    if 'scraped_urls' not in st.session_state:
        st.session_state.scraped_urls = []
    
    # Tabs for different functionalities
    tab1, tab2 = st.tabs(["🌐 URL Scraping", "📁 File Upload"])
    
    with tab1:
        st.header("URLs से Content Scrape करें")
        
        url_input = st.text_area(
            "URLs डालें (एक line में एक URL)",
            placeholder="https://example.com\nhttps://example.org",
            height=100,
            help="एक बार में multiple URLs process कर सकते हैं"
        )
        
        if st.button("🚀 Scrape URLs", type="primary") and url_input:
            urls = [url.strip() for url in url_input.split('\n') if url.strip()]
            
            if urls:
                progress_bar = st.progress(0)
                status_text = st.empty()
                
                for i, url in enumerate(urls):
                    status_text.text(f"Scraping: {url}")
                    result = scrape_url(url)
                    st.session_state.scraped_urls.append(result)
                    progress_bar.progress((i + 1) / len(urls))
                
                status_text.text("✅ Scraping completed!")
        
        # Show scraping results
        if st.session_state.scraped_urls:
            st.subheader("Scraping Results")
            for i, result in enumerate(st.session_state.scraped_urls):
                if result['success']:
                    with st.expander(f"✅ {result['title']}", expanded=False):
                        st.write(f"**URL:** {result['url']}")
                        st.write(f"**Content Preview:** {result['content'][:500]}...")
                        
                        # Download button for each URL content
                        st.download_button(
                            label=f"📥 Download {result['title']} Content",
                            data=result['content'],
                            file_name=f"url_content_{i+1}.txt",
                            mime="text/plain",
                            key=f"url_dl_{i}"
                        )
                else:
                    st.error(f"❌ Failed to scrape: {result['url']}")
                    st.write(f"Error: {result['error']}")
    
    with tab2:
        st.header("Files Upload और Analyze करें")
        
        uploaded_files = st.file_uploader(
            "PDF, CSV, TXT files select करें",
            type=['pdf', 'csv', 'txt'],
            accept_multiple_files=True,
            help="Multiple files select कर सकते हैं"
        )
        
        if uploaded_files:
            st.success(f"✅ {len(uploaded_files)} file(s) uploaded!")
            
            for file in uploaded_files:
                with st.expander(f"📄 {file.name}", expanded=True):
                    col1, col2 = st.columns([1, 2])
                    
                    with col1:
                        st.write(f"**File Type:** {file.type}")
                        st.write(f"**Size:** {file.size / 1024:.1f} KB")
                        
                        if st.button(f"Analyze {file.name}", key=f"btn_{file.name}"):
                            # Process based on file type
                            if file.type == "application/pdf":
                                result = extract_pdf_content(file)
                                if result['success']:
                                    st.success("✅ PDF analysis completed!")
                                    st.write(f"**Pages:** {result['pages']}")
                                    st.write(f"**Content Preview:** {result['content'][:500]}...")
                                    
                                    # Download PDF content
                                    st.download_button(
                                        label="📥 Download PDF Text",
                                        data=result['content'],
                                        file_name=f"{file.name}_content.txt",
                                        mime="text/plain",
                                        key=f"pdf_dl_{file.name}"
                                    )
                                else:
                                    st.error(f"❌ Error: {result['error']}")
                            
                            elif file.type == "text/csv":
                                result = extract_csv_content(file)
                                if result['success']:
                                    st.success("✅ CSV analysis completed!")
                                    st.write(f"**Rows:** {result['rows']}")
                                    st.write(f"**Columns:** {result['columns']}")
                                    st.write(f"**Column Names:** {', '.join(result['column_names'])}")
                                    
                                    # Show data preview
                                    st.subheader("Data Preview")
                                    st.dataframe(result['dataframe'].head(10))
                                    
                                    # Download CSV data
                                    csv_data = result['dataframe'].to_csv(index=False)
                                    st.download_button(
                                        label="📥 Download Processed CSV",
                                        data=csv_data,
                                        file_name=f"processed_{file.name}",
                                        mime="text/csv",
                                        key=f"csv_dl_{file.name}"
                                    )
                                else:
                                    st.error(f"❌ Error: {result['error']}")
                            
                            elif file.type == "text/plain":
                                result = extract_txt_content(file)
                                if result['success']:
                                    st.success("✅ Text analysis completed!")
                                    st.write(f"**Characters:** {result['characters']}")
                                    st.write(f"**Words:** {result['words']}")
                                    st.write(f"**Lines:** {result['lines']}")
                                    st.write(f"**Content Preview:** {result['content'][:500]}...")
                                    
                                    # Download text content
                                    st.download_button(
                                        label="📥 Download Text Content",
                                        data=result['content'],
                                        file_name=f"{file.name}_content.txt",
                                        mime="text/plain",
                                        key=f"txt_dl_{file.name}"
                                    )
                                else:
                                    st.error(f"❌ Error: {result['error']}")
                    
                    with col2:
                        st.info("**File Analysis** - Analyze बटन पर क्लिक करें")

if __name__ == "__main__":
    main()
