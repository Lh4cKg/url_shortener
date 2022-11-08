$(document).ready(function () {

    $('input').on('invalid', function(e){
        console.log('this.value: ', this.value)
        if (this.value != '' && this.type == 'email') {
            return this.setCustomValidity('შეყვანილი ფორმატი არასწორია');
        }
        return this.setCustomValidity('გთხოვთ შეავსოთ ეს ველი');
    }).on('input', function(e){
        return this.setCustomValidity('');
    });

    $('input[name="dob"]').scroller({ theme: 'android-ics light' });

//    $('input[name="dob"]').on('keyup', function (e) {
//        let valid = /^\d{0,4}$|^\d{4}-0?$|^\d{4}-(?:0?[1-9]|1[012])(?:-(?:0?[1-9]?|[12]\d|3[01])?)?$/.test(this.value), input = this.value;
//        if (!valid) {
//            this.value = input.substring(0, input.length - 1);
//            this.style.backgroundColor = '#EEA39C';
//            if (this.value.length === 10 || this.value.length === 9) {
//                this.style.backgroundColor = '#ffffff';
//            } else if (this.value.length === 4 && !this.value.endsWith('-') && !this.value.endsWith('-0') && e.which !== 8) {
//                this.value = `${this.value}-`;
//            } else if (e.which !== 8 && !this.value.endsWith('-') && !this.value.endsWith('-0') && (this.value.length === 7 || this.value.length === 6)) {
//                this.value = `${this.value}-`;
//            }
//        } else if (valid && (input.length === 9 || input.length === 10)) {
//            this.style.backgroundColor = '#ffffff';
//        } else if (valid && this.value.length === 4 && !this.value.endsWith('-') && !this.value.endsWith('-0') && e.which !== 8) {
//            this.value = `${this.value}-`;
//        } else if (valid && (this.value.length === 7 || this.value.length === 6) && !this.value.endsWith('-') && !this.value.endsWith('-0') && e.which !== 8) {
//            this.value = `${this.value}-`;
//        }
//    });

    // $('input[name="email"]').on('focusout', function (e) {
    //     let valid = /^([a-zA-Z0-9_.+-])+\@(([a-zA-Z0-9-])+\.)+([a-zA-Z0-9]{2,4})+$/.test(this.value), input = this.value;
    //     if (!valid) {
    //         this.value = '';
    //         this.style.backgroundColor = '#EEA39C';
    //     }
    // });

})