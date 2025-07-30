import string
from collections import Counter

# Functions

# This function reads and preprocesses text by removing punctuation, converting to lowercase, and splitting into words
def preprocess_text(file_path):
    try:
        with open(file_path, 'r') as file:
            text = file.read()
    except FileNotFoundError:
        print(f"File '{file_path}' not found.")
        return []

    translator = str.maketrans('', '', string.punctuation)
    cleaned = text.translate(translator).lower()
    return cleaned.split()

# Count how many times each word appears
def count_words(words):
    return Counter(words)

# Get a sorted list of words that are common in both essays
def get_common_words(counter1, counter2):
    return sorted(set(counter1.keys()) & set(counter2.keys()))

# Search for a specific word in both essays and return how many times it was found
def search_word(word, count1, count2):
    word = word.lower()
    found1 = count1.get(word, 0)
    found2 = count2.get(word, 0)

    if found1 == 0 and found2 == 0:
        return False, found1, found2
    return True, found1, found2

# Calculate how similar the essays are based on common and unique words
def calculate_plagiarism(set1, set2):
    intersection = set1 & set2
    union = set1 | set2
    if len(union) == 0:
        return 0
    return (len(intersection) / len(union)) * 100, len(intersection), len(union)

# Display a nice side-by-side view of words found in both essays
def print_common_words(counter1, counter2):
    common = get_common_words(counter1, counter2)
    if not common:
        print("No common words found between the two essays.")
        return

    print("\nCommon Words Comparison")
    print("-" * 40)
    print(f"{'Word':<15} {'Essay 1':<10} {'Essay 2':<10}")
    print("-" * 40)
    for word in common:
        print(f"{word:<15} {counter1[word]:<10} {counter2[word]:<10}")
    print("-" * 40)

# Feedback based on how similar the essays are
def personalized_feedback(score, intersection_count, union_count):
    print(f"\n- Plagiarism Analysis")
    print("-" * 40)
    print(f"- Common Words: {intersection_count}")
    print(f"- Total Unique Words: {union_count}")
    print(f"- Plagiarism Percentage: {score:.2f}%")

    if score >= 80:
        print("⚠️ Plagiarism detected, very high similarity! These essays are nearly identical. Consider rewriting or referencing sources properly.")
    elif score >= 50:
        print("⚠️ Plagiarism Detected.")
    else:
        print("✅ No plagiarism detected. These essays appear to be independently written.")

# Main Program

def main():
    print("\n------------------------------------------------------")
    print("       Welcome to Nelly's Plagiarism Detector")
    print("       A friendly tool to compare your two essays")
    print("------------------------------------------------------")

    # Load and preprocess both essays
    essay1 = preprocess_text('essay-1.txt')
    essay2 = preprocess_text('essay-2.txt')

    # Validate files were loaded correctly
    if not essay1 or not essay2:
        print("Unable to load essays. Make sure both files exist.")
        return

    # Word counting and set creation for comparison
    count1 = count_words(essay1)
    count2 = count_words(essay2)
    set1 = set(essay1)
    set2 = set(essay2)

    # Menu loop
    while True:
        print("\nChoose an Option:")
        print("1. View Common Words")
        print("2. Search for a Word")
        print("3. Calculate Plagiarism Percentage")
        print("4. Exit")

        choice = input("Enter your choice (1–4): ").strip()

        if choice == '1':
            print_common_words(count1, count2)

        elif choice == '2':
            word = input("Enter the word to search: ").strip()
            if not word.isalpha():
                print("Please enter a valid word (letters only).")
                continue
            found, f1, f2 = search_word(word, count1, count2)
            if found:
                print(f"\nFound '{word}': Essay 1 → {f1} time(s), Essay 2 → {f2} time(s)")
            else:
                print(f"'{word}' not found in either essay.")

        elif choice == '3':
            score, intersection_count, union_count = calculate_plagiarism(set1, set2)
            personalized_feedback(score, intersection_count, union_count)

        elif choice == '4':
            print("Exiting... Have a great day!")
            break

        else:
            print(" Invalid choice. Please pick a number between 1 and 4.")

# ----------- Run Program -----------

if __name__ == "__main__":
    main()