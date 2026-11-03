# Kredi Kartı Dolandırıcılık Tespiti

## Problem
Günümüzde dijital bankacılık ve online alışverişlerin artmasıyla birlikte finansal dolandırıcılık vakaları da hızla artmaktadır. Kredi kartı sahiplerinin bilgileri dışında yapılan hileli işlemler hem bireysel kullanıcılar hem de finansal kurumlar için büyük maddi kayıplara ve güvenlik açıklarına yol açmaktadır. Manuel olarak milyonlarca işlemi anlık incelemek imkansızdır; bu durum otomatik ve hızlı bir tespit mekanizmasına duyulan ihtiyacı ortaya koymaktadır.

## Hedef Kullanıcı
* Bankalar ve finansal kuruluşların risk yönetimi ve güvenlik birimleri

* E-ticaret platformlarının sahtekarlık önleme ekipleri

* Kredi kartı kullanıcılarının güvenliğini sağlamakla sorumlu yazılım sistemleri

## Proje Amacı
Bu projenin amacı, gerçekleştirilen bir finansal işlemin hileli olup olmadığını makine öğrenmesi algoritmaları kullanarak otomatik olarak tespit edebilen, güvenilir ve modüler bir yazılım altyapısı geliştirmektir. Projede Logistic Regression, Decision Tree ve Random Forest Regression yöntemleri kullanılarak modellerin başarımları karşılaştırılacaktır.

## Kapsam
* Kaggle üzerindeki Credit Card Fraud Dataset veri setinin incelenmesi ve veri analizi yapılması

* Dengesiz veri seti problemi için gerekli ön işleme adımlarının uygulanması

* Logistic Regression, Decision Tree ve Random Forest modellerinin eğitilmesi ve test edilmesi

* Model performanslarının sadece Accuracy metriğiyle değil de Precision, Recall, F1-Score ve ROC-AUC metrikleriyle değerlendirilmesi

* Modellerin her biriyle uygulamalar yapılıp performanslarının ve başarı oranlarının karşılaştırılması, raporlanması

* Modüler bir yazılım mimarisi (src/, notebooks/, data/) oluşturulması

## Kapsam Dışı
* Derin öğrenme (Deep Learning / Neural Networks) veya XGBoost, LightGBM gibi ileri düzey topluluk (ensemble) algoritmalarının bu aşamada projeye dahil edilmesi

* Gerçek zamanlı canlı bir API entegrasyonunun yapılması

## Proje Arayüz
<img width="2880" height="1618" alt="PROJEARAYUZ" src="https://github.com/user-attachments/assets/8b828a1b-30da-4f70-9380-44f2236ca111" />

## Diyagramlar ve iş dağılımları
[📄 Proje Konu Dağılımı (PDF)](./IMG_0561.JPG)

[📄 Sistem Akışı (PDF)](./IMG_0562.JPG)

[📄 Olay Diyagramı (PDF)](./IMG_0563.JPG)


## Ekip ve Roller  
* Çevik proje geliştirme yönteminin prensiplerine uygun olacak şekilde her ekip üyesi projenin her aşamasında aktif rol oynamaktadır. Projedeki temel sorumluluk alanları ise aşağıda açıklandığı şekilde dağıtılmıştır.

* **Naz ([@Th3BourbonKid]) - Dokümentasyon Sorumlusu & İş Analisti**
Literatür taramasının yönetilmesi, proje dokümantasyonunun oluşturulması, proje gereksinimlerinin belirlenmesi, proje ara raporlarının ve final raporunun hazırlanması, diyagramların oluşturulması.

* **Kerem ([@kerem-vi]) - Yazılımcı & Test Uzmanı**
Logistic Regression, Decision Tree ve Random Forest modellerinin kodlanması, model eğitimlerinin ve parametre optimizasyonlarının yapılması.
Model başarı metriklerinin ölçülmesi, modeller arası karşılaştırmalar yapılıp belgelenmesi, hata analizleri.

* **Kaan ([@kaanardakaba]) - Süreç Yöneticisi & Veri Analisti**
Proje Kanban panosunun ve iş akışının yönetilmesi, README dosyasının güncel tutulması, repo düzeni, veri setinin incelenmesi ve keşifsel veri analizi, gerekli ön işleme adımlarının uygulanması.





