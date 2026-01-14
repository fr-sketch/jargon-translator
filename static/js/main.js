  const copyBtn = document.getElementById('copy-result-btn');
  const resultText = document.getElementById('result-text');
  const copyPopup = document.getElementById('copy-popup');
  if (copyBtn && resultText) {
    copyBtn.addEventListener('click', function() {
      let copied = false;
      if (navigator.clipboard) {
        navigator.clipboard.writeText(resultText.textContent)
          .then(() => { copied = true; });
      } else {
        const range = document.createRange();
        range.selectNode(resultText);
        window.getSelection().removeAllRanges();
        window.getSelection().addRange(range);
        try {
          document.execCommand('copy');
          copied = true;
        } catch (err) {}
        window.getSelection().removeAllRanges();
      }
      if (copyPopup) {
        copyPopup.style.display = 'block';
        setTimeout(() => { copyPopup.style.display = 'none'; }, 1200);
      }
    });
  }
(function(){
  const form = document.querySelector('.translate-form');
  const textarea = document.getElementById('input-text');
  const textareaWrap = document.querySelector('.textarea-wrap');
  const fileInput = document.getElementById('file-input');
  const fileStatus = document.getElementById('file-status');
  const fileClear = document.getElementById('file-clear');
  const allowedExtensions = ['txt', 'docx'];
  function getExt(name){
    const idx = name.lastIndexOf('.');
    return idx >= 0 ? name.slice(idx+1).toLowerCase() : '';
  }

  function setStatus(text, kind){
    if (!fileStatus) return;
    fileStatus.textContent = text || '';
    fileStatus.classList.remove('ok','error');
    if (kind === 'ok') fileStatus.classList.add('ok');
    if (kind === 'error') fileStatus.classList.add('error');
  }

  function lockTextarea(lock){
    if (!textarea || !textareaWrap) return;
    textarea.disabled = !!lock;
    textareaWrap.classList.toggle('locked', !!lock);
  }

  if (textarea && form) {
    textarea.addEventListener('keydown', function(e) {
      if (e.key === 'Enter' && !e.shiftKey) {
        e.preventDefault();
        form.requestSubmit ? form.requestSubmit() : form.submit();
      }
    });
  }
  if (fileInput){
    fileInput.addEventListener('change', () => {
      const file = fileInput.files && fileInput.files[0];
      if (!file){
        setStatus('', null);
        lockTextarea(false);
        if (fileClear) fileClear.style.display = 'none';
        return;
      }
      const ext = getExt(file.name);
      if (!allowedExtensions.includes(ext)){
        setStatus(`Недопустимый формат: .${ext}`, 'error');
        fileInput.value = '';
        lockTextarea(false);
        if (fileClear) fileClear.style.display = 'none';
        return;
      }
      setStatus(`Файл загружен: ${file.name}`, 'ok');
      lockTextarea(true);
      if (fileClear) fileClear.style.display = 'inline-block';
    });
  }

  if (fileClear){
    fileClear.addEventListener('click', () => {
      fileInput.value = '';
      setStatus('', null);
      lockTextarea(false);
      fileClear.style.display = 'none';
    });
  }

  if (form){
    form.addEventListener('submit', () => {
      form.classList.add('is-loading');
    });
  }
})();
