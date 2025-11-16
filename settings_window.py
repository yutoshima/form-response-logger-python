"""
設定画面GUI
"""
import customtkinter as ctk
from tkinter import messagebox, filedialog
from config_manager import ConfigManager
import os


class SettingsWindow:
    def __init__(self, window):
        self.window = window
        self.window.title("設定")
        self.window.geometry("800x650")

        self.config_manager = ConfigManager()

        self.setup_ui()
        self.load_settings()

    def setup_ui(self):
        """UIをセットアップ"""
        # メインコンテナ
        main_container = ctk.CTkFrame(self.window)
        main_container.pack(fill="both", expand=True, padx=20, pady=20)

        # タイトル
        title = ctk.CTkLabel(
            main_container,
            text="設定",
            font=("Yu Gothic", 24, "bold")
        )
        title.pack(pady=(0, 20))

        # スクロール可能なフレーム
        scrollable_frame = ctk.CTkScrollableFrame(main_container)
        scrollable_frame.pack(fill="both", expand=True)

        # 問題ファイル設定
        self.create_questions_section(scrollable_frame)

        # ログ設定
        self.create_log_section(scrollable_frame)

        # 回答ファイル設定
        self.create_response_section(scrollable_frame)

        # アプリケーション設定
        self.create_app_section(scrollable_frame)

        # ボタンエリア
        self.create_button_area(main_container)

    def create_questions_section(self, parent):
        """問題ファイル設定セクション"""
        section = ctk.CTkFrame(parent)
        section.pack(fill="x", pady=(0, 20), padx=10)

        inner = ctk.CTkFrame(section, fg_color="transparent")
        inner.pack(fill="both", expand=True, padx=20, pady=20)

        # セクションタイトル
        title = ctk.CTkLabel(
            inner,
            text="問題ファイル設定",
            font=("Yu Gothic", 16, "bold")
        )
        title.pack(anchor="w", pady=(0, 15))

        # 問題ディレクトリ
        dir_frame = ctk.CTkFrame(inner, fg_color="transparent")
        dir_frame.pack(fill="x", pady=(0, 10))

        dir_label = ctk.CTkLabel(
            dir_frame,
            text="問題ファイルのディレクトリ:",
            font=("Yu Gothic", 12)
        )
        dir_label.pack(anchor="w", pady=(0, 5))

        dir_input_frame = ctk.CTkFrame(dir_frame, fg_color="transparent")
        dir_input_frame.pack(fill="x")

        self.questions_dir_entry = ctk.CTkEntry(
            dir_input_frame,
            font=("Yu Gothic", 11),
            height=35
        )
        self.questions_dir_entry.pack(side="left", fill="x", expand=True, padx=(0, 10))

        browse_dir_btn = ctk.CTkButton(
            dir_input_frame,
            text="参照",
            command=self.browse_questions_dir,
            width=80,
            height=35
        )
        browse_dir_btn.pack(side="right")

        # 問題ファイル名
        file_frame = ctk.CTkFrame(inner, fg_color="transparent")
        file_frame.pack(fill="x", pady=(0, 10))

        file_label = ctk.CTkLabel(
            file_frame,
            text="問題ファイル名:",
            font=("Yu Gothic", 12)
        )
        file_label.pack(anchor="w", pady=(0, 5))

        self.questions_file_entry = ctk.CTkEntry(
            file_frame,
            font=("Yu Gothic", 11),
            height=35,
            placeholder_text="例: questions.csv"
        )
        self.questions_file_entry.pack(fill="x")

    def create_log_section(self, parent):
        """ログ設定セクション"""
        section = ctk.CTkFrame(parent)
        section.pack(fill="x", pady=(0, 20), padx=10)

        inner = ctk.CTkFrame(section, fg_color="transparent")
        inner.pack(fill="both", expand=True, padx=20, pady=20)

        # セクションタイトル
        title = ctk.CTkLabel(
            inner,
            text="ログ設定",
            font=("Yu Gothic", 16, "bold")
        )
        title.pack(anchor="w", pady=(0, 15))

        # ログディレクトリ
        dir_frame = ctk.CTkFrame(inner, fg_color="transparent")
        dir_frame.pack(fill="x", pady=(0, 10))

        dir_label = ctk.CTkLabel(
            dir_frame,
            text="ログ出力ディレクトリ:",
            font=("Yu Gothic", 12)
        )
        dir_label.pack(anchor="w", pady=(0, 5))

        dir_input_frame = ctk.CTkFrame(dir_frame, fg_color="transparent")
        dir_input_frame.pack(fill="x")

        self.log_dir_entry = ctk.CTkEntry(
            dir_input_frame,
            font=("Yu Gothic", 11),
            height=35
        )
        self.log_dir_entry.pack(side="left", fill="x", expand=True, padx=(0, 10))

        browse_dir_btn = ctk.CTkButton(
            dir_input_frame,
            text="参照",
            command=self.browse_log_dir,
            width=80,
            height=35
        )
        browse_dir_btn.pack(side="right")

        # ログファイル名フォーマット
        format_frame = ctk.CTkFrame(inner, fg_color="transparent")
        format_frame.pack(fill="x", pady=(0, 10))

        format_label = ctk.CTkLabel(
            format_frame,
            text="ログファイル名フォーマット:",
            font=("Yu Gothic", 12)
        )
        format_label.pack(anchor="w", pady=(0, 5))

        self.log_format_entry = ctk.CTkEntry(
            format_frame,
            font=("Yu Gothic", 11),
            height=35,
            placeholder_text="例: action_log_{date}.csv"
        )
        self.log_format_entry.pack(fill="x")

        # 説明
        help_label = ctk.CTkLabel(
            format_frame,
            text="使用可能: {date}=日付(YYYYMMDD), {time}=時刻(HHMMSS), {respondent_id}=回答者ID, {sequence}=連番",
            font=("Yu Gothic", 10),
            text_color="gray"
        )
        help_label.pack(anchor="w", pady=(5, 0))

    def create_response_section(self, parent):
        """回答ファイル設定セクション"""
        section = ctk.CTkFrame(parent)
        section.pack(fill="x", pady=(0, 20), padx=10)

        inner = ctk.CTkFrame(section, fg_color="transparent")
        inner.pack(fill="both", expand=True, padx=20, pady=20)

        # セクションタイトル
        title = ctk.CTkLabel(
            inner,
            text="回答ファイル設定",
            font=("Yu Gothic", 16, "bold")
        )
        title.pack(anchor="w", pady=(0, 15))

        # 回答ディレクトリ
        dir_frame = ctk.CTkFrame(inner, fg_color="transparent")
        dir_frame.pack(fill="x", pady=(0, 10))

        dir_label = ctk.CTkLabel(
            dir_frame,
            text="回答出力ディレクトリ:",
            font=("Yu Gothic", 12)
        )
        dir_label.pack(anchor="w", pady=(0, 5))

        dir_input_frame = ctk.CTkFrame(dir_frame, fg_color="transparent")
        dir_input_frame.pack(fill="x")

        self.response_dir_entry = ctk.CTkEntry(
            dir_input_frame,
            font=("Yu Gothic", 11),
            height=35
        )
        self.response_dir_entry.pack(side="left", fill="x", expand=True, padx=(0, 10))

        browse_dir_btn = ctk.CTkButton(
            dir_input_frame,
            text="参照",
            command=self.browse_response_dir,
            width=80,
            height=35
        )
        browse_dir_btn.pack(side="right")

        # 回答ファイル名フォーマット
        format_frame = ctk.CTkFrame(inner, fg_color="transparent")
        format_frame.pack(fill="x", pady=(0, 10))

        format_label = ctk.CTkLabel(
            format_frame,
            text="回答ファイル名フォーマット:",
            font=("Yu Gothic", 12)
        )
        format_label.pack(anchor="w", pady=(0, 5))

        self.response_format_entry = ctk.CTkEntry(
            format_frame,
            font=("Yu Gothic", 11),
            height=35,
            placeholder_text="例: responses_{respondent_id}_{date}.csv"
        )
        self.response_format_entry.pack(fill="x")

        # 説明
        help_label = ctk.CTkLabel(
            format_frame,
            text="使用可能: {date}=日付(YYYYMMDD), {time}=時刻(HHMMSS), {respondent_id}=回答者ID, {sequence}=連番",
            font=("Yu Gothic", 10),
            text_color="gray"
        )
        help_label.pack(anchor="w", pady=(5, 0))

    def create_app_section(self, parent):
        """アプリケーション設定セクション"""
        section = ctk.CTkFrame(parent)
        section.pack(fill="x", pady=(0, 20), padx=10)

        inner = ctk.CTkFrame(section, fg_color="transparent")
        inner.pack(fill="both", expand=True, padx=20, pady=20)

        # セクションタイトル
        title = ctk.CTkLabel(
            inner,
            text="アプリケーション設定",
            font=("Yu Gothic", 16, "bold")
        )
        title.pack(anchor="w", pady=(0, 15))

        # 外観モード
        appearance_frame = ctk.CTkFrame(inner, fg_color="transparent")
        appearance_frame.pack(fill="x", pady=(0, 15))

        appearance_label = ctk.CTkLabel(
            appearance_frame,
            text="外観モード:",
            font=("Yu Gothic", 12)
        )
        appearance_label.pack(anchor="w", pady=(0, 5))

        self.appearance_menu = ctk.CTkOptionMenu(
            appearance_frame,
            values=["System", "Light", "Dark"],
            font=("Yu Gothic", 11),
            height=35
        )
        self.appearance_menu.pack(fill="x")

        # カラーテーマ
        theme_frame = ctk.CTkFrame(inner, fg_color="transparent")
        theme_frame.pack(fill="x", pady=(0, 15))

        theme_label = ctk.CTkLabel(
            theme_frame,
            text="カラーテーマ:",
            font=("Yu Gothic", 12)
        )
        theme_label.pack(anchor="w", pady=(0, 5))

        self.theme_menu = ctk.CTkOptionMenu(
            theme_frame,
            values=["blue", "green", "dark-blue"],
            font=("Yu Gothic", 11),
            height=35
        )
        self.theme_menu.pack(fill="x")

        # 出力形式
        format_frame = ctk.CTkFrame(inner, fg_color="transparent")
        format_frame.pack(fill="x", pady=(0, 15))

        format_label = ctk.CTkLabel(
            format_frame,
            text="出力形式:",
            font=("Yu Gothic", 12)
        )
        format_label.pack(anchor="w", pady=(0, 5))

        self.output_format_menu = ctk.CTkOptionMenu(
            format_frame,
            values=["csv", "json", "both"],
            font=("Yu Gothic", 11),
            height=35
        )
        self.output_format_menu.pack(fill="x")

        # フォントサイズ
        fontsize_frame = ctk.CTkFrame(inner, fg_color="transparent")
        fontsize_frame.pack(fill="x", pady=(0, 15))

        fontsize_label = ctk.CTkLabel(
            fontsize_frame,
            text="フォントサイズ:",
            font=("Yu Gothic", 12)
        )
        fontsize_label.pack(anchor="w", pady=(0, 5))

        self.fontsize_menu = ctk.CTkOptionMenu(
            fontsize_frame,
            values=["small", "medium", "large"],
            font=("Yu Gothic", 11),
            height=35
        )
        self.fontsize_menu.pack(fill="x")

        # 自動保存
        autosave_frame = ctk.CTkFrame(inner, fg_color="transparent")
        autosave_frame.pack(fill="x", pady=(0, 10))

        self.auto_save_var = ctk.BooleanVar(value=True)
        self.auto_save_check = ctk.CTkCheckBox(
            autosave_frame,
            text="回答を自動保存（無効にすると毎回保存先を選択）",
            variable=self.auto_save_var,
            font=("Yu Gothic", 11)
        )
        self.auto_save_check.pack(anchor="w")

    def create_button_area(self, parent):
        """ボタンエリア"""
        button_frame = ctk.CTkFrame(parent, fg_color="transparent")
        button_frame.pack(fill="x", pady=(20, 0))

        # 保存ボタン
        save_btn = ctk.CTkButton(
            button_frame,
            text="保存",
            command=self.save_settings,
            font=("Yu Gothic", 14, "bold"),
            width=150,
            height=45
        )
        save_btn.pack(side="left", padx=(0, 10))

        # キャンセルボタン
        cancel_btn = ctk.CTkButton(
            button_frame,
            text="キャンセル",
            command=self.window.destroy,
            font=("Yu Gothic", 14),
            width=150,
            height=45,
            fg_color="gray40",
            hover_color="gray30"
        )
        cancel_btn.pack(side="left")

    def browse_questions_dir(self):
        """問題ディレクトリを参照"""
        directory = filedialog.askdirectory(title="問題ファイルのディレクトリを選択")
        if directory:
            self.questions_dir_entry.delete(0, "end")
            self.questions_dir_entry.insert(0, directory)

    def browse_log_dir(self):
        """ログディレクトリを参照"""
        directory = filedialog.askdirectory(title="ログ出力ディレクトリを選択")
        if directory:
            self.log_dir_entry.delete(0, "end")
            self.log_dir_entry.insert(0, directory)

    def browse_response_dir(self):
        """回答ディレクトリを参照"""
        directory = filedialog.askdirectory(title="回答出力ディレクトリを選択")
        if directory:
            self.response_dir_entry.delete(0, "end")
            self.response_dir_entry.insert(0, directory)

    def load_settings(self):
        """設定を読み込んで表示"""
        self.questions_dir_entry.insert(0, self.config_manager.get("questions_directory", ""))
        self.questions_file_entry.insert(0, self.config_manager.get("questions_file", ""))
        self.log_dir_entry.insert(0, self.config_manager.get("log_directory", ""))
        self.log_format_entry.insert(0, self.config_manager.get("log_name_format", ""))
        self.response_dir_entry.insert(0, self.config_manager.get("response_directory", ""))
        self.response_format_entry.insert(0, self.config_manager.get("response_name_format", ""))

        # アプリケーション設定
        self.appearance_menu.set(self.config_manager.get("appearance_mode", "System"))
        self.theme_menu.set(self.config_manager.get("color_theme", "blue"))
        self.output_format_menu.set(self.config_manager.get("output_format", "csv"))
        self.fontsize_menu.set(self.config_manager.get("font_size", "medium"))
        self.auto_save_var.set(self.config_manager.get("auto_save", True))

    def save_settings(self):
        """設定を保存"""
        # 設定を更新
        self.config_manager.set("questions_directory", self.questions_dir_entry.get())
        self.config_manager.set("questions_file", self.questions_file_entry.get())
        self.config_manager.set("log_directory", self.log_dir_entry.get())
        self.config_manager.set("log_name_format", self.log_format_entry.get())
        self.config_manager.set("response_directory", self.response_dir_entry.get())
        self.config_manager.set("response_name_format", self.response_format_entry.get())

        # アプリケーション設定
        self.config_manager.set("appearance_mode", self.appearance_menu.get())
        self.config_manager.set("color_theme", self.theme_menu.get())
        self.config_manager.set("output_format", self.output_format_menu.get())
        self.config_manager.set("font_size", self.fontsize_menu.get())
        self.config_manager.set("auto_save", self.auto_save_var.get())

        # 保存
        if self.config_manager.save_config():
            # ディレクトリを作成
            self.config_manager.ensure_directories()
            messagebox.showinfo("成功", "設定を保存しました\n外観モードとカラーテーマを反映するにはアプリを再起動してください")
            self.window.destroy()
        else:
            messagebox.showerror("エラー", "設定の保存に失敗しました")
