
# PDF Chat with Gemini

This project allows you to chat with your PDF documents using Google's Gemini AI model. It provides a user-friendly interface to upload PDFs and ask questions about their content.

## Features

- PDF document upload and processing
- Interactive chat interface
- Powered by Google's Gemini AI
- Real-time responses to PDF content queries

## Setup Instructions

1. Clone this repository
2. Install the required dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. Create a `.env` file in the root directory and add your Gemini API key:
   ```
   GEMINI_API_KEY=your_api_key_here
   ```
4. Run the application:
   ```bash
   streamlit run app.py
   ```

## Usage

1. Upload a PDF file using the file uploader
2. Wait for the PDF to be processed
3. Start asking questions about the PDF content in the chat interface

## Note

Make sure you have a valid Gemini API key from Google AI Studio.
