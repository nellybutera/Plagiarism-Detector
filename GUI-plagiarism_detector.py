import tkinter as tk
from tkinter import filedialog, messagebox, simpledialog
from collections import Counter
import string

# ------------ Helper Functions ------------

def preprocess_text(file_path):
    try:
        with open(file_path, 'r') as file:
            text = file.read()
        translator = str.maketrans('', '', string.punctuation)
        cleaned = text.translate(translator).lower()
        return cleaned.split()
    except FileNotFoundError:
        return []

def count_words(words):
    return Counter(words)

def get_common_words(counter1, counter2):
    return set(counter1.keys()) & set(counter2.keys())

def search_word(word, count1, count2):
    word = word.lower()
    found1 = count1.get(word, 0)
    found2 = count2.get(word, 0)
    return found1, found2

def calculate_plagiarism(set1, set2):
    intersection = set1 & set2
    union = set1 | set2
    if not union:
        return 0
    return (len(intersection) / len(union)) * 100

# ------------ GUI App ------------

class PlagiarismApp:
    def __init__(self, root):
        self.root = root
        self.root.title("📝 Plagiarism Detector by Nelly")
        self.root.geometry("600x400")
        self.root.configure(bg="#f0f0f0")

        self.essay1 = []
        self.essay2 = []
        self.count1 = Counter()
        self.count2 = Counter()
        self.set1 = set()
        self.set2 = set()

        self.setup_ui()

    def setup_ui(self):
        tk.Label(self.root, text="Plagiarism Detector", font=("Arial", 18, "bold"), bg="#f0f0f0").pack(pady=10)

        btn_frame = tk.Frame(self.root, bg="#f0f0f0")
        btn_frame.pack(pady=10)

        tk.Button(btn_frame, text="Load Essay 1", command=self.load_essay1, width=15).grid(row=0, column=0, padx=10)
        tk.Button(btn_frame, text="Load Essay 2", command=self.load_essay2, width=15).grid(row=0, column=1, padx=10)
        tk.Button(btn_frame, text="Check Common Words", command=self.show_common_words, width=20).grid(row=1, column=0, columnspan=2, pady=10)
        tk.Button(btn_frame, text="Search Word", command=self.search_word_gui, width=15).grid(row=2, column=0, padx=10)
        tk.Button(btn_frame, text="Calculate Plagiarism", command=self.check_plagiarism, width=20).grid(row=2, column=1, padx=10)
        tk.Button(btn_frame, text="How is plagiarism calculated?", command=self.show_explanation, width=35).grid(row=3, column=0, columnspan=2, pady=10)

        self.output = tk.Text(self.root, height=10, width=70)
        self.output.pack(pady=10)

    def load_essay1(self):
        file_path = filedialog.askopenfilename(title="Select Essay 1")
        self.essay1 = preprocess_text(file_path)
        self.count1 = count_words(self.essay1)
        self.set1 = set(self.essay1)
        messagebox.showinfo("Essay 1", "Essay 1 loaded successfully.")

    def load_essay2(self):
        file_path = filedialog.askopenfilename(title="Select Essay 2")
        self.essay2 = preprocess_text(file_path)
        self.count2 = count_words(self.essay2)
        self.set2 = set(self.essay2)
        messagebox.showinfo("Essay 2", "Essay 2 loaded successfully.")

    def show_common_words(self):
        if not self.essay1 or not self.essay2:
            messagebox.showerror("Error", "Please load both essays first.")
            return
        common = get_common_words(self.count1, self.count2)
        self.output.delete(1.0, tk.END)
        if common:
            self.output.insert(tk.END, "📌 Common Words:\n")
            for word in sorted(common):
                self.output.insert(tk.END, f"{word} → Essay 1: {self.count1[word]}, Essay 2: {self.count2[word]}\n")
        else:
            self.output.insert(tk.END, "No common words found.")

    def search_word_gui(self):
        if not self.essay1 or not self.essay2:
            messagebox.showerror("Error", "Please load both essays first.")
            return
        word = simpledialog.askstring("Search Word", "Enter the word to search:")
        if word:
            f1, f2 = search_word(word, self.count1, self.count2)
            self.output.delete(1.0, tk.END)
            if f1 == 0 and f2 == 0:
                self.output.insert(tk.END, f"❌ '{word}' not found in either essay.\n")
            else:
                self.output.insert(tk.END, f"✅ '{word}' found: Essay 1 → {f1}, Essay 2 → {f2}\n")

    def check_plagiarism(self):
        if not self.essay1 or not self.essay2:
            messagebox.showerror("Error", "Please load both essays first.")
            return
        percent = calculate_plagiarism(self.set1, self.set2)
        self.output.delete(1.0, tk.END)
        self.output.insert(tk.END, f"📊 Plagiarism Percentage: {percent:.2f}%\n")
        if percent >= 50:
            self.output.insert(tk.END, "⚠️ There is a high chance of plagiarism.\n")
        else:
            self.output.insert(tk.END, "✅ No plagiarism detected.\n")

    def show_explanation(self):
        explanation = (
            "🔍 Plagiarism is detected based on the overlap of unique words:\n\n"
            "We calculate:\n"
            "- Intersection: Common unique words between Essay 1 and Essay 2\n"
            "- Union: All unique words from both essays combined\n\n"
            "Then we compute:\n"
            "   plagiarism% = (intersection / union) * 100\n\n"
            "⚠️ If the result is 50% or more, the essays are considered plagiarized."
        )
        messagebox.showinfo("How Plagiarism is Calculated", explanation)

# ------------ Run App ------------

if __name__ == "__main__":
    root = tk.Tk()
    app = PlagiarismApp(root)
    root.mainloop()
