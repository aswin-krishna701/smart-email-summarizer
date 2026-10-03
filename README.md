# Smart Email Summarizer and Priority Analyzer Chrome Extension

## Abstract

The **Smart Email Summarizer and Priority Analyzer Chrome Extension** is an AI-powered productivity tool designed to help users quickly understand, organize, and respond to long emails. The project uses Natural Language Processing and Hugging Face Transformers to generate concise summaries from email content while also extracting key points, detecting action items, classifying email priority, identifying tone, and suggesting quick replies.

The extension allows users to paste email text or extract selected text from a webpage and analyze it through a clean Chrome Extension interface. The backend is built using Python Flask and connects with the Hugging Face Inference API for summarization. Other supporting features such as priority explanation, action item detection, tone identification, and quick reply generation are implemented using rule-based NLP logic.

The project follows a privacy-focused approach by processing only pasted or selected email text and avoiding permanent storage of email content. It demonstrates the practical use of transformer-based NLP in a real-world browser productivity tool for students, professionals, and users who handle multiple emails daily.

---

## Features

* Email summarization using Hugging Face Transformers
* Key point extraction from email content
* Action item detection
* Priority classification: High, Medium, Low
* Priority explanation with reason
* Tone identification: Formal, Urgent, Friendly, Informational, Neutral
* Quick reply suggestion
* Copy reply button
* Extract selected text from webpage
* Privacy-focused design with no permanent email storage

---

## Tech Stack

### Frontend

* Chrome Extension Manifest V3
* HTML
* CSS
* JavaScript

### Backend

* Python
* Flask
* Flask-CORS
* Requests
* Python-dotenv

### AI / NLP

* Hugging Face Inference API
* `facebook/bart-large-cnn` summarization model
* Rule-based NLP logic

---

## Folder Structure

```text
smart-email-summarizer/
├── backend/
│   ├── app.py
│   ├── nlp_utils.py
│   ├── requirements.txt
│   └── .env
│
├── extension/
│   ├── manifest.json
│   ├── popup.html
│   ├── popup.css
│   ├── popup.js
│   ├── content.js
│   └── icons/
│
├── samples/
│   └── sample_emails.txt
│
├── screenshots/
│
├── .gitignore
└── README.md
```

---

## Installation Steps

### 1. Clone or Download the Project

Download the project ZIP or clone the repository.

```powershell
git clone YOUR_REPOSITORY_URL
cd smart-email-summarizer
```

If downloaded as ZIP, extract it and open the folder in VS Code.

---

### 2. Create Hugging Face Token

Create a Hugging Face access token from your Hugging Face account settings.

Then open:

```text
backend/.env
```

Add your token:

```env
HF_API_TOKEN=hf_your_actual_token_here
HF_MODEL=facebook/bart-large-cnn
```

Do not share your `.env` file publicly.

---

### 3. Install Backend Dependencies

Open VS Code terminal and run:

```powershell
cd backend
python -m venv venv
Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass
.\venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

---

## How to Run Backend

From the `backend` folder, run:

```powershell
python app.py
```

The backend will start at:

```text
http://127.0.0.1:5000
```

To check whether the backend is running, open this URL in Chrome:

```text
http://127.0.0.1:5000
```

Expected response:

```json
{
  "message": "Smart Email Summarizer Backend is running",
  "status": "ok"
}
```

Keep the backend terminal open while using the Chrome extension.

---

## How to Load Chrome Extension

1. Open Google Chrome.
2. Go to:

```text
chrome://extensions/
```

3. Turn on **Developer mode**.
4. Click **Load unpacked**.
5. Select only the `extension` folder.

Correct folder to select:

```text
smart-email-summarizer/extension
```

6. Pin the extension from the Chrome toolbar.
7. Make sure the Flask backend is running before clicking **Analyze Email**.

---

## How to Use

### Method 1: Paste Email Text

1. Open the extension popup.
2. Paste email text into the text area.
3. Click **Analyze Email**.
4. View the summary, key points, action items, priority, priority reason, tone, and suggested reply.

### Method 2: Extract Selected Text

1. Open a normal webpage or email page.
2. Select the email text using the mouse.
3. Click the extension icon.
4. Click **Extract Selected Text**.
5. The selected text will appear in the text area.
6. Click **Analyze Email**.

Note: Text extraction may not work on protected Chrome pages such as `chrome://extensions/`, `chrome://settings/`, Chrome Web Store, or some browser system pages.

---

## Sample Input

```text
Dear student,

Please submit your assignment before Friday evening. Also, review the attached document and confirm your availability for tomorrow's project meeting.

Regards,
Project Coordinator
```

---

## Sample Output

```text
Summary:
Dear student, Please submit your assignment before Friday evening. Also, review the attached document and confirm your availability for tomorrow's project meeting.

Priority:
High

Priority Reason:
near deadline mentioned; submission required; meeting mentioned; review requested; confirmation requested.

Tone:
Formal

Key Points:
- Dear student, Please submit your assignment before Friday evening.
- Also, review the attached document and confirm your availability for tomorrow's project meeting.

Action Items:
- Dear student, Please submit your assignment before Friday evening.
- Also, review the attached document and confirm your availability for tomorrow's project meeting.

Suggested Reply:
Thank you for the information. I confirm that I will attend the meeting and complete the required action on time.
```

---

## Screenshots

Add project screenshots inside the `screenshots/` folder.

Recommended screenshot names:

```text
01_backend_running.png
02_extension_loaded.png
03_urgent_email_result.png
04_friendly_email_result.png
05_announcement_email_result.png
```

Suggested screenshots to include:

* Backend running in VS Code terminal
* Chrome extension loaded in `chrome://extensions/`
* Extension popup before analysis
* Urgent email result
* Friendly email result
* Informational announcement result

---

## Privacy Design

This project follows a privacy-focused design:

* Users paste or select only the email text they want to analyze.
* The extension does not permanently store email content.
* No database is used for storing emails.
* The Hugging Face API token is stored only in the backend `.env` file.
* The API token is not exposed in Chrome extension JavaScript files.

---

## Limitations

* The Flask backend must be running locally for the extension to work.
* The current version does not directly connect to Gmail API.
* Text extraction may not work on restricted browser pages.
* Priority, tone, action item detection, and quick replies use rule-based NLP logic.
* Summarization depends on Hugging Face API availability and internet connection.
* Very long emails may be shortened before sending to the summarization model.

---

## Future Scope

* Gmail API integration
* Multilingual email summarization
* More advanced tone detection using machine learning models
* User-customized reply styles
* Offline model support
* Email category classification
* Calendar reminder extraction
* Notification support for high-priority emails

---


## Project Status

The project successfully demonstrates a working Chrome Extension and Flask backend system for email summarization, priority analysis, tone detection, action item detection, key point extraction, and quick reply suggestion using Hugging Face Transformers and rule-based NLP logic.
