"""
アンケート回答用GUI
選択肢を選んだ理由を記述し、理由を書き終えてから選択肢を変更できるルールを実装
"""
import customtkinter as ctk
from tkinter import messagebox, filedialog
from utils import load_questions, save_response, get_timestamp
from logger import ActionLogger
from config_manager import ConfigManager
from constants import (
    SURVEY_WINDOW_SIZE, FONT_FAMILY, FONT_SIZE_NORMAL, FONT_SIZE_SUBTITLE,
    FONT_SIZE_LABEL, FONT_SIZE_BUTTON, COLOR_SELECTED, COLOR_SELECTED_HOVER,
    COLOR_DEFAULT, COLOR_DEFAULT_HOVER, COLOR_GRAY, COLOR_GRAY_HOVER,
    MSG_NO_CHOICE_SELECTED, MSG_NO_REASON, MSG_CANNOT_CHANGE_CHOICE,
    MSG_CHANGE_DISABLED_STATUS, MSG_REASON_STARTED_STATUS, MSG_CAN_CHANGE_STATUS
)
import uuid
import os


class SurveyInterface:
    def __init__(self, window):
        self.window = window
        self.window.title("アンケート回答")
        self.window.geometry(SURVEY_WINDOW_SIZE)

        self.questions = []
        self.current_question_index = 0
        self.responses = []
        self.respondent_id = str(uuid.uuid4())[:8]

        # 設定を読み込み
        self.config_manager = ConfigManager()

        # ログ記録（設定から出力先を取得）
        log_path = self.config_manager.get_log_path(self.respondent_id)
        self.logger = ActionLogger(log_path)

        # 状態管理
        self.selected_choice = None
        self.reason_started = False  # 理由入力が開始されたか

        # ウィジェット
        self.choice_buttons = []
        self.reason_text = None

        self.load_questions_dialog()

    def load_questions_dialog(self):
        """問題を読み込むダイアログ"""
        # 設定から問題ファイルのパスを取得
        filepath = self.config_manager.get_questions_path()

        # 設定にパスがない場合は手動で選択
        if not filepath or not os.path.exists(filepath):
            filepath = filedialog.askopenfilename(
                title="アンケートファイルを選択",
                filetypes=[
                    ("サポートファイル", "*.csv;*.json"),
                    ("CSVファイル", "*.csv"),
                    ("JSONファイル", "*.json"),
                    ("すべてのファイル", "*.*")
                ]
            )

        if not filepath:
            self.window.destroy()
            return

        self.questions = load_questions(filepath)

        if not self.questions:
            messagebox.showerror("エラー", "問題を読み込めませんでした")
            self.window.destroy()
            return

        self.setup_ui()
        self.display_question()

    def setup_ui(self):
        """UIをセットアップ"""
        # メインコンテナ
        main_container = ctk.CTkFrame(self.window)
        main_container.pack(fill="both", expand=True, padx=30, pady=30)

        # ヘッダー
        header_frame = ctk.CTkFrame(main_container, fg_color="transparent")
        header_frame.pack(fill="x", pady=(0, 20))

        self.progress_label = ctk.CTkLabel(
            header_frame,
            text="",
            font=(FONT_FAMILY, FONT_SIZE_LABEL)
        )
        self.progress_label.pack(anchor="w")

        # スクロール可能なフレーム
        scrollable_frame = ctk.CTkScrollableFrame(main_container, height=500)
        scrollable_frame.pack(fill="both", expand=True)

        # 質問テキスト
        self.question_label = ctk.CTkLabel(
            scrollable_frame,
            text="",
            font=(FONT_FAMILY, FONT_SIZE_SUBTITLE, "bold"),
            wraplength=700,
            justify="left"
        )
        self.question_label.pack(anchor="w", pady=(0, 20))

        # 選択肢エリア
        self.choices_frame = ctk.CTkFrame(scrollable_frame, fg_color="transparent")
        self.choices_frame.pack(fill="both", pady=(0, 20))

        # 理由入力エリア
        reason_container = ctk.CTkFrame(scrollable_frame, fg_color="transparent")
        reason_container.pack(fill="both", expand=True, pady=(10, 0))

        reason_label = ctk.CTkLabel(
            reason_container,
            text="選択した理由を記入してください",
            font=(FONT_FAMILY, FONT_SIZE_NORMAL, "bold")
        )
        reason_label.pack(anchor="w", pady=(0, 10))

        self.reason_text = ctk.CTkTextbox(
            reason_container,
            height=150,
            font=(FONT_FAMILY, FONT_SIZE_LABEL),
            wrap="word"
        )
        self.reason_text.pack(fill="both", expand=True)
        self.reason_text.configure(state="disabled")

        # 理由入力のイベント監視
        self.reason_text.bind("<KeyPress>", self.on_reason_keypress)

        # 書き直しボタン
        self.rewrite_button = ctk.CTkButton(
            reason_container,
            text="理由を書き直す",
            command=self.rewrite_reason,
            font=(FONT_FAMILY, FONT_SIZE_BUTTON, "bold"),
            width=200,
            height=40,
            state="disabled",
            fg_color=COLOR_GRAY,
            hover_color=COLOR_GRAY_HOVER
        )
        self.rewrite_button.pack(anchor="w", pady=(10, 0))

        # 状態表示ラベル
        self.status_label = ctk.CTkLabel(
            reason_container,
            text="",
            font=(FONT_FAMILY, FONT_SIZE_LABEL),
            text_color="red"
        )
        self.status_label.pack(anchor="w", pady=(5, 0))

        # ナビゲーションボタン
        nav_frame = ctk.CTkFrame(main_container, fg_color="transparent")
        nav_frame.pack(fill="x", pady=(20, 0))

        self.next_button = ctk.CTkButton(
            nav_frame,
            text="次の問題へ",
            command=self.next_question,
            font=(FONT_FAMILY, FONT_SIZE_BUTTON, "bold"),
            width=150,
            height=45,
            state="disabled"
        )
        self.next_button.pack(side="right")

        self.prev_button = ctk.CTkButton(
            nav_frame,
            text="前の問題へ",
            command=self.prev_question,
            font=(FONT_FAMILY, FONT_SIZE_BUTTON),
            width=150,
            height=45,
            fg_color=COLOR_GRAY,
            hover_color=COLOR_GRAY_HOVER,
            state="disabled"
        )
        self.prev_button.pack(side="left")

    def display_question(self):
        """現在の質問を表示"""
        if self.current_question_index >= len(self.questions):
            self.submit_survey()
            return

        question = self.questions[self.current_question_index]

        # 進捗表示
        self.progress_label.configure(
            text=f"問題 {self.current_question_index + 1} / {len(self.questions)}"
        )

        # 質問文表示
        self.question_label.configure(text=question['text'])

        # 選択肢をクリア
        for widget in self.choices_frame.winfo_children():
            widget.destroy()

        self.choice_buttons = []

        # 選択肢を表示
        for i, choice in enumerate(question['choices']):
            self.create_choice_button(choice, i)

        # 状態をリセット
        self.selected_choice = None
        self.reason_started = False

        # 理由入力をクリアして無効化
        self.reason_text.configure(state="normal")
        self.reason_text.delete("1.0", "end")
        self.reason_text.configure(state="disabled")

        # ボタンの状態を更新
        self.rewrite_button.configure(state="disabled")
        self.next_button.configure(state="disabled")
        self.status_label.configure(text="")

        # 前へボタンの状態
        if self.current_question_index > 0:
            self.prev_button.configure(state="normal")
        else:
            self.prev_button.configure(state="disabled")

    def create_choice_button(self, choice_text, index):
        """選択肢ボタンを作成"""
        choice_button = ctk.CTkButton(
            self.choices_frame,
            text=choice_text,
            command=lambda: self.select_choice(choice_text, index),
            font=(FONT_FAMILY, FONT_SIZE_BUTTON),
            height=50,
            anchor="w"
        )
        choice_button.pack(fill="x", pady=5)

        self.choice_buttons.append(choice_button)

    def select_choice(self, choice_text, index):
        """選択肢を選択"""
        # 理由を書き始めた後は選択不可
        if self.reason_started:
            self.status_label.configure(text=MSG_CHANGE_DISABLED_STATUS)
            messagebox.showwarning("変更できません", MSG_CANNOT_CHANGE_CHOICE)
            return

        # 選択を更新
        self.selected_choice = choice_text

        # ログに記録
        self.logger.log_choice_selection(
            self.current_question_index + 1,
            choice_text
        )

        # 選択したボタンの色を変更
        self._update_choice_button_colors(index)

        # 理由入力を有効化してリセット
        self._reset_reason_input()

    def _update_choice_button_colors(self, selected_index):
        """選択肢ボタンの色を更新"""
        for i, btn in enumerate(self.choice_buttons):
            if i == selected_index:
                # 選択されたボタンは緑色に
                btn.configure(fg_color=COLOR_SELECTED, hover_color=COLOR_SELECTED_HOVER)
            else:
                # 他のボタンはデフォルトに戻す
                btn.configure(fg_color=COLOR_DEFAULT, hover_color=COLOR_DEFAULT_HOVER)

    def _reset_reason_input(self):
        """理由入力エリアをリセット"""
        self.reason_text.configure(state="normal")
        self.reason_text.delete("1.0", "end")
        self.reason_started = False
        self.rewrite_button.configure(state="disabled")
        self.next_button.configure(state="disabled")
        self.status_label.configure(text="")

    def on_reason_keypress(self, event):
        """理由入力が開始されたことを検知"""
        if not self.reason_started:
            self.reason_started = True
            self.rewrite_button.configure(state="normal")
            self.next_button.configure(state="normal")

            # ログに記録
            self.logger.log_reason_start(self.current_question_index + 1)

            self.status_label.configure(
                text=MSG_REASON_STARTED_STATUS,
                text_color="orange"
            )

    def rewrite_reason(self):
        """理由を書き直す"""
        # ログに記録
        self.logger.log_rewrite_reason(self.current_question_index + 1)

        # 理由をクリア
        self.reason_text.delete("1.0", "end")
        self.reason_started = False

        # ボタンの状態を更新
        self.rewrite_button.configure(state="disabled")
        self.next_button.configure(state="disabled")

        self.status_label.configure(
            text=MSG_CAN_CHANGE_STATUS,
            text_color="green"
        )

    def next_question(self):
        """次の問題へ"""
        if not self.selected_choice:
            messagebox.showwarning("警告", MSG_NO_CHOICE_SELECTED)
            return

        reason = self.reason_text.get("1.0", "end").strip()

        if not reason:
            messagebox.showwarning("警告", MSG_NO_REASON)
            return

        # ログに理由の内容を記録
        self.logger.log_reason_text(self.current_question_index + 1, reason)

        # 回答を保存
        response = {
            'respondent_id': self.respondent_id,
            'timestamp': get_timestamp(),
            'question_num': self.current_question_index + 1,
            'question_text': self.questions[self.current_question_index]['text'],
            'selected_choice': self.selected_choice,
            'reason': reason
        }

        self.responses.append(response)

        # ログに記録
        old_index = self.current_question_index
        self.current_question_index += 1

        if self.current_question_index < len(self.questions):
            self.logger.log_next_question(old_index + 1, self.current_question_index + 1)

        # 次の問題を表示
        self.display_question()

    def prev_question(self):
        """前の問題へ"""
        if self.current_question_index > 0:
            old_index = self.current_question_index
            self.current_question_index -= 1

            self.logger.log_next_question(old_index + 1, self.current_question_index + 1)

            # 前の回答があれば削除
            if self.responses:
                self.responses.pop()

            self.display_question()

    def submit_survey(self):
        """アンケートを送信"""
        self.logger.log_submit()

        # 設定から回答ファイルのパスを取得
        filepath = self.config_manager.get_response_path(self.respondent_id)

        # ディレクトリが存在しない場合は作成
        response_dir = os.path.dirname(filepath)
        if response_dir and not os.path.exists(response_dir):
            try:
                os.makedirs(response_dir, exist_ok=True)
            except Exception as e:
                messagebox.showerror("エラー", f"ディレクトリの作成に失敗しました: {e}")
                filepath = filedialog.asksaveasfilename(
                    defaultextension=".csv",
                    filetypes=[("CSVファイル", "*.csv"), ("すべてのファイル", "*.*")],
                    initialfile=f"responses_{self.respondent_id}.csv"
                )

        # 設定にパスがない場合は手動で保存先を選択
        if not filepath:
            filepath = filedialog.asksaveasfilename(
                defaultextension=".csv",
                filetypes=[("CSVファイル", "*.csv"), ("すべてのファイル", "*.*")],
                initialfile=f"responses_{self.respondent_id}.csv"
            )

        if filepath:
            # 出力形式を取得
            output_format = self.config_manager.get("output_format", "csv")

            # 拡張子を削除してベースパスを取得
            base_filepath = filepath.replace(".csv", "").replace(".json", "")

            # 保存
            if save_response(self.responses, base_filepath, output_format):
                saved_files = []
                if output_format in ["csv", "both"]:
                    saved_files.append(f"{base_filepath}.csv")
                if output_format in ["json", "both"]:
                    saved_files.append(f"{base_filepath}.json")

                files_str = "\n".join(saved_files)
                messagebox.showinfo(
                    "完了",
                    f"アンケートが完了しました。\n回答を保存しました:\n{files_str}"
                )
            else:
                messagebox.showerror("エラー", "保存に失敗しました")

        self.window.destroy()
