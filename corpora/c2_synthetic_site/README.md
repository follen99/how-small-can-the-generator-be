# 🧪 TestSite Pro - Piattaforma di Test per Web Scraper

Sito web di controllo progettato per testare in modo professionale l'efficacia di web scraper, 
in particolare per sistemi RAG (Retrieval Augmented Generation).

## 📋 Ground Truth - Cosa Contiene Questo Sito

### Pagine Web (8 totali)
1. **index.html** - Homepage con contenuti dinamici, accordion, tab, lazy loading, tabelle, modal
2. **company/pricing.html** - Listino prezzi con toggle fatturazione (Livello 2)
3. **company/careers.html** - Offerte di lavoro con lazy loading (Livello 2)
4. **company/case-studies.html** - Casi di successo con filtri dinamici (Livello 2)
5. **tech/stack.html** - Stack tecnologico (Livello 2)
6. **tech/api.html** - Documentazione API (Livello 2)
7. **resources/blog.html** - Blog tecnico con tabelle dati (Livello 2)
8. **resources/webinars.html** - Webinar passati (Livello 2)

### Documenti PDF (5 totali)
1. `whitepaper-ai-2024.pdf` - Whitepaper 24 pagine
2. `case-study-finance.pdf` - Case study 12 pagine
3. `guida-implementazione-rag.pdf` - Guida tecnica 45 pagine
4. `brochure-servizi.pdf` - Brochure 8 pagine
5. `condizioni-commerciali.pdf` - Listino prezzi 6 pagine

### Elementi Dinamici da Testare

#### 1. Accordion (3 sezioni)
- Consulenza AI Strategica
- Sviluppo Chatbot Avanzati
- Automazione Processi (RPA)

**Test:** Lo scraper deve espandere tutti gli accordion per catturare il contenuto.

#### 2. Tab Dinamici (3 tab)
- Finanza (FinAlytics Pro)
- Sanità (MediScan AI)
- Retail (RetailMind)

**Test:** Lo scraper deve catturare il contenuto di TUTTI i tab, non solo quello attivo.

#### 3. Lazy Loading (2s delay)
- Testimonial clienti caricati via JavaScript dopo 2 secondi

**Test:** Lo scraper deve aspettare il caricamento o espandere il contenuto.

#### 4. Contenuto Interattivo
- Informazioni di contatto nascoste in un modal

**Test:** Richiede simulazione di click per essere rivelato.

#### 5. Tabelle Dati
- Performance aziendali 2020-2024
- Confronto Vector DB

**Test:** I dati tabellari devono essere preservati in formato leggibile.

## 🚀 Come Usare

### 1. Avvia il Server di Test
```bash
cd test_website
python server.py
```

Il sito sarà disponibile su `http://localhost:8000`

### 2. Configura lo Scraper
Modifica `src/config.py`:
```python
START_URL = "http://localhost:8000"
MAX_DEPTH = 2
```

### 3. Esegui lo Scraper
```bash
python main.py
```

### 4. Valida i Risultati
Controlla la cartella `knowledge_base/`:

```bash
# Conta i file markdown generati
ls -la knowledge_base/markdown/ | wc -l
# Atteso: 5 file

# Conta i PDF scaricati
ls -la knowledge_base/docs/ | wc -l
# Atteso: 5 file

# Verifica contenuto
head -50 knowledge_base/markdown/openandeat_on_render_com_index.md
```

## ✅ Checklist di Validazione Completa

### Quantitativo
- [ ] 5 file markdown generati (una per pagina)
- [ ] 5 PDF scaricati in `docs/`
- [ ] Nessun errore nel log
- [ ] Crawling completato senza timeout

### Qualitativo - Contenuto
- [ ] **Metadati:** Ogni file .md contiene URL e Title
- [ ] **Info Azienda:** Nome, PIVA, sede, dipendenti presenti
- [ ] **Accordion:** Tutti e 3 i servizi con dettagli completi
- [ ] **Tab:** Contenuto Finanza, Sanità E Retail presente
- [ ] **Testimonial:** Citazioni clienti presenti (se supportato)
- [ ] **Tabelle:** Dati 2020-2024 leggibili

### Qualitativo - Pulizia
- [ ] Nessun "Menu", "Cerca", "Torna su" nel testo
- [ ] Nessun footer/header nel contenuto
- [ ] Link rimossi (se IGNORE_LINKS = True) o formattati correttamente
- [ ] No linee vuote eccessive (>2 consecutive)

## 🔧 Modalità di Testing Alternative

### 1. Testing con Siti Reali (Controllo Limitato)
```python
# Siti con contenuto dinamico noto
START_URL = "https://quotes.toscrape.com/js/"  # JS-rendered quotes
START_URL = "https://angular.io/docs"          # Angular docs
START_URL = "https://react.dev/learn"          # React docs
```

**Pro:** Test su casi reali
**Contro:** Ground truth non noto a priori

### 2. Testing con Wayback Machine
```python
# Usa snapshot storici dove conosci il contenuto
START_URL = "https://webcache.googleusercontent.com/search?q=..."
```

### 3. Testing Differenziale
```python
# Confronta output del tuo scraper vs libreria di riferimento
# Es: confronta con scrapy + playwright vs il tuo crawler
```

### 4. Testing Property-Based
```python
# Genera pagine HTML random con contenuto noto
# Verifica che lo scraper preservi sempre certe proprietà
# Es: "se c'è un <h1>, deve essere nel markdown"
```

### 5. Testing con Headless Browser di Riferimento
```python
# Usa Playwright direttamente per estrarre il "ground truth"
# poi confronta con il tuo crawler
```

## 📊 Metriche di Valutazione

### Recall Contenuto
```
Recall = (Contenuto estratto rilevante / Contenuto totale rilevante) * 100
Target: > 95%
```

### Precisione Pulizia
```
Precision = (Contenuto utile / Contenuto totale estratto) * 100
Target: > 90% (poco noise)
```

### Completezza Link
```
Link Coverage = (Link seguiti / Link totali validi) * 100
Target: 100% (dentro MAX_DEPTH)
```

## 🐛 Problemi Noti da Verificare

1. **Accordion non espansi:** Se lo scraper non simula click, perde il contenuto
2. **Tab inattivi:** Solo il tab attivo è nel DOM, gli altri sono nascosti
3. **Lazy loading:** Contenuto caricato dopo scroll/interazione
4. **Infinite scroll:** Alcuni siti caricano contenuto allo scroll
5. **PDF link:** Alcuni link PDF sono intercettati da JS e non sono href diretti

## 📝 Note Tecniche

- Il sito usa solo vanilla JS (no framework) per massima compatibilità
- I PDF sono file PDF validi (minimale ma struttura corretta)
- Tutti i link sono relativi per funzionare su qualsiasi dominio
- Il design è responsive ma testato principalmente per desktop

---

**Creato per:** rag_scraper_v2  
**Data:** 2024  
**Versione:** 1.0
