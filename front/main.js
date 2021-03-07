window.onload=handleTrending()

// fetch and change poster of home page 
async function handleTrending(){
    var data = await getJSON("/trending")
    var dataAir = await getJSON("/airtoday")
    // trending movies
    var imgtre = document.getElementById("imgtre")
    var introtre = document.getElementById("introtre")
    // air today
    var imgair = document.getElementById("imgair")
    var introair = document.getElementById("introair")
    var index = 0
    const change =()=>{
        var item = data[index]
        imgtre.style.backgroundImage= "url("+item["backdrop_path"]+")"
        introtre.innerHTML=item["title"] +"("+item["release_date"].substring(0,4)+")"
        
        var item2 = dataAir[index]
        imgair.style.backgroundImage= "url("+item2["backdrop_path"]+")"
        introair.innerHTML=item2["name"] +"("+item2["first_air_date"].substring(0,4)+")"
        index = (index==4)?0:++index
    }
    change()
    setInterval(function() {  
        change()
    },5000) //  change pic/per 5s 
}


async function getJSON(url) {
    try {
      let response = await fetch(url);
      return await response.json();
    } catch (error) {
      console.log('Request Failed', error);
      return []
    }
  }


function search(){
    var nores = document.getElementById("nores")
    document.getElementById("search_res").style.display="none"
    nores.style.display="none"

    var kv = document.getElementById("keyword").value
    var type =  document.getElementById("category").value
    
    if(kv==""||type==""){
      alert("Please fill out this field")
      return []
    }
    url ="/search?type="+type+"&kv="+kv
    getJSON(url).then(function(resp){
      
      if(resp.length == 0){
        nores.style.display="block"
      }else{
        showResult(resp)
      }
    })  
}


function showResult(data){
  document.getElementById("nores").display="none"
  document.getElementById("search_res").style.display="block"
  var one="";
  data.forEach(item => {
  one += `<div class="res_ele">
    <div class="res_left" style="background-image:url(${item.poster_path})"></div>
    <div class="res_right">
    <div class="stitle">${item.title}</div>
    <div class="year_type">
    <span clas="syear">${item.release_date.substring(0,4)}</span>
    <span class="stype"> |&nbsp${item.genres}</span>
    </div>
    <div>
        <span class="grade">&#9733;${item.vote_average/2}/5</span>
        <span class="votes">${item.vote_count}&nbsp votes</span>
    </div>
    <div class="sreview">${item.overview}</div>
    <button onclick="showDetail(${item.id},${item.type})">Show More</button>
    </div>
    </div>
    `
  });
  var group = document.getElementById("res_group")
  group.innerHTML = one
}

function showDetail(id,type){
  //  1 =tv 2 =movie

  var detail_all = document.getElementById("detail_all")
  var all_ele = document.getElementById("all_ele")
  detail_all.style.display="block"
  all_ele.style.opacity="0.3"
  all_ele.style.zIndex="-1"
  all_ele.style.position="fixed"
}

function closeDetail(){
  var detail_all = document.getElementById("detail_all")
  var all_ele = document.getElementById("all_ele")
  detail_all.style.display="none"
  all_ele.style.opacity="1"
  all_ele.style.zIndex="1"
  all_ele.style.position="relative"
}

function clearForm(){
    document.getElementById("keyword").value="";
    document.getElementById("category").value="";
    
}