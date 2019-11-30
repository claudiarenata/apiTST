$(document).ready(function () {
    //@naresh action dynamic childs
    var next = 0;
    $("#add-more").click(function(e){
        e.preventDefault();
        var addto = "#field" + next;
        var addRemove = "#field" + (next);
        next = next + 1;
        var newIn = ' <div id="field'+ next +'" name="field'+ next +'"><br><!-- Text input--><div class="form-group"><label class="col-md-4 control-label" for="action_name">Judul Lagu</label><div class="col-md-5"><input id="action_name" name="action_name" type="text" placeholder="" class="form-control input-md"></div></div><div class="form-group"><label class="col-md-4 control-label" for="action_artis">Artis</label><div class="col-md-5"><input id="action_name" name="action_artis" type="text" placeholder="" class="form-control input-md"></div></div>';
        var newInput = $(newIn);
        var removeBtn = '<button id="remove' + (next - 1) + '" class="btn btn-danger remove-me" >Remove</button></div></div><div id="field">';
        var removeButton = $(removeBtn);
        $(addto).after(newInput);
        $(addRemove).after(removeButton);
        $("#field" + next).attr('data-source',$(addto).attr('data-source'));
        $("#count").val(next);  
        $('.remove-me').click(function(e){
            e.preventDefault();
            var fieldNum = this.id.charAt(this.id.length-1);
            var fieldID = "#field" + fieldNum;
            $(this).remove();
            $(fieldID).remove();
        });
    });

});

// $("#formbuku").submit(function(event) {

//     /* stop form from submitting normally */
//     event.preventDefault();

//     /* get the action attribute from the <form action=""> element */
//     var $form = $( this ),
//       url = $form.attr( 'action' );

//   /* Send the data using post with element id name and name2*/
//     var posting = $.post( url, { 
//         ISBN: $('#ISBN').val(), 
//         Judul_Buku: $('#judul').val(), 
//         Pengarang: $('#Pengarang').val(),
//         Penerbit: $('#Penerbit').val(), 
//         Tahun_Terbit : $('#Tahun').val(), 
//         Kategori : $('#Kategori').val(), 
//         Sinopsis : $('#sinopsis').val(), 
//         Stok_Buku :$('#Stok_Buku').val()   }
//         );

//     /* Alerts the results */
//     posting.done(function( data ) {
//         alert(data['message']);
//         location.reload();
//     });
// });

function addPlaylist(){
        var newPlaylist = {
<<<<<<< HEAD
            'playlistName' : document.getElementById('action_id').value,
            'songs' : [{
                'songsName': document.getElementById('action_name').value,
                'songsArtist' : document.getElementById('action_artis').value
            }]
        }
        console.log(newPlaylist);
=======
            'playlistName' : $('#action_id').val(),
            'songs' : {
                'songsName': $('#action_name').val(),
                'songsArtist': $('#action_artis').val()
            }
        };
        console.log(newPlaylist); 

            
>>>>>>> 4be4aff9da7e7c05ab4d03ec0e87967ee8f7e35f
        $.ajax({
            url: 'http://3.83.203.203:6001/api/playlist',
            data: JSON.stringify(newPlaylist),
            type: 'POST',
            datatype:'json',
            contentType: "application/json; charset=utf-8",
            crossDomain:true,
            xhrFields: {
                withCredentials: true
             },
            success: function(response) {
                alert('Berhasil Menambahkan Playlist');
            },
            error: function(error) {
                alert(error);
            }
        });
}

$(document).ready(function() {
    $("#submit-btn").on("click",function(){
        addPlaylist();
    })
})