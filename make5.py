import argparse


word_path = './words.txt'


def main(save_path):
    with open(word_path, 'r') as f:
        words = f.read().split('\n')
    words5 = filter(lambda w: len(w) == 5, words)

    with open(save_path, 'w') as f:
        f.write('\n'.join(words5))


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Input save path')
    parser.add_argument('save_path', type=str,
                        help='Path to save word of length 5')

    args = parser.parse_args()
    save_path = args.save_path
    main(save_path)
