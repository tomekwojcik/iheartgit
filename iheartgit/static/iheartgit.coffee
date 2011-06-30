$ = window.jQuery
$(document).ready( ->
    ajaxError = ->
        alert('Communication error has occured. Sorry.')
    
    loadShouts = (offset=0) ->
        loadMore = $('#load-more a')
        loader = $('#load-more')
        
        ajaxSuccess = (data) ->
            count = 0
            $.each(data.shouts, (index, item) ->
                if $("#shout-#{item.id}").length == 0
                    html = """<div id="shout-#{item.id}" class="message">
                        <img src="#{item.user.avatar_url}" alt="" title="" />
                        <p class="message-text"><span><a href="#{item.user.url}" rel="nofollow">#{item.user.nick}</a> loves GIT because:</span><br/>#{item.text}</p>
                        <p class="message-date">#{item.created_at}</p>
                    </div>"""
                    loader.before($(html))
                    count += 1
            )
            loadMore.attr('data-offset', parseInt(loadMore.attr('data-offset'), 10) + count)
            
        $.ajax({
            url: '/shouts?offset=' + offset,
            dataType: 'json',
            beforeSend: ->
                loader.addClass('loading')
                loadMore.text('&nbsp;')
            success: ajaxSuccess,
            error: ajaxError
            complete: ->
                loader.removeClass('loading')
                loadMore.text('Load More')
        })
     
    isPosting = false   
    sendShout = () ->
        if isPosting == true
            return false
        
        form = $('#publish form')
        data = { text: $('textarea', form).val() }
        $.ajax({
            url: form.attr('action'),
            type: 'POST',
            data: data,
            dataType: 'json',
            beforeSend: ->
                $('input[type=submit]', form).val('Just a sec...')
            success: ->
                $('textarea', form).val('')
                window.location.href = window.location.href.replace('#publish', '')
            error: ajaxError
            complete: ->
                $('input[type=submit]', form).val('Send')
        })
        
    $('#load-more a').bind('click', ->
        loadShouts($('#load-more a').attr('data-offset'));
        false
    )
    
    loadShouts()
    
    if window.location.hash == '#publish'
        $('#publish').css('display', 'block')
        $('#publish textarea').bind('keydown', (event) ->
            if event.which != 13
                return true
                
            event.stopPropagation()
            event.preventDefault()
            
            sendShout()
            
            false
        )
        $('#publish form').bind('submit', (event) ->
            event.stopPropagation()
            event.preventDefault()
            
            sendShout()
            
            false
        )
    else
        $('#publish').empty()
)