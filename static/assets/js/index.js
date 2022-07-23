function modalproduct(sku,des,inv,precio,imagen,slug){
    // console.log(sku)
    // console.log(des)
    // console.log(inv)
    // console.log(precio)
    $('#des').text('')
    $('#desp').text('')
    $('#inv').text('')
    $('#precio').text('')
    $('#slug-modal').val('')
    $('#sku_code').val('')

    $('#des').text(des)
    $('#desp').text(des)
    $('#inv').text(inv)
    $('#precio').text('$' + precio)
    $('#image-product-modal').attr('src', imagen)
    $('#exampleModal').modal('show');
    $('#slug-modal').val(slug)
    $('#sku_code').text(sku)
    // console.log(slug)
    var options= $('#'+ sku +'color option:not(:selected)')
    var options1= $('#'+ sku +'cant option:not(:selected)')
    console.log(options.length)
    console.log(options1.length)
    // console.log(options[1].innerHTML)
    // cant_selected
    if(options.length > 0){
    $('#color_selected').empty()
        for (var i = 0; i < options.length; i++) {
            // console.log(options[i].innerHTML)
            $('#color_selected').append($('<option>', { value : options[i].innerHTML })
            .text(options[i].innerHTML))
        }
    }else{
        $('#color_selected').empty()
        $('#color_selected').append($('<option>', { value : '' })
        .text(''))
        $('#modal-color').addClass('d-none')
        
    }
    if(options1.length > 0){
        $('#cant_selected').empty()
        for (var i = 0; i < options1.length; i++) {
        console.log(options1[i].innerHTML)
        $('#cant_selected').append($('<option>', { value : options1[i].innerHTML })
        .text(options1[i].innerHTML))
        }
    }else{
        $('#cant_selected').empty()
        $('#cant_selected').append($('<option>', { value : '' })
        .text(''))
        $('#modal-cant').addClass('d-none')
        
    }
    

}

$('#buynow').on('click', function(){
    event.preventDefault();
    $('#form-modal').submit()
})

function sendForm(){
    event.preventDefault();
    $('#checkout').submit();
}
$('#submitdetailform').on('click', function(){
    event.preventDefault()
    $('#detailform').submit()
})

$('#continue-payment').on('click', function(){
    event.preventDefault();
})