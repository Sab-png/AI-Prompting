import ollama
import chromadb
from pypdf import PdfReader
from sentence_transformers import SentenceTransformer  # AGGIUNTO
import os

class RAGGestionaleOpen:
    def __init__(self, pdf_path, model_name="llama3.2:3b", embedding_model="sentence-transformers/all-MiniLM-L6-v2"):
        self.model_name = model_name
        self.pdf_path = pdf_path
        self.client = chromadb.Client()
        self.collection = None
        # Carica il modello di embedding
        print(f" Caricamento modello embedding: {embedding_model}")
        self.embedding_model = SentenceTransformer(embedding_model)
        
    def load_and_chunk(self, chunk_size=500, chunk_overlap=50):
        """Carica e chunka il PDF"""
        print(" Caricamento PDF...")
        reader = PdfReader(self.pdf_path)
        
        # Estrai tutto il testo
        full_text = ""
        for page in reader.pages:
            full_text += page.extract_text() + "\n"
        
        print(f" Estratto testo da {len(reader.pages)} pagine")
        
        # Chunking manuale semplice
        print("  Chunking del documento...")
        chunks = []
        words = full_text.split()
        
        for i in range(0, len(words), chunk_size - chunk_overlap):
            chunk = " ".join(words[i:i + chunk_size])
            chunks.append(chunk)
        
        print(f"Creati {len(chunks)} chunks")
        return chunks
    
    def create_embeddings(self, chunks):
        """Crea embeddings con SentenceTransformer"""
        print(" Creazione embeddings con MiniLM-L6-v2...")
        
        # Crea collection in ChromaDB
        try:
            self.client.delete_collection("gestionale_open")
        except:
            pass
            
        self.collection = self.client.create_collection(
            name="gestionale_open",
            metadata={"description": "Manuale Gestionale Open"}
        )
        
        # Genera embeddings e salva in ChromaDB
        for i, chunk in enumerate(chunks):
            # Genera embedding con SentenceTransformer
            embedding = self.embedding_model.encode(chunk).tolist()
            
            # Salva in ChromaDB
            self.collection.add(
                embeddings=[embedding],
                documents=[chunk],
                ids=[f"chunk_{i}"]
            )
            
            if (i + 1) % 10 == 0:
                print(f"  Processati {i + 1}/{len(chunks)} chunks")
        
        print(" Vector database creato!")
    
    def retrieve(self, query, k=3):
        """Recupera i chunks più rilevanti"""
        print(f"🔍 Ricerca di '{query}'...")
        
        # Genera embedding della query con SentenceTransformer
        query_embedding = self.embedding_model.encode(query).tolist()
        
        # Cerca in ChromaDB
        results = self.collection.query(
            query_embeddings=[query_embedding],
            n_results=k
        )
        
        return results['documents'][0]
    
    def generate_answer(self, query, k=3):
        """Genera risposta con LLM + contesto"""
        # Recupera documenti rilevanti
        relevant_docs = self.retrieve(query, k=k)
        
        # Costruisci contesto
        context = "\n\n".join(relevant_docs)
        
        # Crea prompt
        prompt = f"""Sei un assistente esperto del software "Gestionale Open", un ERP per PMI italiane.

CONTESTO dal manuale:
{context}

DOMANDA: {query}

Rispondi in modo chiaro e preciso basandoti SOLO sulle informazioni del contesto fornito. 
Se l'informazione non è presente nel contesto, rispondi "Non ho trovato questa informazione nel manuale".
Rispondi in italiano."""

        print(" Generazione risposta...")
        
        # Chiama Ollama
        response = ollama.chat(
            model=self.model_name,
            messages=[{'role': 'user', 'content': prompt}]
        )
        
        return response['message']['content'], relevant_docs

def main():
    PDF_PATH = "presentazione-go-gestionale-open.pdf"
    
    if not os.path.exists(PDF_PATH):
        print(" ERRORE: Scarica prima il PDF da:")
        print("https://www.avx.it/files/presentazione-go-gestionale-open.pdf")
        return
    
    # Inizializza RAG con MiniLM
    rag = RAGGestionaleOpen(
        pdf_path=PDF_PATH, 
        model_name="llama3.2:3b",  # ← Devi comunque avere un modello Ollama per le risposte!
        embedding_model="sentence-transformers/all-MiniLM-L6-v2"
    )
    
    # Caricamento e chunking
    chunks = rag.load_and_chunk(chunk_size=500, chunk_overlap=50)
    rag.create_embeddings(chunks)
    
    # Test
    test_queries = [
        "Quali sono i moduli principali di Gestionale Open?",
        "Come funziona la gestione del magazzino?",
        "Quali funzionalità offre per la contabilità?",
        "Come si gestiscono le vendite?"
    ]
    
    print("\n" + "="*60)
    print(" TEST DEL SISTEMA RAG")
    print("="*60 + "\n")
    
    for query in test_queries:
        print(f"\n DOMANDA: {query}")
        print("-" * 60)
        
        answer, docs = rag.generate_answer(query, k=3)
        
        print(f"\n💡 RISPOSTA:\n{answer}\n")
        print(" Chunks utilizzati:")
        for i, doc in enumerate(docs, 1):
            preview = doc[:100] + "..." if len(doc) > 100 else doc
            print(f"  {i}. {preview}")
        print("\n" + "="*60)

if __name__ == "__main__":
    main()