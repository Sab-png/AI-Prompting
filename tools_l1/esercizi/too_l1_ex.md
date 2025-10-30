

# Esercizio: Sistema di Gestione Vendite con SQL e Function Calling


Sviluppare un agente conversazionale basato su LLM che interagisce con un database SQLite contenente dati di vendite reali. L'agente dovrà essere in grado di rispondere a domande, eseguire analisi sui dati di vendita e generare report utilizzando il function calling.

## Dataset di Riferimento

Il dataset è composto da un CSV di vendite reali scaricabile da:
- **Kaggle Sample Sales Data** [[3]](https://www.kaggle.com/datasets/kyanyoga/sample-sales-data)


## Requisiti dell'Esercizio

Implementa le seguenti funzionalità:

1. **Importazione Dataset**: Carica i dati CSV in un database SQLite
2. **Funzioni SQL**: Crea almeno 5 funzioni Python che eseguono query sul database
3. **Tool Definitions**: Definisci gli schemi JSON per ogni funzione
4. **Agente Conversazionale**: Implementa un agente che risponde a query in linguaggio naturale

## Domande Esempio da Supportare

Il tuo agente dovrà essere in grado di rispondere a domande come:
- "Qual è il fatturato totale per paese?"
- "Chi sono i top 5 clienti per volume di acquisti?"
- "Mostrami i prodotti più venduti nel ..."
- "In quale trimestre abbiamo avuto le migliori performance di vendita?"
