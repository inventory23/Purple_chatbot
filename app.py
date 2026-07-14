from flask import Flask, render_template, request, jsonify
from chat_engine import ask_llm

app = Flask(__name__)


@app.route("/")
def home():
    """
    Home Page
    """
    return render_template("index.html")


@app.route("/chat", methods=["POST"])
def chat():

    try:

        data = request.get_json()

        question = data.get("message", "").strip()

        if question == "":
            return jsonify({
                "status": "error",
                "response": "Please enter a question."
            })

        answer = ask_llm(question)

        return jsonify({
            "status": "success",
            "response": answer
        })

    except Exception as e:

        return jsonify({
            "status": "error",
            "response": str(e)
        })


if __name__ == "__main__":

    app.run(
    host="0.0.0.0",
    port=5000,
    debug=False,
    use_reloader=False
)