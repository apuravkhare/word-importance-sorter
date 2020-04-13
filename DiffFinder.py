import re
from WordImportaneSorter import categorize_words, write_to_file, read_file


def extract_id(string):
    return re.search('^id: \\((\\w+)\\)$', string).group(1)


def extract_scores(string):
    scores_match = re.search('^Scores: \\(#C #S #D #I\\) (\\d+) (\\d+) (\\d+) (\\d+)$', string)
    return [int(scores_match.group(1)), #c
            int(scores_match.group(2)), #s
            int(scores_match.group(3)), #d
            int(scores_match.group(4))] #i


def extract_part(string, begin):
    regex_str = "^" + str(begin) + "(.*)$"
    print(string)
    return re.search(regex_str, string).group(1)


def words(string):
    return re.split('\\s+', string)


class PhraseScore:
    def __init__(self, id, scores, ref, hyp, eval):
        self.id = extract_id(id)
        self.scores = extract_scores(scores)
        self.ref = words(extract_part(ref, 'REF:').lstrip().rstrip())
        self.hyp = words(extract_part(hyp, 'HYP:').lstrip().rstrip())
        self.eval = list(filter(lambda word: word != '', words(extract_part(eval, 'Eval:').lstrip().rstrip())))

    def get_error_words(self):
        print("Evaluating: " + self.id)

        if len(self.scores) > 0 and self.scores[1] == 0 and self.scores[2] == 0 and self.scores[3] == 0:
            return []
        # walk the arrays together, if there's an error, look at the type of error
        # for deletion or substitution, add as error word

        errors = []
        error_index = 0
        hyp_index = 0
        ref_index = 0

        while ref_index < len(self.ref):
            # print(self.ref[ref_index] + " - " + self.hyp[hyp_index])
            if self.ref[ref_index] == self.hyp[hyp_index]:
                ref_index += 1
                hyp_index += 1
            else:
                if self.eval[error_index] != 'I':
                    errors.append(self.ref[ref_index])

                ref_index += 1
                hyp_index += 1
                error_index += 1
                '''
                if self.eval[error_index] == 'I':
                    ref_index += 1
                elif self.eval[error_index] == 'D':
                    hyp_index += 1
                else:
                    ref_index += 1
                    hyp_index += 1
                '''

        return errors

    def __str__(self):
        return str(self.id) + 'ref: ' + str(self.ref) + 'eval_c: ' + str(self.eval)


def get_phrase_scores(lines):
    lines_count = len(lines)
    phrase_scores = []
    for line_index in range(0, lines_count):
        line = lines[line_index]
        if line.startswith('id:'):
            phrase_scores.append(PhraseScore(line, lines[line_index+1],
                                             lines[line_index+2], lines[line_index+3],
                                             lines[line_index+4]))

    return phrase_scores


def write_errors_to_file(bins, file_name):
    """
    Writes the content of the bins to a file with the input name.
    :param bins: The bins containing the words in categories.
    :param file_name: The name of the file to write to.
    :return: None.
    """
    file_content = ''

    file_content += 'SUMMARY: \n'
    file_content += 'Errors in range <= 0.299: ' + str(len(bins['<= 0.299'])) + '\n'
    file_content += 'Errors in range <= 0.549: ' + str(len(bins['<= 0.549'])) + '\n'
    file_content += 'Errors in range > 0.549: ' + str(len(bins['> 0.549'])) + '\n'
    file_content += '\n\n'
    file_content = file_content + ('<= 0.299' + ': \n')
    for word in bins['<= 0.299']:
        # file_content = file_content + (str(word[0]) + '(' + str(word[1]) + ')' + '\n')
        file_content = file_content + (word + '\n')

    file_content = file_content + '\n\n'
    file_content = file_content + ('<= 0.549' + ': \n')
    for word in bins['<= 0.549']:
        file_content = file_content + (word + '\n')

    file_content = file_content + '\n\n'
    file_content = file_content + ('> 0.549' + ': \n')
    for word in bins['> 0.549']:
        file_content = file_content + (word + '\n')

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
    lines = read_file("./files/DonnacruiseTravel2_transcript.txt.pra")
    phrase_scores = get_phrase_scores(lines)
    all_errors = []
    for ps in phrase_scores:
        errors = ps.get_error_words()
        all_errors.extend(errors)

    src_lines = read_file("./files/phase3_simp.txt")
    word_bins = categorize_words(src_lines)
    error_bins = {'<= 0.299': [], '<= 0.549': [], '> 0.549': []}

    for e in all_errors:
        error = e.lower()
        if error in word_bins['> 0.549']:
            error_bins['> 0.549'].append(error)
        elif error in word_bins['<= 0.549']:
            error_bins['<= 0.549'].append(error)
        else:
            error_bins['<= 0.299'].append(error)

    write_errors_to_file(error_bins, './files/error_bins.txt')


if __name__ == "__main__":
    main()
