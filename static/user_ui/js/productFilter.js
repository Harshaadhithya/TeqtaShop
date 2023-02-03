filter_inputs=document.getElementsByName("filter-product");
paginationBtns=document.getElementsByName("pagination-btn");
// console.log(filter_inputs);
let selected_filters=new Object;
// console.log(selected_filters);

const populateProducts=(e)=>{
    let formData=new FormData();
    let filter_type=e.target.dataset.filter;
    let search_query = document.getElementById("search_query").value;
    let products_list_container = document.getElementById("products-list-container");
    let pagination_container = document.getElementById("pagination-wrapper");
    console.log(e.target.value,e.target.dataset.filter);
    selected_filters[filter_type]=Array.from(document.querySelectorAll(`input[data-filter=${filter_type}]:checked`)).map(function (input){
        return input.value;
    });
    formData.append('csrfmiddlewaretoken', csrftoken);
    formData.append('selected_filters',JSON.stringify(selected_filters));
    
    // selected_filters[]
    console.log(JSON.stringify(selected_filters));
    fetch(`/filter_products/?search_query=${search_query}`,{
        method: 'POST',
        body: formData
    })
    .then(response => response.json())
    .then(data => {
        // console.log(typeof(data.template_text),data.template_text);
        products_list_container.innerHTML=``;
        products_list_container.innerHTML=data.template_text;
        pagination_container.innerHTML=``;
        pagination_container.innerHTML=data.pagination_template;
    });
}

for(filter_input of filter_inputs){
    selected_filters[filter_input.dataset.filter]=new Array;   //filter_input.dataset.filter -> gives key for selected_filters object (i.e category,color,compatibilty) and initializes it with empty array for each key => {category:[],color:[],compatibility:[]}
    filter_input.addEventListener("input",populateProducts);
    // console.log(filter_input.dataset.filter);
}


const paginationHandler=(event)=>{
    console.log("yes");
    event.preventDefault();
    let page_no = event.target.dataset.page_no;
    let formData=new FormData();
    let search_query = document.getElementById("search_query").value;
    let filter_inputs = document.getElementsByName("filter-product");
    let products_list_container = document.getElementById("products-list-container");
    let pagination_container = document.getElementById("pagination-wrapper");
    for(filter_input of filter_inputs){
        let filter_type = filter_input.dataset.filter
        selected_filters[filter_type]=Array.from(document.querySelectorAll(`input[data-filter=${filter_type}]:checked`)).map(function (input){
            return input.value;
        });
    }
    formData.append('csrfmiddlewaretoken', csrftoken);
    formData.append('selected_filters',JSON.stringify(selected_filters));
    console.log(selected_filters);

    fetch(`/filter_products/?search_query=${search_query}&page_no=${page_no}`,{
        method: 'POST',
        body: formData
    })
    .then(response => response.json())
    .then(data => {
        console.log(typeof(data.template_text),data.template_text);
        products_list_container.innerHTML=``;
        products_list_container.innerHTML=data.template_text;
        pagination_container.innerHTML=``;
        pagination_container.innerHTML=data.pagination_template;
    });

  };

// for (pagination_btn of paginationBtns){
//     pagination_btn.addEventListener("click", paginationHandler);
// }

console.log(selected_filters);

