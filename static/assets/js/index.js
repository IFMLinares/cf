function modalproduct(sku,des,inv,precio,imagen){
    // console.log(sku)
    // console.log(des)
    // console.log(inv)
    // console.log(precio)
    $('#des').text('')
    $('#desp').text('')
    $('#inv').text('')
    $('#precio').text('')

    $('#des').text(des)
    $('#desp').text(des)
    $('#inv').text(inv)
    $('#precio').text('$' + precio)
    $('#image-product-modal').attr('src', imagen)
    $('#exampleModal').modal('show');

}