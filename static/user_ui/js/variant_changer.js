const variant_img_change_handler=(event)=>{
    console.log(event.target.id);
    let product_id=event.target.id.split('_')[0];
    let variant_id=event.target.id.split('_')[1];
    fetch(`/change_product_img_endpoint/${variant_id}/`)
      .then(response => response.json())
      .then(data => {
        console.log(data)
        if(data['status'] === 'success'){
          console.log(data)
          let img_url=data['image_url']
          
          let img_container= document.getElementById(`${product_id}_product_cover_img_container`);
          //img_container.innerHTML='';
          img_container.innerHTML=`
          <img id="${product_id}_product_cover_img" src="${img_url}" class="card-img-top img-fluid" alt="...">
          `

          let color_boxes=document.getElementsByName(`${product_id}_color_boxes`);
          for(let color_box of color_boxes){
            color_box.classList.remove("active");
          }
          document.getElementById(`${product_id}_${variant_id}_color_box`).classList.add("active");

          let product=data['product']
          let product_detail_container=document.getElementById(`${product_id}_product_detail_container`)
          product_detail_container.innerHTML=`
          <h5 class="card-title">${product.name}</h5>
        
          
          <div class="d-flex justify-content-center align-items-center" >
            ${parseInt(product.original_price) > parseInt(product.current_price) ? `<del class="me-1" style="font-size:14px; color:#7e7e7e;">Rs .${product.original_price}</del>`:''}

            ${product.offer !== null ? `<span class="ms-1 badge bg-success rounded-pill" style="height:fit-content;">${product.offer.percentage}%</span>` : ''}

          </div>
         
          <p class="product-card-price mb-1 text-success">Rs. ${product.current_price}</p>
  
          
          `;
        }
        
      })
  }