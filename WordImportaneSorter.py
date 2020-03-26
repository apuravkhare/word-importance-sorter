def read_file(file_path):
    """
    Reads the file at the give path.
    :param file_path: The lines in the file as a string array.
    :return: An array containing the lines in the file.
    """
    print("Reading file: " + file_path)
    file = None
    try:
        file = open(file_path, "r")
        lines = file.readlines()
        return lines
    except:
        print("An error occurred while reading the file.")
    finally:
        if file is not None:
            file.close()


def extract_word_scores(line):
    """
    Given a line, extracts the score for each word in that line.
    :param line: The input line as a string.
    :return: A 2d array of word to importance.
    """
    pass


def main():
    lines = read_file("./files/phase3_simp.txt")

    for line in lines:
        print(line)


if __name__ == "__main__":
    main()

