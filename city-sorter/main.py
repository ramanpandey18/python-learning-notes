def main():
    # Open the input file
    try:
        input_file = open("cities.txt", "r")
    except OSError as error:
        print("Error opening input file:", error)
        return

    cities = []
    # Read the file line by line
    try:
        for line in input_file:
            city = line.strip()

            if city != "":
                cities.append(city)
    except OSError as error:
        print("Error reading input file:", error)
        input_file.close()
        return
    input_file.close()
    # Sort cities lexicographically
    cities.sort()

    # Create the output file
    try:
        output_file = open("sorted.txt", "w")
    except OSError as error:
        print("Error creating output file:", error)
        return

    # Write sorted cities to the output file
    try:
        for city in cities:
            output_file.write(city + "\n")
    finally:
        output_file.close()

    print("Sorting completed.")
    print("Cities processed:", len(cities))


if __name__ == "__main__":
    main()
