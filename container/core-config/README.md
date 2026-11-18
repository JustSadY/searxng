# SearXNG Deep — Torrent / Derin Bilgi / Veri Kurulumu

Bu klasördeki `settings.yml`, tüm varsayılan SearXNG motorlarını devre dışı
bırakıp yalnızca torrent, derin araştırma ve veri odaklı motorları etkinleştirir.

## Çalıştırma

```sh
cd container
docker compose up -d
```

Arayüz: <http://127.0.0.1:8080>

Durdurma:

```sh
cd container
docker compose down
```

Loglar:

```sh
cd container
docker compose logs -f core
```

## Nasıl çalışıyor?

`settings.yml` içindeki şu bölüm varsayılan motorların hiçbirini yüklemez:

```yaml
use_default_settings:
  engines:
    keep_only: []
```

Dosyanın altındaki `engines:` listesi ise aranan yeni motorları tanımlar.
İkisi (`annas archive` ve `open canada`) hariç hepsi `disabled: false`
olduğu için açılışta etkindir: 41 etkin motor.

## Etkin motorlar

### Torrent / dosya

| Motor | Ne yapar |
| --- | --- |
| `kickass` | KickassTorrents |
| `piratebay` | The Pirate Bay (apibay API) |
| `bt4g` | BT4G magnet/torrent meta araması |
| `torrents-csv` | Torrents-CSV magnet arşivi |
| `nyaa` | Anime/medya torrentleri |
| `annas archive` | Kitap, makale ve doküman arşivi (varsayılan kapalı, DDoS-Guard) |

### Derin bilgi / akademik

| Motor | Ne yapar |
| --- | --- |
| `arxiv` | Bilimsel ön baskılar |
| `crossref` | DOI / akademik yayın meta verisi |
| `openalex` | Akademik çalışma ve yazar verisi |
| `semantic scholar` | Akademik makale araması |
| `pubmed` | Biyomedikal literatür |
| `europepmc` | Avrupa biyomedikal literatürü |
| `openlibrary` | Açık kütüphane / kitaplar |
| `wikidata` | Yapılandırılmış bilgi grafiği |
| `wikipedia` | Ansiklopedi |
| `boardreader` | Forum ve topluluk gönderileri |
| `crowdview` | Forum gönderileri |
| `openaire` | Avrupa açık bilim grafiği: yayın, veri ve yazılım |
| `clinicaltrials` | Küresel klinik araştırma kayıtları |
| `hal` | Fransız açık akademik arşivi |

### Haber / olay verisi

| Motor | Ne yapar |
| --- | --- |
| `gdelt` | Küresel haber ve olay veritabanı (5 saniyede bir istek sınırı) |

### Veri / veri seti

| Motor | Ne yapar |
| --- | --- |
| `internet archive` | Archive.org içerik araması |
| `datacite` | Araştırma verisi DOI'leri |
| `zenodo` | Açık araştırma verisi ve yazılım kayıtları |
| `gbif` | Biyoçeşitlilik veri setleri |
| `figshare` | Araştırma verisi ve makale ekleri |
| `huggingface datasets` | Hugging Face veri setleri |
| `harvard dataverse` | Harvard araştırma veri setleri |
| `dryad` | Küratörlü araştırma verileri |
| `data.gov.uk` | İngiltere açık veri kataloğu (CKAN) |
| `data.gov.au` | Avustralya açık veri kataloğu (CKAN) |
| `data.gov.ie` | İrlanda açık veri kataloğu |
| `openml` | Makine öğrenmesi veri setleri |
| `pdbe` | Protein veri bankası |
| `national vulnerability database` | CVE / güvenlik açığı verisi |

### Şirket sicili / kamu kayıtları

| Motor | Ne yapar |
| --- | --- |
| `gleif` | Global LEI / tüzel kişi kayıtları |
| `sec edgar` | ABD SEC şirket ve dosyalama araması |
| `uk companies house` | İngiltere resmi şirket sicili |
| `brreg` | Norveç resmi şirket sicili |
| `prh` | Finlandiya resmi şirket sicili (YTJ) |
| `federal register` | ABD Federal Register resmî belgeleri |
| `photon` | OpenStreetMap adres/konum araması |

## Yeni motor ekleme

### Mevcut bir SearXNG motorunu açma

`searx/engines/` altında hazır bir motor varsa `engines:` listesine ekleyin:

```yaml
  - name: ornek
    engine: ornek
    shortcut: ornk
    categories: [general]
    disabled: false
```

### JSON API motoru ekleme

Python kodu yazmadan `json_engine` ile yeni bir API bağlanabilir:

```yaml
  - name: ornek api
    engine: json_engine
    shortcut: oapi
    categories: [data]
    paging: true
    page_size: 20
    first_page_num: 1
    search_url: https://api.example.com/search?q={query}&page={pageno}
    results_query: results
    url_query: url
    title_query: title
    content_query: description
    disabled: false
```

Değişiklikten sonra:

```sh
cd container
docker compose restart core
```

## İsteğe bağlı / ek kurulum gerektiren motorlar

Aşağıdakiler bilinçli olarak kapalı bırakıldı:

- **annas archive**: Tüm aynalar arama isteklerine DDoS-Guard JS korumasıyla
  `403` dönüyor. Motor `settings.yml` içinde tanımlı ama `disabled: true`;
  proxy/bot koruması aşılabilen bir ortamda açılabilir.
- **open canada**: Kanada açık veri CKAN API'si zaman zaman 20-30 saniye
  yanıt vermiyor. Bu, SearXNG'nin genel istek sınırını doldurduğu için motor
  şu an `disabled: true`; API düzeldiğinde açılabilir.
- **1337x, solidtorrents/bitsearch, tokyotoshokan, findfiles**: Cloudflare
  koruması nedeniyle doğrudan isteklerde "Just a moment..." sayfası dönüyor.
  Bir HTTP proxy tanımlarsanız `outgoing.proxies` altına ekleyip motoru
  açabilirsiniz.
- **btdigg**: `btdig.com` bu ağdan yanıt vermiyor.
- **core.ac.uk**: API anahtarı gerekiyor.
- **z-library**: motor şu anda `inactive` (upstream kaynaklı sorun).
- **ahmia**: Tor proxy gerektirir (`outgoing.using_tor_proxy: true`).
- **torznab**: Jackett/Prowlarr gibi bir indexer gerektirir.
- **elasticsearch, meilisearch, solr, postgresql, mysql, mongodb, sqlite,
  recoll**: kendi verinizi aramak için ilgili veritabanı bağlantısı gerekir.
- **marginalia**: API anahtarı gerektirir.

## Notlar

- Arayüz yalnızca `127.0.0.1:8080` adresine bağlıdır. Ağdaki başka cihazlardan
  erişmek için `container/.env` içindeki `SEARXNG_HOST` değerini `0.0.0.0`
  yapın.
- `container/.env` gizli anahtar içerdiği için `.gitignore`'a eklendi.
- JSON API: `http://127.0.0.1:8080/search?q=ubuntu&format=json`
- Kategoriyle arama: `...&categories=files`, `...&categories=science`,
  `...&categories=data`

### Bilinen durumlar

- **PubMed**: PubMed HTTP/2 üzerinden bot koruması sayfası döndürüyor. Bu
  yüzden `outgoing.networks.pubmed_http1` tanımlı ve `pubmed` motoru bu ağı
  kullanıyor; HTTP/1.1 ile normal sonuçlar geliyor.
- **Anna's Archive**: `.vg` aynası başka bir alan adına ait SSL sertifikası
  sunuyor; `.gl`, `.pk` ve `.gd` aynaları ise aramada DDoS-Guard JS koruması
  nedeniyle `403` dönüyor. Bu yüzden motor varsayılan olarak kapalı.
- **Crossref / OpenAlex**: API anahtarsız ortak havuzda zaman zaman `429 Too
  Many Requests` dönebilir. Kalıcı çözüm için kendi API anahtarınızı/proxy'nizi
  tanımlayın.
- **Europe PMC**: zaman zaman `503` döndürebilir; upstream kaynaklı geçici bir
  durumdur.
- **BT4G**: zaman zaman 8 saniyelik zaman aşımına uğrayabilir; tekrar denemek
  yeterlidir.
- **Hugging Face datasets**: API varsayılan olarak çok sayıda (1000'e kadar)
  sonuç döndürür. `it` kategorisinde sonuç sayısı bu yüzden yüksek olabilir.
- **Otomatik tamamlama**: Varsayılan DuckDuckGo motoru kaldırıldığı için
  `autocomplete: "wikipedia"` kullanılıyor.
- **GLEIF / SEC EDGAR / UK Companies House / Brreg / PRH**: Yalnızca herkese
  açık şirket ve tüzel kişi kayıtlarını arar; kişisel veri veya kapalı sicil
  erişimi yoktur. SEC EDGAR tarayıcı User-Agent'ı ister, bu ayar `settings.yml`
  içinde tanımlı. UK Companies House HTML tabanlı olduğu için site yapısı
  değişirse kırılabilir.
- **data.gov.uk**: `data.gov.uk` istekleri CKAN sunucusuna yönlendirdiği için
  motor doğrudan `ckan.publishing.service.gov.uk` adresini kullanır.
- **data.gov.au**: CKAN `start` parametresi sayfa başına 20 kayıtla ilerler.
- **data.gov.ie**: CKAN API'sindeki iç içe `organization.title` alanı veri seti
  başlığıyla karıştığı için motor HTML arama sayfasını okur. Site yapısı
  değişirse `results_xpath`/`title_xpath` güncellenmelidir.
- **federal register**: Herkese açık API, anahtar gerektirmez; ABD federal
  kuralları, bildirimleri ve başkanlık belgelerini arar.
- **clinicaltrials**: API sayfa numarası yerine `pageToken` kullanıyor; bu
  yüzden motor tek seferde 20 sonuç getirir ve sayfalama kapalıdır.
- **hal**: Fransız açık akademik arşivi; `start` parametresiyle 20'lik sayfalar
  halinde ilerler.
- **brreg**: Norveç şirket sicili; `page` parametresi 0 tabanlıdır ve sayfa
  başına 20 kayıt gelir.
- **prh**: Finlandiya YTJ sicili; API yaklaşık 100 sonuçla sınırlı ve kullanışlı
  bir sonuç sayısı parametresi yok. Bu yüzden sayfalama kapalı; eski/geçmiş
  şirket adları da eşleşebilir.
- **openml**: Yalnızca veri seti adına göre arama yapar; tam metin araması
  değildir. Sonuç açıklaması yerine veri formatı (ör. `ARFF`) gösterilir.
  Eşleşme yoksa API `412` döner; bu durum boş sonuç olarak kabul edilir.
- **GDELT**: Genel API 5 saniyede bir isteğe izin verir. Hızlı ardışık aramalarda
  `429 Too Many Requests` normaldir; motor 25 saniye bekleyecek şekilde ayarlı
  ve `429` yanıtı boş sonuç sayılıyor, böylece motor bir saat askıya alınmıyor.
- **DOAJ / EU Open Data Portal**: Denendi; `json_engine` iç içe `title`
  alanlarını yanlış eşlediği için şimdilik etkin değil. Bu kaynaklar OpenAIRE ve
  data.gov.uk üzerinden dolaylı olarak kapsanıyor.
