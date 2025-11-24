from flask import Flask, render_template, request
import numpy as np
import joblib

app = Flask(__name__)

# Load model and scaler
model = joblib.load("model.pkl")
scaler = joblib.load("scaler.pkl")

# 33 features EXACTLY as model was trained
FEATURE_COLUMNS = [
    "sessionIndex",
    "rep",
    "H.period",
    "DD.period.t",
    "UD.period.t",
    "H.t",
    "DD.t.i",
    "UD.t.i",
    "H.i",
    "DD.i.e",
    "UD.i.e",
    "H.e",
    "DD.e.five",
    "UD.e.five",
    "H.five",
    "DD.five.Shift.r",
    "UD.five.Shift.r",
    "H.Shift.r",
    "DD.Shift.r.o",
    "UD.Shift.r.o",
    "H.o",
    "DD.o.a",
    "UD.o.a",
    "H.a",
    "DD.a.n",
    "UD.a.n",
    "H.n",
    "DD.n.l",
    "UD.n.l",
    "H.l",
    "DD.l.Return",
    "UD.l.Return",
    "H.Return"
]

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/predict", methods=["POST"])
def predict():
    try:
        # Collect values in correct order
        input_values = []
        for feature in FEATURE_COLUMNS:
            value = request.form.get(feature)
            input_values.append(float(value))

        # Convert to array
        input_array = np.array(input_values).reshape(1, -1)

        # Scale using original scaler
        scaled_input = scaler.transform(input_array)

        # Predict with model
        prediction = model.predict(scaled_input)[0]

        result = "Real User (Champion)" if prediction == 1 else "Impostor (Challenger)"

    except Exception as e:
        result = f"Error: {e}"

    return render_template("index.html", result=result)

if __name__ == "__main__":
    app.run(debug=True)
