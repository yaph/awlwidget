$(document).ready(function() {
  var elt = $('#awlcarousel li:first-child');
  elt.css('display', 'block');
  elt.attr({'class': 'awlactive'});
});

function awlnav(direction) {
  var elt = $('#awlcarousel .awlactive');
  elt.css('display', 'none');
  elt.attr({'class': 'awlinactive'});

  var id_max = $('#awlcarousel li:last-child').attr('id').replace('item-', '');
  var id_curr = elt.attr('id').replace('item-', '');
  var id_alter = 0;
  
  if (1 == id_curr && 'prev' == direction) {
    id_alter = id_max;
  }
  else if (id_max == id_curr && 'next' == direction) {
    id_alter = 1;
  }
  else if ('prev' == direction) {
    id_alter = parseInt(id_curr) - 1;
  }
  else {
    id_alter = parseInt(id_curr) + 1;
  }

  var elt_alter = $('#item-' + id_alter);
  elt_alter.css('display', 'block');
  elt_alter.attr({'class': 'awlactive'});
}