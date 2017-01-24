function get_model_name() {
    var pathArray = window.location.pathname.split( '/' );
    for(var i = 0 ; i+1 < pathArray.length ; i++ ) {
        if(pathArray[i] == "admin") {
            return pathArray[i+1];
        }
    }
    return "" ;
}

function fill_participant(team_id,field) {
    if (response_cache[team_id]) {
        $(field).html(response_cache[team_id]);
    } else {
        var model = get_model_name();
        if(model != "" ) {
            $.getJSON("/"+model+"/member_for_team", {team_id: team_id},
                  function(ret, textStatus) {
                      //var options = '<option value="" selected="selected">---------</option>';                                                               
                      var options = '';
                      for (var i in ret['res']) {
                          options += '<option value="' + ret['res'][i].id + '">'
                              + ret['res'][i].name + '</option>';
                      }
                      response_cache[team_id] = options;
                      $(field).html(options);
                  });
        }
    }
}

function defer() {
    if (window.jQuery)
        $(document).ready(function() {
            $("#id_opponent_team").change(function() { fill_participant($(this).val(),"#id_opponent"); });
            $("#id_reporter_team").change(function() { fill_participant($(this).val(),"#id_reporter"); });
            $("#id_reviewer_team").change(function() { fill_participant($(this).val(),"#id_reviewer"); });
        });
    else
        setTimeout(function() { defer() }, 50);
}

var response_cache = {};
defer();
