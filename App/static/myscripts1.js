
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
var vP = function()
{

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
                    str = str+'<tr>'+'<td>'+allProducts[i].name+'</td>'+'<td>'+allProducts[i].price+'</td>'+'<td>'+allProducts[i].category+'</td>'+'<td>'+allProducts[i].description+'</td>'+'<td>'+allProducts[i].num+'</td>'+'<td>'+allProducts[i].seller+'</td>'+'<td>'+'<img src="/upload/'+allProducts[i].img+'"'+'alt="image">'+'</td>'+'</tr>';
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

