from src.model import DATA_PATH, FraudModel


if __name__ == "__main__":
    model = FraudModel()
    metrics = model.train(DATA_PATH)
    print(metrics["models"])
