import argparse

from tfkit import load_trained_model


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--model", required=True, type=str)
    parser.add_argument("--dumpdir", required=True, type=str)
    arg = parser.parse_args()

    model, model_type = load_trained_model(arg.model)
    model.pretrained.save_pretrained(arg.dumpdir)
    print('==================')
    print("Finish model dump.")


if __name__ == "__main__":
    main()
