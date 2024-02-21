function viewpass(){
    var inputPass = document.getElementById('pass')
    var btnShowPass = document.getElementById('btn-pass')

    if(inputPass.type === 'password'){
        inputPass.setAttribute('type','text')
        btnShowPass.classList.replace('bi-lock-fill','bi-unlock-fill')
    }else{
        inputPass.setAttribute('type','password')
        btnShowPass.classList.replace('bi-unlock-fill','bi-lock-fill')
    }
}
      