# ExamInsight: Real-time Exam Analysis with Pathway RAG

## Introduction

ExamInsight is an innovative, production-ready Real-time Augmented Generation (RAG) application built using Pathway within a Dockerized environment. This powerful tool analyzes exam question papers stored as PDFs in the project's data folder, providing valuable insights to students and educators. By leveraging Pathway's in-memory scalable vector store, ExamInsight adapts in real-time to any changes in the source documents, ensuring that users always have access to the most up-to-date analysis.

Powered by Pathway and containerized with Docker, ExamInsight offers a robust, scalable solution for exam paper analysis that can be easily deployed in various environments. Whether you're a student looking to optimize your study strategy or an educator seeking to understand question patterns, ExamInsight provides the insights you need to succeed.

## Table of Contents

- [What Problem It Solves](#what-problem-it-solves)
- [Architecture Overview](#architecture-overview)
- [Getting Started](#getting-started)
- [Demo](#demo)
- [Contributing](#contributing)
- [Contact Information](#contact-information)

## What Problem It Solves

ExamInsight addresses the challenge of efficiently analyzing exam question papers to identify patterns, frequent topics, and question types. By ingesting PDF files from the data folder, the application provides students with valuable insights to guide their exam preparation. The real-time adaptation to changes in the source documents ensures that users always have access to the most current analysis.

While currently focused on local PDF files, ExamInsight has the potential to connect with Google Drive or over 300 other data sources for future expansions and live updates. This flexibility allows for seamless collaboration and real-time analysis of shared exam resources. For more information on potential data sources and features, visit the Pathway LLM App repository and Pathway App Templates.

## Architecture Overview

ExamInsight's architecture consists of three main components:

1. **Pathway**: The core RAG framework that powers the application, enabling real-time updates and live Gen AI capabilities. Pathway's in-memory vector store allows for efficient storage and retrieval of exam question embeddings.
2. **Docker**: Used for containerization, Docker ensures that ExamInsight can be easily deployed and managed across different environments, maintaining consistency and simplifying the setup process.
3. **Local Data Folder for Data Ingestion**: PDF files containing exam questions are stored in a local data folder. The application monitors this folder for changes, automatically updating its analysis when new files are added or existing ones are modified. This architecture can be easily extended to connect with external dynamic data sources like Google Drive for collaborative scenarios.

## Getting Started

Follow these steps to set up and run ExamInsight on your local machine:

### Prerequisites

- Docker installed on your system
- Python 3.8 or higher
- pip package manager

### Installation and Setup

1. Clone the repository:
    ```bash
    git clone <repository-url>
    cd <repository-directory>
    ```
2. Install Pathway:
    ```bash
    pip install pathway
    ```
3. Build the Docker image:
    ```bash
    docker build -t examinsight .
    ```
4. Run the Docker container:
    ```bash
    docker run -p 8000:8000 examinsight
    ```
5. Access the application at [http://localhost:8000](http://localhost:8000) in your web browser.

### Adding Exam Papers

To analyze exam papers, simply add PDF files to the data folder in the project directory. The application will automatically detect new files and update its analysis accordingly.

## Demo

[Placeholder for demo video or GIF showing ExamInsight in action]

## Contributing

We welcome contributions to ExamInsight! If you'd like to improve or expand the project, please follow these steps:

1. Fork the repository
2. Create a new branch for your feature or bug fix
3. Make your changes and commit them with clear, descriptive messages
4. Push your changes to your fork
5. Submit a pull request with a detailed description of your changes

Please ensure that your code adheres to the project's coding standards and includes appropriate tests.

<!-- ## Contact Information

For questions, suggestions, or collaboration opportunities, please contact:

- [Your Name]
- Email: [your.email@example.com]
- GitHub: [@yourusername] -->

We look forward to hearing from you and seeing how ExamInsight can help improve exam preparation and analysis!
