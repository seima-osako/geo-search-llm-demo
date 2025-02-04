# Geospatial Analysis Advisor 🌍

An intelligent chat-based system that helps users discover and analyze Dutch geospatial data by suggesting relevant analysis methods and data sources from PDOK (Publieke Dienstverlening Op de Kaart).

## 🌟 Key Features

- **Intelligent Data Discovery**: Utilizes RAG (Retrieval Augmented Generation) with self-querying capabilities to find relevant geospatial datasets
- **Smart Analysis Suggestions**: Provides tailored analysis recommendations based on available data
- **Interactive Chat Interface**: Built with Chainlit for a smooth user experience
- **Advanced NLP**: Powered by Google's Gemini model for understanding and processing queries
- **Automated Data Processing**: Includes a comprehensive data pipeline for processing PDOK's WMS services

## 🛠️ Technical Architecture

### Data Pipeline
1. **Data Collection**
   - Scrapes PDOK's geospatial data catalog using Selenium
   - Extracts WMS service metadata and capabilities
   - Processes XML responses to gather layer information

2. **Data Processing**
   - Vectorizes content using Google's Generative AI Embeddings
   - Implements character-based text splitting for optimal processing
   - Stores vectors in ChromaDB for efficient retrieval

3. **Query Processing**
   - Uses LangChain's SelfQueryRetriever for intelligent data filtering
   - Implements custom metadata field handling
   - Provides source references with results

### Key Components

- **Frontend**: Chainlit-based chat interface
- **Backend**: 
  - LangChain for RAG implementation
  - Google Gemini for text generation and embeddings
  - ChromaDB for vector storage
- **Data Sources**: PDOK WMS services

## 🔧 Technology Stack

- **Python**: >= 3.10
- **Key Libraries**:
  - `langchain`: Core RAG and prompt handling
  - `chainlit`: Chat interface
  - `selenium`: Data scraping
  - `google-generative-ai`: LLM and embeddings
  - `chromadb`: Vector storage

## 🚀 Getting Started

1. **Clone the Repository**
```bash
git clone [repository-url]
cd geo-search
```

2. **Environment Setup**
```bash
# Install dependencies using Poetry
poetry install
```

3. **Configuration**
```bash
# Create .env file and add your Google Gemini API key
GEMENI_API_KEY=your_api_key_here
```

4. **Data Preparation**
```bash
# Run the data collection and vectorization notebook
jupyter notebook nl_geodata_scraper_vectorizer.ipynb
```

5. **Launch the Application**
```bash
poetry run chainlit run app_self-query.py
```

## 💡 Usage

1. Start the application using Chainlit
2. Ask questions about geospatial analysis for Dutch geographic data
3. Receive analysis suggestions and relevant data source references
4. Explore recommended PDOK WMS layers for your analysis


## 📜 License

This project is licensed under the MIT License - see the LICENSE file for details.