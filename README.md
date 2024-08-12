# Micro-SaaS Application Example with &amp; Streamlit, OpenAI, and Replicate APIs

This project is a demonstration of a SaaS application built using **Streamlit** in Python, integrating with **OpenAI** and **Replicate APIs** to provide powerful AI-driven features. The app showcases how to seamlessly combine these technologies to create an interactive, user-friendly interface for AI services.

## Features
- **Streamlit Frontend**: An intuitive web interface for user interactions and visualizations.
- **Subscription-only Chat Tool with OpenAI Integration**: Leverage GPT models for natural language processing, text generation, and other AI-driven functionalities.
- **Subscription-only AI Photo Editing Tool with Replicate API Integration**: Access a AI Photo Editing model, through the Replicate API.
- **User Authentication with MongoDB Atlas**: Secure and scalable user data management using MongoDB Cloud Atlas.


### Directory Structure
```
micro-saas/
│
├── auth/                  # Directory containing authentication logic
│   ├─────── __init__.py   # This file initializes the auth package
│   ├─────── authenticate.py     # Chat page
│   ├─────── exceptions.py       # Chat page
│   ├─────── hasher.py           # Chat page
│   └─────── utils.py            # Contact Us page
│
├── mongo_db/              # Directory containing Mongo db connection and table models
│   ├─────── __init__.py           # This file initializes the mongo_db package
│   ├─────── connections.py        # Connection logic
│   └─────── models/               # Directory containing models schemas
│            ├─────── __init__.py         # This file initializes the models package
│            └─────── users.py            # Contact Us page
├── pages/                 # Directory containing additional pages for the app
│   ├─────── ai_photo_editing.py  # AI Photo Editing page
│   ├─────── chat.py              # Chat page
│   └─────── contact_us.py        # Contact Us page
│
├── utils/                 # Directory containing utility functions for the app (e.g., email verification, user registration)
│   └─────── utils.py      # utility function
│
├── .streamlit/            # Directory containing Streamlit config toml file
│   └─────── config.toml         # Streamlit confi file
├── .vscode/               # Directory containing VS Code debug file
│   └─────── launch.json         # VS Code debug launch config file
│
│
├── README.md              # This README file
├── requirements.txt       # Python dependencies required for the app
├── .env                   # Environment variables for the app (e.g., database credentials, API keys)
├── .gitignore             # List of files and directories to be ignored by Git
├── .streamlit             # Stremlit folder that contains config.toml for the stramlit app
├── home.py                # Main home page for the application
├── navigation.py          # Navigation logic
└── __pycache__/           # Directory for Python cache files
```

### Setting Up

1. **Clone the Repository**:
   ```bash
   git clone https://github.com/eejmartin/micro-saas.git
   cd micro-saas
   ```

2. **Create Python Environment**
   Use the following command to create Python environment
   ```bash
   python -m venv saas
   ```
   Use the following command to activate newly created Python environment
   ```bash
   .\saas\Scripts\activate
   ```

4. **Install Dependencies**:
   Use the following command to install the required dependencies:
   ```bash
   pip install -r requirements.txt
   ```

5. **Environment Variables**:
   Rename `.env.example` to `.env` and update the `.env` file with the necessary credentials and API keys.

6. **Run the Streamlit App**:
   ```bash
   streamlit run home.py
   ```