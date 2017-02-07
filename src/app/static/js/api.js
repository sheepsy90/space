function start_bg_switcher(){
    var height2 = $( window ).height();

    $("body")
        .css("height", height2 + "px")
        .bgswitcher({
          images: ["/static/img/bg4.png", "/static/img/bg5.png"],
          loop: true,
          interval: 9000,
          duration: 3000
        });
}

function check_image_bg(){

    setTimeout(check_image_bg, 2000);
}

var audio = new Audio("/static/music/background_music.mp3");

 function audio_switch(){
    var isMuted = $(audio)[0].muted;
    if (isMuted){
        $("#audio_switch").removeClass("muted");
        $(audio)[0].muted = false;
    }else{
        $("#audio_switch").addClass("muted");
        $(audio)[0].muted = true;
    }
 }

function start_and_bind_audio(){
    audio.load();
    if( $("#sound_enabled").html() == "False"){
        $("#audio_switch").addClass("muted");
        $(audio)[0].muted = true;
        audio.play();
        return;
    }else{
        audio.play();
    }
    $("#audio_switch").bind("click", audio_switch);
}

function play_sound(file){
    if($("#sound_enabled").html() == 'False'){
        return;
    }

    var a = new Audio(file);
    a.load();
    a.play();
}


function get_csrftoken(){
    return $("#csrf_token_container > input").val();
}