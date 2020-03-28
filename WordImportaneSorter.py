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
    :param line: The input line as a string of the form "word (score) word (score)".
    :return: A 2d array of word to importance.
    """
    words = line.split(" ")
    print("Processing line: " + line)
    importance = []

    if (len(words) - 1) % 2 != 0:
        print("Invalid line format.")
    else:
        for index in range(1, len(words), 2):
            word = words[index]
            score_str = words[index + 1]
            score = float(score_str[1:len(score_str) - 2])
            importance.append([word, score])

    return importance


def create_bins(importance_scores):
    """
    Given an array of importance scores, separates out the words into three bins.
    :param importance_scores: The array of importance scores.
    :return: A map of the words categorized by score.
    """
    bins = {'<= 0.299': [], '<= 0.549': [], '> 0.549': []}
    for score in importance_scores:
        if score[1] < 0.299:
            bins['<= 0.299'].append(score)
        elif score[1] < 0.549:
            bins['<= 0.549'].append(score)
        else:
            bins['> 0.549'].append(score)

    for key in bins.keys():
        bins[key].sort(key=lambda x: x[1])

    return bins


def write_to_file(bins, file_name):
    """
    Writes the content of the bins to a file with the input name.
    :param bins: The bins containing the words in categories.
    :param file_name: The name of the file to write to.
    :return: None.
    """
    file_content = ''
    file_content = file_content + ('<= 0.299' + ': \n')
    for word in bins['<= 0.299']:
        file_content = file_content + (str(word[0]) + '(' + str(word[1]) + ')' + '\n')

    file_content = file_content + '\n\n'
    file_content = file_content + ('<= 0.549' + ': \n')
    for word in bins['<= 0.549']:
        file_content = file_content + (str(word[0]) + '(' + str(word[1]) + ')' + '\n')

    file_content = file_content + '\n\n'
    file_content = file_content + ('> 0.549' + ': \n')
    for word in bins['> 0.549']:
        file_content = file_content + (str(word[0]) + '(' + str(word[1]) + ')' + '\n')

    file = None
    try:
        file = open(file_name, "w")
        file.write(file_content)
        print("File " + file_name + " saved successfully.")
    except:
        print("An error occurred while writing the file: ")
    finally:
        if file is not None:
            file.close()


def main():
    """
    Reads the file's content, bins the words into importance categories and sorts them,
    then writes the output to a file.
    """
    lines = read_file("./files/phase3_simp.txt")

    importance_scores = []
    # using a range to skip the first line that lists only the params
    for index in range(1, len(lines)):
        line_importance_scores = extract_word_scores(lines[index])

        for imp in line_importance_scores:
            importance_scores.append(imp)

    bins = create_bins(importance_scores)

    write_to_file(bins, './files/bins.txt')


if __name__ == "__main__":
    main()
