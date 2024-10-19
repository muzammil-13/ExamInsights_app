## ExamInsight: A Real-time Augmented Generation (RAG) Application for Exam Preparation

### Introduction

Welcome to ExamInsight, a powerful application powered by the cutting-edge Pathway framework! This project revolutionizes exam preparation by leveraging the capabilities of Real-time Augmented Generation (RAG) to analyze exam papers and provide valuable insights to students and educators.

ExamInsight ingests data from PDFs of exam papers stored in its `data` folder and presents insightful analysis through an interactive Streamlit interface. Built with Pathway, Docker, and Streamlit, this application runs seamlessly in a production-ready, containerized environment. Its in-memory scalable vector store ensures efficient handling of data and adapts in real-time to any changes made to the PDFs. This means you're always working with the most up-to-date information, ensuring accurate analysis and relevant insights.

### Table of Contents

* [What Problem It Solves](vscode-webview://17q0p7vtbq3fvgfki2b6jucqnt08ngujmbct82opqjvfci10r8d9/index.html?id=dcdb8d6e-2f05-4355-9e00-a38568a04f23&origin=d705290a-2635-451b-acdf-cd503f2a6066&swVersion=4&extensionId=googlecloudtools.cloudcode&platform=electron&vscode-resource-base-authority=vscode-resource.vscode-cdn.net&parentOrigin=vscode-file%3A%2F%2Fvscode-app&purpose=webviewView#what-problem-it-solves)
* [Architecture Overview](vscode-webview://17q0p7vtbq3fvgfki2b6jucqnt08ngujmbct82opqjvfci10r8d9/index.html?id=dcdb8d6e-2f05-4355-9e00-a38568a04f23&origin=d705290a-2635-451b-acdf-cd503f2a6066&swVersion=4&extensionId=googlecloudtools.cloudcode&platform=electron&vscode-resource-base-authority=vscode-resource.vscode-cdn.net&parentOrigin=vscode-file%3A%2F%2Fvscode-app&purpose=webviewView#architecture-overview)
* [Getting Started](vscode-webview://17q0p7vtbq3fvgfki2b6jucqnt08ngujmbct82opqjvfci10r8d9/index.html?id=dcdb8d6e-2f05-4355-9e00-a38568a04f23&origin=d705290a-2635-451b-acdf-cd503f2a6066&swVersion=4&extensionId=googlecloudtools.cloudcode&platform=electron&vscode-resource-base-authority=vscode-resource.vscode-cdn.net&parentOrigin=vscode-file%3A%2F%2Fvscode-app&purpose=webviewView#getting-started)
* [Demo](vscode-webview://17q0p7vtbq3fvgfki2b6jucqnt08ngujmbct82opqjvfci10r8d9/index.html?id=dcdb8d6e-2f05-4355-9e00-a38568a04f23&origin=d705290a-2635-451b-acdf-cd503f2a6066&swVersion=4&extensionId=googlecloudtools.cloudcode&platform=electron&vscode-resource-base-authority=vscode-resource.vscode-cdn.net&parentOrigin=vscode-file%3A%2F%2Fvscode-app&purpose=webviewView#demo)
* [Contributing](vscode-webview://17q0p7vtbq3fvgfki2b6jucqnt08ngujmbct82opqjvfci10r8d9/index.html?id=dcdb8d6e-2f05-4355-9e00-a38568a04f23&origin=d705290a-2635-451b-acdf-cd503f2a6066&swVersion=4&extensionId=googlecloudtools.cloudcode&platform=electron&vscode-resource-base-authority=vscode-resource.vscode-cdn.net&parentOrigin=vscode-file%3A%2F%2Fvscode-app&purpose=webviewView#contributing)
* [Contact Information](vscode-webview://17q0p7vtbq3fvgfki2b6jucqnt08ngujmbct82opqjvfci10r8d9/index.html?id=dcdb8d6e-2f05-4355-9e00-a38568a04f23&origin=d705290a-2635-451b-acdf-cd503f2a6066&swVersion=4&extensionId=googlecloudtools.cloudcode&platform=electron&vscode-resource-base-authority=vscode-resource.vscode-cdn.net&parentOrigin=vscode-file%3A%2F%2Fvscode-app&purpose=webviewView#contact-information)

### What Problem It Solves

ExamInsight directly addresses the challenge of effectively analyzing past exam papers to identify patterns and trends. Manually reviewing numerous papers is time-consuming and prone to bias. ExamInsight automates this process, providing data-driven insights into question patterns, frequently tested topics, and potential areas of difficulty.

The application currently ingests data from PDFs located in the `data` folder. However, one of its most powerful features is the ability to connect to external dynamic data sources. Imagine connecting ExamInsight to your Google Drive where exam papers are shared and updated! This opens up a world of possibilities for keeping your information current and relevant. For more information on connecting data sources, check out these resources:

* [LLM App Examples](https://github.com/pathwaycom/llm-app?tab=readme-ov-file#llm-app)
* [Pathway App Templates](https://pathway.com/app-templates)

### Architecture Overview

ExamInsight is built upon a robust and scalable architecture:

* **Pathway:** This powerful RAG framework forms the backbone of our application, enabling real-time updates and powering the live Gen AI features.
* **Docker:** By containerizing our application with Docker, we ensure easy deployment and management across different environments.
* **Streamlit:** Provides an intuitive and interactive web-based frontend for users to easily interact with ExamInsight, ask questions about the exam papers, and visualize the analysis.
* **Local Data Folder for Data Ingestion:** The `data` folder stores the PDFs that fuel the application. When connected to external data sources like Google Drive, ExamInsight dynamically adapts to changes, ensuring you always have the latest information.

### Getting Started

Ready to experience the power of ExamInsight? Follow these steps:

**Prerequisites:**

* Docker
* Install Pathway: `pip install pathway-ai`

**Installation:**

1. Clone the repository:
   ```bash
   git clone https://github.com/your-username/your-repo.git
   cd your-repo
   ```
2. Build the Docker image:
   ```bash
   docker build -t examinsight .
   ```
3. Run the project:
   ```bash
   docker run -p 8000:8000 -p 8501:8501 examinsight
   ```

**Adding PDFs and Connecting Google Drive:**

* **Adding PDFs:** Place your PDF files in the `data` folder.
* **Connecting Google Drive:** Follow the instructions in the documentation to configure Google Drive integration for live updates.

### Demo

[Include a link to a demo video or GIF showcasing the project's functionality]

### Contributing

We welcome contributions from the community! If you'd like to contribute to ExamInsight, please follow our contribution guidelines outlined in [CONTRIBUTING.md](vscode-webview://17q0p7vtbq3fvgfki2b6jucqnt08ngujmbct82opqjvfci10r8d9/CONTRIBUTING.md).

### Contact Information

For any questions, suggestions, or collaboration opportunities, feel free to reach out to us at [muzammilibrahim13@gmail.com]() .
