from __future__ import annotations

from flask import Flask, flash, redirect, render_template, request, url_for

from src.model import DATA_PATH, FraudModel


app = Flask(__name__)
app.secret_key = "local-development-key"
fraud_model = FraudModel()


def initialize_model() -> None:
    if fraud_model.load():
        return
    if DATA_PATH.exists():
        fraud_model.train()


initialize_model()


@app.get("/")
def dashboard():
    return render_template(
        "index.html",
        model_ready=fraud_model.pipeline is not None,
        metrics=fraud_model.metrics,
        class_distribution=fraud_model.class_distribution,
        features=fraud_model.feature_names,
    )


@app.post("/train")
def train():
    try:
        fraud_model.train()
        flash("Model başarıyla eğitildi ve yerel olarak kaydedildi.", "success")
    except (FileNotFoundError, ValueError) as error:
        flash(str(error), "error")
    return redirect(url_for("dashboard"))


@app.post("/predict")
def predict():
    if fraud_model.pipeline is None:
        flash("Önce data/creditcard.csv dosyasını ekleyip modeli eğitin.", "error")
        return redirect(url_for("dashboard"))

    values = {
        key: float(value)
        for key, value in request.form.items()
        if key in fraud_model.feature_names and value.strip()
    }
    try:
        result = fraud_model.predict(values)
        return render_template(
            "index.html",
            model_ready=True,
            metrics=fraud_model.metrics,
            class_distribution=fraud_model.class_distribution,
            features=fraud_model.feature_names,
            prediction=result,
            submitted_values=values,
        )
    except (TypeError, ValueError) as error:
        flash(f"İşlem verileri geçersiz: {error}", "error")
        return redirect(url_for("dashboard"))


if __name__ == "__main__":
    app.run(debug=True, host="127.0.0.1", port=5000)
