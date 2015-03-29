<script type="text/javascript"> // when the page get's loaded call the init function to hijack all the form 
Event.observe(window, 'load', init, false); function init(){
    // hijack the form submit
    Event.observe($('theform'), 'submit', processform, false);
}
function processform(e) {
    // get the form that got submited ( the first parrent element of the element that trigger the event)
    var aform = Event.findElement(e, 'form');
    // where to submit the form
    var ajaxurl = aform.action;
    var formparameters = aform.serialize(true); // take the form field values before you disable it
    //disable the form elements while beeing processed
   aform.disable();
    // get the submit button of the form and show an ajax-loader instead
    var submitbutton = aform.getInputs('submit')[0];
    new Insertion.Before(submitbutton, '<img src="/site_media/ajax-loader.gif" id="ajaxloader" />');
    submitbutton.hide()
    // make the js field empty so that django knows how to handle the request
    // if js is submited with the form django handles it as a normal form
    // if js is None django returns AJAX variables
    document.getElementById('js').value = ''
        var myAjax = new Ajax.Request(
        ajaxurl,
        { method: 'post',
          parameters: formparameters,
          onSuccess: handlereq,
          onFailure: function() {alert('Refresh the Page, something happend to the server');} // what to do if the 
server return something else than 2xx status.
        });
    function handlereq(req) {
        // evaulate the response (get the errors or run the javascript)
        var errors = eval('(' + req.responseText + ')');
        // clean the errors from the previous run (elements with class="errorlist"
        var old = aform.getElementsByClassName('errorlist');
        for (i=0; i<old.length; i++) { old[i].remove(); }
        // if there is an OK attribute in the response, run the javascript
        // if not show the errors in the for_fieldname element
        if ( errors.OK ){
		fo.innerHTML = 'hi';
//            eval(errors.OK)
        } else {
            $H(errors).each(function(pair) {
                $('for_'+pair.key).innerHTML = '<ul class="errorlist"><li>'+pair.value+'</li></ul>';
            });
        aform.enable(); // enable the form
        $('ajaxloader').remove(); // remove the ajax-loader
        submitbutton.show(); // return the submit button
        }
    }
    // don't trigger the actual html submit form
    Event.stop(e);
}
</script>
