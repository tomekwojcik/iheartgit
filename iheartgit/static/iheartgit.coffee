$ = window.jQuery
$(document).ready( ->
    loadShouts = (offset=0) ->
        ajaxSuccess = (data) ->
            loader = $('#shouts div.loading')
            count = 0
            $.each(data, (index, item) ->
                if $("#shout-#{index}").length == 0
                    html = """<div id="shout-#{index}" class="message">
                        <p><img src="#{item.user.avatar_url}" alt="" title="" /><a href="#{item.user.url}" rel="nofollow">#{item.user.nick}</a> loves GIT because: #{item.text}</p>
                        <p class="date">#{item.created_at}</p>
                    </div>"""
                    loader.before($(html))
                    count += 1
            )
            loadMore = $('#load-more a')
            loadMore.attr('data-offset', parseInt(loadMore.attr('data-offset'), 10) + count)
            
        $.ajax({
            url: '/shouts?offset=' + offset,
            dataType: 'json',
            beforeSend: ->
                $('#shouts div.loading').css('display', 'block')
            success: ajaxSuccess,
            error: ->
                alert('Communication error has occured. Sorry.')
            complete: ->
                $('#shouts div.loading').css('display', 'none')
        })
        
    $('#load-more').bind('click', ->
        loadShouts($('#load-more').attr('data-offset'));
        false
    )
    
    loadShouts()
)