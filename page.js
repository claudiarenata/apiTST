function hidetabelPlaylist() {
    document.getElementById('tabelPlaylist').style.display='none';
    
}

function showtabelhasilSearch(){
    document.getElementById('tabelSearch').style.display='block'; 
}

function showHideTabel(){
    hidetabelPlaylist();
    showtabelhasilSearch(); 
}

function openTable(evt, tabName) {
    var i, tabcontent, tablinks;
    tabcontent = document.getElementsByClassName("tabcontent");
    for (i = 0; i < tabcontent.length; i++) {
      tabcontent[i].style.display = "none";
    }
    tablinks = document.getElementsByClassName("tablinks");
    for (i = 0; i < tablinks.length; i++) {
      tablinks[i].className = tablinks[i].className.replace(" active", "");
    }
    document.getElementById(tabName).style.display = "block";
    evt.currentTarget.className += " active";
}

function hideModal(){
    document.getElementById('video-modal').style.display='none'; 
};

// AJAX
$(document).ready(function() {
    $("#theadplaylist").click(function(e) {
        e.preventDefault();
        var tabmodiv = document.getElementById('tbodyplaylist');
        $.ajax({
            url: 'http://3.83.203.203:6001/api/allplaylist',
            crossDomain: true,
            type:'GET',
            dataType: 'json',
            success: function(response) {
                console.log(Headers);
              content="";
              $.each(response, function(key, value){
                  $.each(value, function(key,value) {
                    content+=
                        "<tr>" +
                            "<td>"+value[1]+"</td>\n"+
                        "</tr>";
                  });
              });
              tabmodiv.innerHTML = content;
            //   document.getElementById('namap').value = value[1];
            },
            error: function(response) {
              console.log(response);
            }
        });
    });

    $("#caridata").click(function(e) {
        e.preventDefault();
        var tabmodiv = document.getElementById('tbodysearch');
        endpoint = 'http://3.210.119.72:6002/api/playlist?playlistName=';
        $.ajax({
            url: endpoint + encodeURIComponent(document.getElementById('name').value),
            crossDomain: true,
            type:'GET',
            dataType: 'json',
            success: function(response) {
                content="";
                $.each(response.tracks, function(key, value) {
                    content+=
                        "<tr>" +
                            "<td>"+value.songsName+"</td>\n"+
                            "<td>"+value.songsArtist+"</td>\n"+
                            "<td><button id='vidbtn' onclick=\"showModal('"+value.songsName+"','"+value.songsArtist+"');\">youtube</button>" + "</th>\n" +
                            "<td><a id='songbtn' href='"+ value.songsURL +"' >spotify</a>" + "</th>\n" +
                        "</tr>";
                });
                tabmodiv.innerHTML = content;
            },
            error: function(response) {
              console.log(response);
            }
        });
    });
});

function showModal(a, b){
    document.getElementById('video-modal').style.display='block';

    document.getElementById('judullagu').value = a;
    document.getElementById('linklaguvid').value = b;

    var judul = a;
    var artis = b;
    var tabmodiv = document.getElementById('tbodyvideo');
    $.ajax({
        type : 'GET', 
        url :"http://3.210.119.72:6002/api/youtubesearch="+lagu+" "+artis, 
        dataType : 'json', 
        contentType: 'application/json',
        success : function(response) {
            // console.log(response);
            content = '';
            $.each(response, function(key, value) {
                content+=
                    "<tr>" +
                        "<td>"+value.title+"</td>\n"+
                        "<td><a href='"+value.url+"' target='_blank' >links</a>" +"</td>\n"+
                    "</tr>";
            });
            tabmodiv.innerHTML = content;
        }, 
        error : function(response) {
            console.log(response); 
        }
    });
}
