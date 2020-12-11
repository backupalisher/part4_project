$('.c_phone').keyup(function (event) {
    mask = '+_ (___) ___ __ __'; // Задаем маску
    if (/[0-9\+\ \-\(\)]/.test(event.key)) {
        // Здесь начинаем сравнивать this.value и mask
        // к примеру опять же
        currentString = this.value;
        currentLength = currentString.length;
        if (/[0-9]/.test(event.key)) {
            if (currentLength > 18) {
                this.value = currentString.slice(0, -1);
            } else if (currentLength === 1) {
                this.value = '+' + event.key + ' (';
            } else {
                for (let i = currentLength; i < mask.length; i++) {
                    if (mask[i] === '_') {
                        this.value[i] = event.key;
                        break;
                    }
                    this.value += mask[i];
                }
            }
        }
    }
})