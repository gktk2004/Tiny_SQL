import subprocess
import sqlite3
import time
from prompt_template import BASE_PROMPT

# ==========================================
# CONFIGURATION
# ==========================================
MODEL_NAME = "phi3:mini"   # use:  ollama pull phi3:mini
MAX_RETRIES = 2

# IMPORTANT: Full path for Windows
OLLAMA_PATH = r"C:\Users\hp\AppData\Local\Programs\Ollama\ollama.exe"


# ==========================================
# Validate SQL (forbidden words + basic checks)
# ==========================================
def is_sql_valid(sql_query: str):
    forbidden = ["DROP", "DELETE", "UPDATE", "ALTER", "INSERT"]

    # 1. Check forbidden words
    for word in forbidden:
        if word.lower() in sql_query.lower():
            return False, f"Forbidden keyword detected: {word}"

    # 2. Syntax check using SQLite
    try:
        conn = sqlite3.connect("college.db")
        cursor = conn.cursor()

        cursor.execute(f"EXPLAIN {sql_query}")
        conn.close()
        return True, "OK"

    except Exception as e:
        return False, str(e)


# ==========================================
# Call Ollama Model
# ==========================================
def call_ollama(prompt):
    start = time.time()

    result = subprocess.run(
        [OLLAMA_PATH, "run", MODEL_NAME],
        input=prompt.encode("utf-8"),
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE
    )

    latency = time.time() - start
    output = result.stdout.decode("utf-8").strip()

    return output, latency


# ==========================================
# Main SQL generator with self-correction loop
# ==========================================
def generate_sql(user_question):
    print("\n==============================")
    print("🔍 User Question:", user_question)
    print("==============================")

    prompt = BASE_PROMPT + user_question + "\nSQL:"

    for attempt in range(MAX_RETRIES + 1):
        print(f"\n➡️ Attempt {attempt + 1}")

        sql_output, latency = call_ollama(prompt)

        print(f"⏱️ Model generation latency: {latency:.2f} sec")
        print("📤 Raw Model Output:", sql_output)

        # Keep only SQL until the first semicolon
        if ";" in sql_output:
            sql_output = sql_output.split(";")[0] + ";"

        is_valid, reason = is_sql_valid(sql_output)

        if is_valid:
            print("✅ SQL Validated Successfully")
            return sql_output

        print("❌ SQL Invalid:", reason)

        # Retry logic
        prompt = (
            BASE_PROMPT
            + user_question
            + "\nThe previous SQL was invalid because: "
            + reason
            + "\nPlease fix it. SQL:"
        )

    return "SELECT 'I do not know';"


# ==========================================
# CLI entry point
# ==========================================
if __name__ == "__main__":
    print("📘 TinySQL — Natural Language to SQL using Phi-3 Mini\n")

    user_question = input("Enter your question: ")

    final_sql = generate_sql(user_question)

    print("\n==============================")
    print("✅ FINAL SQL OUTPUT:")
    print("==============================")
    print(final_sql)
