

function cartAction(){
    var cartActionBtns=document.querySelectorAll('.cart-btn');
    cartActionBtns.forEach(cartAction=>{
      cartAction.addEventListener('click',function(e){
        e.preventDefault();
        var productId=this.getAttribute('product-id');
        var check=  checkCartItem(productId)
        if(!check){
        var product=getProductById(productId);
        var cartValue= document.getElementById('shopping-bag').innerText;
        cartValue++;
        document.getElementById('shopping-bag').innerText=cartValue;
        setLocalData('cartCount',cartValue);
        var productsData=getLocalData('products');
        var products=productsData ? JSON.parse(productsData) : [];
        product.cartQty=1;
        product.userId=getLoginUser()
        products.push(product);
        setLocalData('products',JSON.stringify(products));
        cartAction.innerText="Go to cart";
        }
        else{
          routeTo('/cart')
        }
      });
    })
  }



  function updateCartItems(id){
    var inputElement= document.getElementById(`product-${id}`)
    var newQty=parseInt(inputElement.value);
    var products=JSON.parse(getLocalData("products"));
    var index=products.findIndex(product=>product.id == id );
    products[index].cartQty=newQty;
    setLocalData("products",JSON.stringify(products));
    var subTotalPrice =0;
    products.forEach(product=>{
      subTotalPrice += product.price*product.cartQty
    })
    setSubCartTotal(subTotalPrice+" $");
    var couponValue= getCouponValue();
    if(couponValue){

    subTotalPrice -= couponValue;
    setCouponValue(couponValue)
    }
    setShippingLocation()
    var shippingValue= setShippingRate();
    setGrandTotal(subTotalPrice,shippingValue);
  }

function getCartCount(){
    document.getElementById('shopping-bag').innerText=getLocalData('cartCount') || 0;
}

function getCartItems(){
 var products= getLocalData('products');
 var splitData= JSON.parse(products)
 return splitData;
}

function getCartBody(){
  var html=''
 var tBody=document.getElementById('cart-item');
 var products= getCartItems();
 var id=getLoginUser()
 if(id) products = products.filter(pro=>pro.userId == id)
  var subTotalPrice=0;
 if(products && products.length){
 products.forEach(product=>{
   var tr=getCartRow(product);
   html += tr.outerHTML;
   subTotalPrice += product.price*product.cartQty
 })
 tBody.innerHTML=html;
 setSubCartTotal(subTotalPrice+" $");
 setShippingLocation()
 var shippingValue= setShippingRate();
 setGrandTotal(subTotalPrice,shippingValue)
}
else{
  tBody.innerHTML="<h4>Cart is empty</h4>"
  setSubCartTotal(0+" $");
  setShippingLocation()
  setGrandTotal(0,0)
}
}

function getCartRow(product){
  var tr=document.createElement('tr');
  var img=getProductCartImage(product.thumbnailImage)
  var name=getProductCartName(product.name)
  var price=getProductCartPrice(product.price)
  var qty=getProductCartQty(product)
  var totalPrice=getProductCartTotalPrice(product)

  var cartAction=getProductCartAction(product.id)
  
  tr.append(img)
  tr.append(name)
  tr.append(price)
  tr.append(qty)
  tr.append(totalPrice)
  tr.append(cartAction)
  return tr;
}

function getProductCartImage(url){
  var th=document.createElement('th');
  var imgContainer=document.createElement('div');
  var imgInner=document.createElement('img');
  imgContainer.className="d-flex align-items-center";
  imgInner.setAttribute('src',url);
  th.setAttribute('scope','row');
  imgInner.className="img-fluid me-5 rounded-circle";
  imgInner.style="width: 80px; height: 80px;";
  imgContainer.append(imgInner);
  th.append(imgContainer)
  return th;
}

function getProductCartName(name){
  var td=document.createElement('td');
  var p=document.createElement('p');
  p.className="mb-0 mt-4";
  p.innerText=name;
  td.append(p)
  return td;
}

function getProductCartPrice(price){
  var td=document.createElement('td');
  var p=document.createElement('p');
  p.className="mb-0 mt-4";
  p.innerText=price+" $";
  td.append(p)
  return td;
}

function getProductCartTotalPrice(product){
  var td=document.createElement('td');
  var p=document.createElement('p');
  p.id=`total-price-${product.id}`;
  p.className="mb-0 mt-4";
  p.innerText=product.price*product.cartQty+" $";
  td.append(p)
  return td;
}

function getProductCartQty(product){
  var td=document.createElement('td');
  var div=document.createElement('div');
  var divMinus=document.createElement('div');
  var divPlus=document.createElement('div');
  var buttonMinus=document.createElement('button');
  var buttonPlus=document.createElement('button');
  var iMinus=document.createElement('i');
  var iPlus=document.createElement('i');
  var input=document.createElement('input');

  div.className="input-group quantity mt-4";
  div.style="width: 100px;";
  
  divMinus.className="input-group-btn"
  divPlus.className="input-group-btn"

  buttonMinus.className="btn btn-sm btn-minus rounded-circle bg-light border"
  buttonPlus.className="btn btn-sm btn-plus rounded-circle bg-light border"

  buttonMinus.setAttribute('onclick',`removeItemQty(${product.id})`)
  buttonPlus.setAttribute('onclick',`addItemQty(${product.id})`)

  iMinus.className="fa fa-minus";
  iPlus.className="fa fa-plus";

  input.className="form-control form-control-sm text-center border-0"
  input.setAttribute('type','text');
  input.id='product-'+product.id;
  input.setAttribute('value',product.cartQty)
  divMinus.append(buttonMinus)
  buttonMinus.append(iMinus)
  
  divPlus.append(buttonPlus)
  buttonPlus.append(iPlus)

  div.append(divMinus)
  div.append(input)
  div.append(divPlus)
  td.append(div);
  return td;
}

function getProductCartAction(id){
  var td=document.createElement('td');
  var button=document.createElement('button');
  var i=document.createElement('i');
  button.className="btn btn-md rounded-circle bg-light border mt-4";
  button.id=id;
  button.setAttribute('onclick',`removeProduct(${id})`);
  i.className="fa fa-times text-danger";
  button.append(i);
  td.append(button);
  return td;
}

function addItemQty(id){
  var totalPriceElement= document.getElementById(`total-price-${id}`)
 var inputElement= document.getElementById(`product-${id}`)
 var product=getProductById(id)
;
 if(inputElement.value == product.qty){
  inputElement.setAttribute('disabled',true);
}
else{
  inputElement.value++;
}
var totalPrice=parseInt(inputElement.value) * parseInt(product.price)
totalPriceElement.innerText=totalPrice+" $";
updateCartItems(id)

}

function removeItemQty(id){
  var inputElement= document.getElementById(`product-${id}`)
  var totalPriceElement= document.getElementById(`total-price-${id}`)
  var product=getProductById(id)
;
  if(inputElement.value < 2){
    inputElement.setAttribute('disabled',true);
  }
  else{
    inputElement.value--;
  }
  var totalPrice=parseInt(inputElement.value) * parseInt(product.price)
  totalPriceElement.innerText=totalPrice+" $";
  updateCartItems(id)

}

function removeProduct(id){
  var products= JSON.parse(getLocalData('products'));
  var products= products.filter(product=>product.id != parseInt(id));
  setLocalData('products',JSON.stringify(products))
  getCartBody();
  var cartValue= document.getElementById('shopping-bag').innerText;
  cartValue--;
  document.getElementById('shopping-bag').innerText=cartValue;
  setLocalData('cartCount',cartValue);
}

function setSubCartTotal(subTotalPrice){
 var subTotal= document.getElementById('subtotal');
  var h5=document.createElement('h5');
  var p=document.createElement('p');
  h5.className="mb-0 me-4";
  h5.innerText="Subtotal:"
  p.innerText=subTotalPrice;
  subTotal.innerHTML=h5.outerHTML+p.outerHTML;
}


function setShippingRate(){
 var shippingData=getShipping();
 var shipping= document.getElementById('shipping');
 var h5=document.createElement('h5')
 h5.className="mb-0 me-4";
 h5.innerText = "Shipping";
 var div=document.createElement('div')
var p= document.createElement('p');
p.className="mb-0";
p.innerText=`Flat rate: $${shippingData.value}.00`
div.append(p);
shipping.innerHTML=h5.outerHTML+div.outerHTML;
return shippingData.value;
}

function setShippingLocation(){
 var country= getGeolcation();
  var shippingLocation= document.getElementById('location');
  var p=document.createElement('p')
  p.className="mb-0 text-end";
  p.innerText = `Shipping to ${country}`;
 shippingLocation.innerHTML=p.outerHTML;
 }
function setGrandTotal(subTotal,shippingValue){
  var  grandTotal= subTotal+shippingValue
  var total= document.getElementById('total');
  var h5=document.createElement('h5')
  h5.className="mb-0 ps-4 me-4";
  h5.innerText = "Total";
  var p= document.createElement('p');
  p.className="mb-0 pe-4";
  p.innerText=`$${grandTotal}`
  total.innerHTML=h5.outerHTML+p.outerHTML;
 }


 function applyCoupon(){

   var input= document.getElementById('coupon-input');

   var message=getMessages();
   var btn= document.querySelector('#coupon-btn');
  btn.addEventListener('click',(e)=>{
    e.preventDefault();
    var couponAmmount= getCouponValue();
    if(!couponAmmount) {
       messageHandler(message.COUPON_ERROR,'error')
      return;
  }
  var subTotal=setCouponValue(couponAmmount)
    var shippingValue= setShippingRate();
    setGrandTotal(subTotal,shippingValue)
    input.setAttribute('disabled',true);
    btn.setAttribute('disabled',true);
    input.after(couponCloseButton());
    messageHandler(message.COUPON_SUCCESS,'success')
   })
 }

 function getCouponValue(){
  var coupons=getCoupons();
  var input= document.getElementById('coupon-input').value;
  var coupon=coupons.find(coupon=>coupon.code == input);
  if(!coupon) return 0;
  var subTotal= document.getElementById('subtotal').lastChild;
  subTotal= parseInt(subTotal.innerText.replace('$',''));
  var discountValue=subTotal*coupon.value/100;
  return discountValue;
 }

 function couponCloseButton(){
 var button=  document.createElement('button')
 var i=  document.createElement('i')
 button.id="btn-coupon-remove";
 button.className="btn-coupon-close btn btn-md mt-4";
 i.className="fa fa-times text-danger";
 button.setAttribute('onclick',"removeCoupon()");
 button.append(i);
 return button;
 }


 function removeCoupon(){
  var couponForm= document.getElementById('coupon-form');
  var couponContainer= document.getElementById('coupon');
  var closeBtn= document.getElementById('btn-coupon-remove');
  var btn= document.getElementById('coupon-btn');
  var input= document.getElementById('coupon-input');
  var message=getMessages();
  var couponAmmount= getCouponValue();
  var subTotal=setCouponValue(couponAmmount)
  subTotal += couponAmmount;
  setShippingLocation()
  var shippingValue= setShippingRate();
  setGrandTotal(subTotal,shippingValue);
  btn.removeAttribute('disabled')
  input.removeAttribute('disabled')
  input.setAttribute('value','')
  messageHandler(message.COUPON_REMOVED,'success');
  closeBtn.parentNode.removeChild(closeBtn);
  couponContainer.innerHTML="";
  couponForm.reset()
 }

 function setCouponValue(couponAmmount){
  var couponContainer= document.getElementById('coupon');
  var h5=document.createElement('h5');
  var p=document.createElement('p');
  var subTotal= document.getElementById('subtotal').lastChild;
  subTotal= parseInt(subTotal.innerText.replace('$',''));
  subTotal= subTotal -couponAmmount;
  h5.className="mb-0 me-4";
  h5.innerText="Coupon:";
  p.innerText="-"+couponAmmount+"$";
  couponContainer.innerHTML=h5.outerHTML+p.outerHTML;
  return subTotal;
 }

