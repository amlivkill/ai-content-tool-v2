import streamlit as st
import pandas as pd
import requests
import re
import PyPDF2
import docx
import io

# Mobile-friendly page config
st.set_page_config(
    page_title="Content Analyzer Pro",
    page_icon="🔍",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Custom CSS for mobile optimization
st.markdown("""
<style>
    /* Mobile responsive */
    @media (max-width: 768px) {
        .main-header {
            font-size: 1.8rem !important;
        }
        .feature-card {
            padding: 0.8rem !important;
            margin: 0.3rem 0 !important;
        }
        .stButton button {
            width: 100% !important;
        }
        .stDownloadButton button {
            width: 100% !important;
        }
    }
    
    /* General styling */
    .main-header {
        font-size: 2.5rem;
        color: #1f77b4;
        text-align: center;
        margin-bottom: 1rem;
    }
    .feature-card {
        background-color: #f8f9fa;
        padding: 1.2rem;
        border-radius: 10px;
        border-left: 4px solid #1f77b4;
        margin: 0.5rem 0;
    }
    .file-type-badge {
        background-color: #1f77b4;
        color: white;
        padding: 0.3rem 0.8rem;
        border-radius: 15px;
        font-size: 0.8rem;
        display: inline-block;
        margin: 0.2rem;
    }
    .mobile-warning {
        background-color: #fff3cd;
        color: #856404;
        padding: 0.8rem;
        border-radius: 8px;
        border: 1px solid #ffeaa7;
        font-size: 0.9rem;
    }
    .success-box {
        background-color: #d4edda;
        color: #155724;
        padding: 1rem;
        border-radius: 8px;
        border: 1px solid #c3e6cb;
    }
</style>
""", unsafe_allow_html=True)

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
            'title': title[:50],
            'content': clean_text[:2000],
            'url': url,
            'content_length': len(clean_text)
        }
    except Exception as e:
        return {
            'success': False,
            'error': str(e),
            'url': url
        }

def extract_pdf_content(file):
    """PDF file से content extract करें"""
    try:
        pdf_reader = PyPDF2.PdfReader(file)
        text = ""
        for page in pdf_reader.pages:
            text += page.extract_text() + "\n"
        
        return {
            'success': True,
            'content': text,
            'pages': len(pdf_reader.pages),
            'characters': len(text),
            'words': len(text.split())
        }
    except Exception as e:
        return {
            'success': False,
            'error': str(e)
        }

def extract_docx_content(file):
    """DOCX file से content extract करें"""
    try:
        doc = docx.Document(file)
        text = ""
        for paragraph in doc.paragraphs:
            text += paragraph.text + "\n"
        
        return {
            'success': True,
            'content': text,
            'paragraphs': len(doc.paragraphs),
            'characters': len(text),
            'words': len(text.split())
        }
    except Exception as e:
        return {
            'success': False,
            'error': str(e)
        }

def extract_csv_content(file):
    """CSV file से data extract करें"""
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
    """TXT file से content extract करें"""
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
    # Main header
    st.markdown('<h1 class="main-header">🔍 Content Analyzer Pro</h1>', unsafe_allow_html=True)
    st.markdown("**📱 Mobile & 💻 PC Friendly - URLs, PDF, DOCX, CSV, TXT Analyze करें**")
    
    # Mobile warning
    st.markdown("""
    <div class="mobile-warning">
        <strong>📱 Mobile Tips:</strong> 
        - Portrait mode में use करें<br>
        - Files upload के लिए cloud storage apps use कर सकते हैं
    </div>
    """, unsafe_allow_html=True)
    
    # Features grid - All file types
    st.markdown("### 🚀 Supported Formats")
    col1, col2, col3, col4, col5 = st.columns(5)
    
    with col1:
        st.markdown("""
        <div class="feature-card" style="text-align: center;">
            <h4>🌐 URLs</h4>
            <p>Web Scraping</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div class="feature-card" style="text-align: center;">
            <h4>📄 PDF</h4>
            <p>Text Extraction</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown("""
        <div class="feature-card" style="text-align: center;">
            <h4>📝 DOCX</h4>
            <p>Word Documents</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col4:
        st.markdown("""
        <div class="feature-card" style="text-align: center;">
            <h4>📊 CSV</h4>
            <p>Data Analysis</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col5:
        st.markdown("""
        <div class="feature-card" style="text-align: center;">
            <h4>📃 TXT</h4>
            <p>Text Analysis</p>
        </div>
        """, unsafe_allow_html=True)
    
    # Tabs for different features
    tab1, tab2 = st.tabs(["🌐 URL Scraping", "📁 File Analysis"])
    
    with tab1:
        st.header("URLs से Content Scrape करें")
        
        # Mobile-friendly URL input
        url_input = st.text_area(
            "🌐 URLs डालें (एक line में एक URL)",
            placeholder="https://example.com\nhttps://example.org",
            height=80,
            help="एक बार में multiple URLs"
        )
        
        col1, col2 = st.columns([3, 1])
        with col1:
            if st.button("🚀 Scrape URLs", type="primary", use_container_width=True):
                if url_input:
                    urls = [url.strip() for url in url_input.split('\n') if url.strip()]
                    
                    if urls:
                        progress_bar = st.progress(0)
                        status_text = st.empty()
                        
                        for i, url in enumerate(urls):
                            status_text.text(f"Scraping: {url[:30]}...")
                            result = simple_scrape_website(url)
                            
                            if result['success']:
                                with st.expander(f"✅ {result['title']}", expanded=False):
                                    st.write(f"**URL:** {result['url']}")
                                    st.write(f"**Content Length:** {result['content_length']} characters")
                                    st.text_area("Preview", result['content'][:300] + "...", 
                                               height=100, key=f"preview_{i}")
                                    
                                    st.download_button(
                                        label="📥 Download",
                                        data=result['content'],
                                        file_name=f"scraped_{i+1}.txt",
                                        mime="text/plain",
                                        use_container_width=True,
                                        key=f"dl_{i}"
                                    )
                            else:
                                st.error(f"❌ {url[:30]}... - {result['error']}")
                            
                            progress_bar.progress((i + 1) / len(urls))
                        
                        status_text.text("✅ Completed!")
                else:
                    st.warning("⚠️ Please enter URLs")
        
        with col2:
            if st.button("🔄 Clear", use_container_width=True):
                st.rerun()
    
    with tab2:
        st.header("Files Upload और Analyze करें")
        
        # All file types uploader
        uploaded_files = st.file_uploader(
            "📁 Files चुनें (PDF, DOCX, CSV, TXT)",
            type=['pdf', 'docx', 'csv', 'txt'],
            accept_multiple_files=True,
            help="सभी format supported: PDF, Word, CSV, Text"
        )
        
        if uploaded_files:
            st.markdown(f'<div class="success-box">✅ {len(uploaded_files)} file(s) uploaded!</div>', unsafe_allow_html=True)
            
            for file in uploaded_files:
                # File type badge
                file_type_badge = f'<span class="file-type-badge">{file.type}</span>'
                st.markdown(file_type_badge, unsafe_allow_html=True)
                
                with st.expander(f"📄 {file.name}", expanded=True):
                    col1, col2 = st.columns([1, 2])
                    
                    with col1:
                        st.write("**File Info:**")
                        st.write(f"Type: {file.type}")
                        st.write(f"Size: {file.size / 1024:.1f} KB")
                        
                        if st.button(f"Analyze {file.name}", key=file.name, use_container_width=True):
                            # PDF Files
                            if file.type == "application/pdf":
                                result = extract_pdf_content(file)
                                if result['success']:
                                    st.success("✅ PDF analysis completed!")
                                    st.write(f"**Pages:** {result['pages']}")
                                    st.write(f"**Characters:** {result['characters']}")
                                    st.write(f"**Words:** {result['words']}")
                                    
                                    st.text_area("Content Preview", result['content'][:500] + "...", 
                                               height=150, key=f"pdf_{file.name}")
                                    
                                    st.download_button(
                                        label="📥 Download PDF Text",
                                        data=result['content'],
                                        file_name=f"{file.name}_extracted.txt",
                                        mime="text/plain",
                                        use_container_width=True
                                    )
                                else:
                                    st.error(f"❌ PDF Error: {result['error']}")
                            
                            # DOCX Files
                            elif file.type == "application/vnd.openxmlformats-officedocument.wordprocessingml.document":
                                result = extract_docx_content(file)
                                if result['success']:
                                    st.success("✅ DOCX analysis completed!")
                                    st.write(f"**Paragraphs:** {result['paragraphs']}")
                                    st.write(f"**Characters:** {result['characters']}")
                                    st.write(f"**Words:** {result['words']}")
                                    
                                    st.text_area("Content Preview", result['content'][:500] + "...", 
                                               height=150, key=f"docx_{file.name}")
                                    
                                    st.download_button(
                                        label="📥 Download DOCX Text",
                                        data=result['content'],
                                        file_name=f"{file.name}_extracted.txt",
                                        mime="text/plain",
                                        use_container_width=True
                                    )
                                else:
                                    st.error(f"❌ DOCX Error: {result['error']}")
                            
                            # CSV Files
                            elif file.type == "text/csv":
                                result = extract_csv_content(file)
                                if result['success']:
                                    st.success("✅ CSV analysis completed!")
                                    st.write(f"**Rows:** {result['rows']}")
                                    st.write(f"**Columns:** {result['columns']}")
                                    st.write(f"**Columns:** {', '.join(result['column_names'])}")
                                    
                                    st.dataframe(result['dataframe'].head(8), use_container_width=True)
                                    
                                    csv_data = result['dataframe'].to_csv(index=False)
                                    st.download_button(
                                        label="📥 Download Processed CSV",
                                        data=csv_data,
                                        file_name=f"analyzed_{file.name}",
                                        mime="text/csv",
                                        use_container_width=True
                                    )
                                else:
                                    st.error(f"❌ CSV Error: {result['error']}")
                            
                            # TXT Files
                            elif file.type == "text/plain":
                                result = extract_txt_content(file)
                                if result['success']:
                                    st.success("✅ Text analysis completed!")
                                    st.write(f"**Characters:** {result['characters']}")
                                    st.write(f"**Words:** {result['words']}")
                                    st.write(f"**Lines:** {result['lines']}")
                                    
                                    st.text_area("Content Preview", result['content'][:500] + "...", 
                                               height=150, key=f"txt_{file.name}")
                                    
                                    st.download_button(
                                        label="📥 Download Text",
                                        data=result['content'],
                                        file_name=f"analyzed_{file.name}",
                                        mime="text/plain",
                                        use_container_width=True
                                    )
                                else:
                                    st.error(f"❌ Text Error: {result['error']}")
                    
                    with col2:
                        st.info("ℹ️ Analyze बटन पर क्लिक करें")
        
        else:
            st.info("👉 PDF, DOCX, CSV, TXT files upload करने के लिए click करें")
    
    # Footer
    st.markdown("---")
    st.markdown("""
    <div style='text-align: center; color: #666; font-size: 0.9rem;'>
        <p>📱 <strong>Mobile & PC Compatible</strong> - All Formats Supported</p>
        <p>🌐 URLs • 📄 PDF • 📝 DOCX • 📊 CSV • 📃 TXT</p>
    </div>
    """, unsafe_allow_html=True)

if __name__ == "__main__":
    main()
