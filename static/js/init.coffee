define(
    [],
    ()->
        class init
            initialize: ()->
                return this

        class Socket
            ws: null,
            initialize: ()->
                ws = new WebSocket('ws://' + document.location.host + '/notifications');
                ws.onopen = ()->
                    console.log('Socket opened');

                ws.onclose = ()->
                    console.log('Socket close');
                    ws = null;

                ws.onmessage = (e)->
                    message = e.data;
                    console.log(message)

        window.WSConnect = new Socket()
        window.WSConnect.initialize()
        return init
)