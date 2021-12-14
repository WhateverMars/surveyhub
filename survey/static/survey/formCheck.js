document.addEventListener('DOMContentLoaded',() => {

    console.log(document.title)

    // disable login button initially
    document.querySelector('#loginBtn').disabled = true
    // disable password field initially
    document.querySelector('#password').disabled = true
    
    document.querySelector('#username').onkeyup = () => {

        // if username is not blank unlock password form
        if(document.querySelector('#username').value != ''){
            document.querySelector('#password').disabled = false
        }else{
            document.querySelector('#password').disabled = true
        }
    }

    document.querySelector('#password').onkeyup = () => {

        // check if form is not blank
        if(document.querySelector('#username').value != '' && document.querySelector('#password').value.length >= 8 ){
            
            document.querySelector('#loginBtn').disabled = false
            
            console.log('ready to submit')
        }else{

            document.querySelector('#loginBtn').disabled = true
            
        }
    }
    
})