function check() {
  var con = confirm("정말 삭제하시겠습니까?");
  if(con == true)
    return true;

  else (con == false)
    return false;
}
