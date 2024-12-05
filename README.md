# network-security
end to end machine learning system for network security

# Installation Guide

## Overview
This guide provides step-by-step instructions to install and run the **Network Prediction System**, a FastAPI-based application, on your local machine or server.

---

## Prerequisites

### System Requirements
- **Operating System:** Windows/Linux/MacOS
- **Python Version:** Python 3.8 or later

### Dependencies
The system requires the following Python packages, listed in `requirements.txt`:
- python-dotenv  
- pandas  
- numpy<2  
- pymongo  
- certifi  
- pymongo[srv]==3.6  
- scikit-learn  
- pyaml  
- dagshub  
- mlflow  
- fastapi  
- uvicorn  

---

## Installation Steps

### 1. Clone the Repository
```bash
git clone https://github.com/peniel18/network-security
cd network-security
```

### 2. Set Up a Virtual Environment


```bash
python3 -m venv venv
source venv/bin/activate
```

### Install Dependencies

```bash
pip install -r requirements.txt
```

### Run the FastAPI Server

```bash
python3 app.py
```
