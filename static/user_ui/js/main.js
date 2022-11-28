
const helpModalBtnHandler=(event)=>{
    let help_modal=document.getElementById("help_modal")
    console.log(help_modal)
    let help_button=document.getElementById("help-button");
    if(help_modal.style.display==="block"){
      help_button.innerText="Help"
    }
    else{
      help_button.innerText="Close"
    }
}

const mobile_filter_btn=(event)=>{
  let mobile_filter=document.getElementById("left-filter-layout");
  let filter_toggle_btn=document.getElementById("mobile-filter-btn-container");
  mobile_filter.classList.toggle("left-layout-open");
  filter_toggle_btn.classList.toggle("mobile-filter-btn-container-box-open");
}


const searchButton = document.querySelector(".link-search");
const closeButton = document.querySelector(".search-container .link-close");
const desktopNav = document.querySelector(".my-navbar-container");
const searchContainer = document.querySelector(".search-container");
const overlay = document.querySelector(".overlay");

searchButton.addEventListener("click", () => {
    desktopNav.classList.add("hide");
    searchContainer.classList.remove("hide");
    overlay.classList.add("show");
})

closeButton.addEventListener("click", () => {
    desktopNav.classList.remove("hide");
    searchContainer.classList.add("hide");
    overlay.classList.remove("show");
})

overlay.addEventListener("click", () => {
    desktopNav.classList.remove("hide");
    searchContainer.classList.add("hide");
    overlay.classList.remove("show");
})


$('.single-product-carousel').owlCarousel({
  loop:true,
  margin:10,
  nav:false,
  //animateOut: 'fadeOut',
  //autoplay:false,
  //autoplayTimeout: 2000,
  //autoplayHoverPause: true,
  responsive:{
      0:{
          items:1
      },
      600:{
          items:1
      },
      1000:{
          items:1
      }
  }
})

const ratingHandler=(event,element_name)=>{
  let rating_stars=document.getElementsByName(element_name);
  // console.log(rating_stars);
  // console.log(event.type);
  let current_star=parseInt(event.target.dataset.rating_value);
  if (event.type==="mouseover"){
    
    console.log(current_star);
    for(let i=0;i<current_star;i++){
      // console.log("target",event.target);
      if(rating_stars[i].classList.contains("rating_checked")){
        // console.log("contains")
      }
      else{
        rating_stars[i].style.color="#fbc634";
        // rating_stars[i].classList.add("rating_checked");
        // console.log(rating_stars[i]);
      }
      

    }
  }
  else if(event.type==="mouseout"){
    rating_stars[0].style.color="#cecece;"
    for(let i=current_star-1;i>=0;i--){
      console.log(rating_stars[i])
      
    }
  }
}


const btn = document.querySelector("button");
      // const post = document.querySelector(".post");
      const widget = document.querySelector(".star-widget");
      const editBtn = document.querySelector(".edit");
      btn.onclick = ()=>{
        widget.style.display = "none";
        // post.style.display = "block";
        editBtn.onclick = ()=>{
          widget.style.display = "block";
          // post.style.display = "none";
        }
        return false;
      }
