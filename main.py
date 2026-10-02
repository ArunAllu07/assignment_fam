from src.pipeline import run_pipeline


def main():
    input_file = "data/output_file.csv"
    output_dir = "output"

    validation = run_pipeline(
        input_file,
        output_dir
    )

    if all(validation.values()):
        print("\nProcessing completed successfully.")
    else:
        print("\nProcessing completed with validation errors.")


if __name__ == "__main__":
    main()