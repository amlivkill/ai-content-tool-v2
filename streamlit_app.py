import streamlit as st
import pandas as pd
import requests
import re

# Mobile-friendly page config
st.set_page_config(
    page_title="Content Analyzer",
    page_icon="🔍",
    layout="wide",
    initial_sidebar_state="collapsed"  # Mobile के लिए better
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
    .tab-content {
        padding: 0.5rem;
    }
</style>
""", unsafe_allow_html=True)

def simple_scrape_website(url):
    """BeautifulSoup के बिना simple website scraping"""
    try:
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
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
            'title': title[:50],  # Mobile के लिए short title
            'content': clean_text[:2000],  # Mobile के लिए less content
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
    # Main header
    st.markdown('<h1 class="main-header">🔍 Content Analyzer</h1>', unsafe_allow_html=True)
    st.markdown("**📱 Mobile & 💻 PC Friendly - URLs और Files Analyze करें**")
    
    # Mobile warning
    st.markdown("""
    <div class="mobile-warning">
        <strong>📱 Mobile Tips:</strong> 
        - Portrait mode में use करें<br>
        - Files upload के लिए cloud storage apps use कर सकते हैं
    </div>
    """, unsafe_allow_html=True)
    
    # Features grid - Mobile responsive
    st.markdown("### 🚀 Features")
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("""
        <div class="feature-card">
            <h4>🌐 URL Scraping</h4>
            <p>Websites से content निकालें</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div class="feature-card">
            <h4>📊 CSV Analysis</h4>
            <p>Data preview और stats</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown("""
        <div class="feature-card">
            <h4>📝 Text Analysis</h4>
            <p>Word count और analysis</p>
        </div>
        """, unsafe_allow_html=True)
    
    # Tabs for different features - Mobile friendly
    tab1, tab2 = st.tabs(["🌐 URL Scraping", "📁 File Analysis"])
    
    with tab1:
        st.markdown('<div class="tab-content">', unsafe_allow_html=True)
        st.header("URLs से Content Scrape करें")
        
        # Mobile-friendly URL input
        url_input = st.text_area(
            "🌐 URLs डालें (एक line में एक URL)",
            placeholder="https://example.com\nhttps://example.org",
            height=80,  # Mobile के लिए compact
            help="एक बार में multiple URLs"
        )
        
        # Mobile-friendly button
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
                                    st.write(f"**Content:** {result['content_length']} chars")
                                    st.text_area("Preview", result['content'][:300] + "...", 
                                               height=100, key=f"preview_{i}")
                                    
                                    # Mobile-friendly download button
                                    st.download_button(
                                        label="📥 Download",
                                        data=result['content'],
                                        file_name=f"scraped_{i+1}.txt",
                                        mime="text/plain",
                                        use_container_width=True,
                                        key=f"dl_{i}"
                                    )
                            else:
                                st.error(f"❌ {url[:30]}...")
                            
                            progress_bar.progress((i + 1) / len(urls))
                        
                        status_text.text("✅ Completed!")
                else:
                    st.warning("⚠️ Please enter URLs")
        
        with col2:
            if st.button("🔄 Clear", use_container_width=True):
                st.rerun()
        
        st.markdown('</div>', unsafe_allow_html=True)
    
    with tab2:
        st.markdown('<div class="tab-content">', unsafe_allow_html=True)
        st.header("Files Upload और Analyze करें")
        
        # Mobile-friendly file uploader
        uploaded_files = st.file_uploader(
            "📁 CSV or TXT files चुनें",
            type=['csv', 'txt'],
            accept_multiple_files=True,
            help="Mobile से cloud storage से files upload कर सकते हैं"
        )
        
        if uploaded_files:
            st.markdown(f'<div class="success-box">✅ {len(uploaded_files)} file(s) uploaded!</div>', unsafe_allow_html=True)
            
            for file in uploaded_files:
                with st.expander(f"📄 {file.name}", expanded=True):
                    # Mobile-friendly columns
                    col1, col2 = st.columns([1, 2])
                    
                    with col1:
                        st.write("**File Info:**")
                        st.write(f"Type: {file.type}")
                        st.write(f"Size: {file.size / 1024:.1f} KB")
                        
                        # Mobile-friendly analyze button
                        if st.button(f"Analyze {file.name}", key=file.name, use_container_width=True):
                            # CSV File Analysis
                            if file.type == "text/csv":
                                try:
                                    df = pd.read_csv(file)
                                    
                                    st.success("✅ CSV analysis completed!")
                                    st.write(f"**Rows:** {len(df)}")
                                    st.write(f"**Columns:** {len(df.columns)}")
                                    
                                    # Mobile-friendly data preview
                                    st.write("**Preview:**")
                                    st.dataframe(df.head(5), use_container_width=True)
                                    
                                    # Download button
                                    csv_data = df.to_csv(index=False)
                                    st.download_button(
                                        label="📥 Download CSV",
                                        data=csv_data,
                                        file_name=f"analyzed_{file.name}",
                                        mime="text/csv",
                                        use_container_width=True
                                    )
                                    
                                except Exception as e:
                                    st.error(f"❌ Error: {str(e)}")
                            
                            # TXT File Analysis
                            elif file.type == "text/plain":
                                try:
                                    content = file.read().decode("utf-8")
                                    
                                    st.success("✅ Text analysis completed!")
                                    st.write(f"**Characters:** {len(content)}")
                                    st.write(f"**Words:** {len(content.split())}")
                                    st.write(f"**Lines:** {len(content.splitlines())}")
                                    
                                    # Mobile-friendly content preview
                                    st.text_area("Content Preview", content[:500] + "..." if len(content) > 500 else content, 
                                               height=150, key=f"content_{file.name}")
                                    
                                    # Download button
                                    st.download_button(
                                        label="📥 Download Text",
                                        data=content,
                                        file_name=f"analyzed_{file.name}",
                                        mime="text/plain",
                                        use_container_width=True
                                    )
                                    
                                except Exception as e:
                                    st.error(f"❌ Error: {str(e)}")
                    
                    with col2:
                        st.info("ℹ️ Analyze बटन पर क्लिक करें")
        
        else:
            st.info("👉 Files upload करने के लिए click करें")
        
        st.markdown('</div>', unsafe_allow_html=True)
    
    # Footer
    st.markdown("---")
    st.markdown("""
    <div style='text-align: center; color: #666; font-size: 0.9rem;'>
        <p>📱 <strong>Mobile & PC Compatible</strong> - हर device पर smoothly work करेगा</p>
        <p>🔧 Built with Streamlit • Responsive Design</p>
    </div>
    """, unsafe_allow_html=True)

if __name__ == "__main__":
    main()
