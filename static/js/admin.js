(function($) {
    $(document).ready(function($) {

        try {
            if($('#id_title').val().length == 0)
            {
                $('#id_title').syncTranslit({destination: 'id_slug'});
            }
        } catch (e) {}

        try {
                if($('#id_name').val().length == 0)
            {
                $('#id_name').syncTranslit({destination: 'id_slug'});
            }
        } catch (e) {}

	});
})(django.jQuery.noConflict());