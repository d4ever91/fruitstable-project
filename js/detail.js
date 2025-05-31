

function getProductDetail(){
  var currentUrl= getFullUrl();
  var url= new URL(currentUrl)
  var params= new URLSearchParams(url.search);
  var productId=params.get("id");
  var product= getProductById(productId)
  var detail=getProduct(product);
  var divM = document.getElementById("detail-product");
  divM.innerHTML = detail.outerHTML;
}

function getProduct(product){
  
  var divCon1 = document.createElement('div');
  var divCon2 = document.createElement('div');
  // var divR1 = document.createElement('div');
  var divC1 = document.createElement('div');
  var divR2  = document.createElement('div');
 


 divCon1.className ="container-fluid py-5 mt-5";
 divCon2.className ="container py-5";
//  divR1.className ="row g-4 mb-5";
 divC1.className ="col-lg-8 col-xl-9";
 divR2.className = "row g-4";


 var img =detailProductImg(product.fullImage);
 var detailData = detailProductData(product.name,product.categoryId,product.price,product.shortDescription,product.fullDescription)
 
  var buttonDesRev = DesRev();  
  var tabDiv = tabContent(product.reviews,product.shortDescription,product.fullDescription);
  var form1 = form();
  // var cat = categories();
 
  


 divR2.append(img)
 divR2.append(detailData);
 divR2.append(buttonDesRev)
 divR2.append(tabDiv);
 divR2.append(form1);
 divC1.append(divR2)
 
 divR1.append(divC1)
//  divR1.append(cat);

 console.log(divR1);
 divCon2.append(divR1)
 divCon1.append(divCon2)
 

 
  return divCon1;
}


function detailProductImg(url){
 
 var divID = document.getElementById('pic');
 var div = document.createElement('div');
 var a = document.createElement('a');
 var img = document.createElement('img');
 

 
 div.className = "border rounded";
 a.setAttribute("href","javascript.void(0);");
 img.setAttribute('src',url);
 img.className = 'img-fluid rounded';
 
 divID.append(div);
 div.append(a);
 a.append(img);
 return divID;
 

}




function detailProductData(name,categoryId,price,shortDescription,fullDescription){

 var div = document.getElementById('detail');
 
 var h4 =document.createElement('h4');
 h4.className = "fw-bold mb-3";
 h4.innerText = name;
 

 var p =  document.createElement('p');
 p.className = "mb-3";
 var category=getCategoryById(categoryId);
 p.innerText = category.name ;
 
 var h5 =  document.createElement('h5');
 h5.className = "fw-bold mb-3";
 h5.innerText = price ;

 var pShort = document.createElement('p');
 pShort.className = "mb-4";
 pShort.innerText = shortDescription;

 var pFull = document.createElement('p');
 pFull.className = "mb-4";
 pFull.innerText = fullDescription;

 var a = document.getElementById('cart');
 
 div.append(h4);
 div.append(p);
 div.append(h5);
 div.append(pShort)
 div.append(pFull);
 div.append(a);
 return div;
}




function DesRev(){ 

 var DesRev = document.getElementById("DesRev");
 // var nav = document.createElement('nav');

  var div = document.getElementById('change-tab-button').addEventListener("click",function() {


  var buttonRev= document.getElementById('nav-about-tab');

  buttonRev.setAttribute('type','button');
  buttonRev.setAttribute('role','tab');
  buttonRev.setAttribute("data-bs-toggle", "tab");
  buttonRev.setAttribute("data-bs-target", "#nav-about");
  buttonRev.setAttribute("aria-controls", "nav-about");
  buttonRev.setAttribute("aria-selected", "true");

  buttonRev.innerHTML = "<b>Description</b>";

  var buttonDes= document.getElementById('nav-mission-tab');

  buttonDes.setAttribute('type','button');
  buttonDes.setAttribute('role','tab');
  buttonDes.setAttribute("data-bs-toggle", "tab");
  buttonDes.setAttribute("data-bs-target", "#nav-about");
  buttonDes.setAttribute("aria-controls", "nav-about");
  buttonDes.setAttribute("aria-selected", "false");

  buttonDes.innerHTML = "<b>Reviews</b>";

  div.append(buttonRev);
  div.append(buttonDes);
 });
 // nav.append(div);
 DesRev.append(div);
 return DesRev;
}

function tabContent(reviews,shortDescription,fullDescription){
 var con = document.getElementById('DesRev');
 
 var tab= document.getElementById('tab');
 var tabAcitve = document.getElementById('nav-about');
 var p1 =document.createElement('p');
 var p2 = document.createElement('p');

 tabAcitve.setAttribute('role','tabpanel');
 tabAcitve.setAttribute('aria-labelledby','nav-about-tab');


 p1.innerText = shortDescription;
 p2.innerText = fullDescription;

 tabAcitve.append(p1);
 tabAcitve.append(p2);

 tab.append(tabAcitve);

 var div = document.getElementById("nav-mission");
 div.setAttribute('role','tabpanel');
 div.setAttribute('aria-labelledby','nav-mission-tab');


 reviews.forEach(review => {
 var div1 = document.createElement('div');
 div1.className ="d-flex";

 var img =document.createElement('img');
 img.setAttribute('src',review.img);
 img.className = 'img-fluid rounded-circle p-3';
 img.setAttribute('style',"width: 100px; height: 100px;");

 var div2 = document.createElement('div');
 div2.className = "yinyang";
 
 var p3 = document.createElement('p');
 p3.className = "mb-2";
 p3.setAttribute('style','font-size: 14px;');
 p3.innerText = "April1 12, 2025";

 var div3 = document.createElement('div');
 div3.className = "d-flex justify-content-between";
 div3.innerText = review.name;
  
 var starc = document.createElement('div');
 starc.className = "d-flex mb-3";
 rating =  parseInt(review.rating);
 
 for (let i = 1; i <= 5; i++) {
     var star = document.createElement('i');
     star.className = "fa fa-star";
      if(i<=rating){
       star.classList.add('text-secondary');
      }
     starc.append(star)         
}

 var p4 = document.createElement('p');
 p4.innerText = review.description;



 div3.append(starc);

 div2.append(p3)
 div2.append(div3,p4)

 div1.append(img)
 div1.append(div2)

 div.append(div1);
 });


 var vis =document.getElementById('nav-vision');
 vis.setAttribute('role','tabpanel');
 vis.setAttribute('aria-labelledby','nav-vision-tab');
 var p5 = document.createElement('p');
 p5.className='text-dark';
 p5.innerText ='Tempor erat elitr rebum at clita. Diam dolor diam ipsum et tempor sit. Aliqu diam amet diam et eos labore. 3';
 var p6 = document.createElement('p');
 p6.className = 'mb-0';
 p6.innerText ='Diam dolor diam ipsum et tempor sit. Aliqu diam amet diam et eos labore. Clita erat ipsum et lorem et sit';
 vis.append(p6)
 vis.append(p5)

 tab.append(div);
  tab.append(vis);
 con.append(tab);
 return con;
}

function form(){
 var form = document.createElement('form');
 form.setAttribute('action','#');

 
 var h4 = document.createElement('h4');
 h4.className = "mb-5 fw-bold";
 h4.innerText = 'Leave a Reply';

 var div = document.createElement('div');
 div.className = "row g-4";
 var div1= document.createElement('div');
 div1.className = "col-lg-6";
 var div2 = document.createElement('div');
 div2.className = "border-bottom rounded";
 var input = document.createElement('input');
 input.setAttribute('type','text');
 input.className = "form-control border-0 me-4";
 input.setAttribute('placeholder','Your Name');

 div2.append(input);
 div1.append(div2);

 var div3 =document.createElement('div');
 div3.className = "col-lg-6";
 var div4 = document.createElement('div');
 div4.className = "border-bottom rounded";
 var input1 = document.createElement('input');
 input1.setAttribute('type','email');
 input1.className = "form-control border-0";
 input1.setAttribute('placeholder','Your Email');

 div4.append(input1);
 div3.append(div4);

 var div5 =document.createElement('div');
 div5.className = "col-lg-12";
 var div6 = document.createElement('div');
 div6.className = "border-bottom rounded my-4";
 var textarea = document.createElement('textarea');
 textarea.className = "form-control border-0"
 textarea.setAttribute('cols','30')
 textarea.setAttribute('rows','8');
 textarea.setAttribute('placeholder','Your Review *')
 textarea.setAttribute('spellcheck','false')

 div6.append(textarea);
 div5.append(div6);

 var div7 = document.createElement('div');
 div7.className = 'col-lg-12';
 var div8 = document.createElement('div');
 div8.className = 'd-flex justify-content-between py-3 mb-5';
 var div9 = document.createElement('div');
 div9.className = 'd-flex align-items-center';
 var p = document.createElement('p');
 p.className = '"mb-0 me-3';
 p.innerText = 'Please rate:';
 var div10 = document.createElement('div');
 div10.className = 'd-flex align-items-center';
 div10.setAttribute('style','font-size: 12px;');
 
 for (let i=1; i<=5; i++){
 var star = document.createElement('i');
 star.className = 'fa fa-star';
div10.append(star);
 }

 var a = document.createElement('a');
 a.setAttribute('href','javascript.void(0)')
 a.className="btn border border-secondary text-primary rounded-pill px-4 py-3";
 a.setAttribute('type','submit');
 a.innerText ='Post Comment';
 div9.append(p,div10)
 div8.append(div9,a)
 div7.append(div8)

 div.append(div1,div3,div5,div7);
 form.append(h4,div);
 form.addEventListener('submit', async function(e) {
   e.preventDefault()
     var formdata = new FormData();
 
     formdata.append('name',input.value);
     formdata.append('email',input1.value);
     formdata.append('review',textarea.value);
 
     console.log(formdata.entries());
 })

 return form;
}

// function categories(){
//  var div = document.createElement('div');
//  div.className = "col-lg-4 col-xl-3"
//  var div1 = document.createElement('div');
//  div1.className = "row g-4 fruite"
//  var feature = document.getElementById('featured');

//  var div2 = document.createElement('div');
//  div2.className = "col-lg-12"
//  var div3 = document.createElement('div');
//  div3.className = 'input-group w-100 mx-auto d-flex mb-4'


//  var input = document.createElement('input');
//  input.className = "form-control p-3";
//  input.setAttribute('placeholder','keywords');
//  input.setAttribute('aria-descrbedby','search-icon-1');
//  var span = document.createElement('span');
//  span.id ='search-icon-1';
//  var i =document.createElement('i');
//  i.className = 'fa fa-search';
 


//  var div4 = document.createElement('div');
//  div4.className = 'mb-4';
//  var h4 = document.createElement('h4');
//   h4.innerText = 'Categories';
//   var ul = document.createElement('ul');
//    ul.id='shop-categories';
//  div4.append(h4,ul);
//  span.append(i);
//  div3.append(input,span);
//  div2.append(div3);
//  div2.append(div4);
//  div1.append(div2);
//  div1.append(feature);
 
//  div.append(div1);
//  return div;
// }

