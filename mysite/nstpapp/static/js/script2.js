$(document).ready(function() {


    // set password variable

    $('input[type=password]').keyup(function() {

        var pswd = $(this).val();
      //validate the length
        if ( pswd.length < 8 ) {
            $('#length').removeClass('valid').addClass('invalid');
            $('#password1').prop('required', true);
       

        } else {
            $('#length').removeClass('invalid').addClass('valid');
        }



        //validate letter
        if ( pswd.match(/[A-z]/) ) {
            $('#letter').removeClass('invalid').addClass('valid');
            $('#password1').prop('required', true);
        } else {
            $('#letter').removeClass('valid').addClass('invalid');
        }

        //validate capital letter
        if ( pswd.match(/[A-Z]/) ) {
            $('#capital').removeClass('invalid').addClass('valid');
        } else {
            $('#capital').removeClass('valid').addClass('invalid');
        }

        //validate number
        if ( pswd.match(/\d/) ) {
            $('#number').removeClass('invalid').addClass('valid');
        } else {
            $('#number').removeClass('valid').addClass('invalid');
        }

    }).focus(function() {
        $('#pswd_info').show();
    }).blur(function() {
        $('#pswd_info').hide();
    });
});