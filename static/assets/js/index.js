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

    $('#des').text(des)
    $('#desp').text(des)
    $('#inv').text(inv)
    $('#precio').text('$' + precio)
    $('#image-product-modal').attr('src', imagen)
    $('#exampleModal').modal('show');
    $('#slug-modal').val(slug)
    console.log(slug)

}

$('#buynow').on('click', function(){
    event.preventDefault();
    $('#form-modal').submit()
})

function sendForm(){
    // alert('asdasd')
    $('#checkout').submit();
}