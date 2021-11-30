# Natural_Language_Explanation_Movies
Sistema di raccomandazione di film che fornisce all'utente una spiegazione in merito alla raccomandazione ricevuta, realizzato per il lavoro di tesi di Nuzzachi. <br>

# explod-movies
All'interno della directory **explod-movies** sono presenti i file che costituiscono l'interfaccia della webapp.


# explod-movies-backend
All'interno della directory **explod-movies-backend** sono presenti i file python nei quali è implementato il Recommender System e i dataset dei film che vengono usati dal sistema.

## Installazione
Prima di iniziare ad utilizzare il servizio ci si deve assicurare di avere Python 3 e si devono installare i seguenti moduli e librerie:
1. Networkx
```shell
   pip install Networkx
```
2. Matplotlib
```shell
   pip install Matplotlib
```
3. Random
```shell
   pip install Random
```
4. Flask
```shell
   pip install Flask
```
5. Flask_restful
```shell
   pip install Flask-RESTful
```

## Configurazioni
Sono state realizzate due diverse configurazioni del Recommender System: la prima per essere lanciato ed utilizzato da riga di comando (file *main.py*), la seconda per essere lanciato come API in ascolto di richieste provenienti dalla webapp (file *service.py*).

### Recommender da riga di comando
Per eseguire una richiesta al Recommender da rifa di comando, come prima cosa ci si deve spostare nella cartella **explod-movies-backend** e successivamente lanciare il comando con i dati richiesti dal sistema per l'esecuzione. <br>
Un esempio di comando per una richiesta è il seguente:
```shell
   python main.py [I:11033,I:8360,I:1661,I:8487] [I:11768] 3 primolivello 1 False
```
Nel dettaglio, dopo il comando *python* i dati da inserire sono i seguenti nell'ordine:
1. Il file da lanciare che nel nostro caso è sempre *main.py*
2. Gli ID dei film piaciuti all'utente all'interno di parentesi quadre e separati da virgole (si consiglia almeno 3)
3. L'ID o gli ID dei film raccomandati all'interno di parentesi quadre e separati da virgole
4. Il numero di proprietà in comune da considerare per generare la spiegazione
5. Il tipo di spiegazione che si vuole ricevere. Si possono avere 3 tipi diversi di spiegazione:
   - ***baseline*** per una spiegazione basilare;
   - ***schema*** per un elenco di proprietà e informazioni in merito al film o ai film raccomandati;
   - ***primolivello*** per una spiegazione in linguaggio naturale che utilizza le proprietà in comune.
6. Il tipo di configurazione per la frase in linguaggio naturale: ***1*** per la prima e ***2*** per la seconda
7. ***True*** o ***False*** se si desidera o meno aggiungere i tag html ai film e alle proprietà per la formattazione <br>

E' importante inserire tutti i dati nel comando che lancia il recommender, anche se non verranno utilizzati per la spiegazione scelta.

### Recommender Service (API)
Per avviare il Recommender eseguire il comando
```shell
   nohup python3 service.py &
```
Per terminare il Recommender eseguire il comando
```shell
   pkill -f service.py
```
