$ = window.jQuery
$(document).ready( ->
    ajaxError = ->
        alert('Communication error has occured. Sorry.')
    loadShouts = (offset=0) ->
        ajaxSuccess = (data) ->
            loader = $('#shouts div.loading')
            count = 0
            $.each(data.shouts, (index, item) ->
                if $("#shout-#{item.id}").length == 0
                    html = """<div id="shout-#{item.id}" class="message">
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
            error: ajaxError
            complete: ->
                $('#shouts div.loading').css('display', 'none')
        })
        
    sendShout = (event) ->
        if event.which != 13
            return true
        
        event.stopPropagation()
        event.preventDefault()
        
        form = $('#publish form')
        data = { text: $(event.target).val() }
        $.ajax({
            url: form.attr('action'),
            type: 'POST',
            data: data,
            dataType: 'json',
            before: ->
                $('#publish div.loading').css('display', 'block')
            success: ->
                $('textarea', form).val('')
                window.location.href = window.location.href.replace('#publish', '')
            error: ajaxError
            complete: ->
                $('#publish div.loading').css('display', 'none')
        })
        
        false
        
    $('#load-more a').bind('click', ->
        loadShouts($('#load-more a').attr('data-offset'));
        false
    )
    
    loadShouts()
    
    if window.location.hash == '#publish'
        $('#publish').css('display', 'block')
        $('#publish textarea').bind('keydown', sendShout
        )
    else
        $('#publish').empty()
)