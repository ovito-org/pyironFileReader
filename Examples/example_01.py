from ovito.io import import_file


def main():
    pipeline = import_file("lmp.h5")
    data = pipeline.compute()

    print("Particle properties:")
    for prop in data.particles.keys():
        print(prop)
    print("\nAttributes:")
    for attr in data.attributes.keys():
        print(attr)


if __name__ == "__main__":
    main()
