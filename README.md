# 🚀 [Tips Hindawi](https://www.tipshindawi.com/) Challenge (June–July) 2026

> 🏆 This repository is my official submission for the [ **Tips Hindawi** ](https://www.tipshindawi.com/) **Challenge (June–July) 2026**.

## 👤 Participant

| Field            | Value                                |
| ---------------- | ------------------------------------ |
| Full Name        |   Abdelrahman Mahmoud Mossad         |
| Project Name     |   Intelligent Traffic Law Assistant  |
| GitHub Username  |    Abdelrahman590                                  |
| Challenge Batch  | June–July 2026                       |
| Training Program | Large Language Models (LLMs) Program |
| Organization     | [**Edrak for Ai**](https://edrak4ai.com/en)                         |

---

# 📖 Project Overview

The **Intelligent Traffic Law Assistant** is a RAG-based (Retrieval-Augmented Generation) chatbot that answers questions about Egyptian traffic law, including driving license requirements and traffic violations, in both Arabic and English. The project was built entirely on free resources, using open-source models running on Kaggle GPU sessions and exposed through ngrok tunnels, with no local GPU or paid API required.

---

# ✨ Features

* Answers questions about Egyptian traffic law (driving license requirements and traffic violations) in both Arabic and English
* Retrieval-Augmented Generation (RAG) pipeline with source citation display
* Two-stage chain: a Prompt Optimizer chain followed by a Retriever + QA chain
* Runs entirely on free resources (Kaggle GPU + ngrok), with no paid API or local GPU needed
* Streamlit-based frontend with an "Optimize Prompt" button

---

# 🛠️ Technologies Used

* **Compute:** Kaggle GPU sessions (free tier) + ngrok tunnels
* **LLM:** Qwen2.5-3B-Instruct
* **Embeddings:** bge-small-en-v1.5
* **Backend:** FastAPI + pyngrok (served from the Kaggle notebook)
* **Orchestration:** LangChain , with custom `KaggleRemoteLLM` and `KaggleRemoteEmbeddings` wrappers routing inference via HTTP to the Kaggle ngrok URL
* **Vector Store:** FAISS
* **Frontend:** Streamlit
* **Other:** Pydantic, Python (venv for dependency management)

---

# ⚙️ Installation

1. Clone this repository.
2. Create and activate a Python virtual environment (`venv`).
3. Install the dependencies with `pip install -r requirements.txt`.
4. Open the Kaggle notebook, run all cells to start the FastAPI server and generate the ngrok public URL.
5. Update `config.py` with the generated ngrok URL.
6. Run the ingestion pipeline to build the FAISS vector store from the provided documents.
7. Launch the Streamlit app locally.

---

# 🚀 Usage

Open the Streamlit interface, type your question about Egyptian traffic law (driving licenses or violations) in Arabic or English, and optionally click "Optimize Prompt" to refine your query before submitting. The assistant will retrieve relevant sources and generate an answer, displaying the source citations alongside the response.

---

# 📸 Demo


---

# 📈 Results

The project runs successfully end-to-end, providing accurate, source-cited answers to questions about Egyptian traffic law in both Arabic and English, entirely on free-tier infrastructure (Kaggle GPU + ngrok), with no paid API or local GPU required.

---

# 🔮 Future Improvements

* Expand the knowledge base to cover additional Egyptian legal documents beyond driving licenses and violations
* Deploy the backend on a persistent, paid-free hosting alternative to reduce reliance on ngrok tunnel restarts
* Add conversation memory for multi-turn follow-up questions
* Improve retrieval accuracy with hybrid search (keyword + vector)

---

# 📚 About the Challenge

This project was developed as part of the [**Tips Hindawi**](https://www.tipshindawi.com/) **Challenge (June–July) 2026**.

[Tips Hindawi](https://www.tipshindawi.com/) is the internships department of [**Edrak for Ai**](https://edrak4ai.com/en), and the challenge encourages participants to build real-world projects, apply practical skills, and showcase their work through GitHub.

For more information about the challenge, training programs, and upcoming batches, visit the official [Tips Hindawi](https://www.tipshindawi.com/) website.

---

# 📄 License

This project is shared for educational and portfolio purposes.
 
