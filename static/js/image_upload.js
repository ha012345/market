function readURL(input) {
    if (input.files && input.files[0]) {
        var reader = new FileReader();

        reader.onload = function (e) {
            $('#img').attr('src', e.target.result);
        }

        reader.readAsDataURL(input.files[0]);
    }
}
$("#avatar-upload").change(function(){
   readURL(this);
});


function check() {
  if(form.name.value == "") {
    alert("Please enter product name");
    form.name.focus();
    return false;
  }

  else if(form.price.value == "" && $("input:radio[name='options']:checked").val() == "option1") {
    alert("Please enter product price");
    form.price.focus();
    return false;
  }

  else if(form.seller_name.value == "") {
    alert("Please enter your name or phone number");
    form.seller_name.focus();
    return false;
  }

  else if(form.place.value == "") {
    alert("Please enter trading place.");
    form.price.focus();
    return false;
  }

  else if(form.photo.value == "") {
    alert("Please upload image.");
    form.price.focus();
    return false;
  }

  else return true;
}

$('#cancel').click( function() {
  window.history.back();
});
