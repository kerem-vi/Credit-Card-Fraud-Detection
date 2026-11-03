from src.model import DATA_PATH, FraudModel, build_comparison


if __name__ == "__main__":
    model = FraudModel()
    print(model.train(DATA_PATH))
    print(build_comparison(DATA_PATH))
