// password requirements
// at least 8 characters
// Upper case and lower

function checkPassword(password){
    let hasLower = 0
    let hasUpper = 0

    for(let i = 0; i < password.length; i++) {

        asciiChar = password.charCodeAt(i)

        if (asciiChar >= 65 && asciiChar <= 90){

            hasUpper += 1

        }else if(asciiChar >= 97 && asciiChar <= 122){

            hasLower += 1

        }
    }

    let ReqLen = document.querySelector('#ReqLen');
    let ReqUpper = document.querySelector('#ReqUpper');
    let ReqLower = document.querySelector('#ReqLower');

    if (!hasLower){
        ReqLower.hidden = false;
    }else{
        ReqLower.hidden = true;
    }

    if(!hasUpper){
        ReqUpper.hidden = false;
    }else{
        ReqUpper.hidden = true;
    }

    if(password.length < 8){
        ReqLen.hidden = false;
    }else{
        ReqLen.hidden = true;
    }
    
    if(hasUpper && hasLower && password.length >= 8){

        //console.log('password is good')
        return 1
    }else{
        return 0
    }
}

document.addEventListener('DOMContentLoaded',() => {

    console.log(document.title)

    // disable reqister button
    document.querySelector('#registerBtn').disabled = true

    // disable password field initially
    document.querySelector('#email').disabled = true

    // disable password fields initially
    document.querySelector('#password').disabled = true
    document.querySelector('#confirmation').disabled = true
    
    document.querySelector('#username').onkeyup = () => {

        // if username is not blank unlock password form
        if(document.querySelector('#username').value != ''){
            document.querySelector('#email').disabled = false
        }else{
            document.querySelector('#email').disabled = true
        }
    }

    document.querySelector('#email').onkeyup = () => {

        // if username is not blank unlock password form
        if(document.querySelector('#email').value != ''){
            document.querySelector('#password').disabled = false
        }else{
            document.querySelector('#password').disabled = true
        }
    }

    document.querySelector('#password').onkeyup = () => {

        let password = document.querySelector('#password').value
        checkPassword(password)

        // if password is large enough unlock confirmation form
        if(checkPassword(password)){
            document.querySelector('#confirmation').disabled = false
        }else{
            document.querySelector('#confirmation').disabled = true
        }
    }
    
    
    document.querySelector('#confirmation').onkeyup = () => {

        if(document.querySelector('#username') != '' && checkPassword(document.querySelector('#password').value) && document.querySelector('#confirmation').value == document.querySelector('#password').value){
            
            document.querySelector('#registerBtn').disabled = false
            document.querySelector('#ReqMatch').hidden = true
            
            console.log('ready to submit')
        }else{

            document.querySelector('#ReqMatch').hidden = false
            document.querySelector('#registerBtn').disabled = true
            
        }
    }
    
})