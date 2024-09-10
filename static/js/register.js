$(function(){
    function bindCaptchaBtnClick(){
        $("#captcha-btn").click(function(event){
            let $this =$(this);
            let email = $("input[name='email']").val();
           if(!email){
               alert("Please enter your email address!");
               return;
           }
           //取消按钮的点击时间
           $this.off('click');


           //发送ajax请求
           $.ajax({
            url: '/author/captcha?email=' + email, // 请求的URL
            method: 'GET', // HTTP方法，GET请求
            success: function(result) { // 请求成功时的回调函数
                if (result['code'] == 200) {
                    alert("The verification code is sent successfully!"); // 显示成功消息
                } else {
                    alert(result['message']); // 显示错误信息
                }
            },
            error: function(error) { // 请求失败时的回调函数
                console.log(error); // 打印错误信息
            }
        });
        

           //倒计时
           let countdown = 6;
           let timer = setInterval(function(){
              if(countdown<=0){
               $this.text('Get a verification code');
               //清掉定时器
                clearInterval(timer);
               //重新绑定点击事件
               bindCaptchaBtnClick();
              }else{
                  countdown--;
                   $this.text(countdown+"s");
              }
       
           },1000);//每秒执行一次
       
           })
    }

    bindCaptchaBtnClick();
});