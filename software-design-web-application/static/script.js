function peform_main_search() {
    var url = '/mainSearch/' + document.getElementById('main_search_cause').value +
    '/' + document.getElementById('main_search_state').value + '/' + document.getElementById('main_search_start_year').value + '/'
    + document.getElementById('main_search_end_year').value;
    var xhp = new XMLHttpRequest();
    xhp.open('get', url);
    xhp.send();

    location.replace("http://perlman.mathcs.carleton.edu:5134/main_search/" + document.getElementById('main_search_cause_name').value  +
                      '/' + document.getElementById('main_search_state').value + '/' + document.getElementById('main_search_start_year').value
                        + '/' + document.getElementById('main_search_end_year').value);
}

function go_search() {

    var url = '/mostDeadly/' + document.getElementById('state_text').value;
    
    var xhp = new XMLHttpRequest();
    xhp.open('get', url);
    xhp.send();
    
   location.replace("http://perlman.mathcs.carleton.edu:5134/mostDeadly/" + document.getElementById('state_text').value);
}

function go_two_search() {
    var url = '/mostDeathsInState/';
    var xhp = new XMLHttpRequest();
    xhp.open('get', url);
    xhp.send();
    location.replace("http://perlman.mathcs.carleton.edu:5134/mostDeathsInState/");
}


function go_three_search () {
    var url = '/trend/' + document.getElementById('cause_text').value;
    var xhp = new XMLHttpRequest();
    xhp.open('get', url);
    xhp.send();
    location.replace("http://perlman.mathcs.carleton.edu:5134/trend/" + document.getElementById('cause_text').value);
}

