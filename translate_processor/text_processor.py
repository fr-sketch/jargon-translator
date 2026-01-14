import os
from docx import Document
from transformers import T5Tokenizer, T5ForConditionalGeneration

MODEL_DIR = "./translate_processor/models/t5-slang-formal"


class TextProcessor:

    def __init__(self, file_path=None, text=None, field_of_activity=None, model_dir: str = MODEL_DIR):
        self.field_of_activity = field_of_activity
        self.file_path = file_path
        self.text = text
        self.tokenizer = T5Tokenizer.from_pretrained(model_dir)
        self.model = T5ForConditionalGeneration.from_pretrained(model_dir)

    def translate(self, text: str) -> str:
        input_text = f"domain: {self.field_of_activity} | translate slang to formal: {text}"
        input_ids = self.tokenizer(
            input_text, return_tensors="pt", truncation=True
        )

        outputs = self.model.generate(
            input_ids,
            num_beams=4,
            early_stopping=True,
        )

        return self.tokenizer.decode(outputs[0], skip_special_tokens=True)

    def save_uploaded_file(self, file, save_dir, allowed_exts):
        filename = file.filename
        ext = filename.lower().rsplit('.', 1)[-1] if '.' in filename else ''
        if ext not in allowed_exts:
            raise ValueError(f"Недопустимый формат файла: .{ext}")
        if not os.path.exists(save_dir):
            os.makedirs(save_dir)
        save_path = os.path.join(save_dir, filename)
        file.save(save_path)
        self.file_path = save_path
        return save_path

    def remove_uploaded_file(self):
        if self.file_path and os.path.exists(self.file_path):
            try:
                os.remove(self.file_path)
            except Exception:
                pass

    def extract_text(self):
        if not self.file_path:
            return ""

        ext = self.file_path.lower().rsplit('.', 1)[-1]
        text = ""

        if ext == 'txt':
            with open(self.file_path, 'r', encoding='utf-8') as f:
                text = f.read()
        elif ext == 'docx':
            doc = Document(self.file_path)
            text = "\n".join([para.text for para in doc.paragraphs])

        return text

    def get_result(self):
        if self.file_path:
            text_to_translate = self.extract_text()
        else:
            text_to_translate = self.text

        if not text_to_translate:
            return "Нет текста для перевода."

        return self.translate(text_to_translate)
