$(document).ready(function () {

   // $(document).on('click','#create-board',)

    $('#board-modal').on('shown.bs.modal', function(event) {
       var remoteUrl =  $(event.relatedTarget).data('remote')
       var modal = $(this)
        console.log(remoteUrl, 'test')
       $.ajax({
            method: 'GET',
            url: remoteUrl
       }).done(function(response){
        console.log(response, 'testrespon')
        modal.find('.modal-body').html(response)
       })
      })



      

});