function loginFormData(){
   var loginForm= document.querySelector('#login-form');
   loginForm.addEventListener('submit',async function(e){
     e.preventDefault()
     var email=document.getElementById('email').value
     var password=document.getElementById('password').value
     try {
     var response= await fetch(
        `http://127.0.0.1:5000/api/customer/login`,
       { method: "POST", body: JSON.stringify({ email,password }) }
     );
     if(response.ok){
      var data =await  response.json()
      messageHandler(data.message,'success')
      setLocalData('token',data.data.token)
      setLocalData('user',data.data.user.first_name +" "+ data.data.user.last_name)
      window.location="/";
     }
     else{
       var data =await  response.json()
       throw new Error(data.message)
     }
   }
   catch(error){
     messageHandler(error.message,'error')
   }
   });
}

function checkIfLogin(){
  var check=getLocalData('token');
  var user=getLocalData('user');
  if(check) {
     var loginPage= document.getElementById('login-page');
     var p= document.createElement('p');
     var p2= document.createElement('p');
     p2.innerHTML=`Welcome ${user}`
     p.innerHTML=`You have already login you can logout <a href="javascript.void(0)" onclick="logout()" id="logout"> here</a>`;
     loginPage.innerHTML=p2.outerHTML+p.outerHTML;
  }
  else{
    getLoginForm();
  }
}

function logout(){
    window.event.preventDefault();
    setLocalData('token',"");
    routeTo('/login');
}

function getLoginUser(){
    var userId=getLocalData('token') ? JSON.parse(getLocalData('token')) : '';
    return userId;
}

function getLoginForm(){
    var loginPage= document.getElementById('login-page');
    var form= document.createElement('form');
    var email= document.createElement('input');
    var password= document.createElement('input');
    var button= document.createElement('button');
    var messages= document.createElement('div');
    form.id="login-form";
  
    email.id="email";
    email.className="w-100 form-control border-0 py-3 mb-4";
    email.setAttribute('placeholder',"Enter Your Email")
    email.setAttribute('type',"email")
    email.setAttribute('required',true)

    password.id="password";
    password.className="w-100 form-control border-0 py-3 mb-4";
    password.setAttribute('placeholder',"Enter Your Password")
    password.setAttribute('type',"password")
    password.setAttribute('required',true)

    button.className="w-100 btn form-control border-secondary py-3 bg-white text-primary"
    button.setAttribute('type',"submit")
    button.innerText="login"

    messages.id="messages";
    var addOn="<p>Dont have an account ? <a onclick=routeTo('/register') href='/register'>Register</a> </p>";
    form.append(email)
    form.append(password)
    form.append(button)
    form.append(messages)
    loginPage.innerHTML=form.outerHTML+addOn;   
}


function getRegisterForm(){
  var loginPage= document.getElementById('register-page');
  var form= document.createElement('form');
  var firstName= document.createElement('input');
  var lastName= document.createElement('input');
  var email= document.createElement('input');
  var password= document.createElement('input');
  var button= document.createElement('button');
  var messages= document.createElement('div');
  form.id="register-form";


  firstName.id="firstName";
  firstName.className="w-100 form-control border-0 py-3 mb-4";
  firstName.setAttribute('placeholder',"Enter Your First Name")
  firstName.setAttribute('type',"text")
  firstName.setAttribute('required',true)


  lastName.id="lastName";
  lastName.className="w-100 form-control border-0 py-3 mb-4";
  lastName.setAttribute('placeholder',"Enter Your Last Name")
  lastName.setAttribute('type',"text")
  lastName.setAttribute('required',true)

  email.id="email";
  email.className="w-100 form-control border-0 py-3 mb-4";
  email.setAttribute('placeholder',"Enter Your Email")
  email.setAttribute('type',"email")
  email.setAttribute('required',true)

  email.id="email";
  email.className="w-100 form-control border-0 py-3 mb-4";
  email.setAttribute('placeholder',"Enter Your Email")
  email.setAttribute('type',"email")
  email.setAttribute('required',true)

  password.id="password";
  password.className="w-100 form-control border-0 py-3 mb-4";
  password.setAttribute('placeholder',"Enter Your Password")
  password.setAttribute('type',"password")
  password.setAttribute('required',true)

  button.className="register-btn w-100 btn form-control border-secondary py-3 bg-white text-primary"
  button.setAttribute('type',"submit")
  button.innerText="register"
  var addOn="<p>Already have an account ? <a onclick=routeTo('/login') href='/login'>Login</a> </p>";
  messages.id="messages";
  form.append(firstName)
  form.append(lastName)
  form.append(email)
  form.append(password)
  form.append(button)
  form.append(messages)
  loginPage.innerHTML=form.outerHTML+addOn;   
}

async function registerFormData(){
  var registerForm= document.querySelector('#register-form');
  registerForm.addEventListener('submit',async function(e){
    e.preventDefault();
    var first_name=document.getElementById('firstName').value
    var last_name=document.getElementById('lastName').value
    var email=document.getElementById('email').value
    var password=document.getElementById('password').value
    try {
    var response= await fetch(
       `http://127.0.0.1:5000/api/customer/register`,
      { method: "POST", body: JSON.stringify({ first_name,last_name,email,password }) }
    );
    if(response.ok){
     var data =await  response.json()
     messageHandler(data.message,'success')
     registerForm.reset()
    }
    else{
      var data =await  response.json()
      throw new Error(data.message)
    }
  }
  catch(error){
    messageHandler(error.message,'error')
  }
  });
}


