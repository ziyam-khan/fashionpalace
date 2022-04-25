// DOCUMENT START
$(document).ready(function(){
    $("#loadMore").on('click',function(){
        var _currentProducts=$(".product-box").length;
        var _limit=$(this).attr('data-limit');
        var _total=$(this).attr('data-total');

        // JQUERY AJAX TO SEND VALUE TO THE FUNCTION //
        $.ajax({
            url:'/load-more-data',
            data:{
                limit:_limit,
                offset:_currentProducts,
            },
            dataType:'json',
            beforeSend:function(){
                $("#loadMore").attr('disabled',true);
                $(".load-more-icon").addClass('fa-spin');
            },
            success:function(res){
                $("#filteredProducts").append(res.data);
                $("#loadMore").attr('disabled',false);
                $(".load-more-icon").removeClass('fa-spin');

                var _totalShowing=$(".product-box").length;
                if(_totalShowing==_total){
                    $("#loadMore").remove();
                }
            }
        });
        // END AJAX
    });
	// END


    // ////////// PRODUCT VARIATION //////////
	$(".choose-size").hide();

	// SHOW SIZE ACCORDING TO SELECTED COLOR
	$(".choose-color").on('click',function(){
		$(".choose-size").removeClass('active');
		$(".choose-color").removeClass('focused');
		$(this).addClass('focused');

		var _color=$(this).attr('data-color');

		$(".choose-size").hide();
		$(".color"+_color).show();
		$(".color"+_color).first().addClass('active');

		var _price=$(".color"+_color).first().attr('data-price');
		$(".product-price").text(_price);

	});
	// END

	// SHOW THE PRICE ACCORDING TO SELECTED SIZE
	$(".choose-size").on('click',function(){
		$(".choose-size").removeClass('active');
		$(this).addClass('active');

		var _price=$(this).attr('data-price');
		$(".product-price").text(_price);
	})
	// END

	// SHOW THE FIRST SELECTED COLOR
	$(".choose-color").first().addClass('focused');
	var _color=$(".choose-color").first().attr('data-color');
	var _price=$(".choose-size").first().attr('data-price');

	$(".color"+_color).show();
	$(".color"+_color).first().addClass('active');
	$(".product-price").text(_price);
    // END


    // ADD TO CART //
    $(document).on('click',".add-to-cart",function(){
		var _vm=$(this);
		var _index=_vm.attr('data-index');
		var _qty=$(".product-qty-"+_index).val();
		var _productId=$(".product-id-"+_index).val();
		var _productImage=$(".product-image-"+_index).val();
		var _productTitle=$(".product-title-"+_index).val();
		var _productPrice=$(".product-price-"+_index).text();
		// AJAX SERVER REQUEST
		$.ajax({
			url:'/add-to-cart',
			data:{
				'id':_productId,
				'image':_productImage,
				'qty':_qty,
				'title':_productTitle,
				'price':_productPrice
			},
			dataType:'json',
			beforeSend:function(){
				_vm.attr('disabled',true);
			},
			success:function(res){
				$(".cart-list").text(res.totalitems);
				_vm.attr('disabled',false);
			}
		});
		// END AJAX
	});
    // END

     /////////////////////////////////
	//// CART SESSION OPERATIONS ////
   /////////////////////////////////

    // DELETE ITEM FROM CART
    $(document).on('click','.delete-item',function(){
		var _pId=$(this).attr('data-item');
		var _vm=$(this);
		// AJAX
		$.ajax({
			url:'/delete-from-cart',
			data:{
				'id':_pId,
			},
			dataType:'json',
			beforeSend:function(){
				_vm.attr('disabled',true);
			},
			success:function(res){
				$(".cart-list").text(res.totalitems);
				_vm.attr('disabled',false);
				$("#cartList").html(res.data);
			}
		});
		// END AJAX
	});
    // END


    // UPDATE ITEM FROM CART //
	$(document).on('click','.update-item',function(){
		var _pId=$(this).attr('data-item');
		var _pQty=$(".product-qty-"+_pId).val();
		var _vm=$(this);
		// Ajax
		$.ajax({
			url:'/update-cart',
			data:{
				'id':_pId,
				'qty':_pQty
			},
			dataType:'json',
			beforeSend:function(){
				_vm.attr('disabled',false);
			},
			success:function(res){
				// $(".cart-list").text(res.totalitems);
				_vm.attr('disabled',false);
				$("#cartList").html(res.data);
			}
		});
		// END AJAX
	});
	// END


	// ADD WISHLIST //
	$(document).on('click',".add-wishlist",function(){
		var _pid=$(this).attr('data-product');
		console.log(_pid);
		var _vm=$(this);
		// Ajax
		$.ajax({
			url:"/add-wishlist",
			data:{
				product:_pid
			},
			dataType:'json',
			success:function(res){
				if(res.bool==true){
					_vm.addClass('disabled').removeClass('add-wishlist');
				}
			}
		});
		// END AJAX
	});
	// END


	// ACTIVATE SELECTED ADDRESS //
    $(document).on('click','.activate-address',function(){
		var _aId=$(this).attr('data-address');
		var _vm=$(this);
		// Ajax
		$.ajax({
			url:'/activate-address',
			data:{
				'id':_aId,
			},
			dataType:'json',
			success:function(res){
				if(res.bool==true){
					$(".address").removeClass('border-secondary');
					$(".address"+_aId).addClass('border-secondary');

					$(".check").hide();
					$(".actbtn").show();
					
					$(".check"+_aId).show();
					$(".btn"+_aId).hide();
				}
			}
		});
		// ENDAJAX
	});
    // END

	
	// PRODUCT REVIEW SAVE //
	$("#addForm").submit(function(e){
		$.ajax({
			data:$(this).serialize(),
			method:$(this).attr('method'),
			url:$(this).attr('action'),
			dataType:'json',
			success:function(res){
				if(res.bool==true){
					$(".ajaxRes").html('Data has been added.');
					$("#reset").trigger('click');
					// Hide Button
					$(".reviewBtn").hide();
					// End

					// create data for review
					var _html='<blockquote class="blockquote text-right">';
					_html+='<small>'+res.data.review_text+'</small>';
					_html+='<footer class="blockquote-footer">'+res.data.user;
					_html+='<cite title="Source Title">';
					for(var i=1; i<=res.data.review_rating; i++){
						_html+='<i class="fa fa-star text-warning"></i>';
					}
					_html+='</cite>';
					_html+='</footer>';
					_html+='</blockquote>';
					_html+='</hr>';

					$(".no-data").hide();

					// Prepend Data
					$(".review-list").prepend(_html);

					// Hide Modal
					$("#productReview").modal('hide');

					// Avg Rating
					$(".avg-rating").text(res.avg_reviews.avg_rating.toFixed(1))

				}
			}
		});
		// END AJAX
		e.preventDefault();
	});
	// END

	$(document).ready(function() {
		// executes when HTML-Document is loaded and DOM is ready
	   console.log("document is ready");
		 
	   
		 $( ".card" ).hover(
		 function() {
		   $(this).addClass('shadow').css('cursor', 'pointer'); 
		 }, function() {
		   $(this).removeClass('shadow');
		 }
	   );
		 
	   // document ready  
	});
	

});
// END DOCUMENT.READY

