# 🧠 DSA Logic Tutor

An AI-powered web application designed to help students master Data Structures and Algorithms (DSA). Unlike standard debuggers, this tool acts as a **tutor**: it analyzes complexity, finds logical bugs, and gives **optimization hints** without revealing the code solution.

## 🚀 Live Demo
[Link to your Render Website goes here]

## ✨ Features
* **Time & Space Complexity Analysis:** Instantly calculates Big O notation ($O(n)$, $O(\log n)$, etc.).
* **Logic Debugger:** Identifies edge cases and logical errors in your Brute Force approach.
* **Tutor Mode:** Provides **Optimization Strategy Hints** (e.g., "Use a Hash Map") instead of just fixing the code, encouraging learning.
* **Multi-Language Support:** Python, C, C++, Java, JavaScript.

## 🛠️ Tech Stack
* **Frontend:** HTML5, CSS3, Vanilla JavaScript
* **Backend:** Python (FastAPI)
* **AI Engine:** Google Gemini 1.5 Flash
* **Deployment:** Render

## 💻 How to Run Locally

1.  **Clone the repository**
    ```bash
    git clone [https://github.com/your-username/dsa-tutor.git](https://github.com/your-username/dsa-tutor.git)
    cd dsa-tutor
    ```

2.  **Install Dependencies**
    ```bash
    pip install -r requirements.txt
    ```

3.  **Set up Environment Variables**
    * Create a `.env` file in the root directory.
    * Add your Google Gemini API key:
        ```text
        GENAI_API_KEY=your_actual_api_key_here
        ```

4.  **Run the Server**
    ```bash
    uvicorn main:app --reload
    ```

5.  **Open in Browser**
    Go to `http://127.0.0.1:8000`