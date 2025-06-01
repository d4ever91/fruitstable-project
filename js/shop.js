

var filter =[{name:"price",value:500,type:"order"},{ name:"sort",value:"asc",type:"price"},{ name:"cat",value:null,type:"find"},{ name:"search",value:null,type:"search"} ];
var products =[];

function getListProducts(){
  var html='';
  var productContainer= document.getElementById('product-list');
    if(products.length == 0){
      html += '<h3>No Products</h3>'
      productContainer.innerHTML=html;
      return productContainer;
    }
    else{
        products.forEach(product=>{
        var productItem= getFeaturedProduct(product)
        html += productItem.innerHTML;
      })
      productContainer.innerHTML=html
      var productItem =document.querySelectorAll("#product-item");
      productItem.forEach(item=>item.classList.remove('col-xl-3') && item.classList.remove('col-xl-4'))
      return productContainer;
    }
  }

  function getShopCategories(){
    var catContainer=  document.getElementById('shop-categories');
   var catData= getCategoriesData();
   catData.forEach(cat=>{
    var listItem= document.createElement('li');
    var divItem= document.createElement('div');
    var anchorItem= document.createElement('a');
    var spanItem= document.createElement('span');
    var iItem= document.createElement('i');
    divItem.className="d-flex justify-content-between fruite-name";
    iItem.className="fas fa-apple-alt me-2"
    anchorItem.id="cat-anchor";
    anchorItem.setAttribute("catid",cat.id);
    anchorItem.setAttribute("href","javascript.void(0);");
    var count= getProductsCountByCategory(cat.id);
    spanItem.innerText=`(${count})`
    listItem.append(divItem)
    divItem.append(anchorItem)
    anchorItem.append(iItem)
    anchorItem.append(cat.name)
    divItem.append(spanItem)
    catContainer.append(listItem)
   })
  }

  async function filterProductsByPrice(){
    var rangeInput=document.querySelector('#rangeInput');
    rangeInput.value=filter.find(fil=>fil.name=="price").value;
    document.getElementById('amount').innerText=filter.find(fil=>fil.name=="price").value
    rangeInput.addEventListener('change',async function(){
      var rangeValue=  document.getElementById('amount').innerText;
      for(var i=0;i<filter.length;i++){
        if(filter[i].type=='order'){
        filter[i].value=rangeValue;
        }
      }
      products= await getProductsDataByFilter(filter);
      console.log(products)
      getListProducts();
    })
    products=await getProductsDataByFilter(filter);
    getListProducts();
  }

  async function sortProductByPrice(){
    var sortFilter=document.querySelector('#sort-price');
    sortFilter.addEventListener('change',async ()=>{
      var sortValue=document.getElementById('sort-price').value;
      for(var i=0;i<filter.length;i++){
        if(filter[i].name=="sort")
         filter[i].value=sortValue;
      }
      products = await getProductsDataByFilter(filter);
      console.log(products)
      getListProducts();
    })
  }


  async function sortProductByName(){
    var sortFilter=document.querySelector('#sort-name');
    sortFilter.addEventListener('change',async ()=>{
      var sortValue=document.getElementById('sort-name').value;
      for(var i=0;i<filter.length;i++){
        if(filter[i].name=="sort")
         filter[i].value=sortValue;
      }
      products= await getProductsDataByFilter(filter);
      getListProducts();
    })
  }



  async function filterProductByCategory(){
    var catQuery=document.querySelectorAll('#cat-anchor');
    catQuery.forEach(catQu=>{
      catQu.addEventListener('click',async(e)=>{
        e.preventDefault();
        var classListAll=[]
        var cat= catQu.getAttribute('catid');
        var hasClass=catQu.classList.contains('active');
        catQuery.forEach(item => item.classList.remove('active'));
        hasClass ? catQu.classList.remove('active') :  catQu.className="active";
        catQuery.forEach(item => {
          var catId= catQu.getAttribute('catid');
          if(item.classList.contains('active')) { classListAll.push(catId) }
        });
        for(var i=0;i<filter.length;i++){
          if(filter[i].name=="cat"){
            classListAll.length ? filter[i].value=cat:filter[i].value=null;
          }
        }
        products=await getProductsDataByFilter(filter);
        getListProducts();
      })
    })

  }


  function searchQuery(){
    var searchFrom= document.querySelector('#search-form');
    searchFrom.addEventListener('submit',(e)=>{
      e.preventDefault();
      var search= document.getElementById("search").value;
      routeTo(`/shop?q=${search}`)
    })
  }