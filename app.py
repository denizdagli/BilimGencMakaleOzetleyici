import streamlit as st
import requests
from bs4 import BeautifulSoup
import nltk
from nltk.corpus import stopwords
from nltk.tokenize import sent_tokenize, word_tokenize
from nltk.probability import FreqDist
from wordcloud import WordCloud
import yake
import base64
import matplotlib.pyplot as plt

# NLTK verilerini indir
nltk.download('punkt', quiet=True)
nltk.download('stopwords', quiet=True)
nltk.download('punkt_tab')

def fetch_article_content(url):
    """
    Verilen URL'den makale içeriğini çeker.
    """
    try:
        response = requests.get(url)
        soup = BeautifulSoup(response.text, "lxml")
        article_content = soup.find('div', {'class': 'article-detail-content'})
        
        if not article_content:
            article_content = soup.find(['div', 'article'], class_=['content', 'entry-content', 'post-content'])
        
        if article_content:
            paragraphs = article_content.find_all('p')
            text = " ".join(p.text.strip() for p in paragraphs if not p.find('img'))
            return text.strip()
        
        return "Makale içeriği çekilemedi."
    except Exception as e:
        return f"Hata oluştu: {str(e)}"

def summarize_text(text, sent_number=3):
    """
    Metni özetler.
    """
    if not text or len(text) < 100:
        return "Özetlenecek yeterli içerik bulunamadı."
    
    stop_words = set(stopwords.words('turkish'))
    sentences = sent_tokenize(text)
    
    if len(sentences) <= sent_number:
        return text
    
    words = word_tokenize(text.lower())
    filtered_words = [word for word in words if word.isalpha() and word.lower() not in stop_words]
    
    freq_dist = FreqDist(filtered_words)
    
    sentence_scores = {i: sum(freq_dist[word] for word in word_tokenize(sentences[i].lower()) if word in freq_dist) for i in range(len(sentences))}
    
    sorted_scores = sorted(sentence_scores.items(), key=lambda x: x[1], reverse=True)
    selected_indices = sorted([idx for idx, _ in sorted_scores[:sent_number]])
    
    return " ".join(sentences[i] for i in selected_indices)

def create_wordcloud(text):
    """
    Metinden kelime bulutu oluşturur.
    """
    stop_words = set(stopwords.words('turkish'))
    
    wordcloud = WordCloud(
        width=800, height=400, background_color='white',
        stopwords=stop_words, colormap='viridis', collocations=False, max_words=100
    ).generate(text)
    
    return wordcloud

def extract_keywords(text):
    """
    Metinden en önemli 10 anahtar kelimeyi çıkarır.
    """
    kw_extractor = yake.KeywordExtractor(lan="tr", n=1, top=10)
    keywords = kw_extractor.extract_keywords(text)
    return [kw[0] for kw in keywords]

def create_download_link(text, filename="makale_ozet.txt"):
    """
    Özeti indirilebilir bir bağlantıya dönüştürür.
    """
    b64 = base64.b64encode(text.encode()).decode()
    return f'<a href="data:file/txt;base64,{b64}" download="{filename}">Özeti indir 📥</a>'

def main():
    st.set_page_config(page_title="Bilim Genç Makale Özetleyici", page_icon="📚", layout="wide")
    
    st.title("Bilim Genç Makale Özetleyici")
    st.write("Bilim Genç sitesindeki bir makalenin linkini girerek özetini görebilir ve anahtar kelimelerini analiz edebilirsiniz.")
    
    article_url = st.text_input("Makale Linki", placeholder="Özetini almak istediğiniz Bilim Genç makalesinin linkini buraya girin.")
    summary_length = st.slider("Özet Uzunluğu (Cümle Sayısı)", 1, 10, 3)
    
    if st.button("Makaleyi Özetle"):
        if not article_url or not article_url.startswith("https://bilimgenc.tubitak.gov.tr"):
            st.error("Lütfen geçerli bir Bilim Genç makale linki girin.")
        else:
            with st.spinner("Makale içeriği çekiliyor..."):
                article_text = fetch_article_content(article_url)
                
                if "Hata oluştu" in article_text or "Makale içeriği çekilemedi" in article_text:
                    st.error(article_text)
                else:
                    st.success("Makale başarıyla çekildi.")
                    
                    with st.spinner("Makale özetleniyor..."):
                        summary = summarize_text(article_text, summary_length)
                        
                        col1, col2 = st.columns(2)
                        
                        with col1:
                            st.subheader("Makale İçeriği")
                            with st.expander("Tüm İçeriği Göster"):
                                st.write(article_text)
                        
                        with col2:
                            st.subheader("Makale Özeti")
                            st.write(summary)
                            
                            # Özeti indirme butonu
                            st.markdown(create_download_link(summary), unsafe_allow_html=True)
                        
                        # Anahtar kelimeler
                        st.subheader("Anahtar Kelimeler")
                        keywords = extract_keywords(article_text)
                        st.write(", ".join(keywords))
                        
                        # Kelime bulutu
                        st.subheader("Kelime Bulutu")
                        wordcloud = create_wordcloud(article_text)
                        
                        fig, ax = plt.subplots(figsize=(10, 6))
                        ax.imshow(wordcloud, interpolation='bilinear')
                        ax.axis('off')
                        st.pyplot(fig)

if __name__ == "__main__":
    main()
