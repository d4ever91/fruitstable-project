function getMenuItems(){
 var items= document.getElementById('nav-items');
 var navItems=getNavData();
 for(var i=0;i<navItems.length;i++){
   if(navItems[i].nav == true){
    var anchor =document.createElement('a'); 
    var  path =getCurrentUrl();
   anchor.href=navItems[i].link;
    if(navItems[i].link == path){
        var classList=navItems[i].class;
        classList += ' active';
    }
    else{
        var classList=navItems[i].class;
    }
    anchor.setAttribute('onclick',`route()`);
    anchor.className=classList;
    anchor.innerText=navItems[i].name
    items.append(anchor);
 }
}
}

function route(event){
  var event=event || window.event;
  event.preventDefault();
  window.history.pushState({},'',event.target.href);
  handleRouter();
}

function routeTo(href){
  var event= window.event;
  event.preventDefault();
  window.history.pushState({},'',href);
  handleRouter();
}

function handleRouter(){
 var routes= getNavData();
 var currentRoute= routes.find(rou=>window.location.pathname == rou.link);
  if(!currentRoute){
    var currentRoute= routes.find(rou=>rou.dynamic == true && window.location.pathname.includes(rou.link))
  }
 var templateHtml= urlRequest(currentRoute.template);
 document.getElementById('root').innerHTML=templateHtml;
 initiateTemplate();
 initiateFunctions(currentRoute.function);
}

function initiateTemplate(){
 var templates = getTemplateData()
 templates.forEach(temp=> include(temp.path,temp.name));
 getMenuItems();
}

function initiateFunctions(arr){
  arr.length ? arr.forEach(ar=> window[ar]()):null;
}

window.onpopstate=handleRouter;
window.route=route;
handleRouter();








