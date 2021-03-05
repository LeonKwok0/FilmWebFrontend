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
    var kv = document.getElementById("keyword").value
    var type =  document.getElementById("category").value
    if(kv==""||type==""){
      alert("Please fill out this field")
      return []
    }
    url ="/search?type="+type+"&kv="+kv
    getJSON(url).then(function(resp){
      console.log("===========")
      console.log(resp)
    })
    

}

function clearForm(){
    document.getElementById("keyword").value="";
    document.getElementById("category").value="";
}