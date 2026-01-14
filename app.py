from flask import Flask, render_template, request
from translate_processor.text_processor import TextProcessor

app = Flask(__name__)

ALLOWED_EXTENSIONS = (
    "txt", "docx"
)


@app.route('/', methods=['GET', 'POST'])
def home():

    result = None
    input_text = ''
    domain = None
    error = None

    if request.method == 'POST':
        input_text = request.form.get('input_text', '')
        file = request.files.get('file')
        domain = request.form.get('domain')
        if not domain:
            error = 'Пожалуйста, выберите сферу!'
        else:
            processor = TextProcessor(field_of_activity=domain)
            try:
                if file and file.filename:
                    processor.save_uploaded_file(
                        file, 'source_files', ALLOWED_EXTENSIONS)
                elif input_text.strip():
                    processor.text = input_text
                else:
                    processor.file_path = None
            except ValueError as ve:
                error = str(ve)
            except Exception:
                error = "Ошибка при сохранении файла."

            if processor.file_path or processor.text:
                result = processor.get_result()
                processor.remove_uploaded_file()

    return render_template('index.html', result=result, input_text=input_text, domain=domain, error=error)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
