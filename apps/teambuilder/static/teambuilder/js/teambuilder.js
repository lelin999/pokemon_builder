$(document).ready(function() {
  var nature = []
  for(var i=1; i<=151;i++) {
    $('.dex').append(`<img id=\'img${i}\' src=\'/static/teambuilder/img/${i}.png\'>`);
  }
  natures = $.get(`http://pokeapi.co/api/v2/nature/`, function(data) {
    for (i in data.results) {
      $('#naturelist').append(`<option value='${data.results[i].name}'>${data.results[i].name}</option>`)
    }
  });
  morenatures = $.get(`http://pokeapi.co/api/v2/nature/?offset=20`, function(data) {
    for (i in data.results) {
      $('#naturelist').append(`<option value='${data.results[i].name}'>${data.results[i].name}</option>`)
    }
  });

  $(document).on("click", "img", function() {
    $('.stats #numname').text("Loading..")
    $("body").css("cursor", "progress");
    $('.stats #types').text("")
    $('#base_hp').text("")
    $('#base_atk').text("")
    $('#base_def').text("")
    $('#base_spa').text("")
    $('#base_spd').text("")
    $('#base_spe').text("")
    console.log($(this).attr('id').substring(3))
    $('#id').val($(this).attr('id').substring(3))
    pkmn_info = $.get(`http://pokeapi.co/api/v1/pokemon/${$(this).attr('id').substring(3)}`, function(data) {
      $('.stats #numname').text(`#${data.pkdx_id} - ${data.name}`);
      $("body").css("cursor", "default");
      $('#base_hp').text(data.hp)
      $('#base_atk').text(data.attack)
      $('#base_def').text(data.defense)
      $('#base_spa').text(data.sp_atk)
      $('#base_spd').text(data.sp_def)
      $('#base_spe').text(data.speed)
      var type = data.types[0].name[0].toUpperCase() + data.types[0].name.substring(1);
      if(data.types.length > 1) {
        type = data.types[1].name[0].toUpperCase() + data.types[1].name.substring(1) + " " + type;
      }
      $('.stats #types').text(type);
    });
  });

  $('#statform').submit(function() {
    $.ajax({
      url:"/teambuilder/stat_ajax/",
      method:"POST",
      success:function(obj) {
        if(obj.success) {
          // run the graph stuff
          $('.errors').html("")
          console.log(obj)
        }
        else {
          errors_html = ""
          for(errors in obj.errors) {
            errors_html += `<li>${obj.errors[errors]}</li>`;
          }
          $('.errors').html(errors_html)
        }
      },
      data : $('#statform').serialize()
    });
    return false;
  });
});
