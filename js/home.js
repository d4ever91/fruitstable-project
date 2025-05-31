
  
  function getHeaderSlider(){
    var carousel= document.getElementById('carousel-slider');
    var categories =getCategoriesData();
    for(var i=0;i<categories.length;i++){
      var slideContainer =document.createElement('div');
      var slideImage =   document.createElement('img');
      var slideAnchor =  document.createElement('a');
      if(i==0){
          slideContainer.className ='carousel-item active rounded';
      }
      else{
          slideContainer.className ='carousel-item rounded';
      }
      
      slideImage.src ="http://127.0.0.1:5000/static/uploads/category/"+categories[i].image;
      slideImage.className ='img-fluid w-100 h-100 bg-secondary rounded';
      slideAnchor.href="javascript:void(0);";
      slideAnchor.className="btn px-4 py-2 text-white rounded";
      slideAnchor.innerText=categories[i].name;
      
      slideContainer.append(slideImage, slideAnchor);
      carousel.append(slideContainer);
     }
  
  }
  
  function getFeaturedCategories(){
      var catItems= document.getElementById('cat-items');
      var categories =getCategoriesData();
       for(var i=0;i<categories.length;i++){
        var containerCat =document.createElement('li');
        var anchorCat =   document.createElement('a');
        var spanCat =  document.createElement('span');
         containerCat.className ='nav-item';
        if(i == 0){
          anchorCat.className ='d-flex m-2 py-2 bg-light rounded-pill active';
        }
        else{
          anchorCat.className ='d-flex m-2 py-2 bg-light rounded-pill';
        }
  
         anchorCat.href=`#tab-${categories[i].id}`;
         anchorCat.setAttribute('data-bs-toggle','pill');
         spanCat.className ='text-dark';
         spanCat.style.width ='130px';
         spanCat.innerText=categories[i].name;
         anchorCat.append(spanCat);
         containerCat.append(anchorCat);
         catItems.append(containerCat);
        }
    }
  
    function getFeaturedProduct(product){
      var categories =getCategoriesData();
      var productItemContainer= document.createElement('div');
      var productItem= document.createElement('div');
      var productInnerContainer= document.createElement('div');
      var productCatContainer= document.createElement('div');
      var productNameContainer= document.createElement('div');
      var productPriceContainer= document.createElement('div');
      var productCartContainer= document.createElement('div');
      var productCartAction= document.createElement('a');
      var productCartIcon= document.createElement('i');
  
      productCatContainer.className="text-white bg-secondary px-3 py-1 rounded position-absolute";
      productCatContainer.id= 'product-category-name';
      productCatContainer.style.top="10px";
      productCatContainer.style.left="10px";
      productCatContainer.innerText=product.category_name;
     
      productInnerContainer.className ='rounded position-relative fruite-item';
      productItem.className= 'col-md-6 col-lg-4 col-xl-3';
      productItem.id='product-item';
  
      productNameContainer.className="p-4 border border-secondary border-top-0 rounded-bottom";
  
      productPriceContainer.className="text-dark fs-5 fw-bold mb-0";
      productPriceContainer.id="price-container";
    
      productCartAction.className="btn border border-secondary rounded-pill px-3 text-primary cart-btn"
      productCartIcon.className="fa fa-shopping-bag me-2 text-primary";
      productCartAction.setAttribute('product-id',`${product.id}`);
      var check= checkCartItem(product.id)
        if(check) {
          productCartAction.innerText="Go to cart"
        }
        else{
          productCartIcon.innerText="Add to Cart"
          productCartAction.append(productCartIcon);
        }
      productCartContainer.className="d-flex justify-content-between flex-lg-wrap";
      
      var img=getFeatureProductImage(product);
      var name= getFeatureProductName(product);
      var desc= getFeatureProductShortDescription(product);
      var price= getFeatureProductPrice(product);
      
  
      productPriceContainer.append(price);
      productNameContainer.append(name);
      productNameContainer.append(desc);
      productItem.append(productInnerContainer);
      productInnerContainer.append(img);
      productInnerContainer.append(productCatContainer);
      productInnerContainer.append(productNameContainer);
      productNameContainer.append(productCartContainer)
      productCartContainer.append(productPriceContainer)
      productCartContainer.append(productCartAction);
      productItemContainer.append(productItem)
      return productItemContainer;
    }
  
    function getCategoryTabs(){
      var tabContent= document.getElementById('tab-content');
      var categories =getCategoriesData();
      categories.forEach((cat,i)=>{
      var tabItem= document.createElement('div');
      var tabRow= document.createElement('div');
      var tabColumn= document.createElement('div');
      tabRow.className="row g-4";
      tabColumn.className="col-lg-12";
      tabItem.id=`tab-${cat.id}`;
      if(i == 0){
      tabItem.className="tab-pane fade show p-0 active";
      }
      else{
        tabItem.className="tab-pane fade show p-0";
      }
      tabItem.append(tabRow)
      tabRow.append(tabColumn);
      tabColumn.append(getFeaturedProducts(cat.id));
      tabContent.append(tabItem);
      });
    }
  
  function getFeaturedProducts(catid){
    var html="";
    var productContainer= document.createElement('div');
    productContainer.id='feature-product-container';
    productContainer.className='row g-4';
    var products=getProductsDataByCategory(catid);
    if(products.length == 0){
      return "No Products";
    }
    else{
      products.forEach(product=>{
      var productItem= getFeaturedProduct(product)
      html += productItem.innerHTML;
    })
    productContainer.innerHTML=html
    return productContainer;
  }
  }
    
  function getFeatureProductImage(product){
    var productImg= document.createElement('div');
    var anchorImg= document.createElement('a');
    anchorImg.href=`/product/${product.link}`
    anchorImg.setAttribute('onclick',`routeTo('/product/${product.link}')`)
    productImg.className= 'product-thumb-img';
    var containerProductImg =document.createElement('img');
    containerProductImg.className ="img-fluid w-100 rounded-top";
    containerProductImg.style="height:200px"
    containerProductImg.src ="http://127.0.0.1:5000/static/uploads/product/thumb/"+product.thumbnail_image;
    anchorImg.append(containerProductImg);
    productImg.append(anchorImg);
    return productImg;
  }
  
  function getFeatureProductName(product){
    var productName= document.createElement('h4');
    productName.innerText=product.name;
    return productName;
  }
  
  function getFeatureProductPrice(product){
    var productPrice=document.createElement('p');
    productPrice.innerText=`$ ${product.price}/kg`
    return productPrice;
  }
  function getFeatureProductShortDescription(product){
    var productDec= document.createElement('p');
    product.id="short-description"
    productDec.innerText=product.short_description
    return productDec;
  }

  
  
  
  
  