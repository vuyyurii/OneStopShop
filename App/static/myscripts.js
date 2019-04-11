
var aNP = function()
{
    document.getElementById("upload-form").submit();
    var name = document.getElementById("pname").value;
    var price = document.getElementById("pprice").value;
    var category = document.getElementById("pcat").value;
    var description = document.getElementById("pdes").value;
    var num = document.getElementById("pcount").value;
    var img = document.getElementById("file-picker").value;
    var seller = '{{ naam }}';
    console.log(window.location.href );
    console.log(img);
    console.log(seller);
var csrf_token = "{{ csrf_token() }}";

    $.ajaxSetup({
        beforeSend: function(xhr, settings) {
            if (!/^(GET|HEAD|OPTIONS|TRACE)$/i.test(settings.type) && !this.crossDomain) {
                xhr.setRequestHeader("X-CSRFToken", csrf_token);
            }
        }
    });
    $(document).ready(function(){
        $.ajax({
            url:'http://127.0.0.1:5000/addProduct',
            method:'POST',
            data:{
                name:name,price:price,category:category,description:description,num:num,seller:seller,img:img,
            },
            success:function(response){
                console.log(response);
                //viewAllProducts();
                return response;
            },
            error:function(jqXHR,exception){
                console.log(jqXHR.responseText);
                return jqXHR;
            },
        });
    });
};

var vP1 = function()
{
var csrf_token = "{{ csrf_token() }}";

    $.ajaxSetup({
        beforeSend: function(xhr, settings) {
            if (!/^(GET|HEAD|OPTIONS|TRACE)$/i.test(settings.type) && !this.crossDomain) {
                xhr.setRequestHeader("X-CSRFToken", csrf_token);
            }
        }
    });

    $(document).ready(function(){
        $.ajax({
            url:'http://127.0.0.1:5000/products',
            method:'POST',
            data:{
                str:window.location.href,
            },
            success:function(response){
                allProducts = response.products;
                var str='';
                for(var i=0;i<allProducts.length;i++)
                {
                    console.log(allProducts[i].price);
                    str = str+'<div class="polaroid">'+'<img src="/upload/'+allProducts[i].img+'"'+'alt="image" heigth=500 width=500">'+'<div class="container1">'+'<a href="/details1/'+allProducts[i].name+'">'+allProducts[i].name+'</a>'+'</div></div>';

                }
                document.getElementById("pdisplay").innerHTML = str;
                console.log(str);
                return response;
            },
            error:function(jqXHR,exception){
                console.log(jqXHR.responseText);
                return jqXHR;
            },
        });
    });
};

var vP = function()
{
   // document.getElementById("csrfpro").submit();
var csrf_token = "{{ csrf_token() }}";

    $.ajaxSetup({
        beforeSend: function(xhr, settings) {
            if (!/^(GET|HEAD|OPTIONS|TRACE)$/i.test(settings.type) && !this.crossDomain) {
                xhr.setRequestHeader("X-CSRFToken", csrf_token);
            }
        }
    });
    $(document).ready(function(){
        $.ajax({
            url:'http://127.0.0.1:5000/products',
            method:'POST',
            data:{
                str:window.location.href,
            },
            success:function(response){
                allProducts = response.products;
                var str='';
                for(var i=0;i<allProducts.length;i++)
                {
                    console.log(allProducts[i].img);
str = str+'<div class="polaroid">'+'<img src="/upload/'+allProducts[i].img+'"'+'alt="image" heigth=500 width=500">'+'<div class="container1">'+'<a href="/details/'+allProducts[i].name+'">'+allProducts[i].name+'</a>'+'</div></div>';
                    
                }
                document.getElementById("pdisplay").innerHTML=str;        
                return response;
            },
            error:function(jqXHR,exception){
                console.log(jqXHR.responseText);
                return jqXHR;
            },
        });
    });
};


var sign = function(){
    alert("You Have To Login First");
}


