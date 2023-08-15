from ovito.io import import_file
from pathlib import Path


def main():
    pipeline = import_file(Path("example_01", "lmp.h5"))
    data = pipeline.compute()

    print("Particle properties:")
    for prop in data.particles.keys():
        print(prop)
    print("\nAttributes:")
    for attr in data.attributes.keys():
        print(attr)


if __name__ == "__main__":
    main()
