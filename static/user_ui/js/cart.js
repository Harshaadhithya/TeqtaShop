var updateBtns = document.getElementsByClassName('update-cart')



function updateCartTotal(){
	console.log("yess")
	let cartCount=document.getElementById('cart_total_badge');
	fetch('/returnCartTotal/')
	.then(response => response.json())
	.then(data => {
		let cart_total_qty=data['cart_total_qty']
		cartCount.innerText=cart_total_qty;
		console.log("here in",cart_total_qty)
	})
}


for (i = 0; i < updateBtns.length; i++) {
	updateBtns[i].addEventListener('click', function(){
		var productId = this.dataset.product_variant_id
		var action = this.dataset.action
		var page = this.dataset.page
		var btn_type= this.dataset.button_type
		console.log('productId:', productId, 'Action:', action)
		console.log('USER:', user)

		if (user == 'AnonymousUser'){
            // console.log("ananoymous user")
			addCookieItem(productId, action, page, btn_type)
		}else{
			updateUserOrder(productId, action, page, btn_type)
        }	
	})
}

function refreshCartDetails(cartData,user='logged in user'){
	if (user==='Anonymous User'){
		for (let order_item of cartData['items']){
			console.log(order_item['id']);
			document.getElementById(`${order_item['id']}_cart_quantity`).innerHTML=`<span>Quantity</span> : ${order_item['quantity']}`;
			document.getElementById(`${order_item['id']}_product_total`).innerText=`Rs. ${order_item['get_total']}`;
		}
		let subtotal=document.getElementById(`guest_id_order_subtotal`);
		let total=document.getElementById(`guest_id_order_total`);
		subtotal.innerText=`Rs. ${cartData['order']['get_cart_total']}`;
		total.innerText=`Rs. ${cartData['order']['get_cart_total']}`;
	}
	else{
		console.log("refresh cart",cartData['order_items']);
		for (let order_item of cartData['order_items']){
			console.log(order_item['id']);
			document.getElementById(`${order_item['id']}_cart_quantity`).innerHTML=`<span>Quantity</span> : ${order_item['quantity']}`;
			document.getElementById(`${order_item['id']}_product_total`).innerText=`Rs. ${order_item['product_total']}`;
		}
		let subtotal=document.getElementById(`${cartData['id']}_order_subtotal`);
		let total=document.getElementById(`${cartData['id']}_order_total`);
		subtotal.innerText=`Rs. ${cartData['cart_total']}`;
		total.innerText=`Rs. ${cartData['cart_total']}`;
	}
	
}

const removeFromCart=(event, user)=>{
	let product_id = event.target.dataset.product_id;
	let product_item_container = document.getElementById(`${product_id}_product_item_container`);
	// let cart_total_qty;
	if (user === 'AnonymousUser'){
		
		delete cart[product_id];
		document.cookie ='cart=' + JSON.stringify(cart) + ";domain=;path=/";
		cart_total_qty = Object.keys(cart).length;
		console.log("rem",cart_total_qty)
		product_item_container.style.display='none';

		if(parseInt(cart_total_qty)===0){
			location.reload();
		}
		else{
			updateCartTotal();
			fetch('/get_guest_cart_detail/')
			.then(response => response.json())
			.then(data => {
				console.log("guest cart",data);
				refreshCartDetails(data, 'Anonymous User')
			})
		}
		

		
	}
	else{
		let order_item_id=event.target.id.split('_')[0]
		
		fetch(`/removeCartItem/${order_item_id}/`)
		.then(response => response.json())
		.then(data => {
		  console.log(data);
		  if(data['msg']==='success'){
			product_item_container.style.display='none';
			
			updateCartTotal();
			refreshCartDetails(data);
		  }
		  cart_total_qty = data['cart_total_qty']
		  if(parseInt(cart_total_qty)===0){
			location.reload();
			}
		})
	}

	
	
}

function updateUserOrder(productId, action, page, btn_type){
	console.log('User is authenticated, sending data...')
	console.log(page)

		var url = '/updateCartItem/'

		fetch(url, {
			method:'POST',
			headers:{
				'Content-Type':'application/json',
				'X-CSRFToken':csrftoken,
			}, 
			body:JSON.stringify({'productId':productId, 'action':action})
		})
		.then((response) => {
		   return response.json();
		})
		.then((data) => {
		    // location.reload()
            console.log(data)
			
			if(data["status"]==="updated"){

				

				if (page === 'cart_page'){
					let item_detail_container=document.getElementById(`${productId}__product_item_detail`);
					
					if (btn_type === 'plus'){
						document.getElementById(`${productId}_quantity_field`).stepUp();
						console.log("plus",productId);
					}
					else if (btn_type === 'minus'){
						let quantity_field=document.getElementById(`${productId}_quantity_field`)
						quantity_field.stepDown();
						if(parseInt(quantity_field.value)===0){
							document.getElementById(`${productId}_product_item_container`).style.display='none';
						}
						console.log("minus",productId)
					}
					else{
						console.log("else",productId);
					}

					// this is used to check whether any items are still there in cart after updating the cart, if every item is removed and the cart is empty then it will reload the cart page to show the empty cart page
					fetch(`/get_order_item_endpoint/${data['order_item_id']}/`)
					.then(response => response.json())
					.then(data => {
						if (data['msg']==='deleted'){
							console.log("yes deleted");
							fetch('/returnCartTotal/')
							.then(response => response.json())
							.then(data => {
								let cart_total_qty=data['cart_total_qty'];
								console.log("fetch",cart_total_qty);
								if(parseInt(data['cart_total_qty'])===0){
								location.reload();
								}
							  })
						}
						
						console.log("cartd dta",data);
						refreshCartDetails(data,"logged in user");
						
					})
				}
				else{
				    location.href="/cart/"
				}
			}
			else{
				console.log("not updated")
				if(data['message']==='out of stock'){
					console.log("detail msg",data['detail_msg']);
					Swal.fire(`${data['detail_msg']}`,'',`${data['msg_tag']}`)
					return
				}
			}
			updateCartTotal();
		});
}

// for guest cart
function addCookieItem(productId, action, page, btn_type){
	console.log('User is not authenticated')

	if (action == 'add'){
		if (cart[productId] == undefined){
		cart[productId] = {'quantity':1}

		}else{
			cart[productId]['quantity'] += 1
		}
	}

	if (action == 'remove'){
		cart[productId]['quantity'] -= 1

		if (cart[productId]['quantity'] <= 0){
			console.log('Item should be deleted')
			delete cart[productId];
			
		}
	}
	console.log('CART:', cart)
	document.cookie ='cart=' + JSON.stringify(cart) + ";domain=;path=/";
	updateCartTotal();
	
	if (page === 'cart_page'){
		let item_detail_container=document.getElementById(`${productId}__product_item_detail`);
		
		if (btn_type === 'plus'){
			document.getElementById(`${productId}_quantity_field`).stepUp();
			console.log("plus",productId);
		}
		else if (btn_type === 'minus'){
			let quantity_field=document.getElementById(`${productId}_quantity_field`)
			quantity_field.stepDown();
			if(parseInt(quantity_field.value)===0){
				document.getElementById(`${productId}_product_item_container`).style.display='none';
			}
			console.log("minus",productId)
		}
		else{
			console.log("else",productId);
		}

		fetch('/returnCartTotal/')
		.then(response => response.json())
		.then(data => {
			let cart_total_qty = parseInt(data['cart_total_qty'])
			if (cart_total_qty <= 0){
				location.reload();
			}
		})

		fetch('/get_guest_cart_detail/')
		.then(response => response.json())
		.then(data => {
			console.log("guest cart",data);
			refreshCartDetails(data, 'Anonymous User')
		})
		// refreshCartDetails(data, 'Anonymous User')

		// fetch(`/get_order_item_endpoint/${data['order_item_id']}/`)
		// .then(response => response.json())
		// .then(data => {
		// 	if (data['msg']==='deleted'){
		// 		console.log("yes deleted");
		// 		fetch('/returnCartTotal/')
		// 		.then(response => response.json())
		// 		.then(data => {
		// 			let cart_total_qty=data['cart_total_qty'];
		// 			console.log("fetch",cart_total_qty);
		// 			if(parseInt(data['cart_total_qty'])===0){
		// 			location.reload();
		// 			}
		// 		  })
		// 	}
			
		// 	console.log("cartd dta",data);
		// 	refreshCartDetails(data);
			
		// })
	}
	else{
		location.href="/cart/"
	}
	
}