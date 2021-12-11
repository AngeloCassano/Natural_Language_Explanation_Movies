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
Sono state realizzate due diverse configurazioni del Recommender System: la prima per essere lanciato ed utilizzato da riga di comando (file *main.py*), la seconda per essere lanciato come API in ascolto di richieste provenienti dalla webapp (file *service.py*). <br> <br>
Inoltre, anche le singole componenti del sistema possono essere lanciate da riga di comando tramite i rispettivi script. <br>
Di seguito degli esempi di chiamate e di output risultante.

### Mapper
Per effettuare una chiamata al Mapper da riga di comando, è necessario lanciare il seguente comando:
```shell
   python Mapper.py cmd_mapper [I:11033,I:8360,I:1661,I:8487] [I:11768]
```
Dove *Mapper.py* è lo script della componente, *cmd_mapper* è la funzione chiamata nello script che esegue la componente, i dati tra parentesi quadre sono gli ID dei film piaciuti e dei film raccomandati passati come parametri alla funzione chiamata. <br>
Un esempio di output è il seguente:
```shell
   Esecuzione componente Mapper...
   Numero totale di film mappati:  8121
   
   Mappatura del profilo utente realizzata:
   Avatar   http://dbpedia.org/resource/Avatar_(2009_film)
   Full Metal Jacket        http://dbpedia.org/resource/Full_Metal_Jacket
   Toy Story        http://dbpedia.org/resource/Toy_Story
   The Green Mile   http://dbpedia.org/resource/The_Green_Mile_(film)
   
   Mappatura delle raccomandazioni realizzata:
   Aliens of the Deep       http://dbpedia.org/resource/Aliens_of_the_Deep
```

### Builder
Per effettuare una chiamata al Builder da riga di comando, è necessario lanciare il seguente comando:
```shell
   python Builder.py cmd_builder [I:11033,I:8360,I:1661,I:8487] [I:11768] True
```
Dove *Builder.py* è lo script della componente, *cmd_builder* è la funzione chiamata nello script che esegue la componente, i dati tra parentesi quadre sono gli ID dei film piaciuti e dei film raccomandati passati come parametri alla funzione chiamata e *True* o *False* indica se visualizzare o meno il grafo.<br>
Un esempio di output è il seguente:
```shell
   Esecuzione componente Builder...
   Numero di proprietà mappate:  139737
   
   Grafo creato con successo!
   Numero di nodi del grafo:  9
   Numero di archi del grafo:  12
   
   Ecco le proprietà in comune tra film piaciuti e raccomandazioni:
   http://dbpedia.org/resource/Walt_Disney_Studios_Motion_Pictures
   http://dbpedia.org/resource/James_Cameron
   http://dbpedia.org/resource/Category:American_3D_films
   http://dbpedia.org/resource/Category:Walt_Disney_Pictures_films
   http://dbpedia.org/resource/Category:2000s_3D_films
   http://dbpedia.org/resource/Category:Films_directed_by_James_Cameron
```

### Ranker
Per effettuare una chiamata al Ranker da riga di comando, è necessario lanciare il seguente comando:
```shell
   python Ranker.py cmd_ranker [I:11033,I:8360,I:1661,I:8487] [I:11768] True
```
Dove *Ranker.py* è lo script della componente, *cmd_ranker* è la funzione chiamata nello script che esegue la componente, i dati tra parentesi quadre sono gli ID dei film piaciuti e dei film raccomandati passati come parametri alla funzione chiamata e *True* o *False* indica se utilizzare o meno l'IDF nel calcolo.<br>
Un esempio di output è il seguente:
```shell
   Esecuzione componente Ranker...
   Le proprietà sono state rankate e ordinate con successo!
   
   Ecco le proprietà in comune dei film in ordine decrescente per influenza:
   4.4101865182669355       http://dbpedia.org/resource/Category:Films_directed_by_James_Cameron
   3.694478828077559        http://dbpedia.org/resource/James_Cameron
   3.640096717459041        http://dbpedia.org/resource/Category:2000s_3D_films
   2.879849639756232        http://dbpedia.org/resource/Category:American_3D_films
   2.6607977811994754       http://dbpedia.org/resource/Category:Walt_Disney_Pictures_films
   2.2639445154637197       http://dbpedia.org/resource/Walt_Disney_Studios_Motion_Pictures
```

### Recommender da riga di comando
Per eseguire una richiesta al Recommender da rifa di comando, come prima cosa ci si deve spostare nella cartella **explod-movies-backend** e successivamente lanciare il comando con i dati richiesti dal sistema per l'esecuzione. <br>
Un esempio di comando per una richiesta è il seguente:
```shell
   python main.py [I:11033,I:8360,I:1661,I:8487] [I:11768] True 3 True primolivello 1 False
```
Nel dettaglio, dopo il comando *python* i dati da inserire sono i seguenti nell'ordine:
1. Il file da lanciare che nel nostro caso è sempre *main.py*
2. Gli ID dei film piaciuti all'utente all'interno di parentesi quadre e separati da virgole (si consiglia almeno 3)
3. L'ID o gli ID dei film raccomandati all'interno di parentesi quadre e separati da virgole
4. ***True*** o ***False*** se si desidera o meno visualizzare il grafo
5. Il numero di proprietà in comune da considerare per generare la spiegazione
6. ***True*** o ***False*** se si desidera usare il ranking con IDF o meno
7. Il tipo di spiegazione che si vuole ricevere. Si possono avere 3 tipi diversi di spiegazione:
   - ***baseline*** per una spiegazione basilare;
   - ***schema*** per un elenco di proprietà e informazioni in merito al film o ai film raccomandati;
   - ***primolivello*** per una spiegazione in linguaggio naturale che utilizza le proprietà in comune.
8. Il tipo di configurazione per la frase in linguaggio naturale: ***1*** per la prima e ***2*** per la seconda
9. ***True*** o ***False*** se si desidera o meno aggiungere i tag html ai film e alle proprietà per la formattazione <br>

E' importante inserire tutti i dati nel comando che lancia il recommender, anche se non verranno utilizzati per la spiegazione scelta. <br>
Un esempio di output è il seguente:
```shell
   Esecuzione componente Generator...
   
   I suggest you Aliens of the Deep because you like Films directed by James Cameron and 2000s 3D films, such as Avatar.
```

### Recommender Service (API)
Per avviare il Recommender eseguire il comando
```shell
   nohup python3 service.py &
```
Per terminare il Recommender eseguire il comando
```shell
   pkill -f service.py
```
