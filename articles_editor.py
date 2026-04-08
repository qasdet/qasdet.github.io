#!/usr/bin/env python3
"""
Articles Editor - PyQt приложение для редактирования статей в articles.json
После сохранения автоматически коммитит и пушит в GitHub
"""

import json
import base64
import re
import sys
import threading
import webbrowser
from datetime import datetime
from pathlib import Path
from http.server import HTTPServer, BaseHTTPRequestHandler
from urllib.parse import urlencode, urlparse, parse_qs

import requests
from PyQt6.QtCore import Qt, QSize, QTimer
from PyQt6.QtGui import QAction, QFont, QTextCursor
from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QListWidget, QListWidgetItem, QTextEdit, QLineEdit, QLabel,
    QPushButton, QDialog, QMessageBox, QInputDialog, QSplitter,
    QGroupBox, QFormLayout, QDialogButtonBox, QToolBar, QToolButton,
    QComboBox, QScrollArea, QStyle, QProgressDialog
)


class GitConfigDialog(QDialog):
    """Диалог для ввода GitHub credentials"""
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("GitHub настройки")
        self.setModal(True)
        self.setMinimumWidth(450)

        layout = QVBoxLayout(self)

        layout.addWidget(QLabel("Настройки для отправки в GitHub:"))

        self.token_input = QLineEdit()
        self.token_input.setPlaceholderText("Personal Access Token")
        self.token_input.setEchoMode(QLineEdit.EchoMode.Password)
        layout.addWidget(QLabel("Token:"))
        layout.addWidget(self.token_input)

        self.repo_input = QLineEdit()
        self.repo_input.setPlaceholderText("owner/repo")
        layout.addWidget(QLabel("Репозиторий (owner/repo):"))
        layout.addWidget(self.repo_input)

        self.branch_input = QLineEdit()
        self.branch_input.setText("main")
        layout.addWidget(QLabel("Ветка:"))
        layout.addWidget(self.branch_input)

        self.author_name = QLineEdit()
        layout.addWidget(QLabel("Имя автора коммита:"))
        layout.addWidget(self.author_name)

        self.author_email = QLineEdit()
        layout.addWidget(QLabel("Email автора:"))
        layout.addWidget(self.author_email)

        layout.addWidget(QLabel())
        layout.addWidget(QLabel("OAuth для авторизации (опционально):"))

        self.client_id_input = QLineEdit()
        self.client_id_input.setPlaceholderText("Client ID из GitHub OAuth App")
        layout.addWidget(QLabel("Client ID:"))
        layout.addWidget(self.client_id_input)

        self.client_secret_input = QLineEdit()
        self.client_secret_input.setPlaceholderText("Client Secret из GitHub OAuth App")
        self.client_secret_input.setEchoMode(QLineEdit.EchoMode.Password)
        layout.addWidget(QLabel("Client Secret:"))
        layout.addWidget(self.client_secret_input)

        buttons = QDialogButtonBox(
            QDialogButtonBox.StandardButton.Ok | QDialogButtonBox.StandardButton.Cancel
        )
        buttons.accepted.connect(self.accept)
        buttons.rejected.connect(self.reject)
        layout.addWidget(buttons)


class MarkdownHighlighter:
    """Простой highlighter для markdown в QTextEdit"""

    DARK_CSS = """
    <style>
        body {
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
            line-height: 1.6;
            padding: 20px;
            background: #1e1e1e;
            color: #d4d4d4;
        }
        h1 { color: #569cd6; border-bottom: 1px solid #333; padding-bottom: 8px; }
        h2 { color: #4ec9b0; }
        h3 { color: #9cdcfe; }
        h4, h5, h6 { color: #ce9178; }
        p { margin: 12px 0; }
        a { color: #569cd6; }
        code {
            background: #2d2d2d;
            padding: 2px 6px;
            border-radius: 3px;
            font-family: 'Courier New', monospace;
            color: #ce9178;
        }
        pre {
            background: #2d2d2d;
            padding: 16px;
            border-radius: 6px;
            overflow-x: auto;
        }
        pre code {
            background: none;
            padding: 0;
            color: #9cdcfe;
        }
        blockquote {
            border-left: 4px solid #569cd6;
            margin: 12px 0;
            padding-left: 16px;
            color: #6a9955;
        }
        ul, ol {
            margin: 12px 0;
            padding-left: 24px;
        }
        li { margin: 4px 0; }
        hr {
            border: none;
            border-top: 1px solid #333;
            margin: 20px 0;
        }
        strong { color: #ce9178; }
        em { color: #d4d4d4; font-style: italic; }
        table {
            border-collapse: collapse;
            width: 100%;
            margin: 12px 0;
        }
        th, td {
            border: 1px solid #333;
            padding: 8px 12px;
            text-align: left;
        }
        th { background: #2d2d2d; }
    </style>
    """

    @staticmethod
    def render(markdown_text):
        """Конвертирует markdown в HTML для отображения"""
        if not markdown_text:
            return ""

        # Экранируем HTML
        html_escape = {
            '&': '&amp;',
            '<': '&lt;',
            '>': '&gt;',
            '"': '&quot;',
            "'": '&#39;'
        }

        def escape(text):
            for k, v in html_escape.items():
                text = text.replace(k, v)
            return text

        # Разбиваем на блоки
        lines = markdown_text.split('\n')
        blocks = []
        in_code_block = False
        code_content = []

        for line in lines:
            # Code blocks
            if line.strip().startswith('```'):
                if not in_code_block:
                    in_code_block = True
                    code_content = []
                    lang = line.strip()[3:] or ''
                    blocks.append('<pre><code>')
                else:
                    in_code_block = False
                    blocks.append(f'</code></pre>')
                continue

            if in_code_block:
                code_content.append(escape(line))
                continue

            # Headers
            if line.startswith('#### '):
                blocks.append(f'<h4>{escape(line[5:])}</h4>')
            elif line.startswith('### '):
                blocks.append(f'<h3>{escape(line[4:])}</h3>')
            elif line.startswith('## '):
                blocks.append(f'<h2>{escape(line[3:])}</h2>')
            elif line.startswith('# '):
                blocks.append(f'<h1>{escape(line[2:])}</h1>')

            # HR
            elif line.strip() == '---' or line.strip() == '***':
                blocks.append('<hr>')

            # Blockquote
            elif line.startswith('>'):
                blocks.append(f'<blockquote>{escape(line[1:].strip())}</blockquote>')

            # Unordered list
            elif line.startswith('- ') or line.startswith('* '):
                blocks.append(f'<li>{escape(line[2:])}</li>')

            # Ordered list
            elif re.match(r'^\d+\.\s', line):
                num_match = re.sub(r"^\d+\.\s", "", line)
                blocks.append(f'<li>{escape(num_match)}</li>')

            # Table - простой парсинг
            elif line.startswith('|'):
                # Пропускаем разделительную строку
                if re.match(r'^[\|\s\-:]+$', line):
                    continue
                cells = [c.strip() for c in line.strip().strip('|').split('|')]
                row = '<tr>' + ''.join(f'<td>{escape(c)}</td>' for c in cells) + '</tr>'
                blocks.append(row)

            # Paragraph
            elif line.strip():
                # Inline formatting
                text = escape(line)
                text = re.sub(r'\*\*(.+?)\*\*', r'<strong>\1</strong>', text)
                text = re.sub(r'\*(.+?)\*', r'<em>\1</em>', text)
                text = re.sub(r'`(.+?)`', r'<code>\1</code>', text)
                text = re.sub(r'\[(.+?)\]\((.+?)\)', r'<a href="\2">\1</a>', text)
                blocks.append(f'<p>{text}</p>')

            else:
                blocks.append('')

        # Обработка списков
        result = []
        i = 0
        in_ul = False
        in_ol = False

        while i < len(blocks):
            block = blocks[i]

            if block.startswith('<li>'):
                if not in_ul:
                    if in_ol:
                        result.append('</ol>')
                        in_ol = False
                    result.append('<ul>')
                    in_ul = True
                result.append(block)
            else:
                if in_ul:
                    result.append('</ul>')
                    in_ul = False
                result.append(block)

            i += 1

        if in_ul:
            result.append('</ul>')

        # Обработка таблиц
        html = '\n'.join(result)
        if '<tr>' in html:
            html = html.replace('<tr>', '<table><tr>', 1)
            html = html.replace('</tr>', '</tr></table>', html.count('</tr>'))

        return f"<!DOCTYPE html><html><head><meta charset='utf-8'></head><body>{html}</body></html>"


class OAuthCallbackHandler(BaseHTTPRequestHandler):
    """Обработчик для OAuth callback"""
    code_received = None

    def do_GET(self):
        """Получить код авторизации"""
        parsed = urlparse(self.path)
        params = parse_qs(parsed.query)
        if 'code' in params:
            OAuthCallbackHandler.code_received = params['code'][0]
            self.send_response(200)
            self.send_header('Content-type', 'text/html; charset=utf-8')
            self.end_headers()
            message = 'Авторизация успешна!<br><br>Можно закрыть это окно.'
            self.wfile.write(message.encode('utf-8'))
        else:
            self.send_response(400)
            self.end_headers()
            self.wfile.write(b'Bad Request')

    def log_message(self, format, *args):
        pass  # Silent


class OAuthServer:
    """Локальный сервер для OAuth callback"""
    def __init__(self, port=8000):
        self.port = port
        self.server = None
        self.thread = None

    def start(self):
        self.server = HTTPServer(('localhost', self.port), OAuthCallbackHandler)
        OAuthCallbackHandler.code_received = None
        self.thread = threading.Thread(target=self.server.serve_forever)
        self.thread.daemon = True
        self.thread.start()

    def stop(self):
        if self.server:
            self.server.shutdown()
            self.thread.join(timeout=2)

    def get_code(self, timeout=120):
        """Ждать код авторизации"""
        import time
        start = time.time()
        while OAuthCallbackHandler.code_received is None:
            if time.time() - start > timeout:
                return None
            time.sleep(0.1)
        return OAuthCallbackHandler.code_received


class ArticleEditor(QMainWindow):
    def __init__(self):
        super().__init__()
        self.articles_file = Path(__file__).parent / "articles.json"
        self.articles = []
        self.current_article = None
        self.is_new = False
        self.is_dirty = False
        self.git_config = self.load_git_config()
        self.preview_timer = None

        self.setup_ui()
        self.load_articles()

    def load_git_config(self):
        """Загрузка GitHub настроек"""
        config_file = Path(__file__).parent / ".git_editor_config.json"
        if config_file.exists():
            with open(config_file, 'r', encoding='utf-8') as f:
                return json.load(f)
        return {
            "token": "",
            "repo": "",
            "branch": "main",
            "author_name": "",
            "author_email": "",
            "client_id": "",
            "client_secret": ""
        }

    def save_git_config(self):
        """Сохранение GitHub настроек"""
        config_file = Path(__file__).parent / ".git_editor_config.json"
        with open(config_file, 'w', encoding='utf-8') as f:
            json.dump(self.git_config, f, indent=2)

    def setup_ui(self):
        self.setWindowTitle("Articles Editor")
        self.setMinimumSize(QSize(1400, 900))

        # Menu bar
        menubar = self.menuBar()

        file_menu = menubar.addMenu("Файл")

        save_action = QAction("Сохранить", self)
        save_action.setShortcut("Ctrl+S")
        save_action.triggered.connect(self.save_article)
        file_menu.addAction(save_action)

        new_action = QAction("Новая статья", self)
        new_action.setShortcut("Ctrl+N")
        new_action.triggered.connect(self.new_article)
        file_menu.addAction(new_action)

        delete_action = QAction("Удалить", self)
        delete_action.setShortcut("Ctrl+Del")
        delete_action.triggered.connect(self.delete_article)
        file_menu.addAction(delete_action)

        file_menu.addSeparator()

        refresh_action = QAction("Перезагрузить", self)
        refresh_action.setShortcut("F5")
        refresh_action.triggered.connect(self.load_articles)
        file_menu.addAction(refresh_action)

        file_menu.addSeparator()

        settings_action = QAction("Настройки GitHub...", self)
        settings_action.triggered.connect(self.show_git_settings)
        file_menu.addAction(settings_action)

        exit_action = QAction("Выход", self)
        exit_action.setShortcut("Ctrl+Q")
        exit_action.triggered.connect(self.close)
        file_menu.addAction(exit_action)

        # Main widget
        central = QWidget()
        self.setCentralWidget(central)

        layout = QHBoxLayout(central)

        # Left panel - articles list
        left_panel = QWidget()
        left_layout = QVBoxLayout(left_panel)
        left_layout.setContentsMargins(0, 0, 0, 0)

        self.articles_list = QListWidget()
        self.articles_list.currentItemChanged.connect(self.on_article_selected)
        left_layout.addWidget(self.articles_list)

        # Add buttons
        btn_layout = QHBoxLayout()
        add_btn = QPushButton("+")
        add_btn.setMaximumWidth(40)
        add_btn.clicked.connect(self.new_article)
        btn_layout.addWidget(add_btn)

        del_btn = QPushButton("-")
        del_btn.setMaximumWidth(40)
        del_btn.clicked.connect(self.delete_article)
        btn_layout.addWidget(del_btn)

        btn_layout.addStretch()
        left_layout.addLayout(btn_layout)

        # Right panel - editor
        right_panel = QWidget()
        right_layout = QVBoxLayout(right_panel)
        right_layout.setContentsMargins(0, 0, 0, 0)

        # Metadata
        meta_group = QGroupBox("Метаданные")
        meta_layout = QFormLayout(meta_group)
        meta_layout.setVerticalSpacing(8)
        meta_layout.setContentsMargins(10, 10, 10, 10)

        self.title_input = QLineEdit()
        self.title_input.setPlaceholderText("Заголовок статьи")
        self.title_input.textChanged.connect(self.on_field_changed)
        meta_layout.addRow("Заголовок:", self.title_input)
        self.title_input.setFixedHeight(28)

        date_layout = QHBoxLayout()
        self.date_input = QLineEdit()
        self.date_input.setPlaceholderText("YYYY-MM-DD")
        self.date_input.textChanged.connect(self.on_field_changed)
        self.date_input.setFixedHeight(28)
        date_layout.addWidget(self.date_input)

        self.today_btn = QPushButton("Сегодня")
        self.today_btn.setMaximumWidth(70)
        self.today_btn.setFixedHeight(28)
        self.today_btn.clicked.connect(self.set_today_date)
        date_layout.addWidget(self.today_btn)
        meta_layout.addRow("Дата:", date_layout)

        self.excerpt_input = QLineEdit()
        self.excerpt_input.setPlaceholderText("Краткое описание для карточки")
        self.excerpt_input.textChanged.connect(self.on_field_changed)
        self.excerpt_input.setFixedHeight(28)
        meta_layout.addRow("Описание:", self.excerpt_input)

        self.tags_input = QLineEdit()
        self.tags_input.setPlaceholderText("тег1, тег2, тег3")
        self.tags_input.textChanged.connect(self.on_field_changed)
        self.tags_input.setFixedHeight(28)
        meta_layout.addRow("Теги:", self.tags_input)

        right_layout.addWidget(meta_group)

        # Content editor with toolbar
        content_group = QGroupBox("Контент")
        content_layout = QVBoxLayout(content_group)

        # Toolbar
        toolbar = QToolBar("Форматирование")
        toolbar.setMovable(False)

        # Headers
        from PyQt6.QtWidgets import QMenu

        h_btn = QToolButton()
        h_btn.setText("H")
        h_btn.setToolTip("Заголовок")
        h_btn.setPopupMode(QToolButton.ToolButtonPopupMode.InstantPopup)

        h_menu = QMenu()
        h1_action = QAction("H1", self)
        h1_action.triggered.connect(lambda: self.insert_format('h1'))
        h2_action = QAction("H2", self)
        h2_action.triggered.connect(lambda: self.insert_format('h2'))
        h3_action = QAction("H3", self)
        h3_action.triggered.connect(lambda: self.insert_format('h3'))
        h4_action = QAction("H4", self)
        h4_action.triggered.connect(lambda: self.insert_format('h4'))

        h_menu.addAction(h1_action)
        h_menu.addAction(h2_action)
        h_menu.addAction(h3_action)
        h_menu.addAction(h4_action)
        h_btn.setMenu(h_menu)
        toolbar.addWidget(h_btn)

        toolbar.addSeparator()

        # Bold
        bold_btn = QToolButton()
        bold_btn.setText("B")
        bold_btn.setToolTip("Жирный (Ctrl+B)")
        bold_btn.setStyleSheet("font-weight: bold;")
        bold_btn.clicked.connect(self.insert_bold)
        toolbar.addWidget(bold_btn)

        # Italic
        italic_btn = QToolButton()
        italic_btn.setText("I")
        italic_btn.setToolTip("Курсив (Ctrl+I)")
        italic_btn.setStyleSheet("font-style: italic;")
        italic_btn.clicked.connect(self.insert_italic)
        toolbar.addWidget(italic_btn)

        toolbar.addSeparator()

        # Code
        code_btn = QToolButton()
        code_btn.setText("</>")
        code_btn.setToolTip("Код")
        code_btn.clicked.connect(self.insert_code)
        toolbar.addWidget(code_btn)

        # Code block
        codeblock_btn = QToolButton()
        codeblock_btn.setText("```")
        codeblock_btn.setToolTip("Блок кода")
        codeblock_btn.clicked.connect(self.insert_codeblock)
        toolbar.addWidget(codeblock_btn)

        toolbar.addSeparator()

        # Link
        link_btn = QToolButton()
        link_btn.setText("🔗")
        link_btn.setToolTip("Ссылка")
        link_btn.clicked.connect(self.insert_link)
        toolbar.addWidget(link_btn)

        # Quote
        quote_btn = QToolButton()
        quote_btn.setText('"')
        quote_btn.setToolTip("Цитата")
        quote_btn.clicked.connect(self.insert_quote)
        toolbar.addWidget(quote_btn)

        # HR
        hr_btn = QToolButton()
        hr_btn.setText("—")
        hr_btn.setToolTip("Разделитель")
        hr_btn.clicked.connect(self.insert_hr)
        toolbar.addWidget(hr_btn)

        toolbar.addSeparator()

        # Unordered list
        ul_btn = QToolButton()
        ul_btn.setText("•-")
        ul_btn.setToolTip("Маркированный список")
        ul_btn.clicked.connect(self.insert_ul)
        toolbar.addWidget(ul_btn)

        # Ordered list
        ol_btn = QToolButton()
        ol_btn.setText("1.")
        ol_btn.setToolTip("Нумерованный список")
        ol_btn.clicked.connect(self.insert_ol)
        toolbar.addWidget(ol_btn)

        toolbar.addSeparator()

        # Preview toggle
        self.preview_btn = QPushButton("👁 Предпросмотр")
        self.preview_btn.setCheckable(True)
        self.preview_btn.toggled.connect(self.toggle_preview)
        toolbar.addWidget(self.preview_btn)

        content_layout.addWidget(toolbar)

        # Editor and preview splitter
        editor_container = QWidget()
        editor_layout = QHBoxLayout(editor_container)
        editor_layout.setContentsMargins(0, 0, 0, 0)

        self.content_editor = QTextEdit()
        self.content_editor.setPlaceholderText("# Заголовок\n\nНачните писать статью...\n\nИспользуйте панель инструментов для форматирования или markdown:\n- **жирный**\n- *курсив*\n- `код`\n- [ссылка](url)")
        self.content_editor.setFont(QFont("Consolas", 11))
        self.content_editor.textChanged.connect(self.on_content_changed)
        editor_layout.addWidget(self.content_editor)

        # Preview panel
        self.preview_panel = QLabel()
        self.preview_panel.setText("<p style='color:#666;padding:20px;'>Предпросмотр...</p>")
        self.preview_panel.setAlignment(Qt.AlignmentFlag.AlignTop)
        scroll = QScrollArea()
        scroll.setWidget(self.preview_panel)
        scroll.setWidgetResizable(True)
        scroll.setMinimumWidth(400)
        scroll.setVisible(False)
        self.preview_panel.setStyleSheet("background: #1e1e1e; color: #d4d4d4; padding: 10px;")
        self.editor_scroll = scroll

        self.editor_splitter = QSplitter(Qt.Orientation.Horizontal)
        self.editor_splitter.addWidget(self.content_editor)
        self.editor_splitter.addWidget(scroll)
        self.editor_splitter.setSizes([600, 400])

        content_layout.addWidget(self.editor_splitter)
        content_layout.setStretchFactor(self.editor_splitter, 1)

        right_layout.addWidget(content_group)
        right_layout.setStretchFactor(content_group, 1)

        # Buttons
        btn_row = QHBoxLayout()
        btn_row.addStretch()

        self.save_btn = QPushButton("💾 Сохранить")
        self.save_btn.setEnabled(False)
        self.save_btn.clicked.connect(self.save_article)
        btn_row.addWidget(self.save_btn)

        self.push_btn = QPushButton("📤 GitHub")
        self.push_btn.setEnabled(False)
        self.push_btn.clicked.connect(self.push_to_github)
        btn_row.addWidget(self.push_btn)

        self.oauth_btn = QPushButton("🔑 OAuth")
        self.oauth_btn.clicked.connect(self.oauth_login)
        btn_row.addWidget(self.oauth_btn)

        right_layout.addLayout(btn_row)

        # Main splitter
        splitter = QSplitter(Qt.Orientation.Horizontal)
        splitter.addWidget(left_panel)
        splitter.addWidget(right_panel)
        splitter.setSizes([280, 1120])

        layout.addWidget(splitter)

        self.statusBar().showMessage("Готов")

    def insert_format(self, level):
        """Вставка заголовка"""
        prefix = '#' * {'h1': 1, 'h2': 2, 'h3': 3, 'h4': 4}[level]
        cursor = self.content_editor.textCursor()
        cursor.insertText(f'\n{prefix} ')

    def insert_bold(self):
        """Вставка жирного текста"""
        cursor = self.content_editor.textCursor()
        selected = cursor.selectedText()
        if selected:
            cursor.insertText(f'**{selected}**')
        else:
            cursor.insertText('**текст**')

    def insert_italic(self):
        """Вставка курсива"""
        cursor = self.content_editor.textCursor()
        selected = cursor.selectedText()
        if selected:
            cursor.insertText(f'*{selected}*')
        else:
            cursor.insertText('*текст*')

    def insert_code(self):
        """Вставка инлайн-кода"""
        cursor = self.content_editor.textCursor()
        selected = cursor.selectedText()
        if selected:
            cursor.insertText(f'`{selected}`')
        else:
            cursor.insertText('`код`')

    def insert_codeblock(self):
        """Вставка блока кода"""
        cursor = self.content_editor.textCursor()
        cursor.insertText('\n```\nкод\n```\n')

    def insert_link(self):
        """Вставка ссылки"""
        cursor = self.content_editor.textCursor()
        selected = cursor.selectedText()
        if selected:
            cursor.insertText(f'[{selected}](url)')
        else:
            cursor.insertText('[текст](url)')

    def insert_quote(self):
        """Вставка цитаты"""
        cursor = self.content_editor.textCursor()
        cursor.insertText('\n> ')

    def insert_hr(self):
        """Вставка разделителя"""
        cursor = self.content_editor.textCursor()
        cursor.insertText('\n---\n')

    def insert_ul(self):
        """Вставка маркированного списка"""
        cursor = self.content_editor.textCursor()
        cursor.insertText('\n- пункт 1\n- пункт 2\n- пункт 3\n')

    def insert_ol(self):
        """Вставка нумерованного списка"""
        cursor = self.content_editor.textCursor()
        cursor.insertText('\n1. пункт 1\n2. пункт 2\n3. пункт 3\n')

    def toggle_preview(self, checked):
        """Переключение превью"""
        self.editor_scroll.setVisible(checked)
        if checked:
            self.update_preview()

    def update_preview(self):
        """Обновление превью"""
        content = self.content_editor.toPlainText()
        html = MarkdownHighlighter.render(content)
        styled_html = html.replace('<body>', f'<body style="background:#1e1e1e;color:#d4d4d4;font-family:sans-serif;">{MarkdownHighlighter.DARK_CSS}')
        self.preview_panel.setText(styled_html)

    def on_content_changed(self):
        """Обработка изменения контента"""
        self.is_dirty = True
        if self.preview_btn.isChecked():
            self.update_preview()
        self.save_btn.setEnabled(True)

    def on_field_changed(self):
        """Обработка изменения поля"""
        self.is_dirty = True
        self.save_btn.setEnabled(True)

    def load_articles(self):
        """Загрузка статей из файла"""
        self.articles_list.clear()

        if not self.articles_file.exists():
            self.articles = []
            return

        try:
            with open(self.articles_file, 'r', encoding='utf-8') as f:
                self.articles = json.load(f)
        except json.JSONDecodeError:
            QMessageBox.warning(self, "Ошибка", "Не удалось распознать articles.json")
            self.articles = []

        for article in self.articles:
            item = QListWidgetItem(article.get('title', 'Без названия'))
            item.setData(Qt.ItemDataRole.UserRole, article)
            self.articles_list.addItem(item)

        if self.articles:
            self.articles_list.setCurrentRow(0)

        self.statusBar().showMessage(f"Загружено {len(self.articles)} статей")

    def on_article_selected(self, current, previous):
        """Обработка выбора статьи"""
        if previous and self.is_dirty:
            reply = QMessageBox.question(
                self, "Сохранить изменения?",
                "Сохранить изменения в текущей статье?",
                QMessageBox.StandardButton.Save |
                QMessageBox.StandardButton.Discard |
                QMessageBox.StandardButton.Cancel
            )

            if reply == QMessageBox.StandardButton.Save:
                self.save_article()
            elif reply == QMessageBox.StandardButton.Cancel:
                # Restore selection
                for i in range(self.articles_list.count()):
                    if self.articles_list.item(i).data(Qt.ItemDataRole.UserRole) == self.current_article:
                        self.articles_list.setCurrentRow(i)
                        return

        if current:
            self.current_article = current.data(Qt.ItemDataRole.UserRole)
            self.populate_editor()
            self.is_dirty = False
            self.save_btn.setEnabled(False)
        else:
            self.current_article = None
            self.clear_editor()

    def populate_editor(self):
        """Заполнение редактора данными статьи"""
        if not self.current_article:
            return

        self.title_input.setText(self.current_article.get('title', ''))
        self.date_input.setText(self.current_article.get('date', ''))
        self.excerpt_input.setText(self.current_article.get('excerpt', ''))
        self.tags_input.setText(', '.join(self.current_article.get('tags', [])))
        self.content_editor.setPlainText(self.current_article.get('content', ''))

        if self.preview_btn.isChecked():
            self.update_preview()

    def clear_editor(self):
        """Очистка редактора"""
        self.title_input.clear()
        self.date_input.clear()
        self.excerpt_input.clear()
        self.tags_input.clear()
        self.content_editor.clear()

    def set_today_date(self):
        """Установить сегодняшнюю дату"""
        self.date_input.setText(datetime.now().strftime('%Y-%m-%d'))

    def new_article(self):
        """Создание новой статьи"""
        self.is_new = True
        self.current_article = {
            'id': len(self.articles) + 1,
            'title': '',
            'date': datetime.now().strftime('%Y-%m-%d'),
            'excerpt': '',
            'tags': [],
            'content': ''
        }
        self.populate_editor()
        self.save_btn.setEnabled(True)
        self.title_input.setFocus()

    def delete_article(self):
        """Удаление статьи"""
        if not self.current_article:
            return

        reply = QMessageBox.question(
            self, "Удалить статью?",
            f"Удалить статью '{self.current_article.get('title', 'Без названия')}'?",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
        )

        if reply == QMessageBox.StandardButton.Yes:
            article_id = self.current_article.get('id')
            self.articles = [a for a in self.articles if a.get('id') != article_id]
            self.save_to_file()
            self.load_articles()

    def save_article(self):
        """Сохранение статьи"""
        title = self.title_input.text().strip()

        if not title:
            QMessageBox.warning(self, "Ошибка", "Введите заголовок статьи")
            return

        article_data = {
            'id': self.current_article.get('id') if self.current_article else len(self.articles) + 1,
            'title': title,
            'date': self.date_input.text().strip(),
            'excerpt': self.excerpt_input.text().strip(),
            'tags': [t.strip() for t in self.tags_input.text().split(',') if t.strip()],
            'content': self.content_editor.toPlainText()
        }

        if self.is_new:
            self.articles.append(article_data)
            self.is_new = False
        else:
            for i, a in enumerate(self.articles):
                if a.get('id') == article_data['id']:
                    self.articles[i] = article_data
                    break

        self.current_article = article_data
        self.save_to_file()
        self.is_dirty = False
        self.save_btn.setEnabled(False)
        self.push_btn.setEnabled(True)
        self.load_articles()

        # Select saved article
        for i in range(self.articles_list.count()):
            item = self.articles_list.item(i)
            if item.data(Qt.ItemDataRole.UserRole).get('id') == article_data['id']:
                self.articles_list.setCurrentRow(i)
                break

        self.statusBar().showMessage("Статья сохранена")

    def save_to_file(self):
        """Сохранение в файл"""
        with open(self.articles_file, 'w', encoding='utf-8') as f:
            json.dump(self.articles, f, ensure_ascii=False, indent=2)

    def show_git_settings(self):
        """Показать настройки GitHub"""
        dialog = GitConfigDialog(self)

        dialog.token_input.setText(self.git_config.get('token', ''))
        dialog.repo_input.setText(self.git_config.get('repo', ''))
        dialog.branch_input.setText(self.git_config.get('branch', 'main'))
        dialog.author_name.setText(self.git_config.get('author_name', ''))
        dialog.author_email.setText(self.git_config.get('author_email', ''))
        dialog.client_id_input.setText(self.git_config.get('client_id', ''))
        dialog.client_secret_input.setText(self.git_config.get('client_secret', ''))

        if dialog.exec() == QDialog.DialogCode.Accepted:
            self.git_config['token'] = dialog.token_input.text().strip()
            self.git_config['repo'] = dialog.repo_input.text().strip()
            self.git_config['branch'] = dialog.branch_input.text().strip()
            self.git_config['author_name'] = dialog.author_name.text().strip()
            self.git_config['author_email'] = dialog.author_email.text().strip()
            self.git_config['client_id'] = dialog.client_id_input.text().strip()
            self.git_config['client_secret'] = dialog.client_secret_input.text().strip()
            self.save_git_config()
            self.statusBar().showMessage("Настройки GitHub сохранены")

    def oauth_login(self):
        """Авторизация через GitHub OAuth"""
        client_id = self.git_config.get('client_id', '').strip()
        client_secret = self.git_config.get('client_secret', '').strip()

        if not client_id or not client_secret:
            QMessageBox.information(
                self, "OAuth настройка",
                "Для авторизации через GitHub:\n\n"
                "1. Создайте OAuth App на github.com/settings/developers\n"
                "2. Callback URL: http://localhost:8000/callback\n"
                "3. Введите Client ID и Client Secret в настройках (Меню -> Файл -> Настройки GitHub)"
            )
            return

        # Запускаем локальный сервер для callback
        server = OAuthServer(8000)
        server.start()

        import time
        time.sleep(0.5)  # Даем серверу время запуститься

        try:
            # Формируем URL для авторизации
            params = {
                'client_id': client_id,
                'redirect_uri': 'http://localhost:8000/callback',
                'scope': 'repo',
                'response_type': 'code'
            }
            auth_url = 'https://github.com/login/oauth/authorize?' + urlencode(params)

            # Открываем браузер в новом потоке (не блокируем)
            def open_browser():
                webbrowser.open(auth_url)

            threading.Thread(target=open_browser, daemon=True).start()

            self.statusBar().showMessage("Ожидание авторизации в браузере...")

            # Ждем код авторизации
            code = server.get_code(timeout=120)

            if not code:
                self.statusBar().showMessage("Таймаут авторизации")
                QMessageBox.warning(self, "Ошибка", "Таймаут авторизации. Попробуйте снова.")
                return

            # Обмен кода на токен
            self.statusBar().showMessage("Получение токена...")
            token_url = 'https://github.com/login/oauth/access_token'
            token_data = {
                'client_id': client_id,
                'client_secret': client_secret,
                'code': code
            }

            response = requests.post(
                token_url,
                data=token_data,
                headers={'Accept': 'application/json'}
            )

            result = response.json()

            if 'access_token' in result:
                self.git_config['token'] = result['access_token']
                self.save_git_config()
                self.push_btn.setEnabled(True)
                self.statusBar().showMessage("Авторизация успешна!")
                QMessageBox.information(self, "Успех", "Авторизация прошла успешно!")
            else:
                error = result.get('error_description', 'Unknown error')
                self.statusBar().showMessage("Ошибка авторизации")
                QMessageBox.critical(self, "Ошибка", f"Не удалось получить токен:\n{error}")

        finally:
            server.stop()

    def push_to_github(self):
        """Отправка изменений в GitHub"""
        if not self.git_config.get('token'):
            QMessageBox.warning(self, "Ошибка", "Укажите токен GitHub в настройках")
            return

        if not self.git_config.get('repo'):
            QMessageBox.warning(self, "Ошибка", "Укажите репозиторий в настройках")
            return

        self.save_article()

        try:
            # Get file content
            with open(self.articles_file, 'r', encoding='utf-8') as f:
                content = f.read()

            encoded_content = base64.b64encode(content.encode('utf-8')).decode('ascii')

            # Get current file SHA
            url = f"https://api.github.com/repos/{self.git_config['repo']}/contents/{self.articles_file.name}"

            headers = {
                'Authorization': f"token {self.git_config['token']}",
                'Accept': 'application/vnd.github.v3+json'
            }

            # Check if file exists and get SHA
            sha = None
            response = requests.get(url, headers=headers)
            if response.status_code == 200:
                sha = response.json().get('sha')

            # Prepare commit data
            commit_data = {
                'message': f"Update articles.json - {datetime.now().strftime('%Y-%m-%d %H:%M')}",
                'content': encoded_content,
                'branch': self.git_config['branch']
            }

            if sha:
                commit_data['sha'] = sha

            if self.git_config.get('author_name'):
                commit_data['committer'] = {
                    'name': self.git_config['author_name'],
                    'email': self.git_config.get('author_email', '')
                }

            # Commit
            response = requests.put(url, headers=headers, json=commit_data)

            if response.status_code in [200, 201]:
                self.statusBar().showMessage("Успешно отправлено в GitHub!")
                self.push_btn.setEnabled(False)
                QMessageBox.information(self, "Успех", "Файл успешно отправлен в GitHub")
            else:
                error_msg = response.json().get('message', 'Unknown error')
                QMessageBox.critical(self, "Ошибка GitHub", f"Не удалось отправить:\n{error_msg}")

        except requests.RequestException as e:
            QMessageBox.critical(self, "Ошибка", f"Ошибка сети:\n{str(e)}")
        except Exception as e:
            QMessageBox.critical(self, "Ошибка", f"Неожиданная ошибка:\n{str(e)}")

    def closeEvent(self, event):
        """Закрытие приложения"""
        if self.is_dirty:
            reply = QMessageBox.question(
                self, "Сохранить изменения?",
                "Сохранить несохраненные изменения?",
                QMessageBox.StandardButton.Save |
                QMessageBox.StandardButton.Discard |
                QMessageBox.StandardButton.Cancel
            )

            if reply == QMessageBox.StandardButton.Save:
                self.save_article()
                event.accept()
            elif reply == QMessageBox.StandardButton.Discard:
                event.accept()
            else:
                event.ignore()
        else:
            event.accept()


def main():
    app = QApplication(sys.argv)
    app.setStyle('Fusion')

    window = ArticleEditor()
    window.show()

    sys.exit(app.exec())


if __name__ == '__main__':
    main()
