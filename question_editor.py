"""
問題作成用GUIエディタ
"""
import customtkinter as ctk
from tkinter import messagebox, filedialog
from utils import save_questions_to_csv, save_questions_to_json, load_questions
from constants import (
    EDITOR_WINDOW_SIZE, FONT_FAMILY, FONT_SIZE_SECTION, FONT_SIZE_SUBTITLE,
    FONT_SIZE_NORMAL, FONT_SIZE_BUTTON, FONT_SIZE_LABEL, FONT_SIZE_SMALL,
    MIN_CHOICES, COLOR_DEFAULT, COLOR_LIGHT_GRAY, COLOR_DARK_GRAY,
    COLOR_GRAY, COLOR_GRAY_HOVER,
    MSG_NO_QUESTIONS, MSG_NO_QUESTION_TEXT, MSG_MIN_CHOICES, MSG_QUESTION_ADDED
)


class QuestionEditor:
    """問題作成エディタクラス"""

    def __init__(self, window):
        self.window = window
        self.window.title("問題作成エディタ")
        self.window.geometry(EDITOR_WINDOW_SIZE)

        self.questions = []
        self.current_question = None
        self.selected_question_index = None  # 選択された問題のインデックス

        self.setup_ui()

    def setup_ui(self):
        """UIをセットアップ"""
        # メインコンテナ
        main_container = ctk.CTkFrame(self.window)
        main_container.pack(fill="both", expand=True, padx=20, pady=20)

        # タイトル
        title = ctk.CTkLabel(
            main_container,
            text="問題作成エディタ",
            font=(FONT_FAMILY, FONT_SIZE_SECTION, "bold")
        )
        title.pack(pady=(0, 20))

        # スクロール可能なフレーム
        self.scrollable_frame = ctk.CTkScrollableFrame(main_container)
        self.scrollable_frame.pack(fill="both", expand=True)

        # 質問入力エリア
        self.create_question_input_area()

        # 選択肢入力エリア
        self.create_choices_area()

        # 問題リストエリア
        self.create_question_list_area()

        # ボタンエリア
        self.create_button_area()

    def create_question_input_area(self):
        """質問入力エリアを作成"""
        question_frame = ctk.CTkFrame(self.scrollable_frame)
        question_frame.pack(fill="x", pady=(0, 15), padx=5)

        # 内部パディング
        inner_frame = ctk.CTkFrame(question_frame, fg_color="transparent")
        inner_frame.pack(fill="both", expand=True, padx=20, pady=20)

        label = ctk.CTkLabel(
            inner_frame,
            text="質問文",
            font=(FONT_FAMILY, FONT_SIZE_NORMAL, "bold")
        )
        label.pack(anchor="w", pady=(0, 10))

        self.question_text = ctk.CTkTextbox(
            inner_frame,
            height=100,
            font=(FONT_FAMILY, FONT_SIZE_LABEL),
            wrap="word"
        )
        self.question_text.pack(fill="x")

    def create_choices_area(self):
        """選択肢入力エリアを作成"""
        choices_frame = ctk.CTkFrame(self.scrollable_frame)
        choices_frame.pack(fill="x", pady=(0, 15), padx=5)

        # 内部パディング
        inner_frame = ctk.CTkFrame(choices_frame, fg_color="transparent")
        inner_frame.pack(fill="both", expand=True, padx=20, pady=20)

        label = ctk.CTkLabel(
            inner_frame,
            text="選択肢",
            font=(FONT_FAMILY, FONT_SIZE_NORMAL, "bold")
        )
        label.pack(anchor="w", pady=(0, 10))

        # 選択肢入力フィールドを保持するフレーム
        self.choices_container = ctk.CTkFrame(inner_frame, fg_color="transparent")
        self.choices_container.pack(fill="x")

        self.choice_entries = []

        # 初期選択肢（2つ）
        for i in range(2):
            self.add_choice_entry()

        # 選択肢追加ボタン
        add_choice_btn = ctk.CTkButton(
            inner_frame,
            text="+ 選択肢を追加",
            command=self.add_choice_entry,
            font=(FONT_FAMILY, FONT_SIZE_LABEL),
            width=150,
            height=35
        )
        add_choice_btn.pack(anchor="w", pady=(10, 0))

    def add_choice_entry(self):
        """選択肢入力フィールドを追加"""
        choice_frame = ctk.CTkFrame(self.choices_container, fg_color="transparent")
        choice_frame.pack(fill="x", pady=5)

        num_label = ctk.CTkLabel(
            choice_frame,
            text=f"{len(self.choice_entries) + 1}.",
            font=(FONT_FAMILY, FONT_SIZE_LABEL),
            width=30
        )
        num_label.pack(side="left", padx=(0, 5))

        entry = ctk.CTkEntry(
            choice_frame,
            font=(FONT_FAMILY, FONT_SIZE_LABEL),
            height=35
        )
        entry.pack(side="left", fill="x", expand=True, padx=5)

        # 削除ボタン（3つ以上ある場合のみ表示）
        if len(self.choice_entries) >= MIN_CHOICES:
            delete_btn = ctk.CTkButton(
                choice_frame,
                text="✕",
                command=lambda: self.remove_choice_entry(choice_frame, entry),
                font=(FONT_FAMILY, FONT_SIZE_LABEL),
                width=40,
                height=35,
                fg_color=COLOR_GRAY,
                hover_color=COLOR_GRAY_HOVER
            )
            delete_btn.pack(side="right")

        self.choice_entries.append(entry)

    def remove_choice_entry(self, frame, entry):
        """選択肢入力フィールドを削除"""
        if len(self.choice_entries) <= MIN_CHOICES:
            messagebox.showwarning("警告", MSG_MIN_CHOICES)
            return

        self.choice_entries.remove(entry)
        frame.destroy()

        # 番号を振り直す
        for i, entry in enumerate(self.choice_entries):
            # 親フレームのラベルを更新
            parent = entry.master
            for widget in parent.winfo_children():
                if isinstance(widget, ctk.CTkLabel):
                    widget.configure(text=f"{i + 1}.")
                    break

    def create_question_list_area(self):
        """問題リストエリアを作成"""
        list_frame = ctk.CTkFrame(self.scrollable_frame)
        list_frame.pack(fill="both", expand=True, pady=(0, 15), padx=5)

        # 内部パディング
        inner_frame = ctk.CTkFrame(list_frame, fg_color="transparent")
        inner_frame.pack(fill="both", expand=True, padx=20, pady=20)

        label = ctk.CTkLabel(
            inner_frame,
            text="作成した問題一覧",
            font=("Yu Gothic", 14, "bold")
        )
        label.pack(anchor="w", pady=(0, 10))

        # 問題リスト用のスクロール可能なフレーム
        self.question_list_frame = ctk.CTkScrollableFrame(
            inner_frame,
            height=200
        )
        self.question_list_frame.pack(fill="both", expand=True, pady=(0, 10))

        # 操作ボタンフレーム
        control_frame = ctk.CTkFrame(inner_frame, fg_color="transparent")
        control_frame.pack(fill="x")

        # 上に移動ボタン
        move_up_btn = ctk.CTkButton(
            control_frame,
            text="↑ 上へ",
            command=self.move_question_up,
            font=("Yu Gothic", 12),
            width=100,
            height=35
        )
        move_up_btn.pack(side="left", padx=(0, 5))

        # 下に移動ボタン
        move_down_btn = ctk.CTkButton(
            control_frame,
            text="↓ 下へ",
            command=self.move_question_down,
            font=("Yu Gothic", 12),
            width=100,
            height=35
        )
        move_down_btn.pack(side="left", padx=5)

        # 削除ボタン
        delete_btn = ctk.CTkButton(
            control_frame,
            text="✕ 削除",
            command=self.delete_selected_question,
            font=("Yu Gothic", 12),
            width=100,
            height=35,
            fg_color="gray40",
            hover_color="gray30"
        )
        delete_btn.pack(side="left", padx=5)

    def create_button_area(self):
        """ボタンエリアを作成"""
        button_frame = ctk.CTkFrame(self.scrollable_frame, fg_color="transparent")
        button_frame.pack(fill="x", pady=20)

        # 問題追加ボタン
        add_btn = ctk.CTkButton(
            button_frame,
            text="問題を追加",
            command=self.add_question,
            font=("Yu Gothic", 14, "bold"),
            width=150,
            height=45
        )
        add_btn.pack(side="left", padx=5)

        # 保存ボタン
        save_btn = ctk.CTkButton(
            button_frame,
            text="保存",
            command=self.save_questions,
            font=("Yu Gothic", 14, "bold"),
            width=150,
            height=45
        )
        save_btn.pack(side="left", padx=5)

        # 読み込みボタン
        load_btn = ctk.CTkButton(
            button_frame,
            text="読み込み",
            command=self.load_questions,
            font=("Yu Gothic", 14, "bold"),
            width=150,
            height=45
        )
        load_btn.pack(side="left", padx=5)

    def add_question(self):
        """問題を追加"""
        question_text = self.question_text.get("1.0", "end").strip()

        if not question_text:
            messagebox.showwarning("警告", MSG_NO_QUESTION_TEXT)
            return

        choices = []
        for entry in self.choice_entries:
            choice = entry.get().strip()
            if choice:
                choices.append(choice)

        if len(choices) < MIN_CHOICES:
            messagebox.showwarning("警告", MSG_MIN_CHOICES)
            return

        question = {
            'text': question_text,
            'choices': choices
        }

        self.questions.append(question)

        # 選択をリセット
        self.selected_question_index = None

        # リストを更新
        self.refresh_question_list()

        # 入力フィールドをクリア
        self.clear_inputs()

        messagebox.showinfo("成功", MSG_QUESTION_ADDED)

    def delete_selected_question(self):
        """選択した問題を削除"""
        if not self.questions:
            messagebox.showwarning("警告", "削除する問題がありません")
            return

        if self.selected_question_index is None:
            messagebox.showwarning("警告", "削除する問題を選択してください")
            return

        if messagebox.askyesno("確認", f"問題{self.selected_question_index + 1}を削除しますか？"):
            del self.questions[self.selected_question_index]
            self.selected_question_index = None
            self.refresh_question_list()

    def move_question_up(self):
        """選択した問題を上に移動"""
        if self.selected_question_index is None:
            messagebox.showwarning("警告", "移動する問題を選択してください")
            return

        if self.selected_question_index == 0:
            messagebox.showwarning("警告", "これ以上上に移動できません")
            return

        # 問題を入れ替え
        idx = self.selected_question_index
        self.questions[idx], self.questions[idx - 1] = self.questions[idx - 1], self.questions[idx]
        self.selected_question_index = idx - 1
        self.refresh_question_list()

    def move_question_down(self):
        """選択した問題を下に移動"""
        if self.selected_question_index is None:
            messagebox.showwarning("警告", "移動する問題を選択してください")
            return

        if self.selected_question_index >= len(self.questions) - 1:
            messagebox.showwarning("警告", "これ以上下に移動できません")
            return

        # 問題を入れ替え
        idx = self.selected_question_index
        self.questions[idx], self.questions[idx + 1] = self.questions[idx + 1], self.questions[idx]
        self.selected_question_index = idx + 1
        self.refresh_question_list()

    def refresh_question_list(self):
        """問題リストを再表示"""
        # 既存のウィジェットを削除
        for widget in self.question_list_frame.winfo_children():
            widget.destroy()

        # 各問題をフレームとして表示
        for i, question in enumerate(self.questions):
            self.create_question_item(i, question)

    def create_question_item(self, index, question):
        """問題アイテムを作成"""
        # 問題フレーム
        item_frame = ctk.CTkFrame(
            self.question_list_frame,
            fg_color=COLOR_DEFAULT if index == self.selected_question_index else [COLOR_LIGHT_GRAY, COLOR_DARK_GRAY]
        )
        item_frame.pack(fill="x", pady=5, padx=5)

        # クリックで選択
        def select_question(event=None):
            self.selected_question_index = index
            self.refresh_question_list()

        item_frame.bind("<Button-1>", select_question)

        # 問題番号と内容
        question_text = f"Q{index + 1}: {question['text'][:60]}"
        if len(question['text']) > 60:
            question_text += "..."

        label = ctk.CTkLabel(
            item_frame,
            text=question_text,
            font=(FONT_FAMILY, FONT_SIZE_LABEL),
            anchor="w"
        )
        label.pack(fill="x", padx=10, pady=10)
        label.bind("<Button-1>", select_question)

    def clear_inputs(self):
        """入力フィールドをクリア"""
        self.question_text.delete("1.0", "end")

        for entry in self.choice_entries:
            entry.delete(0, "end")

    def save_questions(self):
        """問題ファイルに保存（CSV/JSON対応）"""
        if not self.questions:
            messagebox.showwarning("警告", MSG_NO_QUESTIONS)
            return

        filepath = filedialog.asksaveasfilename(
            defaultextension=".csv",
            filetypes=[
                ("CSVファイル", "*.csv"),
                ("JSONファイル", "*.json"),
                ("すべてのファイル", "*.*")
            ],
            initialfile="questions.csv"
        )

        if filepath:
            # 拡張子に応じて保存形式を決定
            if filepath.endswith('.json'):
                success = save_questions_to_json(self.questions, filepath)
            else:
                success = save_questions_to_csv(self.questions, filepath)

            if success:
                messagebox.showinfo("成功", f"ファイルに保存しました\n{filepath}")
            else:
                messagebox.showerror("エラー", "保存に失敗しました")

    def load_questions(self):
        """問題ファイルから読み込み（CSV/JSON対応）"""
        filepath = filedialog.askopenfilename(
            filetypes=[
                ("サポートファイル", "*.csv;*.json"),
                ("CSVファイル", "*.csv"),
                ("JSONファイル", "*.json"),
                ("すべてのファイル", "*.*")
            ]
        )

        if filepath:
            from utils import load_questions
            questions = load_questions(filepath)

            if questions:
                self.questions = questions
                self.selected_question_index = None
                self.refresh_question_list()
                messagebox.showinfo("成功", f"{len(questions)}個の問題を読み込みました")
            else:
                messagebox.showwarning("警告", "問題を読み込めませんでした")
