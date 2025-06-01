// promises are set of operations to be completed in javascript
function getGeolcation(){
  var obj=urlRequest('http://ip-api.com/json')
  var data= JSON.parse(obj);
  return data.country;
}
function getUsers(){
  var obj=urlRequest('/data/user.json')
  var data= JSON.parse(obj);
  return data;
}

function getUserByEmail(email){
  var data=getUsers()
  var email= data.find(dat=>dat.email == email)
  return email;
}

async function customerLogin(email,password){
  var response=await createRequest('http://127.0.0.1:5000/customer/login','POST',{ email,password})
  return response;
}

function getUserByPassword(password){
  var data=getUsers()
  var password= data.find(dat=>dat.password == password)
  return password;
}

function getCurrentUrl(){
    return window.location.pathname;
   }
   function getFullUrl(){
    return window.location.href;
   }
   
   function setLocalData(name,value){
     localStorage.setItem(name,value);
   }
   
   function getLocalData(name){
    return localStorage.getItem(name);
   }
   
function include(path,tempName){
    var obj=urlRequest(path)
    document.getElementById(`${tempName}-container`).innerHTML=obj;
}

function urlRequest(path){
    var req = new XMLHttpRequest();
    req.open('GET',path,false);
    req.send(null);
    return req.responseText;
}


async function createRequest(url,method,data){
  try{
    var response =await fetch(url, {method:method,body:JSON.stringify(data) })
    if(response.status != 200){
      throw new Error(response.message || "Error found")
    }
    return response;
  }
  catch(error){
    alert(error.message)
  }
}

  function getTemplateData(){
    var obj=urlRequest('/data/templates.json')
    var data= JSON.parse(obj);
    return data;
  }

function getNavData(){
    var obj=urlRequest('/data/nav.json')
    var data= JSON.parse(obj);
    return data;
  }
  
  
function getCategoriesData(){
    var obj=urlRequest('http://127.0.0.1:5000/api/categories')
    var data= JSON.parse(obj);
    return data.data;
}
  
  
function getProductsDataByCategory(catid){
    var obj=urlRequest(`http://127.0.0.1:5000/api/products/${catid}`)
    var data= JSON.parse(obj);
    return data.data;
}

function getProductsData(){
  var obj=urlRequest(`/data/products.json`)
  var data= JSON.parse(obj);
  return data;
}

async function getProductsDataByFilter(filter){
  try{
   var filterObj={}
   var filter1= filter.find(fil=>fil.name=="cat")
   var filter2= filter.find(fil=>fil.name=="price")
   var filter= filter.find(fil=>fil.name=="sort")
   if(filter.type == 'price' && filter.value == 'asc'){
    filterObj['price'] = 1
   }
   if(filter.type == 'price' && filter.value == 'dec'){
    filterObj['price'] = 0
   }

   if(filter1 && filter1.value){
    filterObj['cat_id'] = filter1.value
   }
   if(filter2 && filter2.value){
    filterObj['price_value'] = filter2.value
   }
    var response =await fetch('http://127.0.0.1:5000/api/products/all', { method:'POST',body:JSON.stringify(filterObj) })
    if(response.status != 200){
      throw new Error(response.message || "Error found")
    }
   var data = await response.json();
   return data.data;
  }
  catch(error){
    alert(error.message)
  }
}

function getSortDataAsc(param,data){
  return data.sort((a,b)=> a[param] - b[param]);
}

function getSortDataDec(param,data){
  return data.sort((a,b)=> b[param] - a[param]);
}
function getSortDataByCategory(param,data){
  return data.filter(product=>product.categoryId == param)
}
function getProductsCountByCategory(catid){
  var data= getProductsDataByCategory(catid);
  return data.length;
}
  
  
function getProductById(productid){
  var obj=urlRequest(`http://127.0.0.1:5000/api/product/${productid}`)
  var data= JSON.parse(obj);
  return data.data;
}

function getCategoryById(catid){
  var categories= getCategoriesData();
  return categories.find(category=>category.id == catid)
}
 

function getShipping(){
  var obj=urlRequest('/data/shipping.json')
  var data= JSON.parse(obj);
  return data;
}
 


function getCoupons(){
  var obj=urlRequest('/data/coupon.json')
  var data= JSON.parse(obj);
  return data;
}


function getMessages(){
  var obj=urlRequest('/data/messages.json')
  var data= JSON.parse(obj);
  return data;
}



function getErrorContainer(text){
 var error=  document.createElement('div');
 error.id="error";
 error.innerHTML=text;
 return error;
}



function getSuccessContainer(text){
  var error=  document.createElement('div');
  error.id="success";
  error.innerHTML=text;
  return error;
 }
 
 function messageHandler(message,type){
  var messages= document.getElementById('messages');
  if(type == 'error') {
    var errorContainer= getErrorContainer(message)
    messages.innerHTML =errorContainer.outerHTML;
  } 
  else{
    var successContainer= getSuccessContainer(message)
    messages.innerHTML = successContainer.outerHTML;
  }
 }

 function checkCartItem(productId){
  var productsData=getLocalData('products');
  var products=productsData ? JSON.parse(productsData) : [];
  var product= products.find(product=>product.id == productId)
  if(product) return true;
   return false;
}