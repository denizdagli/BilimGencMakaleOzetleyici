# BilimGenç Makale Özetleyici

**BilimGenç Makale Özetleyici** projesi, BilimGenç sitesindeki makalelerin içeriğini alarak metin özeti çıkaran ve kelime bulutu oluşturan bir web uygulamasıdır. Kullanıcılar, BilimGenç makale linkini girerek makalenin özetini alabilir, kelime bulutunu görüntüleyebilir ve özet dosyasını indirebilirler.

## Özellikler:
- **Makale Özeti Çıkarma:** Kullanıcılar, BilimGenç sitesindeki bir makale URL'sini girerek, makalenin özetini alabilirler.
- **Kelime Bulutu Oluşturma:** Makalenin metninden kelime bulutu oluşturulabilir.
- **Özet İndirme:** Kullanıcılar özetin bir `.txt` dosyası olarak bilgisayarlarına indirilmesini sağlayabilir.
- **Türkçe Destek:** Türkçe metinler üzerinde çalışır.

## Gerekli Kurulum

Projenin çalışabilmesi için aşağıdaki kütüphaneler gereklidir. Bunları kurmak için terminalde aşağıdaki komutu çalıştırabilirsiniz:

```bash
pip install -r requirements.txt
```
```bash
streamlit run app.py
```
Bu projeyi daha ayrıntılı incelemek isterseniz, [bu bağlantıya](https://github.com/denizdagli/BasicNewsSummary) göz atabilirsiniz. Colab üzerinde çalıştırılabilir IPython Notebook dosyasını içeren projeyi burada bulabilirsiniz.