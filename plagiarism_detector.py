import string

# Helper: Clean and split the essay into words
def preprocess_text(file_path):
    with open(file_path, 'r') as file:
        text = file.read()
    # Remove punctuation and convert to lowercase
    translator = str.maketrans('', '', string.punctuation)
    cleaned_text = text.translate(translator).lower()
    words = cleaned_text.split()
    return words

# Step 1: Read both essays
essay1_words = preprocess_text('essay1.txt')
essay2_words = preprocess_text('essay2.txt')

# Step 2: Count word occurrences in both essays
from collections import Counter
count1 = Counter(essay1_words)
count2 = Counter(essay2_words)

# Step 3: Find common words
common_words = set(count1.keys()) & set(count2.keys())

print("🔍 Common Words:")
for word in sorted(common_words):
    print(f"{word}: Essay 1 → {count1[word]} | Essay 2 → {count2[word]}")

# Step 4: Word Search
def search_word(word):
    word = word.lower()
    found_in_essay1 = count1.get(word, 0)
    found_in_essay2 = count2.get(word, 0)
    
    if found_in_essay1 == 0 and found_in_essay2 == 0:
        return False
    else:
        print(f"\n🔎 Word: '{word}'")
        print(f"Essay 1: {found_in_essay1} time(s)")
        print(f"Essay 2: {found_in_essay2} time(s)")
        return True

# Example word search:
# search_word("software")

# Step 5: Calculate plagiarism percentage
set1 = set(essay1_words)
set2 = set(essay2_words)

intersection = set1 & set2
union = set1 | set2

plagiarism_percentage = (len(intersection) / len(union)) * 100

print(f"\n📊 Plagiarism Percentage: {plagiarism_percentage:.2f}%")

# Step 6: Decision
if plagiarism_percentage >= 50:
    print("⚠️ Plagiarism Detected")
else:
    print("✅ No Plagiarism Detected")

# Optional: Prompt user for word search
while True:
    user_input = input("\nEnter a word to search (or type 'exit' to quit): ")
    if user_input.lower() == 'exit':
        break
    result = search_word(user_input)
    if result is False:
        print("Word not found in one or both essays.")
