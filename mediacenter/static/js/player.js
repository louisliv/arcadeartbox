var increment = .1;
var time_increment = 10;
var set_volume = .5;
var player_muted = false;
var videoOptions =  {
    controls: true,
    autoplay: true,
    preload: 'auto'
}

console.log('hey')

var player = new WebSocket(
    'ws://' + window.location.host +
    '/ws/player/');

player.onmessage = function(e) {
    var data = JSON.parse(e.data);
    var message = data['message'];
    var messageType = message['type'];
    
    if(messageType === 'action') {
        var action = message['action'];
        var vid = videojs.getPlayer('player');
        try {
            switch(action) {
                case 'play':
                    vid.play()
                    break;
                case 'pause':
                    vid.pause()
                    break;
                case 'mute':
                    player_muted = !player_muted
                    vid.muted(player_muted)
                    break;
                case 'vol_up':
                    vol_up(vid);
                    break;
                case 'vol_down':
                    vol_down(vid);
                    break;
                case 'skip_forward':
                    skip_forward(vid);
                    break;
                case 'skip_backward':
                    skip_backward(vid);
                    break;
                default:
                    break;
            }
        } catch {
            location.reload()
        }
    } else if (messageType==='source') {
        var source = message['source']
        var type = message['player_type']

        switch(type) {
            case 'video':
                create_video_elm(source);
                break;
            case 'photo':
                create_photo_elm(source);
                break;
            default:
                break;
        }
        
    }
};

player.onclose = function(e) {
    console.error('Chat socket closed unexpectedly');
};

var create_video_elm = function(source) {
    var oldPlayer = document.getElementById('player');
    
    if (oldPlayer) {
        videojs(oldPlayer).dispose();
    }
    
    var container = document.getElementById('media-container')
    var template = `
        <video id="player" class="video-js" 
        style="height: 100%;width: 100%;">
        <source src="` + source + `" 
        type="video/mp4"/></video>
    `
    container.innerHTML = template;

    var vid = videojs('player', videoOptions, function onPlayerReady() {
        var self = this;
        self.on('ended', function() {
            player_muted = self.muted();
            set_volume = self.volume();
            player.send(JSON.stringify({
                'action': 'refresh'
            }))
        });
    });

    vid.muted(player_muted);
    vid.volume(set_volume);
}

var create_photo_elm = function(source) {
    var container = document.getElementById('media-container')
    var template = "<img id=\"image\" src=\"" + source + "\" height=\"100%\"></img>" 
    container.innerHTML = template;
}

var vol_up = function (vid) {
    new_volume = set_volume + increment

    if (new_volume > 1) {
        set_volume = 1
    } else {
        set_volume = new_volume
    }

    vid.volume(set_volume)
}

var vol_down = function (vid) {
    new_volume = set_volume - increment

    if (new_volume < 0) {
        set_volume = 0
    } else {
        set_volume = new_volume
    }

    vid.volume(set_volume)
}

var skip_forward = function (vid) {
    new_time = vid.currentTime() + time_increment;

    if (new_time > vid.duration()) {
        player.send(JSON.stringify({
            'action': 'refresh'
        }))
    } else {
        vid.currentTime(new_time)
    }
}

var skip_backward = function (vid) {
    new_time = vid.currentTime() - time_increment;

    if (new_time < 0) {
        vid.currentTime(0)
    } else {
        vid.currentTime(new_time)
    }
}
