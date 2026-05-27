# ﴾ QuranBot ﴿
---
## ⏾ Genel Görünüm
<br /> بسم الله الرحمن الرحيم

Bu benim kutsal İslami metinleri göstermek amaçlı yaptığım discord.py tabanlı, açık kaynak bir Discord botudur. <br />
Bu sayede Discord kullanırken kutsal İslami metinlere ulaşım daha kolay olur. <br />
Python dilinde yazılmıştır ve Docker'ı destekler. <br />
Ve kullanım kolaylığı mı? Kurması o kadar kolay ki, kurduğunuzu bile unutabilirsiniz! <br />

Bu projeyi yapmamın sebepleri arasında bunlar var:

Osman (r.a) tarafından rivayet edildiğine göre, Hz. Peygamber (ﷺ) şöyle dedi:
>"Aranızda en iyi olanlar Kur'ân'ı öğrenenler ve öğretenlerdir."
(Sâhîh-i Buhâri 5027, kitap-içi referans: Kitap 66, Hadis 49)

Ebû Hüreyre (r.a) tarafından rivayet edildiğine göre, Hz. Peygamber (ﷺ) şöyle dedi:
>"Bir adam vefat ettiğinde, onun amelleri, şu üçü hariç, sona erir: Tekrarlayan sadaka, veya (insanların) faydalandığı ilim, ya da onun için dua eden dindar bir çocuk."
(Sâhîh-i Müslim 1631, kitap-içi referans: Kitap 25, Hadis 20)

Ebû Hüreyre (r.a) tarafından rivayet edildiğine göre, Allah'ın Resûlü (ﷺ) dedi ki:
>"İnsanları doğru yola çağıranın, doğru yolda kalanlarınki gibi bir mükafatı vardır; onların mükafatları hiçbir şekilde eksiltilmez. İnsanları sapıklığa çağıranın ise, sapıklığı işleyenlerin günahları gibi onun günahının yükünü taşıması gerekir; onların günahları hiçbir şekilde eksiltilmez."
(Sâhîh-i Müslim 2674, kitap-içi referans: Kitap 47, Hadis 30)

>Not: Bu hadisler Sunnah.com'daki İngilizce çeviriden Türkçe'ye çevrilmiştir, çeviride hata olabilir.
---
## ⏾ Öne Çıkan Noktalar
### Özellikler ve uygulanması gereken şeyler:

||||
| ------------ | ------------ | ------------ |
| ✓ - Çalışıyor/Eklendi/Destekleniyor | / - Henüz Tamamlanmadı  | x - Desteklenmiyor/Eklenmedi  |

|||
| ------------ | ------------ |
| Kur'ân-ı Kerim ayetlerini gösteren bir komut. | ✓  |
| Uygulama Docker-ize edildi. | ✓  |
| Uv Paket Yöneticisi'ne taşınıldı. | ✓  |
| Muhabbet yerinde kullanılabilen, Kur'ânı Kerim ayetlerini gösteren komutlar. | ✓  |
| Belirli bir kanalda günlük Kur'ân-ı Kerim ayetleri gösterebilme özelliği. | /  |
| Uygulamayı pytest ile test edebilme yolu. | /  |
| Kur'ân-ı Kerim SQLite veritabanı. | x  |
| Botun özel sözü periyodik bir şekilde listeden seçilen rastgele bir söze değişebilmesi. | x  |
| Hadis-i Şerif rivayetleri gösteren bir komut | x  |
| Tefsir gösteren bir komut. | x  |
| Namaz vakitlerini gösteren bir komut. | x  |

---
## ⏾ Özellikler
- `/help`: Diğer eğik çizgi komutlarının listesini gösteren bir komut.
- `/quran`: İki tamsayı tipi argümanını giriş olarak kabul eder, sûre ve ayet, kullanıcının girdiği değerlere göre bir Kur'ân-ı Kerim ayeti gösterir. (Örnek: `/quran chapter:2 verse:4` Bakara Sûresi, 4. ayetin içeriğini gösterecektir.)
---
## ⏾ Gereksinimler
Kendi QuranBot uygulamanızı çalıştırmak için şunlara ihtiyaç duyacaksınız:
- [Docker](https://www.docker.com/get-started/)
- [Python (Preferably version 3.11)](https://www.python.org/downloads/)
>Not: Docker kullanacaksanız Python'a çokta ihtiyaç duymayacaksınız.

Gereksinimler bu kadar.
---
## ⏾ Kurulum
## 1. Docker Kullanarak Kurulum:
### Kısa Talimatlar
- Botunuzu Discord Developer Portalı'ndan oluşturun
- Yetkilendirme belirtecini (yani auth tokenini) kopyalayın
- .env dosyanızı oluşturup .env.example'da anlatıldığına göre doldurun
- Bu terminal komutunu çalıştırın: `docker compose up`

Bu kadar.
### Detaylı Talimatlar:
Başlamadan önce, projenin kaynak kodunu yükleyin ve bir klasöre ayrıştırın, bu klasöre "kuranbot" gibi bir ad verebilirsiniz. <br />
İlk öncelikle yeni bir Discord uygulaması oluşturmanız lazım. <br />
[Discord Developer Portal](https://discord.com/developers/applications)'ına girin ve bot uygulamanızı oluşturun. <br />
Oluşturduktan sonra, botun Yetkilendirme Belirteci'ne (yani Authorization Token'ine) ihtiyaç duyucaksınız. <br />
Şuraya gidin: Uygulamalar -> Uygulaman -> Genel Bakış -> Bot <br />
![Belirteç Sıfırlama](assets/reset_token_location.png)
"Sıfırla" tuşuna basın, size botun belirtecini gösterecektir, onu kopyalayın. <br />
Klasörde bir ".env" dosyası oluşturun, bu dosyanın yapısı ".env.example"in yapısı ile uyuşmalı, ordaki talimatlara uyun, <br />
.env dosyasını sahip olduklarınıza göre doldurun, bu bir belirteç olabilir, PostgreSQL kullanıcı adı, şifresi olabilir vesaire vesaire. <br />
ya da .env.example.clean'deki değişkenlerin değerlerini istediğinize göre değiştirin sonra da dosyanın ismini ".env" yapın <br /> 
Sonra, terminalinizi açın, projenin kök klasörüne gidin, ve şu komutu çalıştırın: <br />

```bash
docker compose up
```
Bu uygulamayı kuracak, veritabanı oluştaracak be konteyneri çalıştaracaktır. <br />

Güvenli bir şekilde kapatmak için, şunu calıştırın:
```bash
docker compose down
```

Eğer uygulamayı hem kapatıp hem de kaydedilmiş veritaban verilerini silmek istiyorsanız, şunu çalıştırın: 
```bash
docker compose down -v
```
>Note: Lütfen bu komutu sorumluluk alarak çalıştırın, bu konteynerin gücünü kesecek VE hem de kaydedilmiş PostgreSQL verilerini silecektir.

Eğer herşeyi doğru yaptıysanız, botun durumunu çevrim içi olarak ve konteynırı çalışıyor olarak görüceksiniz.
## 2. Manuel Python Kurulumu:
### Kısa Talimatlar:
- Projenin kaynak kodunu yükleyin ve bir klasöre ayrıştırın.
- .env dosyanızı oluşturun ve doldurun.
- Önemli gereksinimleri yüklemek için `uv sync --frozen --no-dev` ya da `pip install -r requirements.txt` komutunu çalıştırın
- Şu komut ile uygulamayı çalıştırın: `python main.py`

Bu kadar.
### Detaylı Talimatlar:
- Botun belirtecini alın, not defterinize ya da herhangi gizli bir yere yazın.
- [Python](https://www.python.org/downloads/) versiyon 3.11'i yükleyin.
- Projenin kaynak kodunu yükleyin, eğer bir .zip dosyası olarak indirdiyseniz bir klasöre ayrıştırın ve klasöre "kuranbot" gibi bir isim verin.
- Bir .env dosyası oluşturun, bu dosyayı .env.example'de anlatıldığına göre doldurun (Docker kullanmayacaksanız Docker ile ilgili değişkenleri silebilirsiniz).
- Terminalinizi açın, kuranbot klasörünüzün içinde açtığınızdan emin olun.
- Uv paket yöneticisini kullanıyorsanız `uv sync --frozen --no-dev` komutunu çalıştırın ama requirements.txt kullanmayı tercih ediyorsanız `pip install -r requirements.txt` komutunu çalıştırın, bunları yapmadan önce tabii ki cihazınızda pip paket yöneticisinin yüklü olduğundan emin olun (Uv paket yöneticisini yüklemek isterseniz, ya `pip install uv` komutunu çalıştırın ya da cihazınızda pip yüklü değil ise [burayı ziyaret edin](https://docs.astral.sh/uv/getting-started/installation/)).
![Örnek](assets/manual_py_ins.png)
- `python main.py` komutunu çalıştırın ve bot çalışacaktır, durdurmak istediğinizde terminal içinde Ctrl+C tuş kombinasyonuna basın.
---
## ⏾ Geri Bildirim & İşbirliği:
Lütfen [burada](https://github.com/AzuritilDev/QuranBot/discussions) tartışmalara katılın ve hataları, yanlışları vb. deponun [sorunlar](https://github.com/AzuritilDev/QuranBot/issues) bölümünde bildirin. <br />

Lütfen [katkıda bulunma](CONTRIBUTING.md) ve [davranış kuralları](CODE_OF_CONDUCT.md) ile ilgili depo kılavuzunu inceleyin.
## ⏾ Yazarlar:
[@AzuritilDev](https://github.com/AzuritilDev)


Tutku ve iyi niyetle yapıldı, <br />
Ümmete hediye edildi ❤️
## ⏾ Lisans:
[MIT](LICENSE.md) lisansı altında dağıtılıyor.