console.log("Hi,")
console.log("This is a assigment for csci 571, coded by LiangGuo.")
console.log("Thanks for Prof.Saty and all the TAs/Graders,")
console.log("Have a good day!")

window.onload = handleTrending()
// fetch and change poster of home page 
async function handleTrending() {
  var data = await getJSON("/trending")
  var dataAir = await getJSON("/airtoday")
  // trending movies
  var imgtre = document.getElementById("imgtre")
  var introtre = document.getElementById("introtre")
  // air today
  var imgair = document.getElementById("imgair")
  var introair = document.getElementById("introair")
  var index = 0
  const change = () => {
    var item = data[index]
    imgtre.style.backgroundImage = "url(" + item["backdrop_path"] + ")"
    introtre.innerHTML = item["title"] + "&nbsp;(" + item["release_date"].substring(0, 4) + ")"

    var item2 = dataAir[index]
    imgair.style.backgroundImage = "url(" + item2["backdrop_path"] + ")"
    introair.innerHTML = item2["name"] + "&nbsp;(" + item2["first_air_date"].substring(0, 4) + ")"
    index = (index == 4) ? 0 : ++index
  }
  change()
  setInterval(function () {
    change()
  }, 5000) //  change pic/per 5s 
}


async function getJSON(url) {
  //  for devlopment mode 
  // url = "http://127.0.0.1:5000"+url
  var retry_time = 0
  while (retry_time<5) {
    try {
      let response = await fetch(url);
      return await response.json();
    } catch (error) {
      retry_time +=1
      console.log("Request Failed, Retrying the " + retry_time +" time...." , error);
    }  
  }
  console.log('Retried more than 5 times, canceled')
  return [] 
}


//  check serach input  and send query 
function search() {
  var nores = document.getElementById("nores")
  document.getElementById("search_res").style.display = "none"
  nores.style.display = "none"

  var kv = document.getElementById("keyword").value
  var type = document.getElementById("category").value

  if (kv == "" || type == "") {
    alert("Please enter valid values.")
    return []
  }
  url = "/search?type=" + type + "&kv=" + kv
  getJSON(url).then(function (resp) {

    if (resp.length == 0) {
      nores.style.display = "block"
    } else {
      showResult(resp)
    }
  })
}

function clearForm() {
  document.getElementById("search_res").style.display="none"
  document.getElementById("keyword").value = "";
  document.getElementById("category").value = "";
}


//  fetch and display query result
function showResult(data) {
  document.getElementById("nores").display = "none"
  document.getElementById("search_res").style.display = "block"
  var one = "";
  data.forEach(item => {
    one += `<div class="res_ele">
    <div class="res_left" style="background-image:url(${item.poster_path})"></div>
    <div class="res_right">
    <div class="stitle">${item.title}</div>
    <div class="year_type">
    <span clas="syear">${item.release_date.substring(0, 4)}</span>
    <span class="stype"> |&nbsp${item.genres}</span>
    </div>
    <div>
        <span class="grade">&#9733;${item.vote_average / 2}/5</span>
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



// following are about display 
function closeDetail() {
  var detail_all = document.getElementById("detail_all")
  var all_ele = document.getElementById("all_ele")
  detail_all.style.display = "none"
  all_ele.style.opacity = "1"
  all_ele.style.zIndex = "1"
  all_ele.style.position = "relative"
  all_ele.style.top = 0+"px"
  window.scrollTo(0,current_y)
}

var current_y;
function showDetail(id, type) {
  // display popup 
  var detail_all = document.getElementById("detail_all")
  var all_ele = document.getElementById("all_ele")

  document.getElementById("basic_group").innerHTML = ""
  document.getElementById("cast_container").innerHTML =""
  document.getElementById("rev_container").innerHTML =""
  current_y= window.scrollY  // current y positon page 



  type = (type == 1) ? "tv" : "movie"
  showBasic(id, type)
  showCast(id, type)
  showRewiew(id, type)

  detail_all.style.display = "block"
  window.scrollTo(0,0)
  all_ele.style.opacity = "0.3"
  all_ele.style.zIndex = "-1"
  
  all_ele.style.position = "fixed"
  all_ele.style.top=-current_y+"px"

 
}

function showBasic(id, type) {
  url = "/media_basic?media_id=" + id + "&type=" + type
  getJSON(url).then(
    function (item) {
      document.getElementById("big_poster").style.backgroundImage = "url(" + item.backdrop_path + ")"
      var htmlEle = `
      <div>
          <span class="d_title">${item.name}</span>
          <a href="https://www.themoviedb.org/${type}/${id}" id="d_link" target="_blank">&nbsp;&nbsp;ⓘ</a>
      </div>
      <div id="d_year_type">
          <span id="d_year">${item.year}</span>
          <span id="d_type"> |&nbsp${item.genres}</span>
      </div>
      <div>
          <span id="d_grade">&#9733;${item.vote_average}/5</span>
          <span id="d_votes">${item.vote_count}&nbsp votes</span>
      </div>
      <div id="d_review">
      ${item.overview}
      </div>
      <div id="lag">Spoken languages: ${item.spoken_languages}</div>
      `
      document.getElementById("basic_group").innerHTML = htmlEle
    }
  )
}

function showCast(id, type) {
  url = "/media_cast?media_id=" + id + "&type=" + type
  getJSON(url).then(
    function (resp) {
      var all_ele = ""
      resp.forEach(item => {
        all_ele += `
        <div class="cast_ele">
        <div class="cast_img" style="background-image: url(${item.profile_path});"></div>
        <div class="cast_name">${item.name}</div>
        <div>AS</div>
        <div class="character">${item.character}</div>
        </div>
        `
      })
      document.getElementById("cast_container").innerHTML = all_ele
    }
  )

}

function showRewiew(id, type) {
  url = "/media_review?media_id=" + id + "&type=" + type
  getJSON(url).then(
    function (resp) {
      let all_ele = ""
      resp.forEach(item => {
        all_ele += `
        <div class="rev_ele">
        <div class="rev_ur">
            <span class="rev_user">${item.username}</span> on
            <span class="rev_date">${item.created_at}</span>
        </div>
        <div class="rev_rating" style="display:${(item.rating==-1)?'none':'block'}">&#9733;${item.rating}/5</div>
        <div class="rev_content">${item.content}</div>
        <div class="line_container">
            <div class="rev_line"></div>
        </div>
        </div>
        `
        document.getElementById("rev_container").innerHTML = all_ele
      })
    })

}


